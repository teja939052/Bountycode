import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const JOURNEY_KEY = ["journey", "state"] as const;

export interface JourneyLevel {
  id: string;
  title: string;
  icon: string;
  kind: "level" | "boss";
  order: number;
  concept: string;
  canonical_skill: string;
  status: "completed" | "current" | "unlocked" | "locked";
  mastery: number;
  attempts: number;
  xp: number;
}

export interface JourneyTown {
  id: string;
  title: string;
  icon: string;
  order: number;
  levels: JourneyLevel[];
}

export interface JourneyWorld {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  order: number;
  theme: string;
  status: "completed" | "active" | "locked";
  towns: JourneyTown[];
}

export interface CharacterPosition {
  world_id: string;
  town_id: string;
  level_id: string;
}

export interface JourneyCharacter {
  level: number;
  title: string;
  title_emoji: string;
  position: CharacterPosition | null;
  state: "idle" | "walking" | "discovering" | "thinking" | "correct" | "struggling" | "boss" | "mastery";
}

export interface JourneyStats {
  xp: number;
  level: number;
  coins: number;
  streak: number;
  badges_count: number;
}

export interface JourneyState {
  character: JourneyCharacter;
  worlds: JourneyWorld[];
  today: Record<string, unknown> | null;
  stats: JourneyStats;
}

export function useJourneyState() {
  return useQuery<JourneyState>({
    queryKey: JOURNEY_KEY,
    queryFn: () => api.journey.getState(),
    retry: 1,
    staleTime: 30_000,
    refetchOnWindowFocus: false,
  });
}

export function useRecordActivity() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: Record<string, unknown>) => api.journey.recordActivity(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: JOURNEY_KEY });
    },
  });
}

export function refreshJourneyState() {
  const queryClient = useQueryClient();
  void queryClient.invalidateQueries({ queryKey: JOURNEY_KEY });
}
