import { useEffect, useState, useRef } from "react";
import { aimforgeService } from "../services/api";
import { Loader2 } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import {
  BarChart3,
  Sparkles,
} from "lucide-react";

export default function AnalysisPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentVideoTime, setCurrentVideoTime] = useState(0);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    let isMounted = true;
    const fetchAnalysis = async () => {
      setLoading(true);
      try {
        let currentJobId = jobId;
        
        // If no jobId is in the URL, fetch the latest completed job
        if (!currentJobId) {
            const gameplays = await aimforgeService.getHistory();
            const latestCompleted = gameplays.find((g: any) => g.status === "COMPLETED");
            if (latestCompleted) {
                currentJobId = latestCompleted.job_id;
            } else {
                if (isMounted) {
                    setLoading(false);
                }
                return;
            }
        }
        
        const result = await aimforgeService.getAnalysis(currentJobId);
        if (isMounted) {
            setData(result);
            setLoading(false);
        }
      } catch (e: any) {
        if (isMounted) {
            setError(e.response?.data?.detail || "Failed to load analysis.");
            setLoading(false);
        }
      }
    };

    fetchAnalysis();
    return () => { isMounted = false; };
  }, [jobId]);

  const handleSeek = (seconds: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = seconds;
      videoRef.current.play();
    }
    setCurrentVideoTime(seconds);
  };



  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-neutral-50 p-6 text-center">
        <h2 className="text-3xl font-bold mb-4 text-[#ff6467]">AI Analysis Failed</h2>
        <p className="text-[#9f9fa9] mb-4 text-lg">We were unable to load your coaching report.</p>
        <div className="bg-black/50 border border-white/10 rounded-xl p-6 text-left mb-6 max-w-lg w-full">
          <div className="text-sm text-neutral-300 mb-2 font-mono whitespace-pre-wrap text-xs">Reason: {error}</div>
        </div>
        <button onClick={() => navigate("/history")} className="cursor-pointer px-6 py-3 bg-[#f54900] text-white rounded-lg font-semibold hover:bg-[#ff6467] transition-colors">Return to History</button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-[#f54900]">
        <Loader2 className="size-12 animate-spin mb-6" />
        <h2 className="text-2xl font-bold text-neutral-50 mb-2">Loading Gameplay...</h2>
        <p className="text-[#9f9fa9] text-lg">Fetching your personalized analysis report</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-neutral-50">
        <h2 className="text-2xl font-bold mb-4">No Video Selected</h2>
        <p className="text-[#9f9fa9] mb-6">Upload a gameplay video to get started.</p>
        <button onClick={() => navigate("/dashboard")} className="cursor-pointer px-6 py-2 rounded-xl bg-[#f54900] hover:bg-[#d84000] text-white transition font-semibold">
          Go to Dashboard
        </button>
      </div>
    );
  }

  const analysis = data.report || {};
  const events = data.events || [];
  const videoUrl = data.video?.url;

  return (
    <div className="w-full flex flex-col gap-8">
      <div className="grid gap-6">
            <div className="flex flex-col gap-6">
              <div className="shadow-[0_0_0_1px_oklch(1_0_0/.02),0_24px_80px_oklch(0_141_0_005_285_823/.35)] rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center gap-4">
                  <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid flex px-3 py-1 items-center gap-2">
                    <Sparkles className="size-3.5 text-[#f54900]" />
                    AI-generated timestamp feedback
                  </div>
                  <div className="text-[#9f9fa9] text-xs leading-4">
                    Replay synced to every critical moment
                  </div>
                </div>
                <div className="rounded-2xl bg-black border-white/10 border-1 border-solid mt-5 overflow-hidden">
                  <div className="text-[#9f9fa9] text-xs leading-4 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex px-4 py-3 justify-between items-center">
                    <div className="flex items-center gap-2">
                      <span className="size-2 rounded-full bg-[#ff6467]" />
                      <span className="size-2 rounded-full bg-[#f54900]" />
                      <span className="size-2 rounded-full bg-[#00bc7d]" />
                    </div>
                    <div>Match Replay</div>
                    <div className="text-[#f54900]">Live Analysis</div>
                  </div>
                  <div className="relative aspect-[16/9] overflow-hidden bg-zinc-800">
                    {videoUrl ? (
                      <video
                        ref={videoRef}
                        src={videoUrl}
                        className="object-cover w-full h-full"
                        controls
                        onTimeUpdate={(e) => setCurrentVideoTime(e.currentTarget.currentTime)}
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-zinc-500">
                        No video available
                      </div>
                    )}
                    
                    {events && events.length > 0 && (
                      <div className="pointer-events-none absolute inset-x-6 bottom-16 flex justify-between items-end gap-4">
                        <div className="max-w-md backdrop-blur-sm rounded-2xl bg-zinc-950/80 border-white/10 border-1 border-solid p-4">
                          <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                            AI Insight ({events[0].timestamp})
                          </div>
                          <div className="text-neutral-50 text-sm leading-6 mt-2">
                            {events[0].description}
                          </div>
                        </div>
                        <div className="backdrop-blur-sm text-right rounded-2xl bg-zinc-950/80 border-white/10 border-1 border-solid px-4 py-3">
                          <div className="text-[#9f9fa9] text-xs leading-4">
                            Confidence
                          </div>
                          <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-1">
                            {events[0].confidence}%
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="grid gap-4">
                {events?.map((ev: any, idx: number) => (
                  <div key={idx} className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5 hover:border-[#f54900] transition-colors cursor-pointer" onClick={() => handleSeek(ev.seconds)}>
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                      Timestamp
                    </div>
                    <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-3">
                      {ev.timestamp}
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2 flex justify-between">
                      <span>{ev.description}</span>
                      <span className="text-xs uppercase px-2 py-1 bg-zinc-800 rounded-md ml-4 whitespace-nowrap">{ev.severity}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-sm leading-5">
                      Analysis Summary
                    </div>
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Key metrics from this session
                    </div>
                  </div>
                  <BarChart3 className="size-5 text-[#f54900]" />
                </div>
                <div className="grid grid-cols-2 mt-5 gap-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Overall Score
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      {analysis.overallScore?.toFixed(1) || "N/A"}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Aim Rating
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      {analysis.ratings?.aim || "N/A"}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Game Sense
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      {analysis.ratings?.gameSense || "N/A"}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Events Found
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      {events?.length || 0}
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="font-semibold text-sm leading-5">
                  Strengths & Weaknesses
                </div>
                <div className="mt-4 flex flex-col gap-4">
                  <div>
                    <h4 className="text-[#00bc7d] text-xs font-bold uppercase tracking-wider mb-2">Strengths</h4>
                    <ul className="list-disc pl-4 text-sm text-[#9f9fa9]">
                      {analysis.strengths?.map((s: string, i: number) => <li key={i}>{s}</li>)}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-[#ff6467] text-xs font-bold uppercase tracking-wider mb-2">Weaknesses</h4>
                    <ul className="list-disc pl-4 text-sm text-[#9f9fa9]">
                      {analysis.weaknesses?.map((w: string, i: number) => <li key={i}>{w}</li>)}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          </div>
    );
}
