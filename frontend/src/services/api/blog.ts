import { requestWithRetry } from "./request.ts";

export const blogApi = {
  list: (tag?: string) =>
    requestWithRetry(
      tag ? `/api/v1/blog?tag=${encodeURIComponent(tag)}` : "/api/v1/blog",
    ),
  get: (slug: string) =>
    requestWithRetry(`/api/v1/blog/${encodeURIComponent(slug)}`),
};
