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

  const advanceToLearning = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/welcome/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const advanceToPractice = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/practice/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const advanceToQuiz = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/quiz/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const markComplete = useMutation({
    mutationFn: (moduleId: string) =>
      api.post(`/api/v1/learning-guide/complete/${userId}?moduleId=${moduleId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const claimBounty = useMutation({
    mutationFn: (bountyId: string) =>
      api.post(`/api/v1/learning-guide/bounty/${userId}/${bountyId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const updateStreak = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/streak/${userId}`),
    onSuccess: () => {
      refetch();
    },
  });

  const awardXP = useMutation({
    mutationFn: (amount: number) => api.post(`/api/v1/learning-guide/xp/${userId}`),
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