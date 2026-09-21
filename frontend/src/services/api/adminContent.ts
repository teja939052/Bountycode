import { requestWithRetry as request } from "./request.ts";

export interface ContentItem {
  id: string;
  title: string;
  content: string;
  type?: string;
  category?: string;
  tags?: string[];
  published?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: unknown;
}

export interface AssignmentItem {
  id: string;
  title: string;
  description?: string;
  status: string;
  due_date?: string;
  score?: number;
  max_score?: number;
  feedback?: string;
  graded_at?: string;
  [key: string]: unknown;
}

export const adminContentApi = {
  list(
    params: Record<string, string> = {},
  ): Promise<{ items: ContentItem[]; total?: number }> {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") qs.set(k, v);
    });
    const query = qs.toString();
    return request(`/api/v1/admin/content${query ? `?${query}` : ""}`);
  },

  get(contentId: string): Promise<ContentItem> {
    return request(`/api/v1/admin/content/${encodeURIComponent(contentId)}`);
  },

  create(payload: Partial<ContentItem>): Promise<ContentItem> {
    return request("/api/v1/admin/content", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  update(
    contentId: string,
    payload: Partial<ContentItem>,
  ): Promise<ContentItem> {
    return request(`/api/v1/admin/content/${encodeURIComponent(contentId)}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  },

  remove(contentId: string): Promise<{ deleted?: boolean }> {
    return request(`/api/v1/admin/content/${encodeURIComponent(contentId)}`, {
      method: "DELETE",
    });
  },
};

export interface TrancheSummary {
  tranche: string;
  size: number;
  staged: number;
  rejected: number;
  status: string;
  merged_at?: string | null;
  reviewed_by?: string | null;
}

export interface TrancheSampleItem {
  id: string;
  question?: string;
  correct_answer?: string;
  difficulty?: string;
  topic?: string;
  sub_topic?: string;
  type?: string;
  provenance?: string;
  missing?: boolean;
}

export interface TrancheDetail {
  tranche: string;
  status: string;
  size: number;
  reviewed_by?: string | null;
  merged_at?: string | null;
  sample: TrancheSampleItem[];
  sample_count: number;
  staged?: string[];
}

export const tranchesApi = {
  list(): Promise<{
    tranches: TrancheSummary[];
    pool?: number;
    staged_total?: number;
    serving_merged?: boolean;
  }> {
    return request("/api/v1/admin/content/tranches");
  },

  get(trancheId: string): Promise<{
    tranche: string;
    status: string;
    size: number;
    reviewed_by?: string | null;
    merged_at?: string | null;
    sample: TrancheSampleItem[];
    sample_count: number;
  }> {
    return request(
      `/api/v1/admin/content/tranches/${encodeURIComponent(trancheId)}`,
    );
  },

  approve(
    trancheId: string,
    signoffName: string,
  ): Promise<{ tranche: string; status: string; merged: number }> {
    return request(
      `/api/v1/admin/content/tranches/${encodeURIComponent(trancheId)}/approve`,
      {
        method: "POST",
        body: JSON.stringify({ signoff_name: signoffName, confirm: true }),
      },
    );
  },

  reject(
    trancheId: string,
    reason: string,
  ): Promise<{ tranche: string; status: string }> {
    return request(
      `/api/v1/admin/content/tranches/${encodeURIComponent(trancheId)}/reject`,
      { method: "POST", body: JSON.stringify({ reason }) },
    );
  },
};

export interface CorpusSummary {
  total_concepts: number;
  domains: Record<string, number>;
  categories: Record<string, number>;
  status_counts: Record<string, number>;
  validation: { valid: boolean; issues: Array<{ concept_id?: string; message: string }> };
  last_loaded?: string;
}

export interface CorpusConcept {
  concept_id: string;
  domain: string;
  category: string;
  subcategory?: string;
  language?: string;
  title: string;
  description?: string;
  content_status: string;
  prerequisites?: string[];
  Bloom?: string[];
  difficulty?: string;
  [key: string]: unknown;
}

export interface ConceptDetail extends CorpusConcept {
  worked_examples?: unknown[];
  misconceptions?: unknown[];
  transfer_targets?: unknown[];
  verification?: unknown;
}

export interface GenerationQueueItem {
  concept_id: string;
  title: string;
  domain: string;
  category: string;
  content_status: string;
  missing_types: string[];
  [key: string]: unknown;
}

export interface GenerationReport {
  concept_id: string;
  generated: Record<string, unknown>;
  skipped: Record<string, string>;
  validation?: { valid: boolean; issues: unknown[] };
}

export const corpusApi = {
  summary(): Promise<CorpusSummary> {
    return request("/api/v1/admin/content/corpus/summary");
  },

  concepts(params: Record<string, string> = {}): Promise<{ count: number; concepts: CorpusConcept[] }> {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") qs.set(k, v);
    });
    const query = qs.toString();
    return request(`/api/v1/admin/content/corpus/concepts${query ? `?${query}` : ""}`);
  },

  concept(conceptId: string): Promise<{ concept: ConceptDetail; prerequisites: string[]; all_prerequisites: string[] }> {
    return request(`/api/v1/admin/content/corpus/concepts/${encodeURIComponent(conceptId)}`);
  },

  validate(): Promise<{ valid: boolean; issues: Array<{ concept_id?: string; message: string }> }> {
    return request("/api/v1/admin/content/corpus/validate");
  },

  queue(params: Record<string, string> = {}, limit = 50): Promise<{ count: number; queue: GenerationQueueItem[]; domain?: string; language?: string }> {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") qs.set(k, v);
    });
    qs.set("limit", String(limit));
    const query = qs.toString();
    return request(`/api/v1/admin/content/corpus/queue${query ? `?${query}` : ""}`);
  },

  generate(conceptIds: string[], contentTypes?: string[], mode: "dry_run" | "production" = "dry_run"): Promise<GenerationReport> {
    return request("/api/v1/admin/content/corpus/generate", {
      method: "POST",
      body: JSON.stringify({ concept_ids: conceptIds, content_types: contentTypes, mode }),
    });
  },
};

export const assignmentsApi = {
  list(): Promise<{ assignments: AssignmentItem[] }> {
    return request("/api/v1/assignments");
  },

  listAdmin(): Promise<{ assignments: AssignmentItem[] }> {
    return request("/api/v1/assignments/admin");
  },

  create(payload: Partial<AssignmentItem>): Promise<AssignmentItem> {
    return request("/api/v1/assignments", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  submit(
    assignmentId: string,
    answerText: string,
  ): Promise<{ submitted?: boolean; score?: number; feedback?: string }> {
    return request(
      `/api/v1/assignments/${encodeURIComponent(assignmentId)}/submit`,
      {
        method: "POST",
        body: JSON.stringify({ answer_text: answerText }),
      },
    );
  },

  review(
    assignmentId: string,
    userId: string,
    score: number,
    feedback: string,
  ): Promise<{ reviewed?: boolean }> {
    return request(
      `/api/v1/assignments/${encodeURIComponent(assignmentId)}/review`,
      {
        method: "POST",
        body: JSON.stringify({ user_id: userId, score, feedback }),
      },
    );
  },

  submissions(
    assignmentId: string | null = null,
  ): Promise<{ submissions: AssignmentItem[] }> {
    const qs = assignmentId
      ? `?assignment_id=${encodeURIComponent(assignmentId)}`
      : "";
    return request(`/api/v1/assignments/submissions${qs}`);
  },
};
