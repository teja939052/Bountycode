import { requestWithRetry as request } from "./request.ts";

export interface StudySession {
  session_id: string;
  mode: string;
  duration: number;
  label: string;
  created_at: string;
  status: string;
  completed_at: string | null;
  minutes: number;
}

export interface StudyStats {
  total_sessions: number;
  total_minutes: number;
  week_minutes: number;
  streak_days: number;
  focus_rank: string;
}

export interface StudySessionsResponse {
  today: StudySession[];
  total_completed: number;
  total_minutes: number;
}

export const studyTimerApi = {
  createSession(duration: number, label: string, mode = "pomodoro") {
    return request("/api/v1/study/sessions", {
      method: "POST",
      body: JSON.stringify({ duration, label, mode }),
    }) as Promise<StudySession>;
  },

  listSessions() {
    return request("/api/v1/study/sessions") as Promise<StudySessionsResponse>;
  },

  completeSession(sessionId: string, minutes: number) {
    return request(`/api/v1/study/sessions/${sessionId}/complete`, {
      method: "POST",
      body: JSON.stringify({ minutes }),
    }) as Promise<{ session_id: string; minutes: number; score: number; message: string }>;
  },

  getStats() {
    return request("/api/v1/study/stats") as Promise<StudyStats>;
  },
};
