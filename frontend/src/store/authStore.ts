import { create } from "zustand";
import { authApi } from "../services/api/auth.ts";
import { themesApi } from "../services/api/themes.ts";
import { useThemeStore } from "../store/themeStore";
import type { ThemeMode } from "../store/themeStore";
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
      try {
        const themeRes = await themesApi.current();
        useThemeStore.getState().setMode(themeRes.theme as ThemeMode);
      } catch {
        // anonymous / not logged in — ignore
      }
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
      const res = await fetch("/api/v1/auth/refresh", {
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
