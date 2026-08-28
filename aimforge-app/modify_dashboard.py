import os
import re

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\Dashboard.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
imports = '''
import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Loader2 } from "lucide-react";
'''
content = content.replace('import { useEffect } from "react";', f'import {{ useEffect, useState, useRef }} from "react";\n{imports}')

# Inject state logic
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
content = content.replace('export default function App() {\n  const navigate = useNavigate();\n', f'export default function App() {{\n{hook_logic}')

# Replace static AI Feedback Feed block with dynamic loop
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
                        <span className={ounded-full px-2 py-1 }>
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

# Inject Video Player
# Let's replace the static img with a video player
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

# Save
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Dashboard modified')
