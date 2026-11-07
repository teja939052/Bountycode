/**
 * UI-ONLY token store.
 *
 * ⚠️  The backend enforces all paywall/limits via `_check_question_quota()`
 *     in `app/routes/questions.py` and `questions_solve.py`. This store
 *     exists solely for frontend display (progress bars, remaining counts).
 *     A user modifying localStorage will NOT bypass the backend; the next
 *     API call to /submit or /answer returns HTTP 402 if the true quota
 *     is exhausted.
 *
 * Sync on login:  syncUserFromAuth(authUser)
 * Refresh after submit:  decrementProblem()
 * Auto-reset on new day: handled by backend's _check_question_quota
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AuthUser } from "../services/api/types";

export interface TokenState {
  remainingDailyProblems: number;
  isPro: boolean;
  lastSync: number | null;
  setUsage: (remaining: number, isPro: boolean) => void;
  decrementProblem: () => void;
  resetDaily: () => void;
}

export const useTokenStore = create<TokenState>()(
  persist(
    (set) => ({
      remainingDailyProblems: 3,
      isPro: false,
      lastSync: null,

      setUsage: (remaining, isPro) =>
        set({
          remainingDailyProblems: remaining,
          isPro,
          lastSync: Date.now(),
        }),

      decrementProblem: () =>
        set((state) => ({
          remainingDailyProblems: state.isPro
            ? state.remainingDailyProblems
            : Math.max(0, state.remainingDailyProblems - 1),
          lastSync: Date.now(),
        })),

      resetDaily: () =>
        set({ remainingDailyProblems: 3, lastSync: Date.now() }),
    }),
    { name: "bountycard-tokens" },
  ),
);

export function syncUserFromAuth(user: AuthUser | null) {
  useTokenStore.getState().setUsage(
    user?.plan === "free" ? (user?.usage?.question_bank_used ? 3 - user.usage.question_bank_used : 3) : -1,
    user?.plan === "pro" || user?.plan === "lifetime",
  );
}
