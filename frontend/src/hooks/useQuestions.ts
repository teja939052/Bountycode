import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface QuestionFilters {
  companies: string[];
  roles: string[];
  topics: string[];
  sub_topics: string[];
  types: string[];
  difficulties: string[];
  patterns: string[];
  sources: string[];
}

export interface QuestionItem {
  id: string;
  question?: string;
  question_title?: string;
  difficulty?: string;
  topic?: string;
  sub_topic?: string;
  company?: string | string[];
  type?: string;
  upvotes?: number;
  acceptance_rate?: number;
  [key: string]: unknown;
}

export interface BrowseResult {
  questions: QuestionItem[];
  total: number;
  pages: number;
}

export interface QuestionStats {
  total_solved?: number;
  easy_solved?: number;
  medium_solved?: number;
  hard_solved?: number;
  expert_solved?: number;
  acceptance_rate?: number;
  by_difficulty?: {
    easy: number;
    medium: number;
    hard: number;
    expert: number;
  };
  [key: string]: unknown;
}

export interface DailyChallengeData {
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

const QUESTIONS_FILTERS_KEY = ["questions", "filters"] as const;
const QUESTIONS_STATS_KEY = ["questions", "stats"] as const;
const QUESTIONS_DAILY_KEY = ["questions", "daily"] as const;

export function useQuestionFilters() {
  return useQuery<QuestionFilters>({
    queryKey: QUESTIONS_FILTERS_KEY,
    queryFn: () => api.questions.getFilters(),
    retry: 1,
    staleTime: 5 * 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useQuestionStats() {
  return useQuery<QuestionStats>({
    queryKey: QUESTIONS_STATS_KEY,
    queryFn: () => api.questions.getStats(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useBrowseQuestions(
  params: Record<string, unknown> = {},
  page = 1,
  limit = 80,
) {
  const cleanParams: Record<string, unknown> = { ...params, page, limit };
  Object.keys(cleanParams).forEach((k) => {
    if (!cleanParams[k]) delete cleanParams[k];
  });

  return useQuery<BrowseResult>({
    queryKey: ["questions", "browse", cleanParams] as const,
    queryFn: () => api.questions.browse(cleanParams),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useSolvedStatus(questionIds: string[]) {
  return useQuery<Record<string, boolean>>({
    queryKey: ["questions", "solved-batch", questionIds.sort()],
    queryFn: async () => {
      const results = await Promise.all(
        questionIds.map((id) => api.questions.isSolved(id).catch(() => ({ solved: false }))),
      );
      const map: Record<string, boolean> = {};
      questionIds.forEach((id, i) => {
        map[id] = results[i]?.solved || false;
      });
      return map;
    },
    enabled: questionIds.length > 0,
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useDailyChallenge() {
  return useQuery<DailyChallengeData | null>({
    queryKey: QUESTIONS_DAILY_KEY,
    queryFn: () => api.getDailyChallenge().catch(() => null),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useRandomQuestion() {
  const queryClient = useQueryClient();

  return useMutation<QuestionItem | null, Error, Record<string, string>>({
    mutationFn: (params) => api.questions.getRandom(params),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUESTIONS_STATS_KEY });
    },
  });
}

export function useUpvoteQuestion() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, { questionId: string; vote?: number }>({
    mutationFn: ({ questionId, vote }) => api.questions.upvote(questionId, vote ?? 1),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["questions", "browse"] });
    },
  });
}
