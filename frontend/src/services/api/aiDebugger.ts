// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export const aiDebuggerApi = {
  creativeMind(payload: {
    problemDescription?: string;
    code?: string;
    language?: string;
    topic?: string;
    mode?: string;
  }): Promise<Record<string, unknown>> {
    return request("/api/v1/ai-debugger/creative-coach", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
