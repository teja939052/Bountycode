import { requestWithRetry } from "./request.ts";

export type Lesson = {
  id: string;
  title: string;
  track: string;
  description: string;
  difficulty: string;
  steps: LessonStep[];
  xpReward: number;
  prerequisites?: string[];
};

export type LessonStep = {
  id: string;
  type: "explain" | "exercise" | "quiz";
  title: string;
  content?: string;
  code?: string;
  explanation?: string;
  instruction?: string;
  starterCode?: string;
  solution?: string;
  tests?: any[];
};

export type LessonProgress = {
  completed: Record<string, any>;
  current_lesson: string | null;
  xp_earned: number;
};

export const lessonsApi = {
  list: (track?: string) =>
    requestWithRetry(
      `/api/v1/lessons${track ? `?track=${encodeURIComponent(track)}` : ""}`
    ),

  search: (q: string, track?: string) =>
    requestWithRetry(
      `/api/v1/lessons/search?q=${encodeURIComponent(q)}${
        track ? `&track=${encodeURIComponent(track)}` : ""
      }`
    ),

  get: (lessonId: string) =>
    requestWithRetry(`/api/v1/lessons/${encodeURIComponent(lessonId)}`),

  progress: () => requestWithRetry("/api/v1/lessons/progress"),

  completeStep: (body: {
    lesson_id: string;
    step_id: string;
    code: string;
  }) =>
    requestWithRetry("/api/v1/lessons/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  submitExercise: (body: {
    lesson_id: string;
    step_id: string;
    code: string;
  }) =>
    requestWithRetry("/api/v1/lessons/exercise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  next: () => requestWithRetry("/api/v1/lessons/next"),
};
