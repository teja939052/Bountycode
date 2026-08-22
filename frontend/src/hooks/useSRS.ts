import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface SRSCard {
  concept_id?: string;
  concept?: string;
  topic?: string;
  ease_factor?: number;
  interval_days?: number;
  next_review?: string;
  last_review?: string;
  repetitions?: number;
  [key: string]: unknown;
}

export interface SRSStats {
  total_concepts?: number;
  due_today?: number;
  mastered?: number;
  learning?: number;
  new_count?: number;
  [key: string]: unknown;
}

export interface ReviewResult {
  concept_id?: string;
  next_review?: string;
  ease_factor?: number;
  interval_days?: number;
  [key: string]: unknown;
}

const SRS_DUE_KEY = ["srs", "due"] as const;
const SRS_STATS_KEY = ["srs", "stats"] as const;

export function useSRSDue(limit = 20) {
  return useQuery<SRSCard[]>({
    queryKey: [...SRS_DUE_KEY, limit] as const,
    queryFn: () => api.getDueSRSCards(limit),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useSRSStats() {
  return useQuery<SRSStats>({
    queryKey: SRS_STATS_KEY,
    queryFn: () => api.getSRSStats(),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useRecordReview() {
  const qc = useQueryClient();
  return useMutation<ReviewResult, Error, { conceptId: string; grade: number }>({
    mutationFn: ({ conceptId, grade }) => api.reviewSRSConcept(conceptId, grade),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["srs"] });
    },
  });
}
