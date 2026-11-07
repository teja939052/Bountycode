import { requestWithRetry as request } from "./request.ts";

export interface RolePath {
  id: string;
  name: string;
  short_name: string;
  icon: string;
  color: string;
  description: string;
  target_roles: string[];
  avg_package: string;
  duration_weeks: number;
  difficulty: string;
  prerequisites: string[];
  total_modules: number;
  total_xp: number;
  enrolled?: boolean;
  progress_pct?: number;
  completed?: boolean;
}

export interface PathModule {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  duration_days: number;
  xp_reward: number;
  topics: string[];
  skills: string[];
  activities: string[];
  unlocks: string[];
  depends_on: string[];
  completed: boolean;
  locked: boolean;
  score: number | null;
  xp_earned: number;
  attempts: number;
}

export interface CompanyTrack {
  id: string;
  company_id: string;
  name: string;
  full_name: string;
  icon: string;
  color: string;
  role: string;
  package_range: string;
  duration_minutes: number;
  difficulty: string;
  description: string;
  total_sections: number;
  total_modules: number;
  total_xp: number;
  enrolled?: boolean;
  progress_pct?: number;
  completed?: boolean;
}

export interface TrackSection {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  questions_count: number;
  negative_marking: boolean;
  topics: Array<{ name: string; weight: number; sub_topics: string[] }>;
  modules: TrackModule[];
  completed: boolean;
}

export interface TrackModule {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  questions_count: number;
  xp_reward: number;
  topics: string[];
  completed: boolean;
  locked: boolean;
  score: number | null;
  xp_earned: number;
}

export interface Recommendation {
  path_id: string;
  name: string;
  short_name: string;
  icon: string;
  color: string;
  match_score: number;
  reason: string;
  based_on: string[];
}

export const learningPathsApi = {
  listRoles(): Promise<{ paths: RolePath[] }> {
    return request("/api/v1/learning-paths/roles");
  },

  getRole(roleId: string): Promise<RolePath & { modules: PathModule[]; final_project?: unknown; certification?: string; enrolled: boolean; completed: boolean; total_xp_earned: number; current_module_id: string | null }> {
    return request(`/api/v1/learning-paths/roles/${encodeURIComponent(roleId)}`);
  },

  enroll(pathId: string): Promise<{ success: boolean; path_id: string; enrolled_at: string }> {
    return request("/api/v1/learning-paths/roles/enroll", {
      method: "POST",
      body: JSON.stringify({ path_id: pathId }),
    });
  },

  completeModule(roleId: string, moduleId: string, score?: number): Promise<{ success: boolean; module_id: string; xp_earned: number; base_xp: number; bonus_xp: number; next_unlocks: string[]; path_completed: boolean }> {
    const qs = score !== undefined ? `?score=${encodeURIComponent(String(score))}` : "";
    return request(`/api/v1/learning-paths/roles/${encodeURIComponent(roleId)}/modules/${encodeURIComponent(moduleId)}/complete${qs}`, {
      method: "POST",
    });
  },

  getMyPaths(): Promise<{ paths: Array<{ id: string; name: string; short_name: string; icon: string; color: string; description: string; enrolled: boolean; progress_pct: number; completed: boolean; current_module_id: string | null; total_xp_earned: number; completed_modules: number; total_modules: number }> }> {
    return request("/api/v1/learning-paths/my-paths");
  },

  getRecommendations(): Promise<{ recommendations: Recommendation[] }> {
    return request("/api/v1/learning-paths/recommendations");
  },
};

export const companyTracksApi = {
  listCompanies(): Promise<{ tracks: CompanyTrack[] }> {
    return request("/api/v1/company-tracks/companies");
  },

  getTrack(trackId: string): Promise<CompanyTrack & { sections: TrackSection[]; coding_patterns: string[]; hr_questions: string[]; tips: string[]; success_rate?: string; enrolled: boolean; completed: boolean; total_xp_earned: number; current_section_id: string | null }> {
    return request(`/api/v1/company-tracks/companies/${encodeURIComponent(trackId)}`);
  },

  enroll(trackId: string): Promise<{ success: boolean; track_id: string; enrolled_at: string }> {
    return request("/api/v1/company-tracks/companies/enroll", {
      method: "POST",
      body: JSON.stringify({ path_id: trackId }),
    });
  },

  completeModule(trackId: string, moduleId: string, score?: number): Promise<{ success: boolean; module_id: string; xp_earned: number; base_xp: number; bonus_xp: number }> {
    const qs = score !== undefined ? `?score=${encodeURIComponent(String(score))}` : "";
    return request(`/api/v1/company-tracks/companies/${encodeURIComponent(trackId)}/modules/${encodeURIComponent(moduleId)}/complete${qs}`, {
      method: "POST",
    });
  },

  getMyTracks(): Promise<{ tracks: Array<{ id: string; company_id: string; name: string; full_name: string; icon: string; color: string; role: string; package_range: string; enrolled: boolean; progress_pct: number; completed: boolean; current_section_id: string | null; total_xp_earned: number; completed_modules: number; total_modules: number }> }> {
    return request("/api/v1/company-tracks/my-tracks");
  },
};
