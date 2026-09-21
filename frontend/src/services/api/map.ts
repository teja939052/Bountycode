import { requestWithRetry as request } from "./request.ts";

export interface MapNode {
  node_id: string;
  level_id: string;
  town_id: string;
  title: string;
  kind: string;
  position: { x: number; y: number };
  path_next: string[];
  status: string;
  stars: number;
  mastery: number;
  score: number;
  best_score: number;
  attempts: number;
  failed_attempts: number;
  hints_used: number;
  recovered: boolean;
  diamonds: number;
  visible: boolean;
  fogged: boolean;
  is_current: boolean;
  is_boss: boolean;
  due_count?: number;
  is_branch?: boolean;
  branch_from?: string;
  parent_title?: string;
}

export interface WorldTheme {
  color: string;
  terrain: string;
  bgm: "meadow" | "plains" | "embers";
}

export interface WorldSummary {
  id: string;
  adventure_name: string;
  title: string;
  theme: WorldTheme;
  status: "completed" | "active" | "unlocked" | "locked";
  done: number;
  total: number;
  order: number;
}

export interface MapState {
  world: { id: string; adventure_name: string; title: string; theme: WorldTheme; status: string } | null;
  all_worlds: WorldSummary[];
  nodes: MapNode[];
  character: { node_index: number; node_id: string | null; title?: string; level?: number } & Record<string, unknown>;
  stats: { diamonds: number; level: number; coins: number; streak: number; badges_count: number } | null;
  horizon: number;
  total: number;
  visible_count: number;
  fogged_count: number;
  campfire: { due_count: number } | null;
}

export const mapApi = {
  getState(worldId?: string): Promise<MapState> {
    const q = worldId ? `?world_id=${encodeURIComponent(worldId)}` : "";
    return request(`/api/v1/map/state${q}`);
  },
};
