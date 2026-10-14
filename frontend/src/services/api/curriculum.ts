// @ts-nocheck
export interface CurriculumModule {
  module_id: number;
  title: string;
  description: string;
  concept_count: number;
}

export interface CurriculumConcept {
  concept_id: string;
  module_id: number;
  order: number;
  title: string;
  subtitle: string;
  estimated_minutes: number;
  canonical_lesson_slug?: string;
  unplug_activity?: {
    type: string;
    title: string;
    materials: string[];
    instructions: string[];
    teacher_prompt: string;
    aha_moment: string;
  };
  unpack?: {
    plain_language: string;
    technical_term: string;
    misconceptions: Array<{
      id: string;
      description: string;
      detection_pattern: string;
      fix_explanation: string;
    }>;
  };
  parsons_problems?: Array<{
    id: string;
    title: string;
    language: string;
    lines: string[];
    correct_order: number[];
    distractors: string[];
    hints: string[];
  }>;
  trace_exercises?: Array<{
    id: string;
    title: string;
    language: string;
    code: string;
    questions: Array<{
      line: number;
      question: string;
      answer: string;
      explanation: string;
    }>;
  }>;
  write_exercises?: Array<{
    id: string;
    title: string;
    starter_code: string;
    solution: string;
    hidden_tests: Array<{ input: any; expected: any }>;
    misconception_checks: string[];
    hints: string[];
  }>;
  transfer_task?: {
    type: string;
    title: string;
    description: string;
    rubric: string[];
  };
  placement_link?: {
    patterns: string[];
    companies: string[];
    difficulty: string;
  };
}

export interface CurriculumProgress {
  user_id: string;
  concept_status: Record<string, string>;
  module_status: Record<string, any>;
  current_concept: string | null;
  total_mastered: number;
  total_concepts: number;
}

export interface NextConceptResult {
  concept: CurriculumConcept;
  module_id: number;
  module_title: string;
  status: string;
}

export interface FlagshipMission {
  id: string;
  title: string;
  outcome: string;
  core_mission: string;
  domain: string;
  concept_ids: string[];
  complexity: string;
  interaction: string;
  steps: string[];
  activities: Array<{
    step: string;
    type: string;
    title: string;
    description: string;
  }>;
}

export interface CurriculumMissionsResult {
  missions: FlagshipMission[];
  count: number;
}

const BASE = "/api/v1/curriculum";

export const curriculumApi = {
  async listModules(): Promise<{ modules: CurriculumModule[] }> {
    const res = await fetch(`${BASE}/thinkincode/modules`);
    if (!res.ok) throw new Error("Failed to load modules");
    return res.json();
  },

  async getModule(moduleId: number): Promise<any> {
    const res = await fetch(`${BASE}/thinkincode/modules/${moduleId}`);
    if (!res.ok) throw new Error("Failed to load module");
    return res.json();
  },

  async getConcept(conceptId: string): Promise<CurriculumConcept> {
    const res = await fetch(`${BASE}/thinkincode/concepts/${conceptId}`);
    if (!res.ok) throw new Error("Failed to load concept");
    return res.json();
  },

  async getProgress(): Promise<CurriculumProgress> {
    const res = await fetch(`${BASE}/thinkincode/progress`);
    if (!res.ok) throw new Error("Failed to load progress");
    return res.json();
  },

  async updateProgress(conceptId: string, status: string, metadata?: Record<string, any>): Promise<any> {
    const res = await fetch(`${BASE}/thinkincode/progress`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept_id: conceptId, status, metadata }),
    });
    if (!res.ok) throw new Error("Failed to update progress");
    return res.json();
  },

  async getNextConcept(): Promise<NextConceptResult> {
    const res = await fetch(`${BASE}/thinkincode/next`);
    if (!res.ok) throw new Error("No next concept");
    return res.json();
  },

  async validateParsons(conceptId: string, parsonsId: string, selectedOrder: number[]): Promise<any> {
    const res = await fetch(`${BASE}/thinkincode/parsons/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept_id: conceptId, parsons_id: parsonsId, selected_order: selectedOrder }),
    });
    if (!res.ok) throw new Error("Failed to validate");
    return res.json();
  },

  async recordParsonsAttempt(conceptId: string, parsonsId: string, correct: boolean, attempts: number, timeTaken: number): Promise<any> {
    const res = await fetch(`${BASE}/thinkincode/parsons/attempt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept_id: conceptId, parsons_id: parsonsId, correct, attempts, time_taken: timeTaken }),
    });
    if (!res.ok) throw new Error("Failed to record attempt");
    return res.json();
  },

  async getMisconceptions(conceptId: string): Promise<any[]> {
    const res = await fetch(`${BASE}/thinkincode/concepts/${conceptId}/misconceptions`);
    if (!res.ok) throw new Error("Failed to load misconceptions");
    return res.json();
  },

  async detectMisconception(conceptId: string, code: string, exerciseType: string): Promise<any[]> {
    const res = await fetch(`${BASE}/thinkincode/misconceptions/detect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concept_id: conceptId, code, exercise_type: exerciseType }),
    });
    if (!res.ok) throw new Error("Failed to detect");
    return res.json();
  },

  async getPlacementConcepts(pattern?: string, difficulty?: string, company?: string): Promise<{ concepts: any[] }> {
    const params = new URLSearchParams();
    if (pattern) params.set("pattern", pattern);
    if (difficulty) params.set("difficulty", difficulty);
    if (company) params.set("company", company);
    const res = await fetch(`${BASE}/thinkincode/placement?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to load placement concepts");
    return res.json();
  },

  async listFlagshipMissions(): Promise<CurriculumMissionsResult> {
    const res = await fetch(`${BASE}/missions`);
    if (!res.ok) throw new Error("Failed to load flagship missions");
    return res.json();
  },

  async getFlagshipMission(missionId: string): Promise<{ mission: FlagshipMission }> {
    const res = await fetch(`${BASE}/missions/${encodeURIComponent(missionId)}`);
    if (!res.ok) throw new Error("Failed to load flagship mission");
    return res.json();
  },
};
