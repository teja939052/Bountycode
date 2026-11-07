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
  output?: string;
  explanation?: string;
  instruction?: string;
  starterCode?: string;
  hints?: string[];
  question?: string;
  options?: string[];
};

export type StepResult = {
  is_correct: boolean | null;
  graded: boolean;
  verified: boolean;
  feedback: string;
  test_results?:
    | { index: number; passed: boolean; expected: string; actual: string }[]
    | null;
  step_completed: boolean;
  lesson_complete: boolean;
  lesson_verified: boolean;
  xp_earned: number;
  total_xp: number;
  next_action?: Record<string, unknown>;
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
    code?: string;
    answer?: string;
  }) =>
    requestWithRetry("/api/v1/lessons/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  submitExercise: (body: {
    lesson_id: string;
    step_id: string;
    code?: string;
  }) =>
    requestWithRetry("/api/v1/lessons/exercise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  next: () => requestWithRetry("/api/v1/lessons/next"),
};
