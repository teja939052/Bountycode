import { requestWithRetry as request } from "./request.ts";

export interface PseudocodeQuestion {
  id: string;
  sub_category: string;
  question: string;
  options: string[];
}

export interface CheckResult {
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
}

export const pseudocodeApi = {
  meta(): Promise<{ total: number; topics: Record<string, number> }> {
    return request("/api/v1/pseudocode/meta");
  },

  getQuestions(
    count = 10,
    topic?: string,
  ): Promise<{ questions: PseudocodeQuestion[]; total_available: number }> {
    const q = new URLSearchParams({ count: String(count) });
    if (topic) q.set("topic", topic);
    return request(`/api/v1/pseudocode/questions?${q.toString()}`);
  },

  check(questionId: string, answer: string): Promise<CheckResult> {
    return request("/api/v1/pseudocode/check", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer }),
    });
  },

  complete(correct: number, total: number): Promise<{
    accuracy: number;
    xp_gained: number;
    message: string;
  }> {
    return request("/api/v1/pseudocode/complete", {
      method: "POST",
      body: JSON.stringify({ correct, total }),
    });
  },
};
