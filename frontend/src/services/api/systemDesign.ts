import { requestWithRetry as request } from "./request.ts";
import type {
  InterviewStartResponse,
  QuestionItem,
  LeaderboardEntry,
} from "./types.ts";

export const systemDesignApi = {
  start(difficulty = "medium", topic = ""): Promise<InterviewStartResponse> {
    return request("/api/v1/system-design/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic }),
    });
  },

  submitAnswer(
    sessionId: string,
    question: string,
    answer: string,
    diagramDescription = "",
  ): Promise<{ feedback: string; score?: number; next_question?: string }> {
    return request("/api/v1/system-design/answer", {
      method: "POST",
      body: JSON.stringify({
        session_id: sessionId,
        question,
        answer,
        diagram_description: diagramDescription,
      }),
    });
  },

  getResult(sessionId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/system-design/${encodeURIComponent(sessionId)}/result`,
    );
  },

  getHistory(): Promise<Record<string, unknown>[]> {
    return request("/api/v1/system-design/history");
  },
};

export const systemDesignTestsApi = {
  getCategories(): Promise<{ categories: string[] }> {
    return request("/api/v1/system-design-tests/categories");
  },

  listProblems(
    params: Record<string, string> = {},
  ): Promise<{ problems: QuestionItem[] }> {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, String(v));
    });
    return request(`/api/v1/system-design-tests/problems?${query.toString()}`);
  },

  getProblem(problemId: string): Promise<QuestionItem> {
    return request(
      `/api/v1/system-design-tests/problem/${encodeURIComponent(problemId)}`,
    );
  },

  evaluate(
    problemId: string,
    answer: string,
  ): Promise<{ score: number; feedback: string }> {
    return request(
      `/api/v1/system-design-tests/evaluate/${encodeURIComponent(problemId)}`,
      {
        method: "POST",
        body: JSON.stringify({ answer }),
      },
    );
  },

  getModelAnswer(problemId: string): Promise<{ answer: string }> {
    return request(
      `/api/v1/system-design-tests/model-answer/${encodeURIComponent(problemId)}`,
    );
  },

  getRubric(): Promise<Record<string, unknown>> {
    return request("/api/v1/system-design-tests/rubric");
  },

  getHistory(limit = 20): Promise<Record<string, unknown>[]> {
    return request(`/api/v1/system-design-tests/history?limit=${limit}`);
  },

  getStats(): Promise<Record<string, unknown>> {
    return request("/api/v1/system-design-tests/stats");
  },

  getLeaderboard(): Promise<{ entries: LeaderboardEntry[] }> {
    return request("/api/v1/system-design-tests/leaderboard");
  },
};
