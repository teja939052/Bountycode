// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export interface SearchResult {
  id?: string;
  title?: string;
  type?: string;
  topic?: string;
  difficulty?: string;
  category?: string;
  url?: string;
}

export interface GlobalSearchResponse {
  query: string;
  total: number;
  results: {
    questions?: SearchResult[];
    lessons?: SearchResult[];
    companies?: SearchResult[];
    articles?: SearchResult[];
  };
}

export const searchApi = {
  global(query: string, types?: string): Promise<GlobalSearchResponse> {
    const qs = new URLSearchParams();
    qs.set("q", query);
    if (types) qs.set("types", types);
    return request(`/api/v1/search/global?${qs.toString()}`);
  },

  questions(query: string, filters?: { topic?: string; difficulty?: string; type?: string; limit?: number }): Promise<any> {
    const qs = new URLSearchParams();
    qs.set("q", query);
    if (filters?.topic) qs.set("topic", filters.topic);
    if (filters?.difficulty) qs.set("difficulty", filters.difficulty);
    if (filters?.type) qs.set("type", filters.type);
    if (filters?.limit) qs.set("limit", String(filters.limit));
    return request(`/api/v1/search/questions?${qs.toString()}`);
  },
};
