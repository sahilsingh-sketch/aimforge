/* eslint-disable */
// @ts-nocheck
import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, X, FileVideo, AlertCircle, Play, Info, Cloud, RefreshCw, CheckCircle2, Circle, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAppStore } from "../store/useAppStore";
import { aimforgeService } from "../services/api";
import bgVideo from "../assets/bg-video.mp4";

export default function UploadPage() {
  const navigate = useNavigate();
  const { 
    uploadFile: file, 
    setUploadFile, 
    uploadStatus: uploadState, 
    uploadProgress, 
    uploadEstimatedTime: estimatedTime, 
    uploadError: error,
    setUploadError: setError,
    clearUpload,
    analysisStage,
    analysisProgress,
    jobId
  } = useAppStore();
  
  const [isDragging, setIsDragging] = useState(false);
  const [thumbnail, setThumbnail] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isUploading = uploadState !== "idle" && uploadState !== "error";

  const MAX_VIDEO_SIZE_MB = Number(import.meta.env.VITE_MAX_VIDEO_SIZE_MB) || 500;
  const MAX_FILE_SIZE = MAX_VIDEO_SIZE_MB * 1024 * 1024;

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (isUploading) return;
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  useEffect(() => {
    console.log(`[Upload UI] State changed: ${uploadState}`);
    if (uploadState === "report_ready" && jobId) {
      const timer = setTimeout(() => {
        navigate(`/analysis/${jobId}`);
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [uploadState, jobId, navigate]);

  const validateAndSetFile = (selectedFile: File) => {
    setError(null);
    console.log(`[Upload UI] File selected: ${selectedFile.name} (${selectedFile.size} bytes)`);
    const validTypes = ["video/mp4", "video/quicktime", "video/x-matroska"];
    
    if (!validTypes.includes(selectedFile.type) && !selectedFile.name.endsWith(".mp4") && !selectedFile.name.endsWith(".mov") && !selectedFile.name.endsWith(".mkv")) {
      setError("❌ Unsupported file format. Please upload MP4, MOV, or MKV.");
      return;
    }
    
    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(`❌ File exceeds the ${MAX_VIDEO_SIZE_MB} MB limit.`);
      return;
    }
    
    useAppStore.getState().resetState(); // Clear previous video analysis before starting
    setUploadFile(selectedFile);
    useAppStore.getState().setUploadStatus("ready");
    generateThumbnail(selectedFile);
  };

  const generateThumbnail = (videoFile: File) => {
    const video = document.createElement("video");
    const url = URL.createObjectURL(videoFile);
    
    video.src = url;
    video.currentTime = 1;
    video.muted = true;
    
    video.onloadeddata = () => {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL("image/jpeg");
        setThumbnail(dataUrl);
      }
      URL.revokeObjectURL(url);
    };
  };

  const startUpload = () => {
    if (!file) return;
    useAppStore.getState().setUploadStatus("starting");
  };

  const cancelUpload = () => {
    const { uploadAbortController } = useAppStore.getState();
    if (uploadAbortController) {
       uploadAbortController.abort();
    }
    clearUpload();
    setThumbnail(null);
  };

  const handleCancel = () => {
    cancelUpload();
    navigate("/dashboard");
  };
  
  const retryUpload = async () => {
     setError(null);
     if (jobId) {
         try {
             await aimforgeService.retryJob(jobId);
             useAppStore.getState().setUploadStatus("queued_for_analysis");
         } catch (e: any) {
             setError(e.message);
         }
     } else {
         useAppStore.getState().setUploadStatus("starting");
     }
  };




  const analysisSteps = [
    { id: "QUEUED", label: "Processing queued" },
    { id: "FRAME_EXTRACTION", label: "Extracting frames" },
    { id: "OCR", label: "Reading gameplay HUD" },
    { id: "OBJECT_DETECTION", label: "Detecting gameplay events" },
    { id: "AI_ANALYSIS", label: "Analyzing performance" },
    { id: "REPORT_GENERATION", label: "Generating coaching report" }
  ];

  const getAnalysisStepStatus = (stepId: string, currentStage: string | null) => {
    if (!currentStage) return "pending";
    if (currentStage === "COMPLETED") return "completed";
    
    const currentIndex = analysisSteps.findIndex(s => s.id === currentStage);
    const stepIndex = analysisSteps.findIndex(s => s.id === stepId);
    
    if (stepIndex < currentIndex) return "completed";
    if (stepIndex === currentIndex) return "active";
    return "pending";
  };

  return (
    <div className="relative font-sans text-neutral-50 min-h-screen w-full flex flex-col items-center py-12 px-4 md:px-8">
      {/* Background Video */}
      <video
        autoPlay
        loop
        muted={true}
        playsInline={true}
        className="fixed inset-0 w-full h-full object-cover z-0 opacity-50"
      >
        <source src={bgVideo} type="video/mp4" />
      </video>
      
      {/* Dark overlay for readability */}
      <div className="fixed inset-0 bg-black/60 z-10 pointer-events-none" />

      {/* Main Content Wrapper */}
      <div className="w-full flex flex-col items-center relative z-20">
        <div className="w-full max-w-6xl flex justify-between items-center mb-8">
          <h1 className="font-bold text-2xl">Upload Gameplay</h1>
          <Button variant="outline" className="border-white/10 hover:bg-[#ff6467]/20 hover:text-[#ff6467] hover:border-[#ff6467]/30 transition-colors" onClick={handleCancel}>
            Cancel
          </Button>
        </div>

        <div className="w-full max-w-6xl flex flex-col lg:flex-row gap-8">
        
        {/* Info Card Sidebar */}
        <div className="w-full lg:w-1/3 flex flex-col gap-4">
          <div className="bg-zinc-900 border-white/10 border-1 border-solid rounded-3xl p-6 shadow-xl">
             <div className="flex items-center gap-3 mb-6">
                <Info className="size-6 text-[#f54900]" />
                <h3 className="font-semibold text-lg">Requirements</h3>
             </div>
             
             <ul className="flex flex-col gap-4 text-sm text-[#9f9fa9]">
                <li className="flex justify-between items-center border-b border-white/5 pb-2">
                   <span>Maximum Size:</span>
                   <span className="text-white font-medium">{MAX_VIDEO_SIZE_MB} MB</span>
                </li>
                <li className="flex justify-between items-center border-b border-white/5 pb-2">
                   <span>Recommended Length:</span>
                   <span className="text-white font-medium">15-20 minutes</span>
                </li>
                <li className="flex justify-between items-center border-b border-white/5 pb-2">
                   <span>Formats:</span>
                   <span className="text-white font-medium">MP4, MOV, MKV</span>
                </li>
             </ul>
             
             <div className="mt-8 bg-[#f54900]/10 border border-[#f54900]/20 rounded-xl p-4 flex flex-col gap-2">
               <div className="flex items-start gap-2 text-xs text-[#f54900]">
                  <Cloud className="size-4 shrink-0 mt-0.5" />
                  <p>Videos are securely stored in the cloud.</p>
               </div>
               <div className="flex items-start gap-2 text-xs text-[#f54900]">
                  <AlertCircle className="size-4 shrink-0 mt-0.5" />
                  <p>Gameplay videos are automatically deleted after 30 days.</p>
               </div>
               <div className="flex items-start gap-2 text-xs text-[#f54900]">
                  <CheckCircle2 className="size-4 shrink-0 mt-0.5" />
                  <p>Analysis reports remain permanently available.</p>
               </div>
             </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="w-full lg:w-2/3 bg-zinc-900 border-white/10 border-1 border-solid rounded-3xl p-8 flex flex-col gap-6 shadow-xl">
          
          {error && (
            <div className="bg-[#ff6467]/10 text-[#ff6467] border-[#ff6467]/30 border-1 border-solid p-4 rounded-xl flex items-center justify-between gap-3">
              <div className="flex flex-col gap-1">
                <span className="text-sm font-medium">Analysis failed</span>
                <span className="text-xs">Stage: {analysisStage || "Unknown"}</span>
                <span className="text-xs opacity-80">Reason: {error.replace("❌ ", "")}</span>
              </div>
              {uploadState === "error" && (
                <Button size="sm" onClick={retryUpload} className="bg-[#ff6467]/20 hover:bg-[#ff6467]/40 text-[#ff6467] h-8 shrink-0">
                  <RefreshCw className="size-3.5 mr-2" />
                  Retry Analysis
                </Button>
              )}
            </div>
          )}

          {!file && uploadState === "idle" ? (
            <div 
              className={`border-2 border-dashed rounded-2xl flex flex-col items-center justify-center p-12 transition-colors cursor-pointer min-h-[350px]
                ${isDragging ? 'border-[#f54900] bg-[#f54900]/5' : 'border-white/20 hover:border-white/40 bg-zinc-950'}`}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                className="hidden" 
                ref={fileInputRef} 
                accept=".mp4,.mov,.mkv,video/mp4,video/quicktime,video/x-matroska" 
                onChange={handleFileSelect} 
              />
              <div className="size-16 rounded-full bg-zinc-800 flex justify-center items-center mb-4">
                <Upload className="size-8 text-[#9f9fa9]" />
              </div>
              <h3 className="font-semibold text-lg">Drag & Drop your replay</h3>
              <p className="text-[#9f9fa9] text-sm mt-2 text-center max-w-xs">
                Supports MP4, MOV, and MKV formats up to {MAX_VIDEO_SIZE_MB} MB.
              </p>
              <Button className="mt-6 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-neutral-50" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
                Browse Files
              </Button>
            </div>
          ) : (
            <div className="flex flex-col gap-8 h-full">
              {file && (
                <div className="flex flex-col md:flex-row gap-6 items-center">
                  <div className="relative aspect-video w-full md:w-1/2 rounded-xl overflow-hidden bg-black border-white/10 border-1 border-solid flex items-center justify-center">
                    {thumbnail ? (
                      <img src={thumbnail} alt="Video thumbnail" className="w-full h-full object-cover opacity-80" />
                    ) : (
                      <FileVideo className="size-12 text-[#9f9fa9]" />
                    )}
                    <div className="absolute inset-0 flex items-center justify-center bg-black/40">
                      <Play className="size-10 text-white opacity-80" />
                    </div>
                  </div>
                  
                  <div className="flex-1 flex flex-col w-full h-full justify-center">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold text-lg break-all line-clamp-2">{file.name}</h3>
                        <p className="text-[#9f9fa9] text-sm mt-1">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                      </div>
                      <button onClick={handleCancel} className="cursor-pointer p-2 bg-zinc-800 hover:bg-[#ff6467]/20 hover:text-[#ff6467] rounded-lg transition-colors">
                        <X className="size-4" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Upload Progress Box */}
              {(uploadState === "starting" || uploadState === "uploading" || uploadState === "uploaded") && (
                <div className="mt-4 p-6 bg-zinc-950 rounded-2xl border border-white/5 flex flex-col gap-4 relative">
                  <div className="flex justify-between items-center mb-2">
                     <h4 className="font-semibold text-[#f54900]">Uploading video</h4>
                     {uploadState === "uploaded" && <CheckCircle2 className="size-5 text-[#00bc7d]" />}
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-[#9f9fa9] font-medium flex items-center gap-2">
                       {uploadState === "uploaded" ? "Video uploaded" : "Uploading video..."}
                    </span>
                    <span className="font-medium text-white">{uploadProgress}%</span>
                  </div>
                  <div className="h-2 w-full bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-[#f54900] transition-all duration-300 ease-out" 
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  {file && (
                     <div className="flex justify-between items-center text-xs text-[#9f9fa9]">
                        <span>{((uploadProgress / 100) * (file.size / (1024 * 1024))).toFixed(1)} MB / {(file.size / (1024 * 1024)).toFixed(1)} MB</span>
                        {estimatedTime && uploadProgress < 100 && <span>{estimatedTime}</span>}
                     </div>
                  )}
                </div>
              )}

              {/* Analysis Pipeline Box */}
              {(uploadState === "queued_for_analysis" || uploadState === "analyzing" || uploadState === "report_ready") && (
                <div className="mt-4 p-6 bg-zinc-950 rounded-2xl border border-white/5 flex flex-col gap-4 relative">
                   <div className="flex justify-between items-center mb-4">
                     <h4 className="font-semibold text-white">AI Gameplay Analysis</h4>
                     {uploadState === "report_ready" && <CheckCircle2 className="size-5 text-[#00bc7d]" />}
                   </div>
                   
                   <div className="flex flex-col gap-3 ml-2">
                      <div className="flex items-center gap-3 text-sm text-[#9f9fa9]">
                         <Check className="size-4 text-[#00bc7d]" />
                         <span className="text-white">Video uploaded</span>
                      </div>
                      
                      {analysisSteps.map(step => {
                         const status = getAnalysisStepStatus(step.id, analysisStage);
                         return (
                           <div key={step.id} className={`flex items-center gap-3 text-sm transition-colors ${status === 'active' ? 'text-white' : status === 'completed' ? 'text-[#9f9fa9]' : 'text-zinc-600'}`}>
                              {status === 'completed' ? (
                                <Check className="size-4 text-[#00bc7d]" />
                              ) : status === 'active' ? (
                                <RefreshCw className="size-4 text-[#f54900] animate-spin" />
                              ) : (
                                <Circle className="size-4" />
                              )}
                              <span className={status === 'completed' ? 'text-white' : ''}>
                                {step.label} {status === 'active' && analysisProgress > 0 && `(${analysisProgress}%)`}
                              </span>
                           </div>
                         );
                      })}
                   </div>
                   
                   <div className="mt-4 pt-4 border-t border-white/5">
                      {uploadState === "report_ready" ? (
                         <div className="flex flex-col gap-4">
                            <div className="flex items-center gap-2 text-[#00bc7d] font-medium">
                               <CheckCircle2 className="size-5" />
                               <span>Analysis Complete</span>
                            </div>
                            <p className="text-sm text-[#9f9fa9]">Your coaching report is ready.</p>
                            <Button 
                              className="w-full bg-[#f54900] text-white hover:bg-[#d84000]" 
                              onClick={() => navigate('/history')}
                            >
                              View Analysis
                            </Button>
                         </div>
                      ) : (
                         <div className="flex flex-col gap-2">
                           <div className="flex justify-between text-sm text-[#9f9fa9]">
                             <span>Overall Progress</span>
                             <span className="text-white">{analysisProgress}%</span>
                           </div>
                           <div className="h-1.5 w-full bg-zinc-800 rounded-full overflow-hidden">
                             <div 
                               className="h-full bg-[#f54900] transition-all duration-300 ease-out" 
                               style={{ width: `${analysisProgress}%` }}
                             />
                           </div>
                         </div>
                      )}
                   </div>
                </div>
              )}

              <div className="flex justify-end gap-3 mt-auto pt-4 border-t border-white/10">
                {uploadState === "ready" && (
                  <>
                    <Button variant="outline" className="border-white/10 hover:bg-[#ff6467]/20 hover:text-[#ff6467] transition-colors" onClick={handleCancel}>
                      Cancel
                    </Button>
                    <Button className="bg-[#f54900] text-orange-50 hover:bg-[#d84000]" onClick={startUpload}>
                      Upload & Analyze
                    </Button>
                  </>
                )}
                {isUploading && uploadState !== "error" && uploadState !== "report_ready" && (
                  <>
                    <Button variant="outline" className="border-white/10 hover:bg-[#ff6467]/20 hover:text-[#ff6467] hover:border-[#ff6467]/30 transition-colors" onClick={handleCancel}>
                      Cancel
                    </Button>
                    <Button variant="outline" className="border-white/10 opacity-50 cursor-not-allowed">
                      Processing...
                    </Button>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
    </div>
  );
}
