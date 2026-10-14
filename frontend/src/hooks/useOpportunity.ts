// @ts-nocheck
import { useQuery } from "@tanstack/react-query";
import api from "../services/api";

export function useOpportunityGraph(companyId: string | null, variant?: string) {
  return useQuery({
    queryKey: ["opportunity", companyId, variant],
    queryFn: () => api.opportunity.getOpportunity(companyId!, variant),
    enabled: Boolean(companyId),
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useOpportunityFit(companyId: string | null, variant?: string) {
  return useQuery({
    queryKey: ["opportunity", "fit", companyId, variant],
    queryFn: () => api.opportunity.getOpportunityFit(companyId!, variant),
    enabled: Boolean(companyId),
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useCapabilityGaps(companyId: string | null, variant?: string) {
  return useQuery({
    queryKey: ["opportunity", "gaps", companyId, variant],
    queryFn: () => api.opportunity.getCapabilityGaps(companyId!, variant),
    enabled: Boolean(companyId),
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}

export function useAdaptivePlan(companyId: string | null, variant?: string) {
  return useQuery({
    queryKey: ["opportunity", "plan", companyId, variant],
    queryFn: () => api.opportunity.getAdaptivePlan(companyId!, variant),
    enabled: Boolean(companyId),
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
}
