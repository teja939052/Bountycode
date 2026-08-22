import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";
import type {
  TowerData,
  Challenge,
  GamificationProfile,
  LeaderboardEntry,
  SkillNode,
  StreakStatus,
} from "../services/api/types";

const TOWER_KEY = ["gamification", "tower"] as const;
const CHALLENGES_KEY = ["gamification", "challenges"] as const;
const FOREST_KEY = ["gamification", "forest"] as const;
const DAILY_BONUS_KEY = ["gamification", "daily-bonus"] as const;
const PROFILE_KEY = ["gamification", "profile"] as const;
const LEADERBOARD_KEY = ["gamification", "leaderboard"] as const;
const SKILLS_KEY = ["gamification", "skills"] as const;
const WEAK_KEY = ["gamification", "skills", "weak"] as const;
const STREAK_STATUS_KEY = ["gamification", "streak-status"] as const;

export function useGamificationData() {
  const queryClient = useQueryClient();

  const tower = useQuery<TowerData | null>({
    queryKey: TOWER_KEY,
    queryFn: () => api.gamification.getTower().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const challenges = useQuery<{ challenges: Challenge[] } | null>({
    queryKey: CHALLENGES_KEY,
    queryFn: () => api.gamification.getChallenges().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const forest = useQuery<Record<string, unknown> | null>({
    queryKey: FOREST_KEY,
    queryFn: () => api.gamification.getForest().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const dailyBonus = useQuery<Record<string, unknown> | null>({
    queryKey: DAILY_BONUS_KEY,
    queryFn: () => api.gamification.getDailyBonusHistory().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const profile = useQuery<GamificationProfile | null>({
    queryKey: PROFILE_KEY,
    queryFn: () => api.gamification.getProfile().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const leaderboard = useQuery<{ entries: LeaderboardEntry[] } | null>({
    queryKey: LEADERBOARD_KEY,
    queryFn: () => api.gamification.getLeaderboard().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const skills = useQuery<{
    skills: SkillNode[];
    categories?: string[];
  } | null>({
    queryKey: SKILLS_KEY,
    queryFn: () => api.gamification.getSkillGraph().catch(() => null),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });

  const weakAreas = useQuery<SkillNode[]>({
    queryKey: WEAK_KEY,
    queryFn: () => api.gamification.getWeakAreas().catch(() => []),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });

  const streakStatus = useQuery<StreakStatus | null>({
    queryKey: STREAK_STATUS_KEY,
    queryFn: () => api.gamification.getStreakStatus().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const claimBonus = useMutation({
    mutationFn: () => api.gamification.claimDailyBonus(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: DAILY_BONUS_KEY });
      queryClient.invalidateQueries({ queryKey: STREAK_STATUS_KEY });
    },
  });

  const buyPowerUp = useMutation({
    mutationFn: (powerUpId: string) => api.gamification.buyPowerUp(powerUpId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: TOWER_KEY });
    },
  });

  const usePowerUp = useMutation({
    mutationFn: (powerUpId: string) => api.gamification.usePowerUp(powerUpId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: TOWER_KEY });
    },
  });

  const claimChallenge = useMutation({
    mutationFn: ({ type, id }: { type: string; id: string }) =>
      api.gamification.claimChallenge(type, id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CHALLENGES_KEY });
      queryClient.invalidateQueries({ queryKey: TOWER_KEY });
    },
  });

  const isLoading =
    tower.isLoading ||
    challenges.isLoading ||
    forest.isLoading ||
    dailyBonus.isLoading;

  const refetch = async () => {
    await Promise.all([
      tower.refetch(),
      challenges.refetch(),
      forest.refetch(),
      dailyBonus.refetch(),
    ]);
  };

  return {
    tower: tower.data ?? null,
    challenges: challenges.data ?? null,
    forest: forest.data ?? null,
    dailyBonus: dailyBonus.data ?? null,
    profile: profile.data ?? null,
    leaderboard: leaderboard.data ?? null,
    skills: skills.data ?? null,
    weakAreas: weakAreas.data ?? null,
    streakStatus: streakStatus.data ?? null,
    claimBonus,
    buyPowerUp,
    usePowerUp,
    claimChallenge,
    isLoading,
    isError: tower.isError,
    refetch,
  };
}
