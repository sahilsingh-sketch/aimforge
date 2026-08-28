import os
import re

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
content = content.replace('export default function App() {\n  const navigate = useNavigate();\n', f'export default function App() {{\n{hook_logic}')

# Replace the input and send button
content = content.replace('<textarea\n                      className="min-h-[120px] resize-none outline-none rounded-2xl bg-zinc-900 text-sm leading-5 border-white/15 border-1 border-solid px-4 py-3 flex-1"\n                      defaultValue=""\n                      placeholder="Example: Why was my crosshair placement bad at 02:14?"\n                    />', '<textarea\n                      className="min-h-[120px] resize-none outline-none rounded-2xl bg-zinc-900 text-sm leading-5 border-white/15 border-1 border-solid px-4 py-3 flex-1"\n                      value={inputValue}\n                      onChange={(e) => setInputValue(e.target.value)}\n                      onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}\n                      placeholder="Example: Why was my crosshair placement bad at 02:14?"\n                    />')

content = content.replace('<button className="inline-flex font-medium shadow-[0_10px_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900] text-orange-50 text-sm leading-5 px-5 py-3 items-center gap-2">', '<button onClick={handleSend} disabled={isTyping} className="inline-flex font-medium shadow-[0_10px_30px_rgba(249,115,22,0.25)] rounded-2xl bg-[#f54900] text-orange-50 text-sm leading-5 px-5 py-3 items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">')

# Replace the response area with chat history
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
                      <div key={idx} className={lex gap-3 }>
                        <div className={size-8 shrink-0 rounded-full flex items-center justify-center }>
                          {msg.role === 'user' ? <UserIcon className="size-4" /> : <BotIcon className="size-4" />}
                        </div>
                        <div className={ounded-2xl p-4 text-sm leading-6 max-w-[85%] }>
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
print('AiCoach modified')
