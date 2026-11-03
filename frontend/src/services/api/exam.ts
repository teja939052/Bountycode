import { requestWithRetry } from "./request.ts";

export const examApi = {
  start: (body: unknown) => requestWithRetry("/api/v1/exam/start", { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" } }),
  answer: (body: unknown) => requestWithRetry("/api/v1/exam/answer", { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" } }),
  complete: (attemptId: string) => requestWithRetry(`/api/v1/exam/complete?attempt_id=${encodeURIComponent(attemptId)}`, { method: "POST" }),
  report: (attemptId: string) => requestWithRetry(`/api/v1/exam/report/${encodeURIComponent(attemptId)}`),
  history: () => requestWithRetry("/api/v1/exam/history"),
  diagnose: (attemptId: string) => requestWithRetry(`/api/v1/exam/diagnose/${encodeURIComponent(attemptId)}`, { method: "POST" }),
  repair: (topic: string, count: number) => requestWithRetry(`/api/v1/exam/repair/${encodeURIComponent(topic)}?count=${count}`, { method: "POST" }),
  reassess: (topic: string, count: number) => requestWithRetry(`/api/v1/exam/reassess/${encodeURIComponent(topic)}?count=${count}`, { method: "POST" }),
};
