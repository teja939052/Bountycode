// @ts-nocheck
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

  checkExplain(slug: string, answer: string) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/explain`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    });
  },

  checkBreak(slug: string, payload: { diagnosis: string; fix: string }) {
    return request(`/api/v1/lesson/${encodeURIComponent(slug)}/break`, {
      method: "POST",
      body: JSON.stringify(payload),
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

  startLessonPlayer(ppayload: {
    domain: "coding" | "behavioral" | "system_design";
    world_id?: string;
    level_id?: string;
    company?: string;
    role?: string;
    topic?: string;
    difficulty?: string;
    mastery_threshold?: number;
  }) {
    return request("/api/v1/lesson-player/start", {
      method: "POST",
      body: JSON.stringify(ppayload),
    });
  },

  submitLessonPlayer(sessionId: string, payload: {
    step_index?: number;
    answer?: string;
    code?: string;
    language?: string;
    selected_option?: string;
    selected_component?: string;
    selected_issue?: string;
    selected_failure?: string;
    fixes_applied?: string[];
    matches?: Record<string, string>;
    improved_answer?: string;
    diagram_description?: string;
    question?: string;
    time_spent_seconds?: number;
  }) {
    return request(`/api/v1/lesson-player/session/${encodeURIComponent(sessionId)}/submit`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getLessonPlayerSession(sessionId: string) {
    return request(`/api/v1/lesson-player/session/${encodeURIComponent(sessionId)}`);
  },

  requestLessonPlayerHint(sessionId: string, stepIndex?: number) {
    return request(`/api/v1/lesson-player/session/${encodeURIComponent(sessionId)}/hint`, {
      method: "POST",
      body: JSON.stringify({ step_index: stepIndex }),
    });
  },

  getLessonPlayerReteach(sessionId: string) {
    return request(`/api/v1/lesson-player/session/${encodeURIComponent(sessionId)}/reteach`, {
      method: "POST",
    });
  },

  completeLessonPlayer(sessionId: string) {
    return request(`/api/v1/lesson-player/session/${encodeURIComponent(sessionId)}/complete`, {
      method: "POST",
    });
  },
};

export const unifiedLearningApi = {
  start(topic: string) {
    return request("/api/v1/unified/start", {
      method: "POST",
      body: JSON.stringify({ topic }),
    });
  },

  step(step: string, topic: string) {
    return request("/api/v1/unified/step", {
      method: "POST",
      body: JSON.stringify({ step, payload: { topic } }),
    });
  },

  exercise(payload: { code: string; language?: string; function_name?: string }) {
    return request("/api/v1/unified/exercise", {
      method: "POST",
      body: JSON.stringify({
        code: payload.code,
        language: payload.language || "python",
        function_name: payload.function_name || "",
      }),
    });
  },

  quiz(payload: { answers: Record<string, string> }) {
    return request("/api/v1/unified/quiz", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  continue(payload: { topic?: string; company?: string; role?: string }) {
    return request("/api/v1/unified/continue", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};

export default lessonApi;
