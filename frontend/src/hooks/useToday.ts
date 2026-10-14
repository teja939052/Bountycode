// @ts-nocheck
import { useQuery, type QueryClient } from "@tanstack/react-query";
import { api } from "../services/api";
import useAuthStore from "../store/authStore";

export interface TodayMission {
  id: string;
  kind: string;
  concept: string;
  why: string;
  priority: number;
  company?: string;
  role?: string;
  repair_id?: string;
  due_cards?: number;
  weak_area?: {
    category: string;
    category_name?: string;
    skill: string;
    score: number;
    attempts?: number;
  };
  learner_state: Record<string, any>;
}

export interface TodayPayload {
  mission: TodayMission | null;
  readiness: {
    overall: number;
    categories: Record<string, number>;
  };
  weak_areas: Array<{
    category: string;
    category_name?: string;
    skill: string;
    score: number;
    attempts?: number;
  }>;
  gamification: {
    level: number;
    diamonds: number;
    streak: number;
    last_practice_date?: string;
  };
  srs: {
    due_cards: number;
    total_cards: number;
    mastered_concepts: number;
  };
  repair: {
    open_repairs: number;
    recent_repairs: Array<{
      id: string;
      concept?: string;
      status?: string;
      created_at?: string;
    }>;
  };
  evidence: {
    total_events: number;
    recent_event_count: number;
    last_event_at?: string;
  };
}

const TODAY_KEY = ["today", "state"] as const;
const READINESS_KEY = ["today", "readiness"] as const;
const WEAK_AREAS_KEY = ["today", "weak-areas"] as const;

export function useToday() {
  const { user } = useAuthStore();

  const mission = useQuery<TodayMission | null>({
    queryKey: TODAY_KEY,
    queryFn: () =>
      api.learner
        .getNextMission({
          company: user?.target_company,
          role: user?.target_role,
        })
        .then((m: TodayMission) => ({
          ...m,
          kind: m.kind,
          concept: m.concept,
          why: m.why,
          priority: m.priority,
        }))
        .catch(() => null),
    staleTime: 30_000,
    refetchOnWindowFocus: true,
    enabled: !!user,
  });

  const learner = useQuery<TodayPayload | null>({
    queryKey: ["today", "learner"],
    queryFn: () =>
      api.learner.getState().catch(() => null),
    staleTime: 30_000,
    refetchOnWindowFocus: true,
    enabled: !!user,
  });

  const readiness = useQuery<{
    overall: number;
    categories: Record<string, number>;
  } | null>({
    queryKey: READINESS_KEY,
    queryFn: () =>
      api.gamification
        .getCompanyReadinessBreakdown(user?.target_company)
        .then((r: any) => ({
          overall: Number(r?.overall_readiness ?? r?.overall ?? 0),
          categories: r?.domain_scores ?? r?.categories ?? {},
        }))
        .catch(() => null),
    staleTime: 60_000,
    refetchOnWindowFocus: true,
    enabled: !!user,
  });

  const weakAreas = useQuery<
    TodayPayload["weak_areas"]
  >({
    queryKey: WEAK_AREAS_KEY,
    queryFn: () =>
      api.gamification
        .getWeakAreas(5)
        .then((nodes: any[]) =>
          nodes.map((n: any) => ({
            category: n.category ?? n.id ?? "",
            category_name: n.category_name ?? n.name ?? "",
            skill: n.skill ?? n.id ?? "",
            score: Number(n.score ?? 0),
            attempts: Number(n.attempts ?? 0),
          })),
        )
        .catch(() => []),
    staleTime: 60_000,
    refetchOnWindowFocus: true,
    enabled: !!user,
  });

  const gamification = useQuery<{
    level: number;
    diamonds: number;
    streak: number;
    last_practice_date?: string;
  } | null>({
    queryKey: ["gamification", "profile"],
    queryFn: () =>
      api.gamification.getProfile().then((p: any) => ({
        level: Number(p?.level ?? 1),
        diamonds: Number(p?.diamonds ?? 0),
        streak: Number(p?.streak ?? 0),
        last_practice_date: p?.last_practice_date ?? p?.last_active,
      })).catch(() => null),
    staleTime: 15_000,
    refetchOnWindowFocus: true,
    enabled: !!user,
  });

  const payload: TodayPayload | null = learner.data
    ? {
        mission: mission.data ?? null,
        readiness: readiness.data ?? { overall: 0, categories: {} },
        weak_areas: weakAreas.data ?? [],
        gamification: gamification.data ?? {
          level: 1,
          diamonds: 0,
          streak: 0,
        },
        srs: (learner.data.srs as any) ?? {
          due_cards: 0,
          total_cards: 0,
          mastered_concepts: 0,
        },
        repair: (learner.data.repair as any) ?? {
          open_repairs: 0,
          recent_repairs: [],
        },
        evidence: (learner.data.evidence as any) ?? {
          total_events: 0,
          recent_event_count: 0,
          last_event_at: null,
        },
      }
    : null;

  const isLoading =
    mission.isLoading ||
    learner.isLoading ||
    readiness.isLoading ||
    weakAreas.isLoading ||
    gamification.isLoading;
  const isError =
    mission.isError ||
    learner.isError ||
    readiness.isError ||
    weakAreas.isError ||
    gamification.isError;

  const refetch = async () => {
    await Promise.all([
      mission.refetch(),
      learner.refetch(),
      readiness.refetch(),
      weakAreas.refetch(),
      gamification.refetch(),
    ]);
  };

  return {
    today: payload,
    readiness: readiness.data,
    weakAreas: weakAreas.data ?? [],
    gamification: gamification.data,
    isLoading,
    isError,
    refetch,
  };
}

export function invalidateToday(queryClient: QueryClient) {
  void queryClient.invalidateQueries({ queryKey: TODAY_KEY });
  void queryClient.invalidateQueries({ queryKey: ["today", "learner"] });
  void queryClient.invalidateQueries({ queryKey: READINESS_KEY });
  void queryClient.invalidateQueries({ queryKey: WEAK_AREAS_KEY });
  void queryClient.invalidateQueries({ queryKey: ["gamification", "profile"] });
}
