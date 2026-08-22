import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface Quest {
  id?: string;
  title?: string;
  description?: string;
  category?: string;
  difficulty?: string;
  xp_reward?: number;
  completed?: boolean;
  [key: string]: unknown;
}

export interface DailyQuestData {
  id?: string;
  title?: string;
  description?: string;
  quest?: Quest;
  problem?: {
    id?: string;
    question_title?: string;
    question?: string;
    [key: string]: unknown;
  };
  config?: {
    category?: string;
    difficulty?: string;
    focus?: string;
    [key: string]: unknown;
  };
  streak_bonus?: number;
  [key: string]: unknown;
}

export interface QuestProgress {
  completed_today?: number;
  total_today?: number;
  quests?: Quest[];
  [key: string]: unknown;
}

export interface QuestSolveResult {
  xp_gained?: number;
  completed?: boolean;
  next_quest?: Quest;
  [key: string]: unknown;
}

const DAILY_QUEST_KEY = ["quests", "daily"] as const;
const ACTIVE_QUESTS_KEY = ["quests", "active"] as const;

export function useDailyQuests() {
  return useQuery<DailyQuestData | null>({
    queryKey: DAILY_QUEST_KEY,
    queryFn: () => api.getDailyChallenge(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useActiveQuests() {
  return useQuery<QuestProgress>({
    queryKey: ACTIVE_QUESTS_KEY,
    queryFn: () => api.getDailyChallengeProgress(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useRecordQuestSolve() {
  const qc = useQueryClient();
  return useMutation<QuestSolveResult, Error, Record<string, unknown>>({
    mutationFn: (data) => api.submitDailyChallenge(data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["quests"] });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
