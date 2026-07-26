import { create } from "zustand";
import api from "../services/api";

const useAuthStore = create((set) => ({
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
      set({ user, loading: false });
    } catch {
      set({ user: null, loading: false });
    }
  },
}));

export default useAuthStore;
