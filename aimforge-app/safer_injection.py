import os

# Restore Dashboard
with open(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\frontend\Screen 2\Screen 2\src\App.tsx', 'r', encoding='utf-8') as f:
    dashboard_content = f.read()

imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
'''
dashboard_content = dashboard_content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

hook_logic = '''
  const navigate = useNavigate();
  const { analysis, setAnalysis, currentVideoTime, setCurrentVideoTime } = useAppStore();
  const [loading, setLoading] = useState(!analysis);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    async function loadData() {
      if (!analysis) {
        try {
          const data = await aimforgeService.getAnalysis("demo-job-id");
          setAnalysis(data);
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    }
    loadData();
  }, [analysis, setAnalysis]);

  const handleSeek = (seconds: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = seconds;
      videoRef.current.play();
    }
    setCurrentVideoTime(seconds);
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-zinc-950 text-[#f54900]"><Loader2 className="size-8 animate-spin" /></div>;
  }
'''
dashboard_content = dashboard_content.replace('export default function App() {\n', f'export default function App() {{\n{hook_logic}')

# Re-inject the video. Find the exact static string
old_video = '''<img
                    alt="Gameplay analysis preview"
                    className="w-full h-full object-cover"
                    src="https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&amp;auto=format&amp;fit=crop&amp;w=2070&amp;q=80"
                  />'''
new_video = '''<video ref={videoRef} className="w-full h-full object-cover" controls src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" onTimeUpdate={(e) => setCurrentVideoTime(Math.floor(e.currentTarget.currentTime))} />'''
dashboard_content = dashboard_content.replace(old_video, new_video)

# Fix Nav
dashboard_content = dashboard_content.replace('<span>Dashboard</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Dashboard</span>')
dashboard_content = dashboard_content.replace('<span>Analysis</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Analysis</span>')
dashboard_content = dashboard_content.replace('<span>History</span>', '<span onClick={() => navigate("/history")} className="cursor-pointer hover:text-white w-full h-full">History</span>')
dashboard_content = dashboard_content.replace('<span>Training</span>', '<span onClick={() => navigate("/training")} className="cursor-pointer hover:text-white w-full h-full">Training</span>')
dashboard_content = dashboard_content.replace('<span>AI Coach</span>', '<span onClick={() => navigate("/coach")} className="cursor-pointer hover:text-white w-full h-full">AI Coach</span>')
dashboard_content = dashboard_content.replace('<span>Profile</span>', '<span onClick={() => navigate("/profile")} className="cursor-pointer hover:text-white w-full h-full">Profile</span>')

with open(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\Dashboard.tsx', 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

# Restore AiCoach
with open(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\frontend\Screen 5\Screen 5\src\App.tsx', 'r', encoding='utf-8') as f:
    coach_content = f.read()

imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Loader2, Bot as BotIcon, User as UserIcon } from "lucide-react";
import { useNavigate } from "react-router-dom";
'''
coach_content = coach_content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

hook_logic = '''
  const navigate = useNavigate();
  const { chatHistory, addChatMessage } = useAppStore();
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chatHistory, isTyping]);

  const handleSend = async () => {
    if (!inputValue.trim()) return;
    const msg = inputValue.trim();
    setInputValue("");
    addChatMessage({ role: "user", content: msg, timestamp: Date.now() });
    
    setIsTyping(true);
    try {
      const response = await aimforgeService.sendChatMessage(msg, chatHistory);
      addChatMessage(response);
    } catch (e) {
      console.error(e);
    } finally {
      setIsTyping(false);
    }
  };
'''
coach_content = coach_content.replace('export default function App() {\n', f'export default function App() {{\n{hook_logic}')

coach_content = coach_content.replace('<span>Dashboard</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Dashboard</span>')
coach_content = coach_content.replace('<span>Analysis</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Analysis</span>')
coach_content = coach_content.replace('<span>History</span>', '<span onClick={() => navigate("/history")} className="cursor-pointer hover:text-white w-full h-full">History</span>')
coach_content = coach_content.replace('<span>Training</span>', '<span onClick={() => navigate("/training")} className="cursor-pointer hover:text-white w-full h-full">Training</span>')
coach_content = coach_content.replace('<span>AI Coach</span>', '<span onClick={() => navigate("/coach")} className="cursor-pointer hover:text-white w-full h-full">AI Coach</span>')
coach_content = coach_content.replace('<span>Profile</span>', '<span onClick={() => navigate("/profile")} className="cursor-pointer hover:text-white w-full h-full">Profile</span>')

with open(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\AiCoachPage.tsx', 'w', encoding='utf-8') as f:
    f.write(coach_content)

print("Safer injection done")
