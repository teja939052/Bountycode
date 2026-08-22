import { requestWithRetry as request } from "./request.ts";
import type { AptitudeCategory, TestSession, TestResult } from "./types.ts";

export const aptitudeApi = {
  getCategories(): Promise<{ categories: AptitudeCategory[] }> {
    return request("/api/v1/aptitude/categories");
  },

  startTest(
    category: string,
    difficulty = "medium",
    questionCount = 20,
  ): Promise<TestSession> {
    return request("/api/v1/aptitude/start", {
      method: "POST",
      body: JSON.stringify({
        category,
        difficulty,
        question_count: questionCount,
      }),
    });
  },

  submitAnswer(
    testId: string,
    questionIndex: number,
    answer: number | string,
  ): Promise<{ correct: boolean; score?: number; feedback?: string }> {
    return request("/api/v1/aptitude/answer", {
      method: "POST",
      body: JSON.stringify({
        test_id: testId,
        question_index: questionIndex,
        answer,
      }),
    });
  },

  completeTest(testId: string, timeTaken = 0): Promise<TestResult> {
    return request(
      `/api/v1/aptitude/${testId}/complete?time_taken=${timeTaken}`,
      {
        method: "POST",
      },
    );
  },

  getHistory(): Promise<TestResult[]> {
    return request("/api/v1/aptitude/history");
  },

  getResult(testId: string): Promise<TestResult> {
    return request(`/api/v1/aptitude/${testId}/result`);
  },
};
