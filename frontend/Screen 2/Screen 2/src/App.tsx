import { useEffect } from "react";
import {
  BarChart3,
  History,
  LayoutDashboard,
  MessageCircle,
  Play,
  Sparkles,
  Target,
  User,
  Zap,
} from "lucide-react";

export default function App() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="max-w-[1140px] flex mx-auto px-8 py-6 flex-col gap-8 w-full">
          <div className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-4 justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="size-10 shadow-[0_0_24px_oklch(0.646_0.222_41.116/.35)] rounded-full bg-[#f54900] text-orange-50 flex justify-center items-center">
                <Target className="size-5" />
              </div>
              <div className="flex flex-col">
                <div className="font-semibold text-lg leading-7 tracking-tight">
                  AimForge
                </div>
                <div className="text-[#9f9fa9] text-xs leading-4">
                  AI-powered gameplay analysis
                </div>
              </div>
            </div>
            <div className="text-[#9f9fa9] text-sm leading-5 flex items-center gap-2">
              <div className="rounded-full bg-zinc-900 text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                Desktop Analysis
              </div>
              <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                Live Review
              </div>
            </div>
          </div>
          <div className="text-sm leading-5 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex pb-3 items-center gap-2">
            <div className="rounded-full text-neutral-50 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-3 py-2 items-center gap-2">
              <LayoutDashboard className="size-4" />
              <span>Dashboard</span>
            </div>
            <div className="rounded-full text-neutral-50 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-3 py-2 items-center gap-2">
              <BarChart3 className="size-4" />
              <span>Analysis</span>
            </div>
            <div className="rounded-full text-[#9f9fa9] flex px-3 py-2 items-center gap-2">
              <History className="size-4" />
              <span>History</span>
            </div>
            <div className="rounded-full text-[#9f9fa9] flex px-3 py-2 items-center gap-2">
              <Zap className="size-4" />
              <span>Training</span>
            </div>
            <div className="rounded-full text-[#9f9fa9] flex px-3 py-2 items-center gap-2">
              <MessageCircle className="size-4" />
              <span>AI Coach</span>
            </div>
            <div className="rounded-full text-[#9f9fa9] flex px-3 py-2 items-center gap-2">
              <User className="size-4" />
              <span>Profile</span>
            </div>
          </div>
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
                    <div>Match Replay · Round 12</div>
                    <div className="text-[#f54900]">Live Analysis</div>
                  </div>
                  <div className="relative aspect-[16/9] overflow-hidden">
                    <img
                      alt="Gameplay analysis preview"
                      className="object-cover opacity-70 w-full h-full"
                      src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/city-navigation-map.png"
                    />
                    <div className="bg-[linear-gradient(180deg,oklch(0.141_0.005_285.823/.15),oklch(0.141_0.005_285.823/.55)_70%,oklch(0.141_0.005_285.823/.85))] absolute inset-0" />
                    <div className="backdrop-blur-sm rounded-xl bg-zinc-950/80 text-neutral-50 text-xs leading-4 border-[#f54900]/30 border-1 border-solid absolute left-6 top-6 px-3 py-2">
                      <div className="uppercase text-[#9f9fa9] text-[10px] tracking-[3.84px]">
                        Timestamp
                      </div>
                      <div className="font-semibold text-[#f54900] mt-1">
                        02:14
                      </div>
                    </div>
                    <div className="flex absolute inset-x-6 bottom-6 justify-between items-end gap-4">
                      <div className="max-w-md backdrop-blur-sm rounded-2xl bg-zinc-950/80 border-white/10 border-1 border-solid p-4">
                        <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                          AI Insight
                        </div>
                        <div className="text-neutral-50 text-sm leading-6 mt-2">
                          Crosshair drifted during the peek. Re-center before
                          swing to improve first-shot accuracy.
                        </div>
                      </div>
                      <div className="backdrop-blur-sm text-right rounded-2xl bg-zinc-950/80 border-white/10 border-1 border-solid px-4 py-3">
                        <div className="text-[#9f9fa9] text-xs leading-4">
                          Confidence
                        </div>
                        <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-1">
                          94%
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="border-white/10 border-t-1 border-r-0 border-b-0 border-l-0 border-solid px-4 py-3">
                    <div className="text-[#9f9fa9] text-xs leading-4 flex items-center gap-3">
                      <Play className="size-4 text-[#f54900]" />
                      <div className="rounded-full bg-zinc-800 flex-1 h-1.5 overflow-hidden">
                        <div className="w-[42%] rounded-full bg-[#f54900] h-full" />
                      </div>
                      <span>02:14 / 06:38</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid gap-4">
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                    Timestamp
                  </div>
                  <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-3">
                    01:08
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                    Missed pre-aim before the corner swing.
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                    Timestamp
                  </div>
                  <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-3">
                    02:14
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                    Great reposition, but delayed trigger discipline.
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[3.84px]">
                    Timestamp
                  </div>
                  <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-3">
                    04:41
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                    Excellent trade timing and clean recoil control.
                  </div>
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-sm leading-5">
                      AI Feedback Feed
                    </div>
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Generated from replay timestamps
                    </div>
                  </div>
                  <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                    Auto-synced
                  </div>
                </div>
                <div className="flex mt-5 flex-col gap-3">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4 flex justify-between items-center">
                      <span>01:08</span>
                      <span className="rounded-full bg-[#ff6467]/15 text-[#ff6467] px-2 py-1">
                        Critical
                      </span>
                    </div>
                    <div className="text-sm leading-6 mt-3">
                      Your crosshair was below head level before the peek. Raise
                      pre-aim earlier to secure the opening duel.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4 flex justify-between items-center">
                      <span>02:14</span>
                      <span className="rounded-full bg-[#f54900]/15 text-[#f54900] px-2 py-1">
                        Opportunity
                      </span>
                    </div>
                    <div className="text-sm leading-6 mt-3">
                      You had the angle advantage, but your shot timing lagged
                      by 180ms. Commit sooner after the shoulder check.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4 flex justify-between items-center">
                      <span>04:41</span>
                      <span className="rounded-full bg-[#00bc7d]/15 text-[#00bc7d] px-2 py-1">
                        Positive
                      </span>
                    </div>
                    <div className="text-sm leading-6 mt-3">
                      Excellent recoil reset after the first burst. This is the
                      control pattern to repeat in close-range fights.
                    </div>
                  </div>
                </div>
              </div>
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
                      Aim Stability
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      8.7
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Reaction Time
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      +34%
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Headshot Rate
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      1.9x
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="text-[#9f9fa9] text-xs leading-4">
                      Coach Notes
                    </div>
                    <div className="font-semibold text-2xl leading-8 mt-2">
                      890K
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
