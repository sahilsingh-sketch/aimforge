import { useEffect, useRef } from "react";
import { useAppStore } from "../store/useAppStore";
import { aimforgeService } from "../services/api";
import axios from "axios";

const MULTIPART_THRESHOLD = 5 * 1024 * 1024; // 5MB
const CHUNK_SIZE = 16 * 1024 * 1024; // 16MB
const MAX_CONCURRENCY = 4;

export default function UploadManager() {
  const {
    jobId,
    setJobId,
    setVideoUrl,
    uploadFile,
    uploadStatus,
    setUploadProgress,
    setUploadStatus,
    setUploadError,
    setUploadEstimatedTime,
    setUploadAbortController,
  } = useAppStore();

  const uploadStartTimeRef = useRef<number | null>(null);

  useEffect(() => {
    console.log("[DEBUG UploadManager] useEffect triggered. uploadFile:", uploadFile, "uploadStatus:", uploadStatus);
    // Start Upload
    if (uploadFile && uploadStatus === "starting") {
      const runUpload = async () => {
        const controller = new AbortController();
        setUploadAbortController(controller);
        
        setUploadStatus("uploading");
        setUploadProgress(0);
        uploadStartTimeRef.current = Date.now();
        setUploadError(null);

        try {
          console.log("[UPLOAD] File selected", uploadFile);
          console.log("[UPLOAD] File name:", uploadFile?.name);
          console.log("[UPLOAD] File size:", uploadFile?.size);
          console.log("[UPLOAD] File type:", uploadFile?.type);

          console.log("[UPLOAD] Before health check");
          const health = await aimforgeService.checkUploadHealth();
          console.log("[UPLOAD] After health check", health);
          
          if (health.status === "error") {
            throw new Error(`Pre-flight check failed: ${health.message}`);
          }
          
          setUploadStatus("validating");
          setUploadEstimatedTime("Checking gameplay...");
          console.log("[UPLOAD] Starting BGMI validation...");
          
          const validation = await aimforgeService.validateBgmi(uploadFile);
          
          if (!validation.valid) {
              setUploadError(`⚠️ Invalid Gameplay Video\n\n${validation.reason}\n\nAimForge can only analyze BGMI gameplay videos.`);
              setUploadStatus("error");
              setUploadEstimatedTime("");
              return; // Stop the upload process immediately
          }
          
          console.log("[UPLOAD] BGMI gameplay detected ✓");
          setUploadStatus("uploading");

          setVideoUrl(URL.createObjectURL(uploadFile));
          
          let uploadJobId;
          let uploadMessage;

          if (uploadFile.size > MULTIPART_THRESHOLD) {
            console.log("[UploadManager] File > 100MB. Starting Multipart S3 Upload.");
            
            // 1. Init
            console.log("[UPLOAD] Calling multipart init API");
            const { job_id, upload_id } = await aimforgeService.initMultipart(
              uploadFile.name,
              uploadFile.type || "video/mp4",
              uploadFile.size,
              controller.signal
            );
            console.log(`[UPLOAD] Multipart init response received. job_id: ${job_id}`);
            
            uploadJobId = job_id;
            const totalParts = Math.ceil(uploadFile.size / CHUNK_SIZE);
            const parts: { ETag: string, PartNumber: number }[] = [];
            let uploadedBytes = 0;
            
            // 2. Upload chunks in parallel with limited concurrency
            const uploadQueue = Array.from({ length: totalParts }, (_, i) => i + 1);
            let activeUploads = 0;
            
            await new Promise<void>((resolve, reject) => {
               const processQueue = async () => {
                 if (uploadQueue.length === 0 && activeUploads === 0) {
                   resolve();
                   return;
                 }
                 
                 while (activeUploads < MAX_CONCURRENCY && uploadQueue.length > 0) {
                   const partNumber = uploadQueue.shift()!;
                   activeUploads++;
                   
                   const start = (partNumber - 1) * CHUNK_SIZE;
                   const end = Math.min(start + CHUNK_SIZE, uploadFile.size);
                   const chunk = uploadFile.slice(start, end);
                   
                   (async () => {
                     let attempt = 0;
                     let success = false;
                     let lastErr: any = null;
                     
                     while (attempt < 3 && !success) {
                       try {
                          console.log(`[MULTIPART] Presigning part ${partNumber} (Attempt ${attempt + 1})...`);
                          const { presigned_url } = await aimforgeService.presignMultipart(job_id, upload_id, partNumber, controller.signal);
                          
                          console.log(`[MULTIPART] Uploading part ${partNumber}...`);
                          const response = await axios.put(presigned_url, chunk, {
                            headers: { 'Content-Type': '' }, // AWS requires this to match signature precisely
                            signal: controller.signal
                          });
                          
                          // Extract ETag from response headers.
                          // NOTE: CORS must expose ETag header for this to work.
                          let etag = response.headers.etag;
                          if (!etag) {
                              throw new Error("ETag header missing. Ensure S3 CORS policy exposes ETag header.");
                          }
                          etag = etag.replace(/"/g, '');
                          
                          console.log(`[MULTIPART] ETag received for part ${partNumber}`);
                          parts.push({ ETag: etag, PartNumber: partNumber });
                          
                          uploadedBytes += chunk.size;
                          const percent = Math.round((uploadedBytes * 100) / uploadFile.size);
                          setUploadProgress(percent);
                          
                          if (percent > 5 && uploadStartTimeRef.current) {
                            const elapsed = (Date.now() - uploadStartTimeRef.current) / 1000;
                            const totalEstimated = (elapsed / percent) * 100;
                            const remaining = Math.max(0, totalEstimated - elapsed);
                            
                            if (remaining > 60) {
                               setUploadEstimatedTime(`${Math.round(remaining/60)}m ${Math.round(remaining%60)}s remaining`);
                            } else {
                               setUploadEstimatedTime(`${Math.round(remaining)}s remaining`);
                            }
                          }
                          
                          success = true;
                       } catch (err: any) {
                          lastErr = err;
                          if (axios.isCancel(err) || err.name === 'CanceledError' || err.name === 'AbortError') {
                              break; // Do not retry if user aborted
                          }
                          attempt++;
                          if (attempt < 3) {
                              console.warn(`[MULTIPART] Part ${partNumber} FAILED. Retrying in ${attempt * 2}s...`, err);
                              await new Promise(r => setTimeout(r, attempt * 2000));
                          } else {
                              console.error(`[MULTIPART] Part ${partNumber} FAILED permanently after 3 attempts.`, err);
                          }
                       }
                     }
                     
                     if (!success) {
                        reject(lastErr);
                     } else {
                        resolve();
                     }
                     
                     activeUploads--;
                     processQueue();
                   })();
                 }
               };
               processQueue();
            });
            
            // 3. Complete
            parts.sort((a, b) => a.PartNumber - b.PartNumber);
            console.log("[MULTIPART] All parts uploaded");
            console.log("[MULTIPART] Completing multipart upload");
            const completeResponse = await aimforgeService.completeMultipart(job_id, upload_id, parts, controller.signal);
            console.log("[MULTIPART] Multipart upload completed");
            uploadMessage = completeResponse.message;
            
          } else {
            console.log("[UPLOAD] Calling presign API");
            const { jobId, message } = await aimforgeService.uploadVideo(uploadFile, (percent) => {
              setUploadProgress(percent);
              console.log("[UPLOAD] Progress:", percent);
              
              if (percent > 5 && uploadStartTimeRef.current) {
                const elapsed = (Date.now() - uploadStartTimeRef.current) / 1000;
                const totalEstimated = (elapsed / percent) * 100;
                const remaining = Math.max(0, totalEstimated - elapsed);
                
                if (remaining > 60) {
                   setUploadEstimatedTime(`${Math.round(remaining/60)}m ${Math.round(remaining%60)}s remaining`);
                } else {
                   setUploadEstimatedTime(`${Math.round(remaining)}s remaining`);
                }
              }
            }, controller.signal);
            console.log("[UPLOAD] Upload completed");
            console.log("[UPLOAD] Calling upload completion API");
            uploadJobId = jobId;
            uploadMessage = message;
          }

          console.log(`[UploadManager] Upload POST completed. Job ID: ${uploadJobId}`);
          setUploadProgress(100);
          setJobId(uploadJobId);
          sessionStorage.setItem("aimforge_active_upload_job_id", uploadJobId);

          if (uploadMessage && uploadMessage !== "Multipart upload complete, analysis started.") {
             // For standard upload error messages that don't throw an error but return a warning
             // Actually, the new backend returns "Upload complete, analysis started."
             if (uploadMessage.includes("error") || uploadMessage.includes("fail")) {
                 setUploadStatus("uploaded");
                 setUploadError(`⚠️ ${uploadMessage}`);
                 return;
             }
          }

          setUploadStatus("queued_for_analysis");

        } catch (e: any) {
          if (axios.isCancel(e) || e.name === 'CanceledError' || e.name === 'AbortError') {
             console.log("[UploadManager] Upload cancelled by user.");
             return;
          }
          console.error("[UploadManager] Upload failed:", e);
          setUploadError(`❌ ${e.message || "Upload failed."}`);
          setUploadStatus("error");
        } finally {
          if (useAppStore.getState().uploadAbortController === controller) {
             setUploadAbortController(null);
          }
        }
      };

      runUpload();
    }
  }, [uploadFile, uploadStatus, setUploadStatus, setUploadProgress, setUploadError, setJobId, setVideoUrl, setUploadEstimatedTime, setUploadAbortController]);

  useEffect(() => {
    // Polling logic for analysis status
    const jobIdValue = useAppStore.getState().jobId;
    if (!jobIdValue || uploadStatus === "error" || uploadStatus === "idle" || uploadStatus === "uploading" || uploadStatus === "starting" || uploadStatus === "ready" || uploadStatus === "report_ready") return;

    let isPolling = true;
    let fallbackTimeout: ReturnType<typeof setTimeout>;

    const pollStatus = async () => {
      if (!isPolling) return;
      try {
        const response = await aimforgeService.getJobStatus(jobIdValue);
        
        if (response.current_stage) useAppStore.getState().setAnalysisStage(response.current_stage);
        if (response.progress !== undefined) useAppStore.getState().setAnalysisProgress(response.progress);

        if (response.status === "report_ready" || response.report_ready) {
          console.log("[UploadManager] Backend reported: REPORT_READY");
          
          try {
             const report = await aimforgeService.getAnalysis(jobIdValue);
             if (!report || report.status === "failed") {
                 throw new Error("Analysis completed but the coaching report could not be loaded.");
             }
             useAppStore.getState().setAnalysis(report);
             setUploadStatus("report_ready");
             useAppStore.getState().setAnalysisStage("COMPLETED");
             useAppStore.getState().setAnalysisProgress(100);
             sessionStorage.removeItem("aimforge_active_upload_job_id");
          } catch (e: any) {
             console.error("[UploadManager] Failed to fetch report:", e);
             setUploadError(`❌ Analysis completed but the coaching report could not be loaded.`);
             setUploadStatus("error");
          }
          isPolling = false;
          return;
        } else if (response.status === "error") {
          console.error("[UploadManager] Backend reported: FAILED");
          setUploadError(`❌ Backend analysis failed.`);
          setUploadStatus("error");
          isPolling = false;
          return;
        } else if (response.status === "analyzing" || response.status === "pending") {
           if (uploadStatus !== "analyzing") setUploadStatus("analyzing");
        } else if (response.status === "queued_for_analysis") {
           if (uploadStatus !== "queued_for_analysis") setUploadStatus("queued_for_analysis");
        }
      } catch (err) {
        console.error("[UploadManager] Failed to fetch job status", err);
      }
      
      if (isPolling) {
        fallbackTimeout = setTimeout(pollStatus, 2000);
      }
    };

    pollStatus();
    return () => { 
      isPolling = false; 
      if (fallbackTimeout) clearTimeout(fallbackTimeout);
    };
  }, [jobId, uploadStatus, setUploadStatus, setUploadError]);

  useEffect(() => {
    // Recovery on refresh
    const activeJobId = sessionStorage.getItem("aimforge_active_upload_job_id");
    const jobIdValue = useAppStore.getState().jobId;
    if (activeJobId && !jobIdValue && uploadStatus === "idle") {
      console.log("[UploadManager] Found active upload job ID in session storage. Recovering state...");
      setJobId(activeJobId);
      // We assume if we have a Job ID in session storage without the file, the file upload has already completed
      // and we are just waiting for analysis
      setUploadStatus("queued_for_analysis");
      setUploadProgress(100);
    }
  }, [jobId, uploadStatus, setJobId, setUploadStatus, setUploadProgress]);

  return null;
}
