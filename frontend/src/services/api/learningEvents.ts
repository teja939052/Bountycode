// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export const learningEventsApi = {
  logInteractionAction(payload: {
    atom_id: string;
    session_id: string;
    interaction_type: string;
    action: string;
    data: Record<string, any>;
    misconception_codes?: string[];
  }) {
    return request<{ success: boolean; diagnosis?: any }>("/api/v1/learning/interaction-action", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  diagnose(payload: {
    atom_id: string;
    session_id: string;
    interaction_type: string;
    action: string;
    data: Record<string, any>;
    misconception_codes?: string[];
  }) {
    return request<{ success: boolean; diagnosis: any }>("/api/v1/learning/diagnose", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
