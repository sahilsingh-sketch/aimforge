import { useState, useEffect, useRef } from "react";
import { Bell, Settings2, PlayCircle, Eye, ExternalLink } from "lucide-react";
import { Button } from "./ui/button";
import { useUpdatesStore } from "../store/useUpdatesStore";
import type { UpdateItem } from "../services/updatesApi";

function timeAgo(dateStr?: string) {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (seconds < 60) return "Just now";
  
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function BGMIUpdatesDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  
  const { 
    updates, 
    unreadCount, 
    activeCategory, 
    fetchUpdates, 
    fetchUnreadCount,
    setActiveCategory,
    markAsRead,
    markAllAsRead
  } = useUpdatesStore();

  useEffect(() => {
    // Initial fetch for count
    fetchUnreadCount();
    
    // Auto-refresh count every minute
    const interval = setInterval(fetchUnreadCount, 60000);
    return () => clearInterval(interval);
  }, [fetchUnreadCount]);

  useEffect(() => {
    if (isOpen) {
      fetchUpdates(activeCategory);
    }
  }, [isOpen, activeCategory, fetchUpdates]);

  // Handle outside click
  /*
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);
  */

  const tabs = ["All", "Tournaments", "Pro Play", "News"];

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "ONGOING":
        return <span className="bg-[#00bc7d]/20 text-[#00bc7d] px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider">ONGOING</span>;
      case "UPCOMING":
        return <span className="bg-purple-500/20 text-purple-400 px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider">UPCOMING</span>;
      case "NEWS":
        return <span className="bg-[#f54900]/20 text-[#f54900] px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider">NEWS</span>;
      case "PRO_PLAY":
        return <span className="bg-[#f54900]/20 text-[#f54900] px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider">PRO PLAY</span>;
      default:
        return null;
    }
  };

  const getActionButton = (update: UpdateItem) => {
    const handleClick = () => {
      markAsRead(update.id);
      window.open(update.source_url, "_blank", "noopener,noreferrer");
    };

    let icon = <ExternalLink className="size-3 mr-1.5" />;
    let label = "View Details";

    if (update.source === "YOUTUBE") {
      icon = <PlayCircle className="size-3 mr-1.5" />;
      label = update.status === "ONGOING" ? "Watch Live" : "Watch Now";
    } else if (update.category === "GAME_NEWS") {
      icon = <Eye className="size-3 mr-1.5" />;
      label = "Read More";
    }

    return (
      <button 
        onClick={handleClick}
        className="flex items-center text-xs font-medium bg-white/5 hover:bg-white/10 text-white px-3 py-1.5 rounded transition-colors"
      >
        {icon}
        {label}
      </button>
    );
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        className="relative rounded-full p-2 hover:bg-white/10 transition-colors flex items-center justify-center cursor-pointer"
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          console.log("[NOTIFICATION DEBUG] BELL CLICKED");
          setIsOpen((prev) => {
            const newState = !prev;
            console.log("[NOTIFICATION DEBUG] OPEN STATE:", newState);
            return newState;
          });
        }}
      >
        <Bell className="size-5 text-white" />
        {unreadCount > 0 && (
          <span className="absolute right-1 top-1 flex h-2 w-2 pointer-events-none">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#f54900] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-[#f54900]"></span>
          </span>
        )}
      </button>

      {isOpen && (
          <div
            className="absolute right-0 top-full mt-3 w-[400px] z-50 bg-[#121215] border border-white/10 rounded-xl shadow-2xl overflow-hidden flex flex-col origin-top-right"
            style={{ 
              boxShadow: "0 20px 40px -10px rgba(0,0,0,0.5), 0 0 20px 0 rgba(245, 73, 0, 0.05)" 
            }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/5 bg-black/20">
              <h3 className="font-bold text-base">BGMI Updates</h3>
              <div className="flex items-center gap-3">
                <button 
                  className="text-xs text-[#f54900] hover:text-[#ff6467] font-medium transition-colors"
                  onClick={() => markAllAsRead()}
                >
                  Mark all as read
                </button>
                <Settings2 className="size-4 text-[#9f9fa9] cursor-pointer hover:text-white transition-colors" />
              </div>
            </div>

            {/* Tabs */}
            <div className="flex px-2 pt-2 border-b border-white/5">
              {tabs.map((tab) => {
                const apiCategory = tab === "All" ? "All" : 
                                   tab === "Tournaments" ? "TOURNAMENT" : 
                                   tab === "Pro Play" ? "PRO_PLAY" : "GAME_NEWS";
                                   
                const isActive = activeCategory === apiCategory;
                
                return (
                  <button
                    key={tab}
                    onClick={() => setActiveCategory(apiCategory)}
                    className={`px-3 py-2 text-xs font-medium transition-all relative ${
                      isActive ? "text-white" : "text-[#9f9fa9] hover:text-white"
                    }`}
                  >
                    {tab}
                    {isActive && (
                      <div 
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#f54900]" 
                      />
                    )}
                  </button>
                );
              })}
            </div>

            {/* List */}
            <div className="max-h-[400px] overflow-y-auto custom-scrollbar">
              {updates.length === 0 ? (
                <div className="py-12 flex flex-col items-center justify-center text-center">
                  <Bell className="size-8 text-white/10 mb-3" />
                  <p className="text-[#9f9fa9] text-sm">No updates found.</p>
                </div>
              ) : (
                updates.map((update) => (
                  <div 
                    key={update.id} 
                    className={`p-4 border-b border-white/5 flex gap-4 transition-colors hover:bg-white/[0.02] cursor-pointer ${
                      !update.is_read ? 'bg-white/[0.03]' : ''
                    }`}
                    onClick={() => markAsRead(update.id)}
                  >
                    {/* Thumbnail */}
                    <div className="shrink-0 relative">
                      <div className="w-[100px] h-[60px] rounded-md overflow-hidden bg-black/50 border border-white/10 relative group">
                        {update.thumbnail_url ? (
                          <img 
                            src={update.thumbnail_url} 
                            alt={update.title} 
                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center bg-zinc-900">
                            <span className="text-[10px] text-white/30 font-bold">AIMFORGE</span>
                          </div>
                        )}
                        <div className="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors" />
                      </div>
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between mb-1 gap-2">
                        {getStatusBadge(update.status === 'NEWS' && update.category === 'PRO_PLAY' ? 'PRO_PLAY' : update.status)}
                        <span className="text-[10px] text-[#9f9fa9] whitespace-nowrap flex items-center gap-1.5">
                          {timeAgo(update.published_at)}
                          {!update.is_read && <span className="w-1.5 h-1.5 rounded-full bg-[#f54900]" />}
                        </span>
                      </div>
                      
                      <h4 className="text-sm font-semibold text-white leading-tight mb-1 line-clamp-2" title={update.title}>
                        {update.title}
                      </h4>
                      
                      {update.description && (
                        <p className="text-xs text-[#9f9fa9] line-clamp-2 mb-3 leading-relaxed">
                          {update.description}
                        </p>
                      )}
                      
                      <div className="flex items-center justify-end mt-2">
                        {getActionButton(update)}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            <div className="p-3 border-t border-white/5 text-center bg-black/20">
              <button className="text-xs text-[#9f9fa9] hover:text-white font-medium flex items-center justify-center gap-1.5 w-full transition-colors">
                View All Updates
                <ExternalLink className="size-3" />
              </button>
            </div>
          </div>
        )}
    </div>
  );
}
