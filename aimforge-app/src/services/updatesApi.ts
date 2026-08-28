import { api } from './api';

export interface UpdateItem {
  id: number;
  source: string;
  source_url: string;
  title: string;
  description?: string;
  thumbnail_url?: string;
  category: 'TOURNAMENT' | 'PRO_PLAY' | 'GAME_NEWS';
  status: 'ONGOING' | 'UPCOMING' | 'COMPLETED' | 'NEWS';
  published_at?: string;
  is_read: boolean;
}

export const updatesApi = {
  getUpdates: async (category?: string, limit = 20, offset = 0): Promise<UpdateItem[]> => {
    const params = new URLSearchParams({ limit: limit.toString(), offset: offset.toString() });
    if (category && category !== 'All') {
      params.append('category', category);
    }
    const { data } = await api.get(`/api/v1/updates?${params.toString()}`);
    return data;
  },

  getUnreadCount: async (): Promise<number> => {
    const { data } = await api.get('/api/v1/updates/unread-count');
    return data.unread_count;
  },

  markAsRead: async (id: number): Promise<void> => {
    await api.post(`/api/v1/updates/${id}/read`);
  },

  markAllAsRead: async (): Promise<void> => {
    await api.post('/api/v1/updates/mark-all-read');
  },
};
