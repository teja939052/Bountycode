import { create } from "zustand";
import api from "../services/api";

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  plan?: string;
  usage?: Record<string, any>;
  [key: string]: any;
}

interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  setAuth: (user: AuthUser) => void;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,

  setAuth: (user) => {
    set({ user, loading: false });
  },

  logout: async () => {
    try {
      await api.logout();
    } catch {
      // cookie may already be gone
    }
    set({ user: null, loading: false });
  },

  loadUser: async () => {
    try {
      const user = await api.getMe();
      set({ user: user as AuthUser, loading: false });
    } catch {
      set({ user: null, loading: false });
    }
  },
}));

export default useAuthStore;
