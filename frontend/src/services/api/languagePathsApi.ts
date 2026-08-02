const API_BASE = import.meta.env.VITE_API_URL || "";

async function req(endpoint, options: Record<string, any> = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };
  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers, credentials: "include" });
  if (!response.ok) { const err = await response.json().catch(() => ({ detail: "Request failed" })); throw new Error(err.detail || "Request failed"); }
  return response.json();
}

export const languagePathsApi = {
  getLanguages: () => req("/api/v1/languages/"),
  getLanguagePath: (languageId) => req(`/api/v1/languages/${languageId}`),
  getLanguageLevels: (languageId) => req(`/api/v1/languages/${languageId}/levels`),
  getModuleDetail: (languageId, moduleIndex) => req(`/api/v1/languages/${languageId}/modules/${moduleIndex}`),
  getProgress: (languageId) => req(`/api/v1/languages/${languageId}/progress`),
  completeModule: (languageId, moduleIndex) => req(`/api/v1/languages/${languageId}/modules/${moduleIndex}/complete`, { method: "POST" }),
  getRecommendations: (languageId) => req(`/api/v1/languages/${languageId}/recommendations`),
};

export default languagePathsApi;