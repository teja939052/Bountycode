import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";
import type { GamificationProfile, StreakStatus } from "../services/api/types";

export type { GamificationProfile, StreakStatus };

export interface QuestionStats {
  easy?: number;
  medium?: number;
  hard?: number;
  total_solved?: number;
  [key: string]: unknown;
}

export interface RecentProblem {
  question_id?: string;
  title?: string;
  completed_at?: string;
  timestamp?: string;
  score?: number;
  [key: string]: unknown;
}

export interface ReadinessScore {
  score?: number;
  next_milestone?: string;
  [key: string]: unknown;
}

export interface DailyChallenge {
  id?: string;
  title?: string;
  question_title?: string;
  description?: string;
  question?: string;
  [key: string]: unknown;
}

export interface DailyBonusResult {
  claimed?: boolean;
  xp_bonus?: number;
  [key: string]: unknown;
}

const GAMIFICATION_PROFILE_KEY = [
  "dashboard",
  "gamification",
  "profile",
] as const;
const QUESTION_STATS_KEY = ["dashboard", "questions", "stats"] as const;
const RECENT_PROBLEMS_KEY = ["dashboard", "questions", "recent"] as const;
const READINESS_SCORE_KEY = ["dashboard", "gamification", "readiness"] as const;
const DAILY_CHALLENGE_KEY = ["dashboard", "questions", "daily"] as const;
const STREAK_STATUS_KEY = [
  "dashboard",
  "gamification",
  "streak-status",
] as const;

export function useDashboard() {
  const queryClient = useQueryClient();

  const gamification = useQuery<GamificationProfile | null>({
    queryKey: GAMIFICATION_PROFILE_KEY,
    queryFn: () => api.gamification.getProfile().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const questionStats = useQuery<QuestionStats | null>({
    queryKey: QUESTION_STATS_KEY,
    queryFn: () => api.questions.getStats().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const recentProblems = useQuery<{ recent: RecentProblem[] }>({
    queryKey: RECENT_PROBLEMS_KEY,
    queryFn: () => api.questions.getRecent(10).catch(() => ({ recent: [] })),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const readinessScore = useQuery<ReadinessScore | null>({
    queryKey: READINESS_SCORE_KEY,
    queryFn: () => api.gamification.getReadinessScore().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const dailyChallenge = useQuery<{ question: DailyChallenge | null } | null>({
    queryKey: DAILY_CHALLENGE_KEY,
    queryFn: () =>
      api.questions
        .getRandom({ exclude_solved: true, type: "daily" })
        .catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const streakStatus = useQuery<StreakStatus>({
    queryKey: STREAK_STATUS_KEY,
    queryFn: () => api.gamification.getStreakStatus(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const claimBonus = useMutation<DailyBonusResult, Error, void>({
    mutationFn: () => api.gamification.claimDailyBonus(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STREAK_STATUS_KEY });
    },
  });

  const isLoading =
    gamification.isLoading ||
    questionStats.isLoading ||
    recentProblems.isLoading ||
    readinessScore.isLoading ||
    dailyChallenge.isLoading ||
    streakStatus.isLoading;

  const isError =
    gamification.isError ||
    questionStats.isError ||
    recentProblems.isError ||
    readinessScore.isError ||
    dailyChallenge.isError ||
    streakStatus.isError;

  const refetch = async () => {
    await Promise.all([
      gamification.refetch(),
      questionStats.refetch(),
      recentProblems.refetch(),
      readinessScore.refetch(),
      dailyChallenge.refetch(),
      streakStatus.refetch(),
    ]);
  };

  return {
    gamification: gamification.data ?? null,
    questionStats: questionStats.data ?? null,
    recentProblems: recentProblems.data?.recent ?? [],
    readinessScore: readinessScore.data ?? null,
    dailyChallenge: dailyChallenge.data?.question ?? null,
    streakStatus: streakStatus.data ?? null,
    dailyBonus: null as DailyBonusResult | null,
    claimBonus,
    isLoading,
    isError,
    refetch,
  };
}
