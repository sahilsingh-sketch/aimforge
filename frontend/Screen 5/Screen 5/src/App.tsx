import { useEffect } from "react";
import {
  BarChart3,
  BookMarked,
  Bot,
  Check,
  ChevronRight,
  Clock3,
  Flame,
  History,
  LayoutDashboard,
  MessageCircle,
  MessageSquare,
  Send,
  Settings2,
  Sparkles,
  Star,
  Target,
  User,
  WandSparkles,
  Zap,
} from "lucide-react";

export default function App() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-screen max-w-[1140px] flex mx-auto px-8 py-6 flex-col w-full">
          <div className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-5 justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="size-12 shadow-[0_0_30px_rgba(249,115,22,0.18)] rounded-2xl bg-[#f54900]/15 text-[#f54900] flex justify-center items-center">
                <MessageCircle className="size-6" />
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-2xl leading-8 tracking-tight">
                  AimForge AI Coach
                </div>
                <div className="text-[#9f9fa9] text-sm leading-5">
                  Ask anything about your gameplay, mistakes, timing, or
                  decision-making.
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-zinc-900 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid px-4 py-2">
                Desktop Coach
              </div>
              <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-sm leading-5 border-[#f54900]/30 border-1 border-solid px-4 py-2">
                Live Guidance
              </div>
            </div>
          </div>
          <div className="text-[#9f9fa9] text-sm leading-5 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex mt-6 pb-4 items-center gap-8">
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
            <div className="text-neutral-50 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex pb-3 items-center gap-2">
              <MessageCircle className="size-4" />
              <span>AI Coach</span>
            </div>
            <div className="flex pb-3 items-center gap-2">
              <User className="size-4" />
              <span>Profile</span>
            </div>
          </div>
          <div className="grid grid-cols-[1.35fr_0.85fr] mt-8 flex-1 gap-6">
            <div className="flex flex-col gap-6">
              <div className="shadow-[0_20px_60px_rgba(0,0,0,0.35)] rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center gap-4">
                  <div className="space-y-2">
                    <div className="inline-flex font-medium rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/20 border-1 border-solid px-3 py-1 items-center gap-2">
                      <Sparkles className="size-3.5" />
                      AI Coach Session
                    </div>
                    <div className="font-semibold text-3xl leading-9 tracking-tight">
                      Get instant answers from your replay data
                    </div>
                    <div className="max-w-2xl text-[#9f9fa9] text-sm leading-6">
                      Ask about crosshair placement, recoil control, peeking,
                      utility timing, or why a fight was lost. The coach
                      responds with timestamp-aware guidance and actionable
                      drills.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950/40 border-white/10 border-1 border-solid hidden p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4.8px]">
                      Coach Mode
                    </div>
                    <div className="font-semibold text-lg leading-7 mt-2">
                      Replay + Live Advice
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Built for competitive players
                    </div>
                  </div>
                </div>
                <div className="grid mt-6 gap-4">
                  <div className="rounded-2xl bg-zinc-950/40 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
                      <Clock3 className="size-4 text-[#f54900]" />
                      Timestamp aware
                    </div>
                    <div className="font-semibold text-lg leading-7 mt-3">
                      01:08, 02:14, 04:41
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Coach references critical moments automatically.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950/40 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
                      <Target className="size-4 text-[#f54900]" />
                      Aim feedback
                    </div>
                    <div className="font-semibold text-lg leading-7 mt-3">
                      Crosshair, recoil, tracking
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Clear corrections for mechanical improvement.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950/40 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
                      <Bot className="size-4 text-[#f54900]" />
                      Personalized plan
                    </div>
                    <div className="font-semibold text-lg leading-7 mt-3">
                      Drills after every answer
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Turn insights into repeatable practice.
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center gap-4">
                  <div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Ask the coach
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-1">
                      What do you want to improve?
                    </div>
                  </div>
                  <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid flex px-3 py-2 items-center gap-2">
                    <WandSparkles className="size-4 text-[#f54900]" />
                    AI response ready
                  </div>
                </div>
                <div className="flex mt-5 flex-wrap gap-3">
                  <button className="rounded-full bg-[#f54900]/10 text-[#f54900] text-sm leading-5 border-[#f54900]/30 border-1 border-solid px-4 py-2">
                    Why did I lose that duel?
                  </button>
                  <button className="rounded-full bg-zinc-950 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid px-4 py-2">
                    How do I improve recoil?
                  </button>
                  <button className="rounded-full bg-zinc-950 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid px-4 py-2">
                    When should I peek?
                  </button>
                  <button className="rounded-full bg-zinc-950 text-[#9f9fa9] text-sm leading-5 border-white/10 border-1 border-solid px-4 py-2">
                    Review my utility timing
                  </button>
                </div>
                <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid mt-5 p-4">
                  <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
                    <MessageSquare className="size-4 text-[#f54900]" />
                    Ask a question about your gameplay
                  </div>
                  <div className="flex mt-3 items-end gap-3">
                    <textarea
                      className="min-h-[120px] resize-none outline-none rounded-2xl bg-zinc-900 text-sm leading-5 border-white/15 border-1 border-solid px-4 py-3 flex-1"
                      defaultValue=""
                      placeholder="Example: Why was my crosshair placement bad at 02:14?"
                    />
                    <button className="inline-flex font-medium shadow-[0_10px_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900] text-orange-50 text-sm leading-5 px-5 py-3 items-center gap-2">
                      <Send className="size-4" />
                      Ask Coach
                    </button>
                  </div>
                </div>
              </div>
              <div className="grid gap-4">
                <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Coach response
                      </div>
                      <div className="font-semibold text-xl leading-7 mt-1">
                        Replay-aware answer
                      </div>
                    </div>
                    <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/20 border-1 border-solid px-3 py-1">
                      Live
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 text-[#9f9fa9] text-sm leading-7 border-white/10 border-1 border-solid mt-4 p-4">
                    <span className="text-neutral-50">
                      At 02:14, your crosshair stayed low while clearing the
                      angle.
                    </span>
                    Raise pre-aim earlier, hold head level before the swing, and
                    commit 120-180ms sooner after the shoulder check. In your
                    next 10 reps, focus on one clean pre-aim path and reset
                    after every miss.
                  </div>
                  <div className="flex mt-4 flex-wrap gap-2">
                    <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                      Crosshair placement
                    </div>
                    <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                      Pre-aim timing
                    </div>
                    <div className="rounded-full bg-zinc-950 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                      Angle discipline
                    </div>
                  </div>
                </div>
                <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Coach settings
                      </div>
                      <div className="font-semibold text-xl leading-7 mt-1">
                        How should the coach respond?
                      </div>
                    </div>
                    <Settings2 className="size-5 text-[#f54900]" />
                  </div>
                  <div className="space-y-3 mt-4">
                    <button>
                      <span>Replay Review</span>
                      <Check className="size-4" />
                    </button>
                    <button>
                      <span>Live Tips</span>
                      <Check className="size-4" />
                    </button>
                    <button>
                      <span>Drill Plan</span>
                      <Check className="size-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Recent prompts
                    </div>
                    <div className="font-semibold text-xl leading-7 mt-1">
                      What players ask most
                    </div>
                  </div>
                  <History className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-3 mt-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-sm leading-5 flex justify-between items-center">
                      <span className="text-neutral-50">
                        Why did I lose the opening duel?
                      </span>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Coach checked peek timing and crosshair height.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-sm leading-5 flex justify-between items-center">
                      <span className="text-neutral-50">
                        How do I stop overflicking?
                      </span>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Suggested slower target acquisition drills.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-sm leading-5 flex justify-between items-center">
                      <span className="text-neutral-50">
                        Was my utility late?
                      </span>
                      <ChevronRight className="size-4 text-[#9f9fa9]" />
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                      Coach compared grenade timing to enemy movement.
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Coach focus
                    </div>
                    <div className="font-semibold text-xl leading-7 mt-1">
                      Priority improvements
                    </div>
                  </div>
                  <Flame className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-4 mt-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="font-medium text-sm leading-5">
                        Crosshair discipline
                      </div>
                      <div className="text-[#f54900] text-sm leading-5">
                        High
                      </div>
                    </div>
                    <div className="rounded-full bg-zinc-800 mt-2 h-2">
                      <div className="w-[82%] rounded-full bg-[#f54900] h-2" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="font-medium text-sm leading-5">
                        Recoil control
                      </div>
                      <div className="text-[#f54900] text-sm leading-5">
                        Medium
                      </div>
                    </div>
                    <div className="rounded-full bg-zinc-800 mt-2 h-2">
                      <div className="w-[64%] rounded-full bg-[#f54900] h-2" />
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="flex justify-between items-center">
                      <div className="font-medium text-sm leading-5">
                        Decision speed
                      </div>
                      <div className="text-[#f54900] text-sm leading-5">
                        Medium
                      </div>
                    </div>
                    <div className="rounded-full bg-zinc-800 mt-2 h-2">
                      <div className="w-[58%] rounded-full bg-[#f54900] h-2" />
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Saved insights
                    </div>
                    <div className="font-semibold text-xl leading-7 mt-1">
                      Coach memory
                    </div>
                  </div>
                  <BookMarked className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-3 mt-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex px-4 py-3 justify-between items-center">
                    <div>
                      <div className="font-medium text-sm leading-5">
                        Pre-aim earlier on corner swings
                      </div>
                      <div className="text-[#9f9fa9] text-xs leading-4">
                        Saved from 02:14 review
                      </div>
                    </div>
                    <Star />
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex px-4 py-3 justify-between items-center">
                    <div>
                      <div className="font-medium text-sm leading-5">
                        Reset recoil after first burst
                      </div>
                      <div className="text-[#9f9fa9] text-xs leading-4">
                        Saved from 04:41 review
                      </div>
                    </div>
                    <Star />
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex px-4 py-3 justify-between items-center">
                    <div>
                      <div className="font-medium text-sm leading-5">
                        Commit sooner after shoulder check
                      </div>
                      <div className="text-[#9f9fa9] text-xs leading-4">
                        Saved from 01:08 review
                      </div>
                    </div>
                    <Star />
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
