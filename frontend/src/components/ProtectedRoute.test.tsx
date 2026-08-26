import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";
import useAuthStore from "../store/authStore";

vi.mock("../store/authStore");

function renderWithRouter(ui: React.ReactElement) {
  return render(<MemoryRouter>{ui}</MemoryRouter>);
}

describe("ProtectedRoute", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows spinner while loading", () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: null,
      loading: true,
      setAuth: vi.fn(),
      logout: vi.fn(),
      loadUser: vi.fn(),
      refreshToken: vi.fn(),
    });

    renderWithRouter(<ProtectedRoute><div>Protected</div></ProtectedRoute>);
    expect(screen.queryByText("Protected")).not.toBeInTheDocument();
    const spinner = document.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it("redirects to /login when no user", () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: null,
      loading: false,
      setAuth: vi.fn(),
      logout: vi.fn(),
      loadUser: vi.fn(),
      refreshToken: vi.fn(),
    });

    renderWithRouter(<ProtectedRoute><div>Protected</div></ProtectedRoute>);
    expect(screen.queryByText("Protected")).not.toBeInTheDocument();
  });

  it("renders children when authenticated", () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: "1", email: "test@test.com", name: "Test", plan: "free" },
      loading: false,
      setAuth: vi.fn(),
      logout: vi.fn(),
      loadUser: vi.fn(),
      refreshToken: vi.fn(),
    });

    renderWithRouter(<ProtectedRoute><div>Protected Content</div></ProtectedRoute>);
    expect(screen.getByText("Protected Content")).toBeInTheDocument();
  });

  it("renders nothing when no children", () => {
    vi.mocked(useAuthStore).mockReturnValue({
      user: { id: "1", email: "test@test.com", name: "Test", plan: "free" },
      loading: false,
      setAuth: vi.fn(),
      logout: vi.fn(),
      loadUser: vi.fn(),
      refreshToken: vi.fn(),
    });

    const { container } = renderWithRouter(<ProtectedRoute />);
    expect(container.innerHTML).toBe("");
  });
});
