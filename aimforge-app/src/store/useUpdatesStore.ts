import { create } from 'zustand';
import type { UpdateItem } from '../services/updatesApi';
import { updatesApi } from '../services/updatesApi';

interface UpdatesState {
  updates: UpdateItem[];
  unreadCount: number;
  isLoading: boolean;
  error: string | null;
  activeCategory: string;
  hasLoadedInitial: boolean;

  fetchUpdates: (category?: string) => Promise<void>;
  fetchUnreadCount: () => Promise<void>;
  markAsRead: (id: number) => Promise<void>;
  markAllAsRead: () => Promise<void>;
  setActiveCategory: (category: string) => void;
}

export const useUpdatesStore = create<UpdatesState>((set, get) => ({
  updates: [],
  unreadCount: 0,
  isLoading: false,
  error: null,
  activeCategory: 'All',
  hasLoadedInitial: false,

  setActiveCategory: (category: string) => {
    set({ activeCategory: category });
    get().fetchUpdates(category);
  },

  fetchUpdates: async (category = get().activeCategory) => {
    set({ isLoading: true, error: null });
    try {
      const data = await updatesApi.getUpdates(category);
      set({ updates: data, hasLoadedInitial: true, isLoading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to fetch updates', isLoading: false });
    }
  },

  fetchUnreadCount: async () => {
    try {
      const count = await updatesApi.getUnreadCount();
      set({ unreadCount: count });
    } catch (error) {
      console.error('Failed to fetch unread count', error);
    }
  },

  markAsRead: async (id: number) => {
    const { updates, unreadCount } = get();
    const targetUpdate = updates.find(u => u.id === id);
    
    if (!targetUpdate || targetUpdate.is_read) return;

    // Optimistic update
    set({
      updates: updates.map(u => u.id === id ? { ...u, is_read: true } : u),
      unreadCount: Math.max(0, unreadCount - 1)
    });

    try {
      await updatesApi.markAsRead(id);
    } catch (error) {
      // Revert if failed
      get().fetchUpdates();
      get().fetchUnreadCount();
    }
  },

  markAllAsRead: async () => {
    const { updates } = get();
    
    // Optimistic update
    set({
      updates: updates.map(u => ({ ...u, is_read: true })),
      unreadCount: 0
    });

    try {
      await updatesApi.markAllAsRead();
    } catch (error) {
      // Revert if failed
      get().fetchUpdates();
      get().fetchUnreadCount();
    }
  }
}));
