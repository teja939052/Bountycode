import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const GUIDE_KEY = ["learning-guide", "state"] as const;

export function useLearningGuide(userId: string) {
  const { data: state, refetch } = useQuery({
    queryKey: [...GUIDE_KEY, userId],
    queryFn: () => api.get(`/api/v1/learning-guide/state/${userId}`).catch(() => null),
    staleTime: 30_000,
    refetchOnWindowFocus: true,
  });

  const advanceToLearning = (useMutation as any)({
    mutationFn: () => (api as any).post(`/api/v1/learning-guide/welcome/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const advanceToPractice = (useMutation as any)({
    mutationFn: () => (api as any).post(`/api/v1/learning-guide/practice/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const advanceToQuiz = (useMutation as any)({
    mutationFn: () => (api as any).post(`/api/v1/learning-guide/quiz/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const markComplete = (useMutation as any)({
    mutationFn: (moduleId: string) =>
      (api as any).post(`/api/v1/learning-guide/complete/${userId}?moduleId=${moduleId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const claimBounty = (useMutation as any)({
    mutationFn: (bountyId: string) =>
      (api as any).post(`/api/v1/learning-guide/bounty/${userId}/${bountyId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const updateStreak = (useMutation as any)({
    mutationFn: () => (api as any).post(`/api/v1/learning-guide/streak/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const awardXP = (useMutation as any)({
    mutationFn: (amount: number) => (api as any).post(`/api/v1/learning-guide/xp/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  return {
    state,
    advanceToLearning,
    advanceToPractice,
    advanceToQuiz,
    markComplete,
    claimBounty,
    updateStreak,
    awardXP,
    refetch,
  };
}