/* eslint-disable */
// @ts-nocheck
import { useNavigate } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { useAppStore } from "../store/useAppStore";
import { ComingSoonModal } from "@/components/ComingSoonModal";
import {
  Activity,
  Award,
  BarChart3,
  BrainCircuit,
  Crosshair,
  History,
  LayoutDashboard,
  MessageCircle,
  Move3D,
  SlidersHorizontal,
  Target,
  TimerReset,
  User,
  WandSparkles,
  Zap,
} from "lucide-react";

export default function App() {
  const navigate = useNavigate();
  const { analysis } = useAppStore();
  const [modalOpen, setModalOpen] = useState(false);
  const [modalFeature, setModalFeature] = useState("");

  const handleComingSoon = (feature: string) => {
    setModalFeature(feature);
    setModalOpen(true);
  };
  return (
    <div className="w-full flex flex-col gap-8">
      <div className="grid grid-cols-[1.35fr_0.85fr] flex-1 gap-6">
            <div className="flex flex-col gap-6">
              <div className="shadow-[0_0_0_1px_oklch(1_0_0/.02),0_20px_60px_oklch(0_0_0/.35)] rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div className="rounded-full bg-zinc-800 text-[#9f9fa9] text-xs leading-4 flex px-3 py-1 items-center gap-2">
                    <Target className="size-3.5 text-[#f54900]" />
                    <span>Training Session</span>
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5">
                    Warm-up drill synced to live aim metrics
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid mt-5 overflow-hidden">
                  <div className="text-[#9f9fa9] text-xs leading-4 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex px-4 py-3 justify-between items-center">
                    <div className="flex items-center gap-2">
                      <span className="size-2 rounded-full bg-[#ff6467]" />
                      <span className="size-2 rounded-full bg-[#f54900]" />
                      <span className="size-2 rounded-full bg-[#00bc7d]" />
                    </div>
                    <div>Training Replay · Drill 04</div>
                    <div className="text-[#f54900]">Live Coaching</div>
                  </div>
                  <div className="relative h-105 overflow-hidden">
                    <img
                      alt="Training session visual"
                      className="object-cover opacity-70 w-full h-full"
                      data-authorname="Onur Binay"
                      data-authorurl="https://unsplash.com/@onurbinay"
                      data-blurhash="L9Eyb^?b00?b~qRjRjRj%MxuRjRj"
                      data-photoid="Q1p7bh3SHj8"
                      src="https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3OTAzMTh8MHwxfHNlYXJjaHwxfHxjb21wdXRlciUyMGdhbWluZyUyMHNldHVwfGVufDF8fHx8MTc1NDkyMzc3N3ww&ixlib=rb-4.1.0&q=80&w=1200"
                    />
                    <div className="bg-[linear-gradient(180deg,oklch(0.141_0.005_285.823/.15)_0%,oklch(0.141_0.005_285.823/.55)_100%)] absolute inset-0" />
                    <div className="backdrop-blur-sm rounded-2xl bg-zinc-900/90 border-white/10 border-1 border-solid absolute left-5 top-5 px-4 py-3">
                      <div className="uppercase text-[#9f9fa9] text-[11px] tracking-[5.6px]">
                        Current Drill
                      </div>
                      <div className="font-semibold text-lg leading-7 mt-1">
                        Flick Control
                      </div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Track targets across three lanes
                      </div>
                    </div>
                    <div className="text-right rounded-2xl bg-[#f54900]/10 border-[#f54900]/30 border-1 border-solid absolute right-5 top-5 px-4 py-3">
                      <div className="uppercase text-[#9f9fa9] text-[11px] tracking-[5.6px]">
                        Accuracy
                      </div>
                      <div className="font-semibold text-[#f54900] text-3xl leading-9">
                        {analysis?.ratings?.accuracy || "92"}%
                      </div>
                    </div>
                    <div className="backdrop-blur-sm rounded-2xl bg-zinc-900/90 border-white/10 border-1 border-solid absolute inset-x-5 bottom-5 p-4">
                      <div className="text-[#9f9fa9] text-xs leading-4 flex justify-between items-center">
                        <span>Session Progress</span>
                        <span>18:42 / 24:00</span>
                      </div>
                      <div className="rounded-full bg-zinc-800 mt-3 h-2">
                        <div className="w-[78%] shadow-[0_0_18px_oklch(0.646_0.222_41.116/.55)] rounded-full bg-[#f54900] h-2" />
                      </div>
                      <div className="text-[#9f9fa9] text-xs leading-4 flex mt-3 justify-between items-center">
                        <span>Warm-up</span>
                        <span>Tracking</span>
                        <span>Cooldown</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] text-sm leading-5 flex justify-between items-center">
                    <span>Reaction Time</span>
                    <TimerReset className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    {analysis?.ratings?.reactionTime || "184"}ms
                  </div>
                  <div className="text-[#00bc7d] text-sm leading-5 mt-2">
                    -12% from baseline
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] text-sm leading-5 flex justify-between items-center">
                    <span>Accuracy</span>
                    <Crosshair className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    {analysis?.ratings?.accuracy || "92"}%
                  </div>
                  <div className="text-[#00bc7d] text-sm leading-5 mt-2">
                    +8% this week
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] text-sm leading-5 flex justify-between items-center">
                    <span>Consistency</span>
                    <Activity className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    8.7
                  </div>
                  <div className="text-[#00bc7d] text-sm leading-5 mt-2">
                    Stable across drills
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      Training Plan
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Structured progression for the next 30 minutes
                    </div>
                  </div>
                  <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                    Auto-adjusted
                  </div>
                </div>
                <div className="grid mt-5 gap-4">
                  {analysis?.trainingPlan?.drills?.length > 0 ? (
                    analysis.trainingPlan.drills.map((drill: string, idx: number) => (
                      <div key={idx} className="cursor-pointer rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 hover:border-[#f54900] transition-colors">
                        <div className="flex justify-between items-center">
                          <div className="flex items-center gap-3">
                            <div className="size-10 rounded-xl bg-[#f54900]/10 text-[#f54900] flex justify-center items-center">
                              <Target className="size-5" />
                            </div>
                            <div>
                              <div className="font-medium">Drill {idx + 1}</div>
                              <div className="text-[#9f9fa9] text-sm leading-5">
                                {drill}
                              </div>
                            </div>
                          </div>
                          <div className="text-[#f54900] text-sm leading-5">
                            {idx === 0 ? "Ready" : "Queued"}
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-[#9f9fa9] text-sm leading-5 py-4">No specific drills generated yet. Complete a gameplay analysis to get started.</div>
                  )}
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      Coach Panel
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Live guidance during the session
                    </div>
                  </div>
                  <MessageCircle className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-3 mt-5">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4.8px]">
                      Tip 01
                    </div>
                    <div className="text-sm leading-5 mt-2">
                      Lower your sensitivity slightly for the next drill.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4.8px]">
                      Tip 02
                    </div>
                    <div className="text-sm leading-5 mt-2">
                      Pause for a micro-reset after each miss.
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4.8px]">
                      Tip 03
                    </div>
                    <div className="text-sm leading-5 mt-2">
                      Focus on center mass before flicking to the head.
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      Session Controls
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Adjust the training flow
                    </div>
                  </div>
                  <SlidersHorizontal className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-4 mt-5">
                  <div className="cursor-pointer rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 hover:border-white/20 transition-colors">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Aim Assist</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          Subtle correction overlay
                        </div>
                      </div>
                      <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                        On
                      </div>
                    </div>
                  </div>
                  <div className="cursor-pointer rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 hover:border-white/20 transition-colors">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Drill Length</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          Short, focused repetitions
                        </div>
                      </div>
                      <div className="rounded-full bg-zinc-800 text-[#9f9fa9] text-xs leading-4 border-white/10 border-1 border-solid px-3 py-1">
                        30 min
                      </div>
                    </div>
                  </div>
                  <div className="cursor-pointer rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 hover:border-white/20 transition-colors">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium">Auto Review</div>
                        <div className="text-[#9f9fa9] text-sm leading-5">
                          Generate notes after each set
                        </div>
                      </div>
                      <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/30 border-1 border-solid px-3 py-1">
                        Enabled
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg leading-7">
                      Next Milestone
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5">
                      Unlock the advanced recoil module
                    </div>
                  </div>
                  <Award className="size-5 text-[#f54900]" />
                </div>
                <div className="rounded-2xl bg-[#f54900]/10 border-[#f54900]/20 border-1 border-solid mt-5 p-4">
                  <div className="text-[#9f9fa9] text-sm leading-5">Target</div>
                  <div className="font-semibold text-[#f54900] text-2xl leading-8 mt-1">
                    95% accuracy
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-2">
                    Complete two more drills to unlock
                  </div>
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
