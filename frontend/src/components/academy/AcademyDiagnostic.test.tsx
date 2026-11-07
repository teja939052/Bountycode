import { beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import AcademyDiagnostic from "./AcademyDiagnostic";
import api from "../../services/api";

vi.mock("../../services/api", () => ({
  default: {
    academy: {
      getLatestDiagnostic: vi.fn(),
      startDiagnostic: vi.fn(),
      answerDiagnostic: vi.fn(),
      completeDiagnostic: vi.fn(),
    },
  },
}));

function renderDiagnostic() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <AcademyDiagnostic />
    </QueryClientProvider>,
  );
}

describe("AcademyDiagnostic confidence tracking", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.academy.getLatestDiagnostic).mockResolvedValue({ success: true, result: null });
    vi.mocked(api.academy.startDiagnostic).mockResolvedValue({
      success: true,
      diagnostic: {
        diagnostic_id: "diag-test",
        total_questions: 1,
        questions: [{
          id: "q1",
          index: 0,
          title: "Quant",
          question: "What is 2 + 2?",
          topic: "Arithmetic",
          domain: "quantitative_aptitude",
          difficulty: "easy",
          type: "mcq",
          options: ["3", "4"],
        }],
      },
    });
    vi.mocked(api.academy.answerDiagnostic).mockResolvedValue({ success: true });
    vi.mocked(api.academy.completeDiagnostic).mockResolvedValue({
      success: true,
      result: { overall_score: 100, correct_answers: 1, total_questions: 1, skills: [], evidence: { average_time_seconds: 2, confidence_score: 100, weakest_skill: "quantitative_aptitude" } },
    });
  });

  it("requires confidence and sends it with response timing", async () => {
    const user = userEvent.setup();
    renderDiagnostic();

    await user.click(await screen.findByRole("button", { name: /start diagnostic/i }));
    await user.click(await screen.findByRole("button", { name: /B\.?\s*4/i }));
    await user.click(screen.getByRole("button", { name: /5 certain/i }));
    await user.click(screen.getByRole("button", { name: /finish diagnostic/i }));

    expect(api.academy.answerDiagnostic).toHaveBeenCalledWith(
      "diag-test",
      "q1",
      "1",
      expect.objectContaining({ confidence: 5, time_taken_seconds: expect.any(Number) }),
    );
    expect(api.academy.completeDiagnostic).toHaveBeenCalledWith("diag-test");
    expect(await screen.findByText("Evidence beyond correctness")).toBeInTheDocument();
  });
});
