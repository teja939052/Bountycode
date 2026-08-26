import { create } from "zustand";
import { authApi } from "../services/api/auth.ts";
import { API_BASE } from "../services/api/request.ts";
import type { AuthUser } from "../services/api/types.ts";

export interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  setAuth: (user: AuthUser) => void;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,

  setAuth: (user) => {
    set({ user, loading: false });
  },

  logout: async () => {
    try {
      await authApi.logout();
    } catch {
      // cookie may already be gone
    }
    set({ user: null, loading: false });
  },

  loadUser: async () => {
    try {
      const user = await authApi.getMe();
      set({ user: user as AuthUser, loading: false });
    } catch (err) {
      if ((err as Error).message === "Session expired") {
        try {
          await useAuthStore.getState().refreshToken();
          const user = await authApi.getMe();
          set({ user: user as AuthUser, loading: false });
          return;
        } catch {
          // refresh failed, continue to logout
        }
      }
      set({ user: null, loading: false });
    }
  },

  refreshToken: async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });
      if (!res.ok) throw new Error("Refresh failed");
    } catch {
      set({ user: null, loading: false });
      throw new Error("Session expired");
    }
  },
}));

export default useAuthStore;
