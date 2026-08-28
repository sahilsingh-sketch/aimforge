import sys
import codecs

file_path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\aimforge-app\src\pages\AiCoachPage.tsx'

with codecs.open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import { ComingSoonModal } from \"@/components/ComingSoonModal\";\n', '')
content = content.replace('  const [modalOpen, setModalOpen] = useState(false);\n', '')
content = content.replace('  const [modalFeature, setModalFeature] = useState(\"\");\n', '')

coming_soon_func = '''  const handleComingSoon = (feature: string) => {
    setModalFeature(feature);
    setModalOpen(true);
  };'''
content = content.replace(coming_soon_func, '')

modal_comp = '''      <ComingSoonModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        featureName={modalFeature} 
      />'''
content = content.replace(modal_comp, '')

start_idx = content.find('<div className=\"grid grid-cols-[1.35fr_0.85fr] mt-8 flex-1 gap-6\">')
end_idx = content.rfind('        </div>\n      </div>\n    </div>\n  );\n}')

if start_idx == -1 or end_idx == -1:
    print('Could not find boundaries')
    sys.exit(1)

chat_block = '''          <div className=\"max-w-[850px] mx-auto w-full flex-1 flex flex-col mt-4 overflow-hidden relative\">
            {chatHistory.length === 0 ? (
              <div className=\"flex-1 flex flex-col items-center justify-center text-center px-4 pb-20\">
                <div className=\"size-16 shadow-[0_0_40px_rgba(249,115,22,0.2)] rounded-3xl bg-[#f54900]/10 text-[#f54900] flex justify-center items-center mb-6\">
                  <Target className=\"size-8\" />
                </div>
                <h1 className=\"text-4xl font-bold tracking-tight text-white mb-4\">
                  What\\'s on your AIM?
                </h1>
                <p className=\"text-[#9f9fa9] text-lg max-w-lg mb-10\">
                  Ask me anything about your gameplay, aim, positioning, fights, rotations, or how you can improve.
                </p>
                <div className=\"flex flex-wrap justify-center gap-3\">
                  <button onClick={() => handleSuggestedPrompt(\"Why did I lose my last fight?\")} className=\"rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 cursor-pointer transition-colors shadow-sm\">
                    Why did I lose my last fight?
                  </button>
                  <button onClick={() => handleSuggestedPrompt(\"How can I improve my aim?\")} className=\"rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 cursor-pointer transition-colors shadow-sm\">
                    How can I improve my aim?
                  </button>
                  <button onClick={() => handleSuggestedPrompt(\"Analyze my positioning\")} className=\"rounded-full bg-zinc-900 hover:bg-zinc-800 text-[#9f9fa9] hover:text-white text-sm leading-5 border-white/10 border-1 border-solid px-5 py-2.5 cursor-pointer transition-colors shadow-sm\">
                    Analyze my positioning
                  </button>
                </div>
              </div>
            ) : (
              <div className=\"flex-1 overflow-y-auto pr-2 pb-24 space-y-6 mt-6\" ref={scrollRef}>
                {chatHistory.map((msg, idx) => (
                  <div key={idx} className={lex w-full }>
                    <div className={lex gap-4 max-w-[85%] }>
                      {msg.role === 'assistant' ? (
                        <div className=\"size-8 shrink-0 rounded-full bg-[#f54900]/20 flex items-center justify-center border border-[#f54900]/30 mt-1\">
                          <Target className=\"size-4 text-[#f54900]\" />
                        </div>
                      ) : (
                        <div className=\"size-8 shrink-0 rounded-full bg-zinc-800 flex items-center justify-center mt-1\">
                          <User className=\"size-4 text-[#9f9fa9]\" />
                        </div>
                      )}
                      <div className={ounded-2xl px-5 py-4 text-[15px] leading-relaxed border-1 border-solid }>
                        <div className=\"whitespace-pre-wrap\">{msg.content}</div>
                      </div>
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className=\"flex w-full justify-start\">
                    <div className=\"flex gap-4 max-w-[85%]\">
                      <div className=\"size-8 shrink-0 rounded-full bg-[#f54900]/20 flex items-center justify-center border border-[#f54900]/30 mt-1\">
                        <Target className=\"size-4 text-[#f54900]\" />
                      </div>
                      <div className=\"rounded-2xl px-2 py-4 text-[15px] leading-relaxed flex items-center gap-2\">
                        <span className=\"text-[#9f9fa9] italic text-sm\">AI Coach is thinking...</span>
                        <Loader2 className=\"size-4 animate-spin text-[#f54900]\" />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            <div className=\"absolute bottom-0 left-0 w-full bg-gradient-to-t from-zinc-950 via-zinc-950 to-transparent pt-10 pb-6\">
              <div className=\"rounded-3xl bg-zinc-900 border border-white/10 shadow-[0_0_40px_rgba(0,0,0,0.5)] p-2 flex flex-col focus-within:border-[#f54900]/50 transition-colors\">
                <textarea
                  value={inputValue}
                  onChange={(e) => {
                    setInputValue(e.target.value);
                    e.target.style.height = 'auto';
                    e.target.style.height = ${Math.min(e.target.scrollHeight, 200)}px;
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  className=\"w-full resize-none outline-none bg-transparent text-[15px] text-neutral-50 placeholder-[#70707a] px-4 py-3 max-h-[200px] overflow-y-auto\"
                  placeholder={jobId ? \"Ask your coach anything...\" : \"Please select a job from History first to start coaching\"}
                  disabled={!jobId}
                  rows={1}
                  style={{ minHeight: '52px' }}
                />
                <div className=\"flex justify-between items-center px-2 pb-1\">
                  <div className=\"text-xs text-[#70707a] px-2 font-medium\">
                    Your coach uses your gameplay analysis to give personalized advice.
                  </div>
                  <button 
                    onClick={handleSend}
                    disabled={!jobId || !inputValue.trim() || isTyping}
                    className=\"size-9 rounded-full bg-[#f54900] disabled:bg-zinc-800 disabled:text-[#70707a] text-white flex items-center justify-center cursor-pointer transition-all hover:scale-105 active:scale-95 shadow-[0_4px_14px_rgba(249,115,22,0.3)] disabled:shadow-none\"
                  >
                    <Send className=\"size-4\" />
                  </button>
                </div>
              </div>
            </div>
          </div>
'''

new_content = content[:start_idx] + chat_block + content[end_idx:]

with codecs.open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Modification complete.')
