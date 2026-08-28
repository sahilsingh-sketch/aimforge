/* eslint-disable */
// @ts-nocheck
import { useEffect, useState, useRef } from "react";

import { aimforgeService } from "../services/api";
import { useAppStore } from "../store/useAppStore";
import { Target, User, Send } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function App() {
  const navigate = useNavigate();
  const { chatHistory, addChatMessage, setChatHistory, jobId, setJobId } = useAppStore();
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  
  // Typewriter State
  const [typingContent, setTypingContent] = useState("");
  const [fullContent, setFullContent] = useState("");
  const [isTypewriterActive, setIsTypewriterActive] = useState(false);

  const scrollRef = useRef<HTMLDivElement>(null);
  const userScrolledUp = useRef(false);

  // Auto-scroll logic
  const scrollToBottom = () => {
    if (scrollRef.current && !userScrolledUp.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth"
      });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isTyping, typingContent, errorMsg]);

  // Track if user scrolls up
  const handleScroll = () => {
    if (scrollRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
      // If user scrolls up more than 50px from bottom, consider it a manual scroll up
      if (scrollHeight - scrollTop - clientHeight > 50) {
        userScrolledUp.current = true;
      } else {
        userScrolledUp.current = false;
      }
    }
  };

  useEffect(() => {
    if (jobId) {
      aimforgeService.getChatHistory(jobId).then(history => {
        if (history && history.length > 0) {
          setChatHistory(history);
        }
      });
    }
  }, [jobId]);

  // Typewriter effect hook
  useEffect(() => {
    if (isTypewriterActive && typingContent.length < fullContent.length) {
      const timer = setTimeout(() => {
        // Add 1-2 characters per tick for smooth speed (roughly 15-30ms)
        setTypingContent(fullContent.slice(0, typingContent.length + 2));
      }, 20);
      return () => clearTimeout(timer);
    } else if (isTypewriterActive && typingContent.length >= fullContent.length) {
      setIsTypewriterActive(false);
      // Once animation finishes, push the actual message to global state
      addChatMessage({ role: "assistant", content: fullContent, timestamp: Date.now() });
      setTypingContent("");
      setFullContent("");
    }
  }, [typingContent, fullContent, isTypewriterActive]);

  const handleSend = async (overrideMsg?: string) => {
    const textToSend = typeof overrideMsg === 'string' ? overrideMsg : inputValue;
    if (!textToSend.trim()) return;
    
    let activeJobId = jobId;
    if (!activeJobId) {
      activeJobId = `general-${Date.now()}`;
      setJobId(activeJobId);
    }
    
    const msg = textToSend.trim();
    if (typeof overrideMsg !== 'string') {
      setInputValue("");
    }
    setErrorMsg("");
    userScrolledUp.current = false; // Reset scroll lock
    
    addChatMessage({ role: "user", content: msg, timestamp: Date.now() });
    
    setIsTyping(true);
    try {
      const response = await aimforgeService.sendChatMessage(activeJobId, msg);
      
      // Instead of instantly adding to global state, trigger the typewriter
      setFullContent(response.content);
      setTypingContent("");
      setIsTypewriterActive(true);
      
    } catch (e: any) {
      console.error(e);
      setErrorMsg(e.message || "I couldn't generate your coaching response right now. Please try again.");
    } finally {
      setIsTyping(false);
    }
  };

  const handleSuggestedPrompt = (prompt: string) => {
    handleSend(prompt);
  };

  // Reusable Chat Input Element
  const chatInputBoxElement = (
    <div className="w-full flex-shrink-0 pt-4 pb-6">
      <div className="rounded-3xl bg-zinc-900 border border-white/10 shadow-[0_0_40px_rgba(0,0,0,0.5)] p-2 flex flex-col focus-within:border-[#f54900]/50 transition-colors">
        <textarea
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            e.target.style.height = 'auto';
            e.target.style.height = `${Math.min(e.target.scrollHeight, 200)}px`;
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          className="w-full resize-none outline-none bg-transparent text-[15px] text-neutral-50 placeholder-[#70707a] px-4 py-3 max-h-[200px] overflow-y-auto"
          placeholder={jobId ? "Ask your coach anything..." : "Ask your coach anything..."}
          rows={1}
          style={{ minHeight: '52px' }}
        />
        <div className="flex justify-between items-center px-2 pb-1">
          <div className="text-xs text-[#70707a] px-2 font-medium">
            Your coach uses your gameplay analysis to give personalized advice.
          </div>
          <button 
            onClick={() => handleSend()}
            disabled={(!inputValue.trim() && !isTyping) || isTyping || isTypewriterActive}
            className="size-9 rounded-full bg-[#f54900] disabled:bg-zinc-800 disabled:text-[#70707a] text-white flex items-center justify-center cursor-pointer disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95 shadow-[0_4px_14px_rgba(249,115,22,0.3)] disabled:shadow-none"
          >
            <Send className="size-4 ml-0.5" />
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full flex-1 flex flex-col h-[calc(100vh-80px)] max-w-[850px] mx-auto px-4 overflow-hidden">
      {chatHistory.length === 0 && !isTypewriterActive && !isTyping ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center">
          <div className="size-16 shadow-[0_0_40px_rgba(249,115,22,0.2)] rounded-3xl bg-[#f54900]/10 text-[#f54900] flex justify-center items-center mb-6">
            <Target className="size-8" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-white mb-4">
            What's on your AIM?
          </h1>
          <p className="text-[#9f9fa9] text-lg max-w-lg mb-8">
            Ask me anything about your gameplay, aim, positioning, fights, rotations, or how you can improve.
          </p>
          <div className="flex flex-wrap justify-center gap-3 mb-10">
            <button onClick={() => handleSuggestedPrompt("Why did I lose my last fight?")} className="rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 transition-colors shadow-sm cursor-pointer">
              Why did I lose my last fight?
            </button>
            <button onClick={() => handleSuggestedPrompt("How can I improve my aim?")} className="rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 transition-colors shadow-sm cursor-pointer">
              How can I improve my aim?
            </button>
            <button onClick={() => handleSuggestedPrompt("Analyze my positioning")} className="rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 transition-colors shadow-sm cursor-pointer">
              Analyze my positioning
            </button>
          </div>
          <div className="w-full max-w-2xl">
            {chatInputBoxElement}
          </div>
        </div>
      ) : (
        <>
          <div 
            className="flex-1 overflow-y-auto pr-2 pt-6 space-y-6" 
            ref={scrollRef}
            onScroll={handleScroll}
          >
            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex gap-4 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {msg.role === 'assistant' ? (
                    <div className="size-8 shrink-0 rounded-full bg-[#f54900]/20 flex items-center justify-center border border-[#f54900]/30 mt-1">
                      <Target className="size-4 text-[#f54900]" />
                    </div>
                  ) : (
                    <div className="size-8 shrink-0 rounded-full bg-zinc-800 flex items-center justify-center mt-1">
                      <User className="size-4 text-[#9f9fa9]" />
                    </div>
                  )}
                  <div className={`rounded-2xl px-5 py-4 text-[15px] leading-relaxed border-1 border-solid ${
                    msg.role === 'user' 
                      ? 'bg-zinc-800 text-neutral-50 border-white/10' 
                      : 'bg-transparent text-[#d1d1d6] border-transparent p-0'
                  }`}>
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              </div>
            ))}

            {/* Typewriter Animation Bubble */}
            {isTypewriterActive && (
              <div className="flex w-full justify-start">
                <div className="flex gap-4 max-w-[85%] flex-row">
                  <div className="size-8 shrink-0 rounded-full bg-[#f54900]/20 flex items-center justify-center border border-[#f54900]/30 mt-1">
                    <Target className="size-4 text-[#f54900]" />
                  </div>
                  <div className="rounded-2xl py-4 text-[15px] leading-relaxed bg-transparent text-[#d1d1d6]">
                    <div className="whitespace-pre-wrap">{typingContent}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Typing Indicator */}
            {isTyping && !isTypewriterActive && (
              <div className="flex w-full justify-start">
                <div className="flex gap-4 max-w-[85%]">
                  <div className="size-8 shrink-0 rounded-full bg-[#f54900]/20 flex items-center justify-center border border-[#f54900]/30 mt-1">
                    <Target className="size-4 text-[#f54900]" />
                  </div>
                  <div className="rounded-2xl py-4 text-[15px] flex items-center gap-1.5 h-[56px]">
                    <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                    <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                    <span className="size-1.5 bg-[#f54900] rounded-full animate-bounce"></span>
                  </div>
                </div>
              </div>
            )}
            
            {errorMsg && (
              <div className="flex w-full justify-center mt-4 pb-4">
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-2 rounded-xl text-sm">
                  {errorMsg}
                </div>
              </div>
            )}
            {/* Bottom spacer for padding inside the scrolling container */}
            <div className="h-4 w-full"></div>
          </div>
          
          {chatInputBoxElement}
        </>
      )}
    </div>
  );
}
