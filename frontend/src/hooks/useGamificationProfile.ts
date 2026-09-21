import { useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";

/** Canonical gamification query keys. Every gamified surface reads these. */
export const gamificationKeys = {
  profile: ["gamification", "profile"] as const,
  leaderboard: (timeframe: string, scope: string) =>
    ["gamification", "leaderboard", timeframe, scope] as const,
  map: ["map", "state"] as const,
};

/**
 * THE profile hook. Auth owns identity; this owns diamonds/level/streak/rank.
 * Listens for reward events so completions anywhere refresh every
 * subscriber (Tower, Dashboard, VoyagePath, DiamondsPopup) from one source.
 */
export function useGamificationProfile() {
  const qc = useQueryClient();
  const q = useQuery({
    queryKey: gamificationKeys.profile,
    queryFn: () => api.gamification.getProfile(),
    staleTime: 15_000,
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const onReward = () => {
      void qc.invalidateQueries({ queryKey: gamificationKeys.profile });
      void qc.invalidateQueries({ queryKey: gamificationKeys.map });
    };
    window.addEventListener("diamonds-gained", onReward);
    window.addEventListener("practice-recorded", onReward);
    window.addEventListener("streak-updated", onReward);
    return () => {
      window.removeEventListener("diamonds-gained", onReward);
      window.removeEventListener("practice-recorded", onReward);
      window.removeEventListener("streak-updated", onReward);
    };
  }, [qc]);

  return q;
}
