import { useEffect } from "react";
import {
  BarChart3,
  Bell,
  Check,
  ChevronDown,
  Cpu,
  Crosshair,
  History,
  LayoutDashboard,
  Map,
  MessageCircle,
  MessageSquare,
  Play,
  Sparkles,
  Star,
  Trophy,
  Upload,
  User,
  Zap,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ChartContainer, ChartTooltip } from "@/components/ui/chart";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Area,
  AreaChart as RechartsAreaChart,
  PolarAngleAxis,
  PolarGrid,
  Radar as RechartsRadar,
  RadarChart,
  XAxis,
} from "recharts";
import { FallbackComponent } from "./CustomComponents";

export default function App() {
  return (
    <div>
      <div className="font-sans bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <nav className="sticky z-50 backdrop-blur-xl bg-zinc-950/80 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex top-0 px-8 py-4 justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="size-9 shadow-[0_0_20px_oklch(0.646_0.222_41.116/0.5)] rounded-lg bg-[#f54900] flex justify-center items-center">
              <Crosshair className="size-5 text-orange-50" />
            </div>
            <span className="font-bold text-xl leading-7 tracking-tight">
              Aim<span className="text-[#f54900]">Forge</span>
            </span>
          </div>
          <div className="flex items-center gap-1">
            <button className="font-medium text-neutral-50 text-sm leading-5 border-[#f54900] border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <LayoutDashboard className="size-4" />
              Dashboard
            </button>
            <button className="border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <BarChart3 className="size-4" />
              Analysis
            </button>
            <button className="border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <History className="size-4" />
              History
            </button>
            <button className="border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <Zap className="size-4" />
              Training
            </button>
            <button className="border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <MessageCircle className="size-4" />
              AI Coach
            </button>
            <button className="border-transparent font-medium text-[#9f9fa9] text-sm leading-5 border-black/1 border-t-0 border-r-0 border-b-2 border-l-0 border-solid flex px-4 py-2 items-center gap-2">
              <User className="size-4" />
              Profile
            </button>
          </div>
          <div className="flex items-center gap-3">
            <Button
              className="relative rounded-full"
              size="icon"
              variant="ghost"
            >
              <Bell className="size-5" />
              <span className="size-2 rounded-full bg-[#f54900] absolute right-1 top-1" />
            </Button>
            <Button className="rounded-lg bg-[#f54900] text-orange-50">
              Get Started
            </Button>
          </div>
        </nav>
        <section className="relative px-8 pt-16 pb-12 overflow-hidden">
          <div className="-z-10 absolute inset-0">
            <img
              alt="Tactical terrain"
              className="object-cover opacity-25 w-full h-full"
              data-authorname="Keghan Crossland"
              data-authorurl="https://unsplash.com/@keghancphoto"
              data-blurhash="LyKBU6xrVsf7T#M{r=kC%Nt7xajY"
              data-photoid="tKyt-GZowHQ"
              src="https://images.unsplash.com/photo-1446488614340-2d1a68d662f9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3ODc2NDd8MHwxfHNlYXJjaHwxfHxnYW1pbmclMjBiYXR0bGVmaWVsZCUyMG1vdW50YWluJTIwdGFjdGljYWwlMjBsYW5kc2NhcGV8ZW58MXwwfHx8MTc4NTg1NTIwOHww&ixlib=rb-4.1.0&q=80&w=1400"
            />
          </div>
          <div className="-z-10 bg-[radial-gradient(ellipse_at_top,oklch(0.646_0.222_41.116/0.18),transparent_60%)] absolute inset-0" />
          <div className="-z-10 bg-gradient-to-b from-background/40 via-background/70 to-background absolute inset-0" />
          <div className="left-1/4 -z-10 size-2 animate-pulse shadow-[0_0_12px_oklch(0.646_0.222_41.116)] rounded-full bg-[#f54900] absolute top-24" />
          <div className="right-1/3 -z-10 size-1.5 animate-pulse shadow-[0_0_10px_oklch(0.646_0.222_41.116)] rounded-full bg-[#f54900]/80 absolute top-40" />
          <div className="left-1/3 -z-10 size-1 animate-pulse shadow-[0_0_8px_oklch(0.646_0.222_41.116)] rounded-full bg-[#f54900]/60 absolute bottom-24" />
          <div className="max-w-3xl text-center flex mx-auto flex-col items-center gap-6">
            <Badge className="rounded-full bg-zinc-800 text-neutral-50 border-white/10 border-1 border-solid px-4 py-1.5 gap-2">
              <Sparkles className="size-3.5 text-[#f54900]" />
              AI-Powered BGMI Coaching
            </Badge>
            <h1 className="leading-tight font-bold text-5xl leading-12 tracking-tight">
              Level Up Every BGMI Match with
              <span className="text-[#f54900]">AI</span>
            </h1>
            <p className="max-w-xl text-[#9f9fa9] text-lg leading-7">
              Upload your gameplay and receive professional AI coaching,
              strengths, mistakes, and personalized improvement plans.
            </p>
            <div className="flex mt-2 items-center gap-4">
              <Button
                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"
                size="lg"
              >
                <Upload className="size-5" />
                Upload Gameplay
              </Button>
              <Button
                className="backdrop-blur rounded-xl bg-zinc-900/50 border-white/10 border-0 border-solid gap-2"
                size="lg"
                variant="outline"
              >
                <Play className="size-5" />
                Watch Demo
              </Button>
            </div>
          </div>
          <div className="relative max-w-5xl mx-auto mt-14">
            <div className="bg-gradient-to-r from-primary/40 via-primary/10 to-primary/40 blur-lg rounded-3xl absolute -inset-1" />
            <div className="relative shadow-2xl rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid overflow-hidden">
              <div className="bg-zinc-800/40 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex px-5 py-3 justify-between items-center">
                <div className="flex items-center gap-2">
                  <span className="size-3 rounded-full bg-[#ff6467]/70" />
                  <span className="size-3 rounded-full bg-[#f54900]/70" />
                  <span className="size-3 rounded-full bg-[#00bc7d]/70" />
                </div>
                <span className="font-mono text-[#9f9fa9] text-xs leading-4">
                  aimforge.gg/analysis
                </span>
                <span className="font-medium text-[#f54900] text-xs leading-4">
                  Live Analysis
                </span>
              </div>
              <div className="relative aspect-[16/8]">
                <img
                  alt="Gameplay analysis"
                  className="object-cover w-full h-full"
                  data-authorname="Audrey Shattuck"
                  data-authorurl="https://unsplash.com/@aud_kat"
                  data-blurhash="LED8979EY50x%f4:^jIV6^EN=xnQ"
                  data-photoid="DnUCYI1Wbw4"
                  src="https://images.unsplash.com/photo-1614465014824-74f885b50c83?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3ODc2NDd8MHwxfHNlYXJjaHwxfHxlc3BvcnRzJTIwZ2FtaW5nJTIwYmF0dGxlJTIwcm95YWxlJTIwZGFyayUyMG5lb258ZW58MXwwfHx8MTc4NTg1NTIwM3ww&ixlib=rb-4.1.0&q=80&w=1200"
                />
                <div className="bg-gradient-to-t from-background via-transparent to-transparent absolute inset-0" />
                <div className="top-1/3 left-1/4 size-16 shadow-[0_0_20px_oklch(0.646_0.222_41.116/0.6)] rounded-md border-[#f54900] border-2 border-solid absolute">
                  <span className="font-bold rounded-sm bg-zinc-950/80 text-[#f54900] text-[10px] absolute left-0 -top-6 px-1.5 py-0.5">
                    ENEMY 82%
                  </span>
                </div>
                <div className="top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 absolute">
                  <Crosshair className="size-8 drop-shadow-[0_0_8px_oklch(0.646_0.222_41.116)] text-[#f54900]" />
                </div>
                <div className="flex absolute inset-x-4 bottom-4 items-center gap-3">
                  <Play className="size-4 text-neutral-50" />
                  <div className="rounded-full bg-zinc-800 flex-1 h-1.5 overflow-hidden">
                    <div className="w-2/5 rounded-full bg-[#f54900] h-full" />
                  </div>
                  <span className="font-mono text-[#9f9fa9] text-xs leading-4">
                    02:14 / 05:30
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="border-y bg-zinc-900/40 border-white/10 border-0 border-solid p-8">
          <div className="max-w-5xl flex mx-auto justify-between items-center">
            <div className="flex flex-col items-center gap-1">
              <span className="font-bold text-[#f54900] text-3xl leading-9">
                2.4M+
              </span>
              <span className="text-[#9f9fa9] text-xs leading-4">
                Matches Analyzed
              </span>
            </div>
            <div className="bg-white/10 w-px h-10" />
            <div className="flex flex-col items-center gap-1">
              <span className="font-bold text-3xl leading-9">8.7</span>
              <span className="text-[#9f9fa9] text-xs leading-4">
                Average Rating
              </span>
            </div>
            <div className="bg-white/10 w-px h-10" />
            <div className="flex flex-col items-center gap-1">
              <span className="font-bold text-3xl leading-9">+34%</span>
              <span className="text-[#9f9fa9] text-xs leading-4">
                Accuracy Boost
              </span>
            </div>
            <div className="bg-white/10 w-px h-10" />
            <div className="flex flex-col items-center gap-1">
              <span className="font-bold text-[#f54900] text-3xl leading-9">
                +1.9
              </span>
              <span className="text-[#9f9fa9] text-xs leading-4">
                K/D Improvement
              </span>
            </div>
            <div className="bg-white/10 w-px h-10" />
            <div className="flex flex-col items-center gap-1">
              <span className="font-bold text-3xl leading-9">890K</span>
              <span className="text-[#9f9fa9] text-xs leading-4">
                Coaching Sessions
              </span>
            </div>
          </div>
        </section>
        <section className="px-8 py-16">
          <div className="text-center flex mb-10 flex-col items-center gap-3">
            <Badge
              className="rounded-full text-[#9f9fa9] border-white/10 border-0 border-solid"
              variant="outline"
            >
              How It Works
            </Badge>
            <h2 className="font-bold text-3xl leading-9 tracking-tight">
              From Replay to Rank-Up in 3 Steps
            </h2>
          </div>
          <div className="grid grid-cols-3 max-w-5xl mx-auto gap-6">
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardHeader className="p-0 gap-2">
                <div className="size-12 rounded-xl bg-zinc-800 flex justify-center items-center">
                  <Upload className="size-6 text-[#f54900]" />
                </div>
                <span className="font-mono text-[#f54900] text-xs leading-4">
                  STEP 01
                </span>
                <CardTitle className="text-lg leading-7">
                  Upload Gameplay
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Drop your MP4 replay, pick your map, match type, and
                  perspective — TPP or FPP.
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardHeader className="p-0 gap-2">
                <div className="size-12 rounded-xl bg-zinc-800 flex justify-center items-center">
                  <Cpu className="size-6 text-[#f54900]" />
                </div>
                <span className="font-mono text-[#f54900] text-xs leading-4">
                  STEP 02
                </span>
                <CardTitle className="text-lg leading-7">
                  AI Processing
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Our models track crosshair, recoil, movement, positioning and
                  audio events frame by frame.
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardHeader className="p-0 gap-2">
                <div className="size-12 rounded-xl bg-zinc-800 flex justify-center items-center">
                  <Trophy className="size-6 text-[#f54900]" />
                </div>
                <span className="font-mono text-[#f54900] text-xs leading-4">
                  STEP 03
                </span>
                <CardTitle className="text-lg leading-7">
                  Get Your Report
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Receive strengths, mistakes, timestamped feedback and a
                  personalized training plan.
                </p>
              </CardContent>
            </Card>
          </div>
        </section>
        <section className="border-y bg-zinc-900/40 border-white/10 border-0 border-solid px-8 py-16">
          <div className="text-center flex mb-10 flex-col items-center gap-3">
            <Badge
              className="rounded-full text-[#9f9fa9] border-white/10 border-0 border-solid"
              variant="outline"
            >
              Features
            </Badge>
            <h2 className="font-bold text-3xl leading-9 tracking-tight">
              Built for Competitive BGMI Athletes
            </h2>
          </div>
          <div className="grid grid-cols-4 max-w-5xl mx-auto gap-6">
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-3">
              <CardHeader className="p-0 gap-2">
                <Crosshair className="size-6 text-[#f54900]" />
                <CardTitle className="text-base leading-6">{`Aim & Recoil Analysis`}</CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Frame-level crosshair tracking and spray-transfer scoring.
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-3">
              <CardHeader className="p-0 gap-2">
                <Map className="size-6 text-[#f54900]" />
                <CardTitle className="text-base leading-6">
                  Positioning Heatmaps
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Movement, deaths and high-risk zones mapped across Erangel.
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-3">
              <CardHeader className="p-0 gap-2">
                <MessageCircle className="size-6 text-[#f54900]" />
                <CardTitle className="text-base leading-6">
                  AI Coach Chat
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Ask why you lost a fight — it seeks the exact timestamp.
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-3">
              <CardHeader className="p-0 gap-2">
                <Zap className="size-6 text-[#f54900]" />
                <CardTitle className="text-base leading-6">
                  Training Plans
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0 gap-2">
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Daily drills, XP, skill levels and weekly progress tracking.
                </p>
              </CardContent>
            </Card>
          </div>
          <div className="grid grid-cols-3 max-w-5xl mx-auto mt-6 gap-6">
            <Card className="col-span-2 rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-4">
              <CardHeader className="p-0 gap-1">
                <CardTitle className="text-lg leading-7">
                  Radar Skill Analysis
                </CardTitle>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Eight-axis breakdown of your competitive profile.
                </p>
              </CardHeader>
              <CardContent className="p-0">
                <ChartContainer
                  className="w-full h-60"
                  config={{
                    score: {
                      color: "oklch(0.646 0.222 41.116)",
                      label: "Skill",
                    },
                  }}
                >
                  <RadarChart
                    data={[
                      { score: 88, skill: "Aim" },
                      { score: 76, skill: "Movement" },
                      { score: 62, skill: "Positioning" },
                      { score: 71, skill: "Game Sense" },
                      { score: 91, skill: "Recoil" },
                      { score: 84, skill: "Crosshair" },
                      { score: 67, skill: "Decisions" },
                      { score: 58, skill: "Utility" },
                    ]}
                  >
                    <PolarGrid stroke="oklch(1 0 0 / 10%)" />
                    <PolarAngleAxis
                      dataKey="skill"
                      tick={{
                        fill: "oklch(0.705 0.015 286.067)",
                        fontSize: 11,
                      }}
                    />
                    <RechartsRadar
                      dataKey="score"
                      fill="oklch(0.646 0.222 41.116)"
                      fillOpacity={0.35}
                      stroke="oklch(0.646 0.222 41.116)"
                    />
                    <ChartTooltip />
                  </RadarChart>
                </ChartContainer>
              </CardContent>
            </Card>
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-4">
              <CardHeader className="p-0 gap-1">
                <CardTitle className="text-lg leading-7">
                  Weekly Progress
                </CardTitle>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  Your rating trend.
                </p>
              </CardHeader>
              <CardContent className="p-0">
                <ChartContainer
                  className="w-full h-60"
                  config={{
                    rating: {
                      color: "oklch(0.646 0.222 41.116)",
                      label: "Rating",
                    },
                  }}
                >
                  <RechartsAreaChart
                    data={[
                      { day: "Mon", rating: 6.2 },
                      { day: "Tue", rating: 6.9 },
                      { day: "Wed", rating: 7.1 },
                      { day: "Thu", rating: 7.8 },
                      { day: "Fri", rating: 8.1 },
                      { day: "Sat", rating: 8.7 },
                    ]}
                  >
                    <defs>
                      <linearGradient id="gradR" x1="0" x2="0" y1="0" y2="1">
                        <stop
                          offset="0%"
                          stopColor="oklch(0.646 0.222 41.116)"
                          stopOpacity={0.5}
                        />
                        <stop
                          offset="100%"
                          stopColor="oklch(0.646 0.222 41.116)"
                          stopOpacity={0}
                        />
                      </linearGradient>
                    </defs>
                    <XAxis
                      axisLine={false}
                      dataKey="day"
                      tick={{
                        fill: "oklch(0.705 0.015 286.067)",
                        fontSize: 11,
                      }}
                      tickLine={false}
                    />
                    <Area
                      dataKey="rating"
                      fill="url(#gradR)"
                      stroke="oklch(0.646 0.222 41.116)"
                      strokeWidth={2}
                    />
                    <ChartTooltip />
                  </RechartsAreaChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
        </section>
        <section className="px-8 py-16">
          <div className="text-center flex mb-10 flex-col items-center gap-3">
            <Badge
              className="rounded-full text-[#9f9fa9] border-white/10 border-0 border-solid"
              variant="outline"
            >
              Testimonials
            </Badge>
            <h2 className="font-bold text-3xl leading-9 tracking-tight">
              Trusted by Top Players
            </h2>
          </div>
          <div className="grid grid-cols-3 max-w-5xl mx-auto gap-6">
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardContent className="p-0 gap-4">
                <div className="text-[#f54900] flex gap-1">
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                </div>
                <p className="text-neutral-50 text-sm leading-5">
                  "AimForge caught positioning mistakes I never noticed. Pushed
                  from Diamond to Conqueror in a season."
                </p>
              </CardContent>
              <CardFooter className="p-0 gap-3">
                <div className="size-10 rounded-full overflow-hidden">
                  <img
                    alt="Player"
                    className="object-cover w-full h-full"
                    data-authorname="Alef Morais"
                    data-authorurl="https://unsplash.com/@aleff_jpg"
                    data-blurhash="LgKJ0*?u~B%1~BtRxtafI;IpaKNG"
                    data-photoid="mTMlC4BgHa8"
                    src="https://images.unsplash.com/photo-1759701547687-45af72f44e7e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3ODc2NDd8MHwxfHNlYXJjaHwxfHxlc3BvcnRzJTIwcGxheWVyJTIwcG9ydHJhaXQlMjBoZWFkc2V0fGVufDF8Mnx8fDE3ODU4NTUyMDN8MA&ixlib=rb-4.1.0&q=80&w=100"
                  />
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-sm leading-5">
                    Rohan "Sniper" M.
                  </span>
                  <span className="text-[#9f9fa9] text-xs leading-4">
                    Conqueror · TPP
                  </span>
                </div>
              </CardFooter>
            </Card>
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardContent className="p-0 gap-4">
                <div className="text-[#f54900] flex gap-1">
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                </div>
                <p className="text-neutral-50 text-sm leading-5">
                  "The timestamp feedback is unreal. It's like having a pro
                  coach reviewing every single fight."
                </p>
              </CardContent>
              <CardFooter className="p-0 gap-3">
                <div className="size-10 rounded-full overflow-hidden">
                  <img
                    alt="Player"
                    className="object-cover w-full h-full"
                    data-authorname="Foto Bakirkoy"
                    data-authorurl="https://unsplash.com/@fotobakirkoy"
                    data-blurhash="L43SR~r=MHOsx_n%R4S#VrbHo$jZ"
                    data-photoid="RS56YoMaotk"
                    src="https://images.unsplash.com/photo-1645106281719-7b7c50266a04?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3ODc2NDd8MHwxfHNlYXJjaHwxfHx5b3VuZyUyMG1hbiUyMGdhbWVyJTIwZmFjZSUyMHBvcnRyYWl0fGVufDF8Mnx8fDE3ODU4NTUyMDh8MA&ixlib=rb-4.1.0&q=80&w=100"
                  />
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-sm leading-5">
                    Arjun "Blaze" K.
                  </span>
                  <span className="text-[#9f9fa9] text-xs leading-4">
                    Ace · FPP
                  </span>
                </div>
              </CardFooter>
            </Card>
            <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
              <CardContent className="p-0 gap-4">
                <div className="text-[#f54900] flex gap-1">
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                  <Star className="size-4 fill-primary" />
                </div>
                <p className="text-neutral-50 text-sm leading-5">
                  "My recoil control jumped instantly with the AI drills. The
                  training plan actually keeps me consistent."
                </p>
              </CardContent>
              <CardFooter className="p-0 gap-3">
                <div className="size-10 rounded-full overflow-hidden">
                  <img
                    alt="Player"
                    className="object-cover w-full h-full"
                    data-authorname="Sabeer Darr"
                    data-authorurl="https://unsplash.com/@sabeerdarr"
                    data-blurhash="L25Xok~Va0Dj9GD*R+oy00IUx]-:"
                    data-photoid="3NXtjO5khXY"
                    src="https://images.unsplash.com/photo-1675410202405-5ef270c857d3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3ODc2NDd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBnYW1lciUyMHNldHVwJTIwZGFya3xlbnwxfDF8fHwxNzg1ODU1MjAzfDA&ixlib=rb-4.1.0&q=80&w=100"
                  />
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-sm leading-5">
                    Priya "Vortex" S.
                  </span>
                  <span className="text-[#9f9fa9] text-xs leading-4">
                    Crown · TPP
                  </span>
                </div>
              </CardFooter>
            </Card>
          </div>
        </section>
        <section className="border-y bg-zinc-900/40 border-white/10 border-0 border-solid px-8 py-16">
          <div className="text-center flex mb-10 flex-col items-center gap-4">
            <Badge
              className="rounded-full text-[#9f9fa9] border-white/10 border-0 border-solid"
              variant="outline"
            >
              Pricing
            </Badge>
            <h2 className="font-bold text-3xl leading-9 tracking-tight">
              Choose Your Rank Path
            </h2>
            <Tabs className="w-fit" defaultValue="annual">
              <TabsList className="rounded-full bg-zinc-800">
                <TabsTrigger className="rounded-full" value="monthly">
                  Monthly
                </TabsTrigger>
                <TabsTrigger className="rounded-full" value="annual">
                  Annual · Save 20%
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
          <div className="grid grid-cols-3 max-w-5xl mx-auto gap-6">
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-6">
              <CardHeader className="p-0 gap-2">
                <CardTitle className="text-[#9f9fa9] text-base leading-6">
                  Rookie
                </CardTitle>
                <div className="flex items-end gap-1">
                  <span className="font-bold text-4xl leading-10">Free</span>
                </div>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  For casual players getting started.
                </p>
              </CardHeader>
              <CardContent className="p-0 gap-3">
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />3 analyses / month
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Basic AI feedback
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Match statistics
                </div>
              </CardContent>
              <CardFooter className="p-0">
                <Button
                  className="rounded-xl border-white/10 border-0 border-solid w-full"
                  variant="outline"
                >
                  Start Free
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative shadow-[0_0_40px_oklch(0.646_0.222_41.116/0.25)] rounded-2xl bg-zinc-950 border-[#f54900] border-0 border-solid p-6 gap-6">
              <Badge className="left-1/2 -translate-x-1/2 rounded-full bg-[#f54900] text-orange-50 absolute -top-3">
                Most Popular
              </Badge>
              <CardHeader className="p-0 gap-2">
                <CardTitle className="text-[#f54900] text-base leading-6">
                  Pro Athlete
                </CardTitle>
                <div className="flex items-end gap-1">
                  <span className="font-bold text-4xl leading-10">$15</span>
                  <span className="text-[#9f9fa9] mb-1">/mo</span>
                </div>
                <div className="hidden items-end gap-1">
                  <span className="font-bold text-4xl leading-10">$19</span>
                  <span className="text-[#9f9fa9] mb-1">/mo</span>
                </div>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  For competitive climbers.
                </p>
              </CardHeader>
              <CardContent className="p-0 gap-3">
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Unlimited analyses
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  {`Interactive overlays & timeline`}
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  AI Coach chat
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Personalized training plans
                </div>
              </CardContent>
              <CardFooter className="p-0">
                <Button className="rounded-xl bg-[#f54900] text-orange-50 w-full">
                  Go Pro
                </Button>
              </CardFooter>
            </Card>
            <Card className="rounded-2xl bg-zinc-950 border-white/10 border-0 border-solid p-6 gap-6">
              <CardHeader className="p-0 gap-2">
                <CardTitle className="text-[#9f9fa9] text-base leading-6">
                  Team
                </CardTitle>
                <div className="flex items-end gap-1">
                  <span className="font-bold text-4xl leading-10">$49</span>
                  <span className="text-[#9f9fa9] mb-1">/mo</span>
                </div>
                <div className="hidden items-end gap-1">
                  <span className="font-bold text-4xl leading-10">$59</span>
                  <span className="text-[#9f9fa9] mb-1">/mo</span>
                </div>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  For squads and orgs.
                </p>
              </CardHeader>
              <CardContent className="p-0 gap-3">
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Everything in Pro
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Up to 5 players
                </div>
                <div className="text-sm leading-5 flex items-center gap-2">
                  <Check className="size-4 text-[#f54900]" />
                  Team analytics dashboard
                </div>
              </CardContent>
              <CardFooter className="p-0">
                <Button
                  className="rounded-xl border-white/10 border-0 border-solid w-full"
                  variant="outline"
                >
                  Contact Sales
                </Button>
              </CardFooter>
            </Card>
          </div>
        </section>
        <section className="px-8 py-16">
          <div className="max-w-3xl mx-auto">
            <div className="text-center flex mb-8 flex-col items-center gap-3">
              <Badge
                className="rounded-full text-[#9f9fa9] border-white/10 border-0 border-solid"
                variant="outline"
              >
                FAQ
              </Badge>
              <h2 className="font-bold text-3xl leading-9 tracking-tight">
                Frequently Asked Questions
              </h2>
            </div>
            <div className="flex flex-col gap-3">
              <Card className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid p-5 gap-2">
                <button className="text-left flex justify-between items-center">
                  <span className="font-medium">
                    What replay formats are supported?
                  </span>
                  <ChevronDown />
                </button>
                <p className="text-[#9f9fa9] text-sm leading-5">
                  We support MP4 up to 2GB. Just export your BGMI replay and
                  drop it into the upload zone.
                </p>
              </Card>
              <Card className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid p-5 gap-2">
                <button className="text-left flex justify-between items-center">
                  <span className="font-medium">
                    How accurate is the AI analysis?
                  </span>
                  <ChevronDown />
                </button>
                <p className="text-[#9f9fa9] text-sm leading-5 hidden">
                  Our models are trained on millions of pro matches and report
                  per-event confidence scores you can verify.
                </p>
              </Card>
              <Card className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid p-5 gap-2">
                <button className="text-left flex justify-between items-center">
                  <span className="font-medium">
                    Does it work for both TPP and FPP?
                  </span>
                  <ChevronDown />
                </button>
                <p className="text-[#9f9fa9] text-sm leading-5 hidden">
                  Yes — pick your perspective at upload and the analysis adapts
                  crosshair and positioning logic accordingly.
                </p>
              </Card>
            </div>
          </div>
        </section>
        <section className="px-8 pb-16">
          <div className="relative max-w-5xl rounded-3xl bg-zinc-900 border-[#f54900]/40 border-1 border-solid mx-auto p-12 overflow-hidden">
            <div className="bg-[radial-gradient(ellipse_at_center,oklch(0.646_0.222_41.116/0.2),transparent_70%)] absolute inset-0" />
            <div className="relative text-center flex flex-col items-center gap-5">
              <h2 className="font-bold text-3xl leading-9 tracking-tight">
                Ready to Forge Your Aim?
              </h2>
              <p className="max-w-md text-[#9f9fa9]">
                Upload your first replay and see exactly where your next rank is
                hiding.
              </p>
              <Button
                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"
                size="lg"
              >
                <Upload className="size-5" />
                Upload Gameplay
              </Button>
            </div>
          </div>
        </section>
        <footer className="bg-zinc-900/40 border-white/10 border-t-1 border-r-0 border-b-0 border-l-0 border-solid px-8 py-10">
          <div className="max-w-5xl flex mx-auto justify-between items-start">
            <div className="max-w-xs flex flex-col gap-3">
              <div className="flex items-center gap-2">
                <div className="size-8 rounded-lg bg-[#f54900] flex justify-center items-center">
                  <Crosshair className="size-4 text-orange-50" />
                </div>
                <span className="font-bold text-lg leading-7">
                  Aim<span className="text-[#f54900]">Forge</span>
                </span>
              </div>
              <p className="text-[#9f9fa9] text-sm leading-5">
                AI-powered BGMI gameplay coaching for players who refuse to
                plateau.
              </p>
              <div className="flex mt-1 items-center gap-3">
                <FallbackComponent className="size-5 text-[#9f9fa9]" />
                <FallbackComponent className="size-5 text-[#9f9fa9]" />
                <FallbackComponent className="size-5 text-[#9f9fa9]" />
                <MessageSquare className="size-5 text-[#9f9fa9]" />
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-semibold text-sm leading-5 mb-1">
                Product
              </span>
              <span className="text-[#9f9fa9] text-sm leading-5">Features</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Analysis</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Training</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Pricing</span>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-semibold text-sm leading-5 mb-1">
                Company
              </span>
              <span className="text-[#9f9fa9] text-sm leading-5">About</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Careers</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Blog</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Contact</span>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-semibold text-sm leading-5 mb-1">
                Legal
              </span>
              <span className="text-[#9f9fa9] text-sm leading-5">Privacy</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Terms</span>
              <span className="text-[#9f9fa9] text-sm leading-5">Security</span>
            </div>
          </div>
          <div className="max-w-5xl border-white/10 border-t-1 border-r-0 border-b-0 border-l-0 border-solid flex mx-auto mt-8 pt-6 justify-between items-center">
            <span className="text-[#9f9fa9] text-xs leading-4">
              © 2025 AimForge. Not affiliated with BGMI or Krafton.
            </span>
            <span className="text-[#9f9fa9] text-xs leading-4">
              Made for competitive players.
            </span>
          </div>
        </footer>
      </div>
    </div>
  );
}
