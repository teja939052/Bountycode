import { requestWithRetry as request } from "./request.ts";

export interface ChatSessionStart {
  session_id: string;
  opener: string;
  briefing: string;
  round_type: string;
  max_turns: number;
}

export interface ChatTurnResponse {
  reply: string;
  turn_count: number;
  turns_left: number;
}

export interface ChatReport {
  overall_score?: number;
  breakdown?: Record<string, number>;
  strengths?: string[];
  improvements?: string[];
  verdict?: string;
}

export interface ChatEndResponse {
  report: ChatReport;
  final_score: number;
  xp_gained: number;
  level?: number;
  new_badges: string[];
  streak?: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export const interviewChatApi = {
  start(
    roundType: string,
    companyTarget = "general",
    jobRole = "Software Engineer",
    difficulty = "medium",
  ): Promise<ChatSessionStart> {
    return request("/api/v1/interview-chat/start", {
      method: "POST",
      body: JSON.stringify({
        round_type: roundType,
        company_target: companyTarget,
        job_role: jobRole,
        difficulty,
      }),
    });
  },

  submitTurn(sessionId: string, message: string): Promise<ChatTurnResponse> {
    return request(`/api/v1/interview-chat/${sessionId}/turn`, {
      method: "POST",
      body: JSON.stringify({ message }),
    });
  },

  end(sessionId: string): Promise<ChatEndResponse> {
    return request(`/api/v1/interview-chat/${sessionId}/end`, { method: "POST" });
  },

  getSession(
    sessionId: string,
  ): Promise<{ session: Record<string, unknown> & { messages: ChatMessage[] } }> {
    return request(`/api/v1/interview-chat/${sessionId}`);
  },
};
