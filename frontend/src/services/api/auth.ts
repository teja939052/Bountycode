import { requestWithRetry as request, requestBlob, clearApiCache } from "./request.ts";


export const authApi = {
  register(email, password, name) {
    return request("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    });
  },

  login(email, password) {
    return request("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },

  logout() {
    return request("/api/v1/auth/logout", { method: "POST" });
  },

  getMe() {
    return request("/api/v1/auth/me");
  },

  updateProfile(name, email) {
    return request("/api/v1/auth/update-profile", {
      method: "POST",
      body: JSON.stringify({ name, email }),
    });
  },

  changePassword(currentPassword, newPassword) {
    return request("/api/v1/auth/change-password", {
      method: "POST",
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    });
  },

  forgotPassword(email) {
    return request("/api/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  },

  resetPassword(email, token, newPassword) {
    return request("/api/v1/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ email, token, new_password: newPassword }),
    });
  },

  onboardingStatus() {
    return request("/api/v1/auth/onboarding-status");
  },

  onboardingComplete(data) {
    return request("/api/v1/auth/onboarding-complete", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  clearCache() {
    clearApiCache();
  },
};