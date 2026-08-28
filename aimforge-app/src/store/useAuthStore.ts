import { create } from 'zustand';
import { api } from '@/services/api'; // Or standard axios if api is not exported

export interface User {
  id: number;
  email: string;
  username?: string;
  profile_image?: string;
  gaming_id?: string;
  auth_provider: string;
  created_at: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (credentials: any) => Promise<void>;
  signup: (data: any) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  login: async (credentials) => {
    try {
      set({ isLoading: true, error: null });
      const response = await api.post('/auth/login', credentials);
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch (err: any) {
      let errorMessage = 'Unable to sign in. Please try again.';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response?.status >= 500) {
        errorMessage = 'Service temporarily unavailable. Please try again later.';
      } else if (err.request && !err.response) {
        errorMessage = 'Network error. Please check your connection and try again.';
      }
      set({ isLoading: false, error: errorMessage });
      throw err;
    }
  },

  signup: async (data) => {
    try {
      set({ isLoading: true, error: null });
      const response = await api.post('/auth/signup', data);
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch (err: any) {
      let errorMessage = 'Unable to sign up. Please try again.';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response?.status >= 500) {
        errorMessage = 'Service temporarily unavailable. Please try again later.';
      } else if (err.request && !err.response) {
        errorMessage = 'Network error. Please check your connection and try again.';
      }
      set({ isLoading: false, error: errorMessage });
      throw err;
    }
  },

  logout: async () => {
    try {
      set({ isLoading: true });
      await api.post('/auth/logout');
    } catch (err) {
      console.error('Logout failed:', err);
    } finally {
      set({ user: null, isAuthenticated: false, isLoading: false, error: null });
    }
  },

  checkAuth: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await api.get('/auth/me');
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch (err) {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
