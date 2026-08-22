import { useCallback, useEffect, useState } from "react";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import type { GamificationProfile, StartupState } from "../services/api/types";

export type { GamificationProfile, StartupState };

export function useGamification() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<GamificationProfile | null>(null);
  const [startup, setStartup] = useState<StartupState | null>(null);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(async () => {
    if (!user) {
      setProfile(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      const data = await api.gamification.getProfile().catch(() => null);
      setProfile(data || null);
      const startupData = await api.gamification
        .getStartupState()
        .catch(() => null);
      if (startupData)
        setStartup({
          level: startupData.level,
          xp: startupData.xp,
          streak: startupData.streak,
          streak_freezes: startupData.streak_freezes,
          streak_protected: startupData.streak_protected,
          streak_protect_message: startupData.streak_protect_message || "",
          tier: startupData.league?.tier,
          rank: startupData.league?.rank,
          of: startupData.league?.of,
          weekly_xp: startupData.league?.weekly_xp,
          promoted_next_week: startupData.league?.promoted_next_week,
          relegated_next_week: startupData.league?.relegated_next_week,
        });
    } catch {
      setProfile(null);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    let active = true;
    refetch().then(() => {
      if (!active) return;
    });
    const onXp = () => {
      if (active) refetch();
    };
    window.addEventListener("xp-gained", onXp);
    window.addEventListener("celebrate", onXp);
    return () => {
      active = false;
      window.removeEventListener("xp-gained", onXp);
      window.removeEventListener("celebrate", onXp);
    };
  }, [refetch]);

  return { profile, startup, loading, refetch };
}
