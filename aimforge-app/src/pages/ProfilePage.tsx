/* eslint-disable */
// @ts-nocheck
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import {
  BarChart3,
  Clock3,
  Gamepad2,
  History,
  LayoutDashboard,
  MessageCircle,
  Pencil,
  Settings2,
  ShieldCheck,
  Target,
  User,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";

import { ComingSoonModal } from "@/components/ComingSoonModal";
import { useState } from "react";
import { useAuthStore } from "../store/useAuthStore";
import { LogOut } from "lucide-react";

export default function App() {
  const navigate = useNavigate();
  const [modalOpen, setModalOpen] = useState(false);
  const [modalFeature, setModalFeature] = useState("");
  const { user, logout } = useAuthStore();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };


  const handleComingSoon = (feature: string) => {
    setModalFeature(feature);
    setModalOpen(true);
  };
  return (
    <div className="w-full flex flex-col gap-8">
          <div className="grid grid-cols-[1.15fr_0.85fr] mt-8 gap-6">
            <div className="flex flex-col gap-6">
              <div className="shadow-[0_20px_60px_rgba(0,0,0,0.25)] rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-start gap-6">
                  <div className="flex items-center gap-5">
                    <div className="size-24 shadow-[0_0_40px_rgba(249,115,22,0.18)] rounded-3xl bg-[#f54900]/10 text-[#f54900] border-[#f54900]/20 border-1 border-solid flex justify-center items-center">
                      <User className="size-11" />
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-3">
                        <h2 className="font-semibold text-3xl leading-9 tracking-tight">
                          {user?.username || user?.email?.split('@')[0] || "AimForge Player"}
                        </h2>
                        <span className="font-medium rounded-full bg-[#f54900]/15 text-[#f54900] text-xs leading-4 px-3 py-1">
                          Verified Player
                        </span>
                      </div>
                      <p className="max-w-xl text-[#9f9fa9] text-sm leading-6">
                        Competitive FPS player focused on aim consistency,
                        decision speed, and replay-driven improvement.
                      </p>
                      <div className="text-[#9f9fa9] text-xs leading-4 flex pt-1 flex-wrap gap-2">
                        <span className="rounded-full bg-zinc-950 border-white/10 border-1 border-solid px-3 py-1">
                          NA Region
                        </span>
                        <span className="rounded-full bg-zinc-950 border-white/10 border-1 border-solid px-3 py-1">{`PC / Mouse & Keyboard`}</span>
                        <span className="rounded-full bg-zinc-950 border-white/10 border-1 border-solid px-3 py-1">
                          Ranked Grinder
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4.8px]">
                      Profile Strength
                    </div>
                    <div className="font-semibold text-[#f54900] text-3xl leading-9 mt-2">
                      92%
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Complete your bio and socials
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] flex justify-between items-center">
                    <span className="text-sm leading-5">Matches Reviewed</span>
                    <History className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    248
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                    Across all sessions
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] flex justify-between items-center">
                    <span className="text-sm leading-5">Aim Stability</span>
                    <Target className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    8.7
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                    Tracked weekly
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-white/10 border-1 border-solid p-5">
                  <div className="text-[#9f9fa9] flex justify-between items-center">
                    <span className="text-sm leading-5">Coach Notes</span>
                    <MessageCircle className="size-4 text-[#f54900]" />
                  </div>
                  <div className="font-semibold text-3xl leading-9 mt-4">
                    890K
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-5 mt-1">
                    Saved insights
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-xl leading-7">
                      Account Details
                    </h3>
                    <p className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Your public and private profile information.
                    </p>
                  </div>
                  <Button className="rounded-full bg-[#f54900] text-orange-50 px-5 hover:bg-[#ff6467]" onClick={() => handleComingSoon("Edit Profile")}>
                    <Pencil className="size-4 mr-2" />
                    Edit Profile
                  </Button>
                </div>
                <div className="grid grid-cols-2 mt-6 gap-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Username
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      @{user?.username || user?.email?.split('@')[0] || "player"}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Email
                    </div>
                    <div className="font-medium text-base leading-6 mt-2 overflow-hidden text-ellipsis">
                      {user?.email || "No email"}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Phone
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      +1 (415) 555-0198
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Location
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      San Francisco, CA
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex flex-col gap-6">
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-xl leading-7">
                      Preferences
                    </h3>
                    <p className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Customize your profile experience.
                    </p>
                  </div>
                  <Settings2 className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-4 mt-5">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center">
                    <div>
                      <div className="font-medium">Email Notifications</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Receive replay and coach updates
                      </div>
                    </div>
                    <Switch checked={true} />
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center">
                    <div>
                      <div className="font-medium">Public Profile</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Show stats to teammates
                      </div>
                    </div>
                    <Switch checked={false} />
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center">
                    <div>
                      <div className="font-medium">Dark Appearance</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Match the AimForge theme
                      </div>
                    </div>
                    <Switch checked={true} />
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-xl leading-7">
                      Gaming Identity
                    </h3>
                    <p className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Your competitive setup and role.
                    </p>
                  </div>
                  <Gamepad2 className="size-5 text-[#f54900]" />
                </div>
                <div className="grid grid-cols-2 mt-5 gap-4">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Main Role
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      Entry Fragger
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Preferred Mode
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      Ranked
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Sensitivity
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      Low / Controlled
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4">
                    <div className="uppercase text-[#9f9fa9] text-xs leading-4 tracking-[4px]">
                      Coach Plan
                    </div>
                    <div className="font-medium text-base leading-6 mt-2">
                      Pro Athlete
                    </div>
                  </div>
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-xl leading-7">
                      Security
                    </h3>
                    <p className="text-[#9f9fa9] text-sm leading-5 mt-1">
                      Keep your account protected.
                    </p>
                  </div>
                  <ShieldCheck className="size-5 text-[#f54900]" />
                </div>
                <div className="space-y-3 mt-5">
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center">
                    <div>
                      <div className="font-medium">
                        Two-factor authentication
                      </div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Enabled for login protection
                      </div>
                    </div>
                    <div className="font-medium rounded-full bg-[#f54900]/15 text-[#f54900] text-xs leading-4 px-3 py-1">
                      On
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center">
                    <div>
                      <div className="font-medium">Last login</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        {user?.last_login_at ? new Date(user.last_login_at).toLocaleDateString() : 'Just now'}
                      </div>
                    </div>
                    <Clock3 className="size-4 text-[#9f9fa9]" />
                  </div>
                  
                  <div className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid flex p-4 justify-between items-center mt-6 border-red-500/20 bg-red-500/5">
                    <div>
                      <div className="font-medium text-red-500">Sign Out</div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        End your current session
                      </div>
                    </div>
                    <Button variant="outline" className="text-red-500 border-red-500 hover:bg-red-500 hover:text-white" onClick={handleLogout}>
                      <LogOut className="size-4 mr-2" />
                      Sign Out
                    </Button>
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
