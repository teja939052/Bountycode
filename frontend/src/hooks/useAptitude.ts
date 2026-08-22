import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface AptitudeQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
}

export interface AptitudeTestResult {
  score: number;
  total_questions: number;
  correct: number;
  incorrect: number;
  by_section: Record<string, number>;
  feedback: string;
}

export function useAptitudeStats() {
  return useQuery({
    queryKey: ["aptitude", "stats"],
    queryFn: () => api.aptitude.getStats(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useAptitudeStart(testType: string) {
  const queryClient = useQueryClient();

  return useMutation<{ test_id: string }, Error, { test_type: string }>({
    mutationFn: ({ test_type }) => api.aptitude.start(test_type),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}

export function useAptitudeSubmit(questionId: string) {
  const queryClient = useQueryClient();

  return useMutation<{
    correct: boolean;
    explanation: string;
  }, Error, { answer: string; time_taken?: number }>({
    mutationFn: (params) =>
      api.aptitude.submit(questionId, params.answer, params.time_taken),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}

export function useAptitudeComplete(testId: string) {
  const queryClient = useQueryClient();

  return useMutation<AptitudeTestResult, Error, { test_id: string }>({
    mutationFn: ({ test_id }) => api.aptitude.complete(test_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}