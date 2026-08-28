/* eslint-disable */
// @ts-nocheck
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Cpu, CheckCircle2, Crosshair, Map, WandSparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useAppStore } from "../store/useAppStore";
import { aimforgeService } from "../services/api";
export default function ProcessingPage() {
  const navigate = useNavigate();
  const { jobId } = useAppStore();
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState(0);

  const stages = [
    { icon: <Cpu className="size-5 text-[#f54900]" />, text: "Extracting match frames..." },
    { icon: <Crosshair className="size-5 text-[#f54900]" />, text: "Analyzing crosshair placement and recoil..." },
    { icon: <Map className="size-5 text-[#f54900]" />, text: "Mapping positioning heatmaps..." },
    { icon: <WandSparkles className="size-5 text-[#f54900]" />, text: "Generating personalized coaching tips..." },
    { icon: <CheckCircle2 className="size-5 text-[#00bc7d]" />, text: "Analysis Complete!" }
  ];

  useEffect(() => {
    if (!jobId) {
      console.warn("No jobId found, cannot poll status");
      return;
    }
    
    let isPolling = true;

    const pollStatus = async () => {
      if (!isPolling) return;
      try {
        const response = await aimforgeService.getJobStatus(jobId);
        const status = response.status ? response.status.toUpperCase() : "";
        console.log(`[FRONTEND] Parsed status: ${status}, current_stage: ${response.current_stage}, report_ready: ${response.report_ready}`);

        if (response.report_ready || status === "REPORT_READY") {
          console.log("[FRONTEND] Job is complete! Navigating to dashboard...");
          setProgress(100);
          setStage(4);
          isPolling = false;
          setTimeout(() => navigate("/dashboard"), 1000);
          return;
        } else if (status === "FAILED" || status === "ERROR" || status === "CANCELLED") {
          console.error(`[FRONTEND] Job failed with status: ${status}`);
          isPolling = false;
          alert("Video processing failed or timed out. Please try again.");
          navigate("/dashboard");
          return;
        } else {
          console.log(`[FRONTEND] Still processing... (stage: ${response.current_stage})`);
          // Map backend stage to frontend stage
          const stageMap: Record<string, number> = {
            "QUEUED": 0,
            "UPLOADING": 0,
            "PROCESSING": 0,
            "METADATA_EXTRACTION": 0,
            "FRAME_EXTRACTION": 0,
            "OCR": 1,
            "OBJECT_DETECTION": 1,
            "CROSSHAIR": 1,
            "MOVEMENT": 2,
            "DEBUG_GENERATION": 2,
            "AI_ANALYSIS": 3,
            "REPORT_GENERATION": 3,
            "COMPLETED": 4
          };
          if (response.stage && response.stage in stageMap) {
             setStage(stageMap[response.stage]);
          }
          if (response.progress !== undefined) {
             setProgress(response.progress);
          }
        }
      } catch (err) {
        console.error("Failed to fetch job status", err);
      }
      
      if (isPolling) {
        setTimeout(pollStatus, 2000); // poll every 2 seconds
      }
    };
    
    pollStatus();

    return () => { isPolling = false; };
  }, [jobId, navigate]);

  return (
    <div className="font-sans bg-zinc-950 text-neutral-50 min-h-screen w-full flex items-center justify-center py-12 px-8 overflow-hidden relative">
      <div className="-z-10 bg-[radial-gradient(ellipse_at_center,oklch(0.646_0.222_41.116/0.15),transparent_60%)] absolute inset-0" />
      
      <div className="w-full max-w-lg flex flex-col items-center gap-8">
        <Badge className="rounded-full bg-zinc-800 text-neutral-50 border-white/10 border-1 border-solid px-4 py-1.5 gap-2 shadow-[0_0_20px_rgba(249,115,22,0.2)]">
          <Cpu className="size-3.5 text-[#f54900] animate-pulse" />
          AI Processing
        </Badge>
        
        <div className="relative size-32">
          {/* Animated rings */}
          <div className="absolute inset-0 rounded-full border-2 border-[#f54900]/20 border-t-[#f54900] animate-spin" style={{ animationDuration: '2s' }} />
          <div className="absolute inset-2 rounded-full border-2 border-[#f54900]/20 border-b-[#f54900] animate-spin" style={{ animationDuration: '3s', animationDirection: 'reverse' }} />
          
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-3xl font-bold font-mono text-neutral-50">
              {progress}%
            </span>
          </div>
        </div>

        <div className="w-full bg-zinc-900 border-white/10 border-1 border-solid rounded-2xl p-6 shadow-2xl flex flex-col gap-4 relative overflow-hidden">
          {/* Progress bar background in card */}
          <div 
            className="absolute top-0 left-0 bottom-0 bg-[#f54900]/5 transition-all duration-300 ease-out z-0"
            style={{ width: `${progress}%` }}
          />
          
          <div className="z-10">
            <h3 className="font-semibold text-lg mb-4">Processing Pipeline</h3>
            <div className="flex flex-col gap-3">
              {stages.map((s, idx) => (
                <div 
                  key={idx} 
                  className={`flex items-center gap-3 text-sm transition-all duration-500 ${
                    idx < stage ? "opacity-50 text-[#9f9fa9]" : 
                    idx === stage ? "opacity-100 font-medium" : "opacity-20 text-[#9f9fa9]"
                  }`}
                >
                  <div className={`size-8 rounded-full flex justify-center items-center ${idx === stage ? 'bg-[#f54900]/10 border border-[#f54900]/30 shadow-[0_0_10px_rgba(249,115,22,0.3)]' : 'bg-transparent'}`}>
                    {idx < stage ? <CheckCircle2 className="size-5 text-[#00bc7d]" /> : s.icon}
                  </div>
                  <span>{s.text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
