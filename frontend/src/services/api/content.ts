import { requestWithRetry } from "./request.ts";

export const contentApi = {
  topics: () => requestWithRetry("/api/v1/content/topics"),
  topic: (topicId: string) => requestWithRetry(`/api/v1/content/${encodeURIComponent(topicId)}`),
};
