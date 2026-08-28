import { useNavigate, useLocation, useOutlet } from "react-router-dom";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import {
  BarChart3,
  Crosshair,
  History,
  LayoutDashboard,
  MessageCircle,
  User,
  Zap,
} from "lucide-react";
import { Button } from "./ui/button";
import { BGMIUpdatesDropdown } from "./BGMIUpdatesDropdown";

import { useAppStore } from "../store/useAppStore";
import { RefreshCw, Cloud, Cpu, Activity, CheckCircle2, AlertCircle } from "lucide-react";

export function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const outlet = useOutlet();
  const shouldReduceMotion = useReducedMotion();
  

  const { uploadStatus, uploadProgress, uploadFile, uploadEstimatedTime, uploadError } = useAppStore();

  const getNavClasses = (path: string) => {
    const isActive = path === "/" ? location.pathname === "/" : location.pathname.startsWith(path);
    if (isActive) {
      return "cursor-pointer font-medium text-neutral-50 text-sm leading-5 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2";
    }
    return "cursor-pointer border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2 hover:text-white transition-colors";
  };

  return (
    <div className="font-sans text-neutral-50 min-h-screen w-full flex flex-col overflow-x-hidden">
      <nav className="sticky z-50 backdrop-blur-xl bg-zinc-950/80 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex top-0 px-8 py-4 justify-between items-center w-full">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate("/")}>
          <div className="size-9 shadow-[0_0_20px_oklch(0.646_0.222_41.116/0.5)] rounded-lg bg-[#f54900] flex justify-center items-center">
            <Crosshair className="size-5 text-orange-50" />
          </div>
          <span className="font-bold text-xl leading-7 tracking-tight">
            Aim<span className="text-[#f54900]">Forge</span>
          </span>
        </div>
        <div className="flex items-center gap-1 overflow-x-auto">
          <button onClick={() => navigate("/dashboard")} className={getNavClasses("/dashboard")}>
            <LayoutDashboard className="size-4" />
            Dashboard
          </button>
          <button onClick={() => navigate("/analysis")} className={getNavClasses("/analysis")}>
            <BarChart3 className="size-4" />
            Analysis
          </button>
          <button onClick={() => navigate("/history")} className={getNavClasses("/history")}>
            <History className="size-4" />
            History
          </button>
          <button onClick={() => navigate("/training")} className={getNavClasses("/training")}>
            <Zap className="size-4" />
            Training
          </button>
          <button onClick={() => navigate("/coach")} className={getNavClasses("/coach")}>
            <MessageCircle className="size-4" />
            AI Coach
          </button>
          <button onClick={() => navigate("/profile")} className={getNavClasses("/profile")}>
            <User className="size-4" />
            Profile
          </button>
        </div>
        <div className="flex items-center gap-3">
          <BGMIUpdatesDropdown />
          <Button className="rounded-lg bg-[#f54900] text-orange-50" onClick={() => navigate("/upload")}>
            Upload
          </Button>
        </div>
      </nav>

      {/* Global Upload Indicator */}
      {uploadStatus !== "idle" && uploadStatus !== "report_ready" && (
        <div className="w-full bg-zinc-900 border-b border-white/10 px-8 py-2 flex items-center justify-between text-sm shadow-sm relative z-40">
           <div className="flex items-center gap-3 w-1/3">
             {uploadStatus === "error" ? (
                <AlertCircle className="size-4 text-[#ff6467]" />
             ) : uploadStatus === "uploading" ? (
                <RefreshCw className="size-4 text-[#f54900] animate-spin" />
             ) : uploadStatus === "uploaded" ? (
                <Cloud className="size-4 text-[#00bc7d]" />
             ) : uploadStatus === "queued_for_analysis" ? (
                <Cpu className="size-4 text-[#00bc7d]" />
             ) : uploadStatus === "analyzing" ? (
                <Activity className="size-4 text-[#f54900]" />
             ) : (
                <CheckCircle2 className="size-4 text-[#00bc7d]" />
             )}
             <span className="font-medium truncate max-w-[200px]" title={uploadFile?.name || "Gameplay"}>
                {uploadFile?.name || "Gameplay Video"}
             </span>
             {uploadError && <span className="text-[#ff6467] truncate ml-2">{uploadError}</span>}
           </div>

           {!uploadError && (
              <div className="w-1/3 flex justify-center flex-col gap-1">
                 <div className="flex justify-between items-center text-xs">
                    <span className="text-[#9f9fa9]">
                      {uploadStatus === "uploading" ? "Uploading..." : 
                       uploadStatus === "uploaded" ? "Upload Complete" : 
                       uploadStatus === "queued_for_analysis" ? "Queued for Analysis..." :
                       "Analyzing..."}
                    </span>
                    <span className="text-white font-medium">{uploadStatus === "uploading" ? `${uploadProgress}%` : ""}</span>
                 </div>
                 <div className="h-1.5 w-full bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-300 ease-out ${uploadStatus === "uploading" ? "bg-[#f54900]" : "bg-[#00bc7d]"}`} 
                      style={{ width: `${uploadStatus === "uploading" ? uploadProgress : 100}%` }}
                    />
                 </div>
              </div>
           )}

           <div className="w-1/3 flex justify-end">
              {uploadStatus === "uploading" && uploadEstimatedTime && (
                <span className="text-xs text-[#9f9fa9]">{uploadEstimatedTime}</span>
              )}
           </div>
        </div>
      )}

      <main className="flex-1 w-full max-w-[1400px] mx-auto pt-4 pb-12 px-6 flex flex-col items-center overflow-visible">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{
              duration: shouldReduceMotion ? 0 : 0.25,
              ease: "easeOut"
            }}
            className="w-full flex-1 flex flex-col items-center"
          >
            {outlet}
          </motion.div>
        </AnimatePresence>
      </main>

    </div>
  );
}
