import { X, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ComingSoonModalProps {
  isOpen: boolean;
  onClose: () => void;
  featureName: string;
}

export function ComingSoonModal({ isOpen, onClose, featureName }: ComingSoonModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-zinc-950 border border-white/10 rounded-3xl p-8 max-w-md w-full shadow-[0_20px_60px_rgba(0,0,0,0.5)] relative flex flex-col items-center text-center animate-in zoom-in-95 duration-200">
        <button 
          onClick={onClose}
          className="cursor-pointer absolute top-4 right-4 p-2 text-zinc-400 hover:text-white bg-zinc-900 rounded-full transition-colors"
        >
          <X className="size-4" />
        </button>
        
        <div className="size-16 rounded-full bg-[#f54900]/10 border border-[#f54900]/30 flex items-center justify-center mb-6 text-[#f54900] shadow-[0_0_30px_rgba(245,73,0,0.2)]">
          <Sparkles className="size-8" />
        </div>
        
        <h3 className="text-2xl font-bold text-neutral-50 mb-2">Coming Soon</h3>
        <p className="text-[#9f9fa9] text-base mb-8">
          The <strong className="text-white font-semibold">{featureName}</strong> feature is currently in development. We're training our AI models to bring you this capability very soon!
        </p>
        
        <Button 
          onClick={onClose}
          className="w-full bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl py-6 text-base font-semibold"
        >
          Got it, thanks!
        </Button>
      </div>
    </div>
  );
}
