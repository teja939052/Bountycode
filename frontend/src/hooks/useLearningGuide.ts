// @ts-nocheck
import { useQuery, useMutation } from "@tanstack/react-query";
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
    mutationFn: () => api.post(`/api/v1/learning-guide/welcome/${userId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const advanceToPractice = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/practice/${userId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const advanceToQuiz = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/quiz/${userId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const markComplete = useMutation({
    mutationFn: (moduleId: string) =>
      api.post(`/api/v1/learning-guide/complete/${userId}?moduleId=${moduleId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const claimBounty = useMutation({
    mutationFn: (bountyId: string) =>
      api.post(`/api/v1/learning-guide/bounty/${userId}/${bountyId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const updateStreak = useMutation({
    mutationFn: () => api.post(`/api/v1/learning-guide/streak/${userId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

  const awardXP = useMutation({
    mutationFn: (_amount: number) => api.post(`/api/v1/learning-guide/diamonds/${userId}`, {}),
    onSuccess: () => {
      refetch();
    },
  }, undefined);

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
