import { requestWithRetry as request } from "./request.ts";

export const studyApi = {
  getCategories() {
    return request("/api/v1/study/categories");
  },

  getArticles(params: { category?: string; q?: string } = {}) {
    const query = new URLSearchParams();
    if (params.category) query.append("category", params.category);
    if (params.q) query.append("q", params.q);
    const qs = query.toString();
    return request(`/api/v1/study/articles${qs ? `?${qs}` : ""}`);
  },

  getArticle(articleId: string) {
    return request(`/api/v1/study/articles/${articleId}`);
  },

  getCategoryArticles(categoryId: string) {
    return request(`/api/v1/study/categories/${categoryId}/articles`);
  },

  getRelatedArticles(params: { language?: string; q?: string; limit?: number } = {}) {
    const query = new URLSearchParams();
    if (params.language) query.append("language", params.language);
    if (params.q) query.append("q", params.q);
    if (params.limit) query.append("limit", String(params.limit));
    const qs = query.toString();
    return request(`/api/v1/study/related${qs ? `?${qs}` : ""}`);
  },
};
