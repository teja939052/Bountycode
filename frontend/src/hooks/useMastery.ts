import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface MasteryNode {
  category: string;
  total?: number;
  solved?: number;
  mastery_pct?: number;
  [key: string]: unknown;
}

export interface MasteryGraph {
  nodes?: MasteryNode[];
  overall_mastery?: number;
  [key: string]: unknown;
}

export interface WeakArea {
  category: string;
  accuracy?: number;
  attempts?: number;
  [key: string]: unknown;
}

export interface RecordActivityResult {
  xp_gained?: number;
  level?: number;
  new_badges?: string[];
  [key: string]: unknown;
}

const MASTERY_GRAPH_KEY = ["mastery", "graph"] as const;
const WEAK_AREAS_KEY = ["mastery", "weak"] as const;

export function useMasteryGraph() {
  return useQuery<MasteryGraph>({
    queryKey: MASTERY_GRAPH_KEY,
    queryFn: () => api.gamification.getSkillGraph(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useWeakAreas() {
  return useQuery<WeakArea[]>({
    queryKey: WEAK_AREAS_KEY,
    queryFn: () => api.gamification.getWeakAreas(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useRecordSolve() {
  const qc = useQueryClient();
  return useMutation<RecordActivityResult, Error, Record<string, unknown>>({
    mutationFn: (data) => api.adaptive.recordActivity(data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["mastery"] });
      qc.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
