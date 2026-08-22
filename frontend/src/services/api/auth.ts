import { requestWithRetry as request, clearApiCache } from "./request.ts";
import type {
  AuthUser,
  LoginResponse,
  RegisterResponse,
  OnboardingStatus,
  OnboardingData,
} from "./types.ts";

export const authApi = {
  register(
    email: string,
    password: string,
    name: string,
  ): Promise<RegisterResponse> {
    return request("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    });
  },

  login(email: string, password: string): Promise<LoginResponse> {
    return request("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },

  logout(): Promise<void> {
    return request("/api/v1/auth/logout", { method: "POST" });
  },

  getMe(): Promise<AuthUser> {
    return request("/api/v1/auth/me");
  },

  updateProfile(name: string, email: string): Promise<AuthUser> {
    return request("/api/v1/auth/update-profile", {
      method: "POST",
      body: JSON.stringify({ name, email }),
    });
  },

  changePassword(
    currentPassword: string,
    newPassword: string,
  ): Promise<{ message: string }> {
    return request("/api/v1/auth/change-password", {
      method: "POST",
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
      }),
    });
  },

  forgotPassword(email: string): Promise<{ message: string }> {
    return request("/api/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  },

  resetPassword(
    email: string,
    token: string,
    newPassword: string,
  ): Promise<{ message: string }> {
    return request("/api/v1/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ email, token, new_password: newPassword }),
    });
  },

  onboardingStatus(): Promise<OnboardingStatus> {
    return request("/api/v1/auth/onboarding-status");
  },

  onboardingComplete(data: OnboardingData): Promise<{ message: string }> {
    return request("/api/v1/auth/onboarding-complete", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  clearCache(): void {
    clearApiCache();
  },
};
