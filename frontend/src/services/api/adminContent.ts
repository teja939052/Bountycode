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
