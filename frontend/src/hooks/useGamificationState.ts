import { useCallback, useMemo, useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { requestWithRetry as request } from "../services/api/request.ts";
import type { GamificationProfile, StartupState } from "../services/api/types";

const PROFILE_KEY = ["gamification", "profile"] as const;
const STARTUP_KEY = ["gamification", "startup"] as const;

export type { GamificationProfile, StartupState };

function computeLevel(diamonds: number): number {
  if (diamonds <= 0) return 1;
  return Math.max(1, Math.min(100, Math.floor(Math.sqrt(diamonds / 50)) + 1));
}

export function useGamificationState() {
  const queryClient = useQueryClient();

  const profileQuery = useQuery<GamificationProfile | null>({
    queryKey: PROFILE_KEY,
    queryFn: () => request<GamificationProfile>("/api/v1/gamification/profile").catch(() => null),
    staleTime: 60_000,
    refetchOnWindowFocus: true,
  });

  const startupQuery = useQuery<StartupState | null>({
    queryKey: STARTUP_KEY,
    queryFn: () => request<StartupState>("/api/v1/gamification/startup").catch(() => null),
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const profile = profileQuery.data ?? null;
  const startup = startupQuery.data ?? null;

  const optimisticPreview = useMemo(() => {
    if (!profile) return null;
    return {
      diamonds: profile.diamonds ?? 0,
      level: profile.level ?? computeLevel(profile.diamonds ?? 0),
      streak: profile.streak ?? 0,
      coins: profile.coins ?? 0,
      stars: profile.stars_total ?? 0,
      combo: profile.current_combo ?? 0,
    };
  }, [profile]);

  const recordActivity = useMutation({
    mutationFn: async (params: {
      activityType: string;
      score?: number;
      category?: string | null;
      skill?: string | null;
      metadata?: Record<string, unknown> | null;
    }) => {
      const qs = new URLSearchParams({
        activity_type: params.activityType,
        score: String(params.score ?? 0),
      });
      if (params.category) qs.append("category", params.category);
      if (params.skill) qs.append("skill", params.skill);
      const opts: Record<string, unknown> = { method: "POST" };
      if (params.metadata) opts.body = JSON.stringify(params.metadata);
      return request<{
        xp_earned: number;
        leveled_up?: boolean;
        new_level?: number;
        coins_earned?: number;
        stars_earned?: number;
        new_streak?: number;
        combo?: { current: number; max: number; multiplier: number };
        critical_hit?: boolean;
        critical_bonus?: number;
        streak_multiplier?: number;
        streak_frozen?: boolean;
        streak_freezes_remaining?: number;
        daily_goal_count?: number;
        daily_goal_target?: number;
        milestone?: Record<string, unknown>;
        boss_level?: number | null;
        base_xp?: number;
        multipliers?: {
          streak: number;
          combo: number;
          first_of_day: boolean;
          critical: number;
          double_xp: boolean;
        };
      }>(`/api/v1/gamification/record?${qs.toString()}`, opts);
    },
    onMutate: async (params) => {
      await queryClient.cancelQueries({ queryKey: PROFILE_KEY });
      const previous = queryClient.getQueryData<GamificationProfile | null>(PROFILE_KEY);

      if (previous) {
        const previewXP = (previous.diamonds ?? 0) + Math.max(0, params.score ?? 0);
        const next: GamificationProfile = {
          ...previous,
          diamonds: previewXP,
          level: previous.level ?? computeLevel(previewXP),
        };
        queryClient.setQueryData(PROFILE_KEY, next);
      }

      return { previous };
    },
    onError: (_err, _params, ctx) => {
      if (ctx?.previous) {
        queryClient.setQueryData(PROFILE_KEY, ctx.previous);
      }
    },
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: PROFILE_KEY });
      queryClient.invalidateQueries({ queryKey: STARTUP_KEY });
      if (result?.xp_earned) {
        window.dispatchEvent(
          new CustomEvent("juice:diamonds", {
            detail: {
              amount: result.xp_earned,
              leveledUp: result.leveled_up,
              newLevel: result.new_level,
              coins: result.coins_earned,
              stars: result.stars_earned,
              streak: result.new_streak,
              combo: result.combo,
              critical: result.critical_hit,
              criticalBonus: result.critical_bonus,
              streakMultiplier: result.streak_multiplier,
              streakFrozen: result.streak_frozen,
              freezesRemaining: result.streak_freezes_remaining,
              dailyGoal: result.daily_goal_count != null && result.daily_goal_target != null
                ? { count: result.daily_goal_count, target: result.daily_goal_target }
                : undefined,
              milestone: result.milestone,
              bossLevel: result.boss_level,
              baseXP: result.base_xp,
              multipliers: result.multipliers,
            },
          })
        );
      }
      if (result?.leveled_up) {
        window.dispatchEvent(
          new CustomEvent("juice:levelup", {
            detail: { newLevel: result.new_level },
          })
        );
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: PROFILE_KEY });
      queryClient.invalidateQueries({ queryKey: STARTUP_KEY });
    },
  });

  const refetch = useCallback(async () => {
    await Promise.all([profileQuery.refetch(), startupQuery.refetch()]);
  }, [profileQuery.refetch, startupQuery.refetch]);

  // Bridge: keep window events as juice-only, but also apply a lightweight
  // optimistic cache bump so bars move even if a caller still uses the raw API.
  useEffect(() => {
    const onXp = (event: Event) => {
      const detail = (event as CustomEvent<{ amount?: number }>).detail;
      const amount = detail?.amount;
      if (!amount || !queryClient) return;
      queryClient.setQueryData(PROFILE_KEY, (old: GamificationProfile | null | undefined) => {
        if (!old) return old;
        const currentXP = Number(old.diamonds ?? 0);
        return { ...old, diamonds: currentXP + amount };
      });
    };
    window.addEventListener("juice:diamonds", onXp as EventListener);
    return () => window.removeEventListener("juice:diamonds", onXp as EventListener);
  }, [queryClient]);

  return {
    profile,
    startup,
    optimisticPreview,
    isLoading: profileQuery.isLoading && startupQuery.isLoading,
    isError: profileQuery.isError || startupQuery.isError,
    refetch,
    recordActivity,
  };
}
