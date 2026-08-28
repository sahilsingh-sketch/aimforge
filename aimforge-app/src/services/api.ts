import axios from "axios";
import type { AnalysisResponse, ChatMessage } from "../types";

export const API_BASE_URL = import.meta.env.VITE_API_URL || "";

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

export const aimforgeService = {
  checkUploadHealth: async (): Promise<{ status: "ok" | "error"; message?: string }> => {
    try {
      const response = await api.get(`${API_BASE_URL}/api/v1/health/upload`);
      return response.data;
    } catch (error: any) {
      return { 
        status: "error", 
        message: error.response?.data?.message || "Backend health check failed. Cannot connect to server." 
      };
    }
  },

  uploadVideo: async (file: File, onProgress?: (percent: number) => void, signal?: AbortSignal): Promise<{ jobId: string, message?: string }> => {
    if (!file || !file.name || file.size === 0) {
      console.warn("[UPLOAD API] Presign blocked: invalid or no file provided");
      throw new Error("Invalid file provided for upload.");
    }
    try {
      console.log("[UPLOAD API] Requesting upload session (presign)...");
      // 1. Get Presigned URL
      const presignResponse = await api.post(`/api/v1/upload/presign`, {
        filename: file.name,
        content_type: file.type || "video/mp4",
        file_size: file.size
      }, { signal });
      const { job_id, presigned_url } = presignResponse.data;
      console.log(`[UPLOAD API] Upload session received. Job ID: ${job_id}`);

      console.log("[UPLOAD API] Starting S3 upload...");
      // 2. Upload directly to S3
      await axios.put(presigned_url, file, {
        headers: {
          'Content-Type': file.type || "video/mp4"
        },
        signal,
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            console.log(`[UPLOAD API] Upload progress: ${percentCompleted}%`);
            if (onProgress) {
              onProgress(Math.min(99, percentCompleted));
            }
          }
        }
      });
      console.log("[UPLOAD API] S3 upload complete.");

      console.log("[UPLOAD API] Calling completion endpoint...");
      // 3. Complete Upload
      const completeResponse = await api.post(`/api/v1/upload/complete`, {
        job_id: job_id
      }, { signal });
      console.log("[UPLOAD API] Upload completed successfully.");

      return { jobId: completeResponse.data.job_id, message: completeResponse.data.message };
    } catch (error: any) {
      if (axios.isCancel(error)) {
        console.log("[UPLOAD API] Upload cancelled by user.");
        throw error;
      }
      console.error("[UPLOAD API] Upload error:", error);
      const detail = error.response?.data?.detail;
      const message = typeof detail === 'string' ? detail : (error.response?.data?.error?.message || "Failed to upload video");
      throw new Error(message);
    }
  },

  validateBgmi: async (file: File): Promise<{ valid: boolean, reason: string }> => {
    return new Promise(async (resolve, reject) => {
        const video = document.createElement("video");
        video.src = URL.createObjectURL(file);
        video.muted = true;
        
        video.onloadedmetadata = async () => {
            try {
                const duration = video.duration;
                if (!duration || duration <= 0) {
                     return resolve({ valid: false, reason: "Invalid video duration." });
                }
                
                // Sample at 10s, 25%, 50%, 75%, and 90%
                const sampleTimes = [10, duration * 0.25, duration * 0.5, duration * 0.75, duration * 0.9].filter(t => t < duration);
                const formData = new FormData();
                
                const canvas = document.createElement("canvas");
                // Downscale for fast transport and OCR
                canvas.width = 1280;
                canvas.height = 720;
                const ctx = canvas.getContext("2d");
                
                if (!ctx) return resolve({ valid: false, reason: "Canvas context not supported" });
                
                for (let i = 0; i < sampleTimes.length; i++) {
                    const time = sampleTimes[i];
                    video.currentTime = time;
                    await new Promise<void>((r) => { video.onseeked = () => r(); });
                    
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const blob = await new Promise<Blob | null>((r) => canvas.toBlob(r, 'image/jpeg', 0.8));
                    if (blob) {
                        formData.append("frames", blob, `frame_${i}.jpg`);
                    }
                }
                
                const response = await api.post(`/api/v1/upload/validate-bgmi`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                
                resolve({ valid: response.data.valid, reason: response.data.reason });
            } catch (err: any) {
                console.error("[BGMI_VALIDATOR] Failed to validate", err);
                // Fail-open or Fail-closed? The user wants strict validation.
                resolve({ valid: false, reason: "Unable to verify gameplay." });
            } finally {
                URL.revokeObjectURL(video.src);
            }
        };
        
        video.onerror = () => {
            resolve({ valid: false, reason: "Unsupported or corrupted video file." });
        };
    });
  },

  initMultipart: async (filename: string, contentType: string, fileSize: number, signal?: AbortSignal) => {
    if (!filename || !fileSize || fileSize === 0) {
      console.warn("[UPLOAD API] Multipart Init blocked: missing or invalid file information");
      throw new Error("Invalid file information provided for multipart upload.");
    }
    console.log("[UPLOAD API] Init multipart request...");
    const response = await api.post(`/api/v1/upload/multipart/init`, {
      filename,
      content_type: contentType,
      file_size: fileSize
    }, { signal });
    return response.data;
  },

  presignMultipart: async (jobId: string, uploadId: string, partNumber: number, signal?: AbortSignal) => {
    const response = await api.post(`/api/v1/upload/multipart/presign`, {
      job_id: jobId,
      upload_id: uploadId,
      part_number: partNumber
    }, { signal });
    return response.data;
  },

  completeMultipart: async (jobId: string, uploadId: string, parts: { ETag: string, PartNumber: number }[], signal?: AbortSignal) => {
    console.log("[UPLOAD API] Calling multipart completion endpoint...");
    const response = await api.post(`/api/v1/upload/multipart/complete`, {
      job_id: jobId,
      upload_id: uploadId,
      parts
    }, { signal });
    return response.data;
  },
  getJobStatus: async (jobId: string): Promise<{ status: "pending" | "queued_for_analysis" | "analyzing" | "report_ready" | "error", current_stage?: string, progress?: number, report_ready?: boolean }> => {
    try {
      console.log(`[API] Polling status for job: ${jobId}`);
      const response = await api.get(`${API_BASE_URL}/api/v1/jobs/${jobId}`);
      const data = response.data;
      console.log(`[API] Received status payload:`, data);
      
      if (data.status === "COMPLETED" || data.report_ready === true) return { status: "report_ready", current_stage: data.stage || data.current_stage, progress: data.progress, report_ready: true };
      if (data.status === "FAILED") return { status: "error", current_stage: data.stage || data.current_stage, progress: data.progress };
      if (data.status === "PROCESSING") return { status: "analyzing", current_stage: data.stage || data.current_stage, progress: data.progress };
      if (data.status === "QUEUED") return { status: "queued_for_analysis", current_stage: data.stage || data.current_stage, progress: data.progress };
      return { status: "pending", current_stage: data.stage || data.current_stage, progress: data.progress };
    } catch (e) {
      console.error("[API] Status polling error:", e);
      return { status: "error" };
    }
  },

  retryJob: async (jobId: string) => {
    try {
      const response = await api.post(`${API_BASE_URL}/api/v1/jobs/${jobId}/retry`);
      return response.data;
    } catch (e: any) {
      console.error("[API] Retry error:", e);
      throw new Error(e.response?.data?.detail || "Failed to retry analysis.");
    }
  },

  getAnalysis: async (jobId: string): Promise<AnalysisResponse | any> => {
    try {
      const response = await api.get(`${API_BASE_URL}/api/v1/analysis/${jobId}`);
      return response.data as AnalysisResponse;
    } catch (e: any) {
      if (e.response && e.response.data && e.response.data.status === "failed") {
        return e.response.data; // return structured error
      }
      console.error("Analysis error:", e);
      throw e;
    }
  },

  sendChatMessage: async (jobId: string, message: string): Promise<ChatMessage> => {
    try {
      const response = await api.post(`${API_BASE_URL}/api/v1/chat/${jobId}`, {
        message
      });
      return response.data.message;
    } catch (e: any) {
      console.error("Chat error:", e);
      const message = e.response?.data?.detail || "Failed to connect to the AI Coach.";
      throw new Error(message);
    }
  },

  getChatHistory: async (jobId: string): Promise<ChatMessage[]> => {
    try {
      const response = await api.get(`${API_BASE_URL}/api/v1/chat/${jobId}`);
      return response.data;
    } catch (e) {
      console.error("Chat history error:", e);
      return [];
    }
  },

  getHistory: async () => {
    try {
      const response = await api.get(`${API_BASE_URL}/api/v1/gameplays`);
      return response.data;
    } catch (e) {
      console.error("History error:", e);
      return [];
    }
  }
};
