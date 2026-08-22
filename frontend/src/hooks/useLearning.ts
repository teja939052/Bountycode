import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const LANGUAGES_KEY = ["learning", "languages"] as const;
const LEADERBOARD_KEY = ["learning", "leaderboard"] as const;
const MODULES_KEY = ["learning-modules", "list"] as const;
const MODULE_PROGRESS_KEY = ["learning-modules", "progress"] as const;

export function moduleKey(moduleId: string) {
  return ["learning-modules", "detail", moduleId] as const;
}

export function moduleRecommendationsKey(company: string | null) {
  return ["learning-modules", "recommendations", company || "all"] as const;
}

export function useLearning() {
  const languages = useQuery({
    queryKey: LANGUAGES_KEY,
    queryFn: () => api.get("/api/v1/learning/languages").catch(() => null),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });

  const leaderboard = useQuery({
    queryKey: LEADERBOARD_KEY,
    queryFn: () => api.get("/api/v1/learning/leaderboard").catch(() => null),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });

  const isLoading = languages.isLoading;

  const refetch = async () => {
    await Promise.all([languages.refetch(), leaderboard.refetch()]);
  };

  return {
    data: languages.data ?? null,
    leaderboard: leaderboard.data?.leaderboard ?? null,
    isLoading,
    isError: languages.isError,
    refetch,
  };
}

export function useLearningModules(params: Record<string, any> = {}) {
  return useQuery({
    queryKey: [...MODULES_KEY, params] as const,
    queryFn: () => api.learningModules.list(params),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });
}

export function useLearningModule(moduleId: string | null) {
  return useQuery({
    queryKey: moduleKey(moduleId || ""),
    queryFn: () => api.learningModules.get(moduleId),
    enabled: Boolean(moduleId),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });
}

export function useLearningProgress() {
  return useQuery({
    queryKey: MODULE_PROGRESS_KEY,
    queryFn: () => api.learningModules.getProgress(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useLearningRecommendations(company: string | null = null) {
  return useQuery({
    queryKey: moduleRecommendationsKey(company),
    queryFn: () => (api as any).learningModules.getRecommendations(company),
    retry: 1,
    staleTime: 120_000,
    refetchOnWindowFocus: false,
  });
}

export function useStartModule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (moduleId: string) => api.learningModules.start(moduleId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MODULE_PROGRESS_KEY });
    },
  });
}

export function useCompleteStep() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ moduleId, stepNumber }: { moduleId: string; stepNumber: number }) =>
      api.learningModules.completeStep(moduleId, stepNumber),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MODULE_PROGRESS_KEY });
    },
  });
}
