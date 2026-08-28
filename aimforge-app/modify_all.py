import os
import re

def modify_dashboard():
    path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\Dashboard.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Loader2 } from "lucide-react";
'''
    content = content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

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
    content = content.replace('export default function App() {\n', f'export default function App() {{\n{hook_logic}')

    feedback_regex = r'<div className="flex mt-5 flex-col gap-3">.*?</div>\s*</div>\s*<div className="rounded-3xl bg-zinc-900 border-white/10'
    dynamic_feedback = '''<div className="flex mt-5 flex-col gap-3">
                  {analysis?.events.map((event) => (
                    <div 
                      key={event.id}
                      className="rounded-2xl bg-zinc-950 border-white/10 border-1 border-solid p-4 cursor-pointer hover:border-[#f54900]/50 transition-colors"
                      onClick={() => handleSeek(event.seconds)}
                    >
                      <div className="text-[#9f9fa9] text-xs leading-4 flex justify-between items-center">
                        <span>{event.timestamp}</span>
                        <span className={`rounded-full px-2 py-1 ${
                          event.severity === 'critical' ? 'bg-[#ff6467]/15 text-[#ff6467]' : 
                          event.severity === 'warning' ? 'bg-[#f54900]/15 text-[#f54900]' : 
                          'bg-[#00bc7d]/15 text-[#00bc7d]'
                        }`}>
                          {event.title}
                        </span>
                      </div>
                      <div className="text-sm leading-6 mt-3">
                        {event.description}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-3xl bg-zinc-900 border-white/10'''

    content = re.sub(feedback_regex, dynamic_feedback, content, flags=re.DOTALL)

    video_regex = r'<img\s+alt="Gameplay analysis preview".*?/>\s*<div className="bg-\[linear-gradient.*?/>'
    dynamic_video = '''
                    <video 
                      ref={videoRef}
                      className="object-cover w-full h-full"
                      controls
                      src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" 
                      onTimeUpdate={(e) => setCurrentVideoTime(Math.floor(e.currentTarget.currentTime))}
                    />
'''
    content = re.sub(video_regex, dynamic_video, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def modify_coach():
    path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\AiCoachPage.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Loader2, Bot as BotIcon, User as UserIcon } from "lucide-react";
'''
    content = content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

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
    content = content.replace('export default function App() {\n', f'export default function App() {{\n{hook_logic}')

    content = content.replace('<textarea\n                      className="min-h-[120px] resize-none outline-none rounded-2xl bg-zinc-900 text-sm leading-5 border-white/15 border-1 border-solid px-4 py-3 flex-1"\n                      defaultValue=""\n                      placeholder="Example: Why was my crosshair placement bad at 02:14?"\n                    />', '<textarea\n                      className="min-h-[120px] resize-none outline-none rounded-2xl bg-zinc-900 text-sm leading-5 border-white/15 border-1 border-solid px-4 py-3 flex-1"\n                      value={inputValue}\n                      onChange={(e) => setInputValue(e.target.value)}\n                      onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}\n                      placeholder="Example: Why was my crosshair placement bad at 02:14?"\n                    />')

    content = content.replace('<button className="inline-flex font-medium shadow-[0_10px_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900] text-orange-50 text-sm leading-5 px-5 py-3 items-center gap-2">', '<button onClick={handleSend} disabled={isTyping} className="inline-flex font-medium shadow-[0_10px_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900] text-orange-50 text-sm leading-5 px-5 py-3 items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">')

    response_regex = r'<div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6">\s*<div className="flex justify-between items-center">.*?<div className="flex mt-4 flex-wrap gap-2">.*?</div>\s*</div>'
    dynamic_chat = '''<div className="rounded-3xl bg-zinc-900 border-white/10 border-1 border-solid p-6 flex flex-col h-[500px]">
                  <div className="flex justify-between items-center mb-4 shrink-0">
                    <div>
                      <div className="text-[#9f9fa9] text-sm leading-5">
                        Coach response
                      </div>
                      <div className="font-semibold text-xl leading-7 mt-1">
                        Live Conversation
                      </div>
                    </div>
                    <div className="rounded-full bg-[#f54900]/10 text-[#f54900] text-xs leading-4 border-[#f54900]/20 border-1 border-solid px-3 py-1">
                      Live
                    </div>
                  </div>
                  <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                    {chatHistory.map((msg, idx) => (
                      <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        <div className={`size-8 shrink-0 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-zinc-800' : 'bg-[#f54900]/20 text-[#f54900]'}`}>
                          {msg.role === 'user' ? <UserIcon className="size-4" /> : <BotIcon className="size-4" />}
                        </div>
                        <div className={`rounded-2xl p-4 text-sm leading-6 max-w-[85%] ${msg.role === 'user' ? 'bg-zinc-800 text-neutral-50 rounded-tr-sm' : 'bg-zinc-950 border-white/10 border-1 border-solid text-[#9f9fa9] rounded-tl-sm'}`}>
                          {msg.role === 'assistant' ? <span className="text-neutral-50">{msg.content}</span> : msg.content}
                        </div>
                      </div>
                    ))}
                    {isTyping && (
                      <div className="flex gap-3">
                        <div className="size-8 shrink-0 rounded-full flex items-center justify-center bg-[#f54900]/20 text-[#f54900]">
                          <BotIcon className="size-4" />
                        </div>
                        <div className="rounded-2xl p-4 bg-zinc-950 border-white/10 border-1 border-solid rounded-tl-sm flex items-center gap-1">
                          <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                          <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                          <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>'''

    content = re.sub(response_regex, dynamic_chat, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def modify_training():
    path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\TrainingPlanPage.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
'''
    content = content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

    hook_logic = '''
  const navigate = useNavigate();
  const { analysis } = useAppStore();
'''
    content = content.replace('export default function App() {\n', f'export default function App() {{\n{hook_logic}')

    content = content.replace('>184ms<', '>{analysis?.ratings.reactionTime || "184"}ms<')
    content = content.replace('>92%<', '>{analysis?.ratings.accuracy || "92"}%<')
    content = content.replace('>8.7<', '>{analysis?.ratings.aim || "8.7"}<')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def modify_nav():
    files = [
        'LandingPage.tsx',
        'Dashboard.tsx',
        'HistoryPage.tsx',
        'TrainingPlanPage.tsx',
        'AiCoachPage.tsx',
        'ProfilePage.tsx'
    ]

    for page in files:
        path = os.path.join('src', 'pages', page)
        if not os.path.exists(path): continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'import { useNavigate }' not in content:
            if 'import { useEffect' in content:
                content = content.replace('import { useEffect', 'import { useNavigate } from "react-router-dom";\nimport { useEffect')
            else:
                content = 'import { useNavigate } from "react-router-dom";\n' + content

        if 'const navigate = useNavigate();' not in content:
            # We only inject if not already injected (e.g. Dashboard/AiCoach/Training already have it from earlier modifications)
            content = content.replace('export default function App() {\n  return', 'export default function App() {\n  const navigate = useNavigate();\n  return')

        if page == 'LandingPage.tsx':
            content = content.replace('>Dashboard<', ' onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}>Dashboard<')
            content = content.replace('>Analysis<', ' onClick={() => navigate("/dashboard")} style={{cursor: "pointer"}}>Analysis<')
            content = content.replace('>History<', ' onClick={() => navigate("/history")} style={{cursor: "pointer"}}>History<')
            content = content.replace('>Training<', ' onClick={() => navigate("/training")} style={{cursor: "pointer"}}>Training<')
            content = content.replace('>AI Coach<', ' onClick={() => navigate("/coach")} style={{cursor: "pointer"}}>AI Coach<')
            content = content.replace('>Profile<', ' onClick={() => navigate("/profile")} style={{cursor: "pointer"}}>Profile<')
            content = content.replace('<Button className="rounded-lg bg-[#f54900] text-orange-50">', '<Button className="rounded-lg bg-[#f54900] text-orange-50" onClick={() => navigate("/dashboard")}>')
            content = content.replace('<Button\\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\\n                size="lg"\\n              >', '<Button\\n                className="shadow-[0_0_30px_oklch(0.646_0.222_41.116/0.4)] rounded-xl bg-[#f54900] text-orange-50 gap-2"\\n                size="lg"\\n                onClick={() => navigate("/upload")}\\n              >')
            # Need to fix the new lines format for upload button since read handles it differently
            content = re.sub(r'(<Button\s+className="shadow-\[0_0_30px_oklch\(0\.646_0\.222_41\.116/0\.4\)\] rounded-xl bg-\[#f54900\] text-orange-50 gap-2"\s+size="lg")', r'\1 onClick={() => navigate("/upload")}', content)
        else:
            content = content.replace('<span>Dashboard</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Dashboard</span>')
            content = content.replace('<span>Analysis</span>', '<span onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-white w-full h-full">Analysis</span>')
            content = content.replace('<span>History</span>', '<span onClick={() => navigate("/history")} className="cursor-pointer hover:text-white w-full h-full">History</span>')
            content = content.replace('<span>Training</span>', '<span onClick={() => navigate("/training")} className="cursor-pointer hover:text-white w-full h-full">Training</span>')
            content = content.replace('<span>AI Coach</span>', '<span onClick={() => navigate("/coach")} className="cursor-pointer hover:text-white w-full h-full">AI Coach</span>')
            content = content.replace('<span>Profile</span>', '<span onClick={() => navigate("/profile")} className="cursor-pointer hover:text-white w-full h-full">Profile</span>')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    modify_dashboard()
    modify_coach()
    modify_training()
    modify_nav()
    print('All modifications applied successfully.')
