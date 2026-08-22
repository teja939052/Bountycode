import { requestWithRetry as request } from "./request.ts";
import type { LanguageInfo, ExecutionResult, TestCaseResult } from "./types.ts";

export const codingApi = {
  getTopics(): Promise<{
    topics: string[];
    sub_topics?: Record<string, string[]>;
  }> {
    return request("/api/v1/coding/topics");
  },

  startChallenge(
    difficulty = "medium",
    topic = "arrays",
    language = "python",
  ): Promise<{
    challenge_id: string;
    question: Record<string, unknown>;
    code?: string;
  }> {
    return request("/api/v1/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language }),
    });
  },

  startChallengeV2(
    difficulty = "medium",
    topic = "arrays",
    language = "python",
    company = "",
    role = "SDE",
  ): Promise<{
    challenge_id: string;
    question: Record<string, unknown>;
    code?: string;
  }> {
    return request("/api/v1/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language, company, role }),
    });
  },

  getHint(
    challengeId: string,
    hintLevel = 1,
  ): Promise<{ hint: string; hints?: string[] }> {
    return request("/api/v1/coding/hint", {
      method: "POST",
      body: JSON.stringify({
        challenge_id: challengeId,
        hint_level: hintLevel,
      }),
    });
  },

  getInterviewerReview(
    challengeId: string,
    code: string,
    language = "python",
  ): Promise<{ review: string; score?: number; suggestions?: string[] }> {
    return request("/api/v1/coding/interviewer-review", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, language }),
    });
  },

  submitAnswer(
    challengeId: string,
    code: string,
    timeTaken = 0,
  ): Promise<{ passed?: boolean; score?: number; feedback?: string }> {
    return request("/api/v1/coding/submit", {
      method: "POST",
      body: JSON.stringify({
        challenge_id: challengeId,
        code,
        time_taken: timeTaken,
      }),
    });
  },

  getSolution(
    challengeId: string,
  ): Promise<{ solution: string; explanation?: string }> {
    return request(`/api/v1/coding/${challengeId}/solution`);
  },

  getHistory(): Promise<
    Array<{
      challenge_id: string;
      score: number;
      date: string;
      difficulty?: string;
    }>
  > {
    return request("/api/v1/coding/history");
  },
};

export const compilerApi = {
  executeCode({
    code,
    language,
    stdin = "",
    timeout = 5,
  }: {
    code: string;
    language: string;
    stdin?: string;
    timeout?: number;
  }): Promise<ExecutionResult> {
    return request("/api/v1/compiler/execute", {
      method: "POST",
      body: JSON.stringify({ code, language, stdin, timeout }),
    });
  },

  executeTestCases({
    code,
    language,
    test_cases,
    timeout = 5,
  }: {
    code: string;
    language: string;
    test_cases: string[];
    timeout?: number;
  }): Promise<{ results: TestCaseResult[]; passed: number; total: number }> {
    return request("/api/v1/compiler/execute-test-cases", {
      method: "POST",
      body: JSON.stringify({ code, language, test_cases, timeout }),
    });
  },

  getLanguages(): Promise<LanguageInfo[]> {
    return request("/api/v1/compiler/languages");
  },

  getBoilerplate(
    language: string,
    topics: string[] = [],
  ): Promise<{ code: string; language: string }> {
    return request("/api/v1/compiler/boilerplate", {
      method: "POST",
      body: JSON.stringify({ language, topics }),
    });
  },

  traceCode({
    code,
    language,
    stdin = "",
  }: {
    code: string;
    language: string;
    stdin?: string;
  }): Promise<{ trace: string[]; output?: string; errors?: string[] }> {
    return request("/api/v1/compiler/trace", {
      method: "POST",
      body: JSON.stringify({ code, language, stdin }),
    });
  },
};
