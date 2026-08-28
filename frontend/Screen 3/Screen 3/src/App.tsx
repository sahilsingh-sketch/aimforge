import { useEffect } from "react";
import {
  ArrowDownUp,
  BarChart3,
  CalendarRange,
  ChevronRight,
  Clock3,
  Filter,
  History,
  LayoutDashboard,
  MessageCircle,
  PlayCircle,
  Sparkles,
  Target,
  TimerReset,
  Trophy,
  User,
  Video,
  Zap,
} from "lucide-react";

export default function App() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="max-w-[1140px] flex mx-auto p-8 flex-col gap-8 w-full">
          <div className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-6 justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="size-12 shadow-[0_0_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900]/15 text-[#f54900] flex justify-center items-center">
                <History className="size-6" />
              </div>
              <div className="flex flex-col gap-1">
                <div className="font-semibold text-2xl leading-8 tracking-tight">
                  AimForge
                </div>
                <div className="text-[#9f9fa9] text-sm leading-5">
                  Gameplay history and replay archive
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-zinc-900 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid px-4 py-2">
                Desktop History
              </div>
              <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-sm leading-5 border-[#f54900]/30 border-1 border-solid px-4 py-2">
                Saved 128 replays
              </div>
            </div>
          </div>
          <div className="text-[#9f9fa9] text-sm leading-5 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-4 items-center gap-6">
            <div className="text-neutral-50 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex pb-3 items-center gap-2">
              <LayoutDashboard className="size-4" />
              <span>Dashboard</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <BarChart3 className="size-4" />
              <span>Analysis</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <History className="size-4" />
              <span>History</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <Zap className="size-4" />
              <span>Training</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <MessageCircle className="size-4" />
              <span>AI Coach</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <User className="size-4" />
              <span>Profile</span>
            </div>
          </div>
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
                      248
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
                      <div className="rounded-full bg-[#f54900] text-orange-50 px-3 py-1">
                        Ranked
                      </div>
                      <div className="rounded-full text-[#9f9fa9] border-white/10 border-1 border-solid px-3 py-1">
                        Scrim
                      </div>
                      <div className="rounded-full text-[#9f9fa9] border-white/10 border-1 border-solid px-3 py-1">
                        Custom
                      </div>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="font-medium text-sm leading-5">
                      Date Range
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 flex mt-2 justify-between items-center">
                      <span>Last 7 days</span>
                      <CalendarRange className="size-4" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="font-medium text-sm leading-5">Sort By</div>
                    <div className="text-[#9f9fa9] text-sm leading-5 flex mt-2 justify-between items-center">
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
                    24 new
                  </div>
                </div>
                <div className="flex mt-5 flex-col gap-3">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Miramar Ranked</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          02:14 · 94% confidence
                        </div>
                      </div>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Erangel Scrim</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          04:41 · clutch review
                        </div>
                      </div>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Sanhok Duo</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          01:08 · pre-aim check
                        </div>
                      </div>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
