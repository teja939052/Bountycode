import { requestWithRetry as request } from "./request.ts";

export const lessonApi = {
  getLesson<T = any>(slug: string): Promise<T> {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}`);
  },

  getStep(slug: string, stepKey: string) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/step/${encodeURIComponent(stepKey)}`);
  },

  runCode(slug: string, payload: { code: string; language?: string; stdin?: string }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/run`, {
      method: "POST",
      body: JSON.stringify({
        code: payload.code,
        language: payload.language || "python",
        stdin: payload.stdin || "",
      }),
    });
  },

  submitBuild(slug: string, payload: {
    code: string;
    function_name: string;
    language?: string;
    step_index?: number;
  }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/build`, {
      method: "POST",
      body: JSON.stringify({
        code: payload.code,
        function_name: payload.function_name,
        language: payload.language || "python",
        step_index: payload.step_index,
      }),
    });
  },

  submitTransfer(slug: string, payload: {
    code: string;
    function_name: string;
    language?: string;
  }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/transfer`, {
      method: "POST",
      body: JSON.stringify({
        code: payload.code,
        function_name: payload.function_name,
        language: payload.language || "python",
      }),
    });
  },

  checkPrediction(slug: string, answer: string) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/predict`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    });
  },

  checkAssessment(slug: string, payload: { answers: Record<string, string>; time_spent_seconds?: number }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/assess`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  completeLesson(slug: string, payload: { score: number; time_spent_seconds?: number }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};

export default lessonApi;
