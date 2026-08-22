import { requestWithRetry as request } from "./request.ts";
import type {
  QuestionFilters,
  QuestionItem,
  QuestionDetail,
  BrowseResult,
  QuestionStats,
  SolutionHint,
  SubmitResult,
} from "./types.ts";

interface BrowseParams {
  company?: string;
  role?: string;
  topic?: string;
  sub_topic?: string;
  pattern?: string;
  source?: string;
  difficulty?: string;
  type?: string;
  search?: string;
  page?: number;
  limit?: number;
}

interface RandomParams {
  type?: string;
  difficulty?: string;
  topic?: string;
  company?: string;
  source?: string;
  exclude_solved?: boolean;
}

export const questionsApi = {
  browse(params: BrowseParams = {}): Promise<BrowseResult> {
    const qs = new URLSearchParams();
    if (params.company) qs.set("company", params.company);
    if (params.role) qs.set("role", params.role);
    if (params.topic) qs.set("topic", params.topic);
    if (params.sub_topic) qs.set("sub_topic", params.sub_topic);
    if (params.pattern) qs.set("pattern", params.pattern);
    if (params.source) qs.set("source", params.source);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.type) qs.set("type", params.type);
    if (params.search) qs.set("search", params.search);
    if (params.page) qs.set("page", String(params.page));
    if (params.limit) qs.set("limit", String(params.limit));
    return request(`/api/v1/questions/browse?${qs.toString()}`);
  },

  getFilters(): Promise<QuestionFilters> {
    return request("/api/v1/questions/filters");
  },

  getFull(questionId: string): Promise<QuestionDetail> {
    return request(`/api/v1/questions/${encodeURIComponent(questionId)}`);
  },

  isSolved(questionId: string): Promise<{ solved: boolean }> {
    return request(
      `/api/v1/questions/${encodeURIComponent(questionId)}/solved`,
    );
  },

  submitAnswer(
    questionId: string,
    answer: string,
    timeTaken: number | null = null,
  ): Promise<{ score: number; feedback: string }> {
    return request("/api/v1/questions/answer", {
      method: "POST",
      body: JSON.stringify({
        question_id: questionId,
        answer,
        time_taken: timeTaken,
      }),
    });
  },

  submitCode(
    questionId: string,
    payload: Record<string, unknown>,
  ): Promise<SubmitResult> {
    return request(
      `/api/v1/questions/${encodeURIComponent(questionId)}/submit`,
      payload,
    );
  },

  getSolution(questionId: string, hintLevel = 1): Promise<SolutionHint> {
    return request(
      `/api/v1/questions/${encodeURIComponent(questionId)}/solution`,
      {
        method: "POST",
        body: JSON.stringify({ hint_level: hintLevel }),
      },
    );
  },

  upvote(questionId: string, vote = 1): Promise<{ success: boolean }> {
    return request("/api/v1/questions/upvote", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, vote }),
    });
  },

  getStats(): Promise<QuestionStats> {
    return request("/api/v1/questions/stats");
  },

  getRecent(limit = 20): Promise<{ recent: QuestionItem[] }> {
    return request(`/api/v1/questions/recent?limit=${limit}`);
  },

  getRandom(params: RandomParams = {}): Promise<{ question: QuestionItem }> {
    const qs = new URLSearchParams();
    if (params.type) qs.set("type", params.type);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.topic) qs.set("topic", params.topic);
    if (params.company) qs.set("company", params.company);
    if (params.source) qs.set("source", params.source);
    qs.set("exclude_solved", "true");
    return request(`/api/v1/questions/random?${qs.toString()}`);
  },

  getCompanyQuestions(company: string): Promise<{ questions: QuestionItem[] }> {
    return request(`/api/v1/questions/company/${encodeURIComponent(company)}`);
  },

  getCompanyQuestionList(
    company: string,
    category: string | null = null,
    page = 1,
    limit = 20,
  ): Promise<{ questions: QuestionItem[]; total: number }> {
    const qs = new URLSearchParams();
    qs.set("page", String(page));
    qs.set("limit", String(limit));
    if (category) qs.set("category", category);
    return request(
      `/api/v1/questions/company/${encodeURIComponent(company)}/list?${qs.toString()}`,
    );
  },

  getUserAttempts(): Promise<Record<string, unknown>> {
    return request("/api/v1/questions/attempts");
  },

  submitQuestion(
    question: Record<string, unknown>,
  ): Promise<{ submitted: boolean; id?: string }> {
    return request("/api/v1/questions/submit", {
      method: "POST",
      body: JSON.stringify(question),
    });
  },

  getAnswerFeedback(
    questionId: string,
    answer: string,
  ): Promise<{ score: number; feedback: string }> {
    return request(
      `/api/v1/questions/${encodeURIComponent(questionId)}/answer`,
      {
        method: "POST",
        body: JSON.stringify({ answer }),
      },
    );
  },

  getDiscussionSummary(questionId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/questions/${encodeURIComponent(questionId)}/discussion-summary`,
    );
  },
};
