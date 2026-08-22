import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";
import type {
  InterviewResult,
  InterviewHistoryItem,
} from "../services/api/types";

export type { InterviewResult, InterviewHistoryItem };

export interface StartInterviewResponse {
  interview_id: string;
  question: string;
  tips?: string;
  difficulty?: string;
  company?: string;
  company_style?: string;
  question_type?: string;
  total_questions?: number;
  [key: string]: unknown;
}

export interface SubmitAnswerResponse {
  feedback?: {
    score?: number;
    strengths?: string[];
    improvements?: string[];
    better_answer?: string;
    reaction?: string;
    breakdown?: Record<string, number>;
  };
  current_score: number;
  next_question?: string;
  next_tips?: string;
  next_difficulty?: string;
  next_question_type?: string;
  is_follow_up?: boolean;
  finished?: boolean;
  questions_answered?: number;
  xp_gained?: number;
  level?: number;
  streak?: number;
  new_badges?: string[];
  reaction?: string;
  [key: string]: unknown;
}

const INTERVIEW_RESULT_KEY = (id: string) =>
  ["interview", "result", id] as const;
const INTERVIEW_HISTORY_KEY = ["interview", "history"] as const;

export function useInterviewResult(
  interviewId: string | undefined,
  enabled = true,
) {
  return useQuery<InterviewResult>({
    queryKey: INTERVIEW_RESULT_KEY(interviewId ?? ""),
    queryFn: () => api.interview.getInterviewResult(interviewId!),
    enabled: !!interviewId && enabled,
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useInterviewHistory() {
  return useQuery<InterviewHistoryItem[]>({
    queryKey: INTERVIEW_HISTORY_KEY,
    queryFn: () => api.interview.getInterviewHistory(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useStartInterview() {
  return useMutation<
    StartInterviewResponse,
    Error,
    {
      jobRole: string;
      company?: string;
      interviewType?: string;
      difficulty?: string;
    }
  >({
    mutationFn: ({ jobRole, company, interviewType, difficulty }) =>
      api.interview.startInterviewV2(
        jobRole,
        company ?? "general",
        interviewType ?? "mixed",
        difficulty ?? "medium",
      ),
  });
}

export function useSubmitAnswer() {
  const queryClient = useQueryClient();

  return useMutation<
    SubmitAnswerResponse,
    Error,
    {
      interviewId: string;
      question: string;
      answer: string;
      timeTaken?: number;
      isFollowUp?: boolean;
      questionType?: string;
    }
  >({
    mutationFn: ({
      interviewId,
      question,
      answer,
      timeTaken,
      isFollowUp,
      questionType,
    }) =>
      api.post("/api/v1/interview/answer", {
        interview_id: interviewId,
        question,
        answer,
        time_taken: timeTaken,
        is_follow_up: isFollowUp,
        question_type: questionType,
      }),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["interview", "result", variables.interviewId],
      });
    },
  });
}
