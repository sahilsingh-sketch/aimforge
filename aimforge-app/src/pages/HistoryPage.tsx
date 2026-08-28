import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  ArrowDownUp,
  CalendarRange,
  ChevronRight,
  Clock3,
  Filter,
  PlayCircle,
  Sparkles,
  Target,
  TimerReset,
  Trophy,
  Video,
} from "lucide-react";

import { ComingSoonModal } from "@/components/ComingSoonModal";
import { aimforgeService } from "../services/api";

export default function App() {
  const navigate = useNavigate();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [modalOpen, setModalOpen] = useState(false);
  const [modalFeature] = useState("");
  const [gameplays, setGameplays] = useState<any[]>([]);

  useEffect(() => {
    const loadGameplays = async () => {
      try {
        const results = await aimforgeService.getHistory();
        setGameplays(results);
      } catch (e) {
        console.error("Failed to load history", e);
      }
    };
    loadGameplays();
  }, []);

  return (
    <div className="w-full flex flex-col gap-8">
      <div className="grid gap-6">
            <div className="flex flex-col gap-6">
              <div className="shadow-[0_20px_60px_rgba(0,0,0,0.35)] rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-4 justify-between items-center gap-4">
                  <div className="flex items-center gap-3">
                    <div className="font-medium rounded-full bg-[#f54900]/15 text-[#f54900] text-xs leading-4 px-3 py-1">
                      Replay Library
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Filter, compare, and revisit previous matches
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-2">
                      All Modes
                    </div>
                    <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-2">
                      Ranked
                    </div>
                  </div>
                </div>
                <div className="grid mt-6 gap-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Total Matches
                      </div>
                      <PlayCircle className="size-4 text-[#f54900]" />
                    </div>
                    <div className="font-semibold text-3xl leading-9 mt-3">
                      {gameplays.length || 248}
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Recorded sessions in archive
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Win Rate
                      </div>
                      <Trophy className="size-4 text-[#f54900]" />
                    </div>
                    <div className="font-semibold text-3xl leading-9 mt-3">
                      61%
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Across the last 90 days
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Avg. Review Time
                      </div>
                      <Clock3 className="size-4 text-[#f54900]" />
                    </div>
                    <div className="font-semibold text-3xl leading-9 mt-3">
                      14m
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Per replay session
                    </div>
                  </div>
                </div>
                <div className="rounded-3xl bg-zinc-950 border-white/10 border-1 border-solid mt-6 p-5">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-semibold text-lg leading-7">
                        Recent Match Timeline
                      </div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Jump back into any critical moment
                      </div>
                    </div>
                    <div className="rounded-full text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                      Auto-synced
                    </div>
                  </div>
                  <div className="flex mt-5 items-center gap-4">
                    <div className="size-16 rounded-2xl bg-[#f54900]/15 text-[#f54900] flex justify-center items-center">
                      <Video className="size-7" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm leading-5 flex justify-between items-center">
                        <span className="font-medium">
                          Match Replay · Round 12
                        </span>
                        <span className="text-[#9f9fa9]">02:14 / 06:38</span>
                      </div>
                      <div className="rounded-full bg-zinc-800 mt-3 h-2">
                        <div className="w-[68%] shadow-[0_0_18px_rgba(249,115,22,0.45)] rounded-full bg-[#f54900] h-2" />
                      </div>
                      <div className="text-[#9f9fa9] text-xs leading-4 flex mt-3 justify-between items-center">
                        <span>Opening</span>
                        <span>Mid-round</span>
                        <span>Clutch</span>
                        <span>Endgame</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid gap-4">
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-[#f54900]/15 text-[#f54900] p-2">
                      <Target className="size-4" />
                    </div>
                    <div>
                      <div className="font-medium">Aim Stability</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Tracked across sessions
                      </div>
                    </div>
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-5">
                    8.7
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-[#f54900]/15 text-[#f54900] p-2">
                      <TimerReset className="size-4" />
                    </div>
                    <div>
                      <div className="font-medium">Reaction Time</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Compared to baseline
                      </div>
                    </div>
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-5">
                    +34%
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-[#f54900]/15 text-[#f54900] p-2">
                      <Sparkles className="size-4" />
                    </div>
                    <div>
                      <div className="font-medium">Coach Notes</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        AI summaries saved
                      </div>
                    </div>
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-5">
                    890K
                  </div>
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      History Filters
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Narrow down previous gameplay
                    </div>
                  </div>
                  <Filter className="size-5 text-[#f54900]" />
                </div>
                <div className="flex mt-5 flex-col gap-3">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="font-medium text-sm leading-5">Mode</div>
                    <div className="text-sm leading-5 flex mt-2 gap-2">
                      <div className="cursor-pointer rounded-full bg-[#f54900] text-orange-50 px-3 py-1">
                        Ranked
                      </div>
                      <div className="cursor-pointer rounded-full text-[#9f9fa9] border-white/10 border-1 border-solid px-3 py-1 hover:text-white transition-colors">
                        Scrim
                      </div>
                      <div className="cursor-pointer rounded-full text-[#9f9fa9] border-white/10 border-1 border-solid px-3 py-1 hover:text-white transition-colors">
                        Custom
                      </div>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="font-medium text-sm leading-5">
                      Date Range
                    </div>
                    <div className="cursor-pointer text-[#9f9fa9] text-sm leading-5 flex mt-2 justify-between items-center hover:text-white transition-colors">
                      <span>Last 7 days</span>
                      <CalendarRange className="size-4" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="font-medium text-sm leading-5">Sort By</div>
                    <div className="cursor-pointer text-[#9f9fa9] text-sm leading-5 flex mt-2 justify-between items-center hover:text-white transition-colors">
                      <span>Most recent</span>
                      <ArrowDownUp className="size-4" />
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      Saved Replays
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Quick access to previous games
                    </div>
                  </div>
                  <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                    {gameplays.length} new
                  </div>
                </div>
                <div className="flex mt-5 flex-col gap-3">
                  {gameplays.map(job => (
                    <div 
                      key={job.job_id} 
                      onClick={() => job.status === "COMPLETED" ? navigate(`/analysis/${job.job_id}`) : null}
                      className={`cursor-pointer rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 transition-colors ${job.status === "COMPLETED" ? 'hover:border-[#f54900]' : 'opacity-60 cursor-not-allowed'}`}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <div className="font-medium max-w-[200px] md:max-w-[300px] truncate">{job.filename}</div>
                          <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
                            <span>{new Date(job.created_at).toLocaleDateString()}</span>
                            <span>·</span>
                            <span className={job.status === "COMPLETED" ? "text-[#00bc7d]" : "text-yellow-500"}>{job.status}</span>
                          </div>
                        </div>
                        {job.status === "COMPLETED" && <ChevronRight className="size-4 text-[#9f9fa9]" />}
                      </div>
                    </div>
                  ))}
                  {gameplays.length === 0 && (
                    <div className="text-center py-6 text-[#9f9fa9]">
                      No replays found. Upload a video to see it here!
                    </div>
                  )}
                </div>
              </div>
            </div>
        </div>
      <ComingSoonModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        featureName={modalFeature} 
      />
    </div>
  );
}
