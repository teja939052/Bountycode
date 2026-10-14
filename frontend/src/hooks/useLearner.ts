// @ts-nocheck
import { useQuery } from "@tanstack/react-query";
import api from "../services/api";

const LEARNER_STATE_KEY = ["learner", "state"] as const;

export function useLearnerState() {
  return useQuery({
    queryKey: LEARNER_STATE_KEY,
    queryFn: () => api.learner.getState(),
    staleTime: 30_000,
    refetchOnWindowFocus: false,
  });
}
