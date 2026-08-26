import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("../services/api/auth.ts", () => ({
  authApi: {
    getMe: vi.fn(),
    logout: vi.fn(),
    login: vi.fn(),
  },
}));

import useAuthStore from "./authStore";
import { authApi } from "../services/api/auth.ts";

describe("authStore", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useAuthStore.setState({ user: null, loading: true });
  });

  it("starts with null user and loading true", () => {
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
    expect(state.loading).toBe(true);
  });

  it("setAuth sets user and loading false", () => {
    const user = { id: "1", email: "test@test.com", name: "Test", plan: "free" } as any;
    useAuthStore.getState().setAuth(user);
    expect(useAuthStore.getState().user).toEqual(user);
    expect(useAuthStore.getState().loading).toBe(false);
  });

  it("logout clears user and calls authApi.logout", async () => {
    vi.mocked(authApi.logout).mockResolvedValue(undefined as any);
    useAuthStore.setState({ user: { id: "1" } as any, loading: false });

    await useAuthStore.getState().logout();

    expect(authApi.logout).toHaveBeenCalled();
    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().loading).toBe(false);
  });

  it("logout handles API error gracefully", async () => {
    vi.mocked(authApi.logout).mockRejectedValue(new Error("Network error"));
    useAuthStore.setState({ user: { id: "1" } as any, loading: false });

    await useAuthStore.getState().logout();

    expect(useAuthStore.getState().user).toBeNull();
  });

  it("loadUser sets user on success", async () => {
    const mockUser = { id: "1", email: "test@test.com", name: "Test User", plan: "free" };
    vi.mocked(authApi.getMe).mockResolvedValue(mockUser as any);

    await useAuthStore.getState().loadUser();

    expect(useAuthStore.getState().user).toEqual(mockUser);
    expect(useAuthStore.getState().loading).toBe(false);
  });

  it("loadUser clears user on failure", async () => {
    vi.mocked(authApi.getMe).mockRejectedValue(new Error("Unauthorized"));

    await useAuthStore.getState().loadUser();

    expect(useAuthStore.getState().user).toBeNull();
    expect(useAuthStore.getState().loading).toBe(false);
  });

  it("refreshToken rejects and clears user on failure", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue({
      ok: false,
    } as Response);

    await expect(useAuthStore.getState().refreshToken()).rejects.toThrow("Session expired");
    expect(useAuthStore.getState().user).toBeNull();
  });
});
