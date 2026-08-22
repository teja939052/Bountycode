import { useQuery } from "@tanstack/react-query";
import api from "../services/api";

export interface ReadinessData {
  score?: number;
  breakdown?: Record<string, number>;
  next_milestone?: string;
  recommendations?: string[];
  [key: string]: unknown;
}

export interface CompanyReadinessData {
  company?: string;
  score?: number;
  category_scores?: Record<string, number>;
  tips?: string[];
  [key: string]: unknown;
}

const READINESS_KEY = ["readiness", "score"] as const;

export function useReadinessScore() {
  return useQuery<ReadinessData>({
    queryKey: READINESS_KEY,
    queryFn: () => api.adaptive.getReadinessScore(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useCompanyReadiness(company: string) {
  return useQuery<CompanyReadinessData>({
    queryKey: ["readiness", "company", company] as const,
    queryFn: () => api.readiness.getCompanyReadiness(company),
    enabled: !!company,
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}
