// @ts-nocheck
import { create } from "zustand";
import { authApi } from "../services/api/auth.ts";
import { ensureAuth } from "../services/api/request.ts";
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
    let lastError: unknown;
    for (let attempt = 0; attempt <= 2; attempt++) {
      try {
        const user = await authApi.getMe();
        set({ user: user as AuthUser, loading: false });
        return;
      } catch (err) {
        lastError = err;
        const msg = (err as Error).message || "";
        const isAuthError = msg.includes("Session expired") || msg.includes("401") || msg.includes("Unauthorized");
        if (isAuthError) {
          try {
            await useAuthStore.getState().refreshToken();
            const user = await authApi.getMe();
            set({ user: user as AuthUser, loading: false });
            return;
          } catch {
            set({ user: null, loading: false });
            return;
          }
        }
        if (attempt < 2) {
          await new Promise((r) => setTimeout(r, 500 * Math.pow(2, attempt)));
        }
      }
    }
    set({ user: null, loading: false });
  },

  refreshToken: async () => {
    try {
      await ensureAuth();
    } catch {
      set({ user: null, loading: false });
      throw new Error("Session expired");
    }
  },
}));

export default useAuthStore;
