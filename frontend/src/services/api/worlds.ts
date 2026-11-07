import { requestWithRetry as request } from "./request.ts";

export interface WorldsLevel {
  id: string;
  title: string;
  icon: string;
  kind: "level" | "boss";
  order: number;
  concept: string;
  mental_model?: string;
  canonical_skill?: string;
  maps_to_competency?: string;
  story: { location: string; npc: string; line: string };
  tutor: { name: string; avatar: string; discover: string; explain: string };
  discover: { visual: string; interaction: string; prompt: string; answer: string; values?: any[] };
  manipulate: { type: string; template?: string; answer: string | string[]; blocks?: string[]; hint?: string };
  predict?: { prompt: string; answer: string; explanation: string };
  build?: { prompt: string; starter: string; placeholder: string; language: string };
  break?: { prompt: string; broken_code: string; expected_failure: string };
  debug?: { prompt: string; buggy_code: string; fix_steps: string[]; answer: string };
  code: { prompt: string; starter: string; placeholder: string; language: string };
  checks: { required_patterns: string[]; forbidden: string[]; hint_triggers: string[] };
  hints: string[];
  retrieval?: { prompt: string; answer: string; explanation: string };
  transfer?: { prompt: string; answer: string; context: string };
  mastery_threshold?: number;
  estimated_minutes?: number;
  success: {
    world_before?: string;
    world_after?: string;
    world_reaction: string;
    reward_text: string;
    byte_line?: string;
    diamonds: number;
  };
  completed: boolean;
  unlocked: boolean;
  score: number;
  attempts: number;
  diamonds: number;
}

export interface WorldMeta {
  id: string;
  name: string;
  subtitle: string;
  description: string;
  icon: string;
  order: number;
  theme: string;
  recommended_roles: string[];
  prerequisites: string[];
  towns_count: number;
  levels_count: number;
  completed_count: number;
  progress_pct: number;
  unlocked: boolean;
}

export interface WorldView {
  world: {
    id: string;
    name: string;
    subtitle: string;
    description: string;
    icon: string;
    order: number;
    theme: string;
    recommended_roles: string[];
    prerequisites: string[];
    towns: Array<{
      id: string;
      name: string;
      icon: string;
      description: string;
      order: number;
      mental_model: string;
      canonical_skills: string[];
      competencies: string[];
      levels: WorldsLevel[];
      boss?: WorldsLevel;
    }>;
    completion_reward?: { diamonds: number; coins: number; badges: string[] };
  };
  progress: {
    levels: WorldsLevel[];
    character_pos: number;
    completed_count: number;
    total_count: number;
    progress_pct: number;
    boss_defeated: boolean;
    next_town_unlocked: boolean;
  };
  mastery: Record<string, number>;
}

export const worldsApi = {
  /** Generic world definition + progress overlay. */
  getWorld(worldId: string) {
    return request<WorldView>(`/api/v1/worlds/${encodeURIComponent(worldId)}`);
  },
  listWorlds() {
    return request<{ worlds: WorldMeta[] }>(`/api/v1/worlds/`);
  },
  getProgress(worldId: string) {
    return request(`/api/v1/worlds/${encodeURIComponent(worldId)}/progress`);
  },
  attempt(worldId: string, levelId: string, code: string, timeSpentSeconds = 0) {
    return request(`/api/v1/worlds/${encodeURIComponent(worldId)}/levels/${encodeURIComponent(levelId)}/attempt`, {
      method: "POST",
      body: JSON.stringify({ code, time_spent_seconds: timeSpentSeconds }),
    });
  },
  complete(worldId: string, levelId: string, code: string, timeSpentSeconds = 0) {
    return request(`/api/v1/worlds/${encodeURIComponent(worldId)}/levels/${encodeURIComponent(levelId)}/complete`, {
      method: "POST",
      body: JSON.stringify({ code, time_spent_seconds: timeSpentSeconds }),
    });
  },
  hint(worldId: string, levelId: string, hintIndex: number, timeSpentSeconds = 0) {
    return request(`/api/v1/worlds/${encodeURIComponent(worldId)}/levels/${encodeURIComponent(levelId)}/hint`, {
      method: "POST",
      body: JSON.stringify({ hint_index: hintIndex, time_spent_seconds: timeSpentSeconds }),
    });
  },
  listTowns(worldId: string) {
    return request(`/api/v1/worlds/${encodeURIComponent(worldId)}/towns`);
  },
};

export default worldsApi;
