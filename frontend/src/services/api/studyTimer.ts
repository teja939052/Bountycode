import { requestWithRetry as request } from "./request.ts";

export const studyTimerApi = {
  getStats(): Promise<any> {
    return request("/api/v1/study-timer/stats").then((s: any) => ({
      ...s,
      total_minutes: Math.round((s?.total_seconds ?? 0) / 60),
      focus_rank:
        (s?.avg_focus ?? 0) >= 80
          ? "Pro"
          : (s?.avg_focus ?? 0) >= 50
            ? "Consistent"
            : "Novice",
    }));
  },

  createSession(_seconds: number, label: string, mode: string): Promise<any> {
    const activity = mode === "custom" ? "focus" : mode;
    return request("/api/v1/study-timer/start", {
      method: "POST",
      body: JSON.stringify({ activity_type: activity, topic: label }),
    });
  },

  completeSession(sessionId: string, _minutes: number): Promise<any> {
    return request("/api/v1/study-timer/complete", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId }),
    }).then((r: any) => ({
      ...r,
      score: r?.xp_earned ?? 10,
      new_badges: r?.new_badges || [],
      critical_hit: false,
    }));
  },
};