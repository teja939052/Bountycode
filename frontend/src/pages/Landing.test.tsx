import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import Landing from "./Landing";

function renderLanding() {
  return render(
    <MemoryRouter>
      <Landing />
    </MemoryRouter>,
  );
}

const REGISTERED = new Set([
  "/",
  "/login",
  "/register",
  "/percentages-academy",
  "/lessons",
  "/aptitude",
  "/mock-oa",
  "/skills",
  "/practice",
  "/daily-challenge",
  "/tower",
  "/leaderboard",
  "/pricing",
  "/terms",
  "/privacy",
]);

describe("Landing (locked composition + honesty rules)", () => {
  it("keeps the locked headline with gold on 'to your first offer.'", () => {
    const { container } = renderLanding();
    const h1 = container.querySelector("h1")!;
    expect(h1.textContent).toContain("From your first line of code");
    expect(h1.textContent).toContain("to your first offer.");

    const gold = Array.from(h1.querySelectorAll("span")).find(
      (el) => el.textContent === "to your first offer.",
    )!;
    expect(gold).toBeTruthy();
    expect(window.getComputedStyle(gold).color).toBe("rgb(212, 168, 67)");
  });

  it("renders the wallpaper-free hero on the pink base", () => {
    const { container } = renderLanding();

    const hero = container.querySelector("section.spring-hero")!;
    expect(window.getComputedStyle(hero).backgroundColor).toBe("rgb(251, 228, 236)");

    // No stock wallpaper: the hero must not load any photographic image.
    expect(container.querySelectorAll("img")).toHaveLength(0);
    expect(container.innerHTML).not.toMatch(/unsplash/i);
  });

  it("renders one page nav and the Diagnose → Learn → Practice → Get Hired strip", () => {
    const { container } = renderLanding();
    expect(container.querySelectorAll("header")).toHaveLength(1);

    const strip = screen.getByLabelText("How BountyCode works");
    expect(strip.textContent).toContain("Diagnose");
    expect(strip.textContent).toContain("Learn");
    expect(strip.textContent).toContain("Practice");
    expect(strip.textContent).toContain("Get Hired");
  });

  it("links only to registered routes and never mints local progress", () => {
    const { container } = renderLanding();
    const hrefs = Array.from(container.querySelectorAll("a[href^='/']")).map(
      (a) => a.getAttribute("href")!,
    );
    const unknown = hrefs.filter((href) => !REGISTERED.has(href));
    expect(unknown).toEqual([]);
    expect(hrefs.length).toBeGreaterThan(10);
    expect(window.localStorage.setItem).not.toHaveBeenCalled();
  });

  it("does not claim FAANG positioning", () => {
    const { container } = renderLanding();
    expect(container.textContent!.toLowerCase()).not.toContain("faang");
  });

  it("the lesson predict demo grades a real answer", () => {
    renderLanding();
    fireEvent.click(screen.getByRole("button", { name: "6" }));
    expect(screen.getByText("Correct. 0 + 1 + 2 + 3 = 6.")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "10" }));
    expect(screen.getByText(/Not yet\./)).toBeTruthy();
  });

  it("shows the 12-station loop in order", () => {
    const { container } = renderLanding();
    const figure = container.querySelector("figure")!;
    const text = figure.textContent!;
    const order = [
      "Company",
      "Blueprint",
      "Skill",
      "Pattern",
      "Interactive",
      "Lesson",
      "Practice",
      "Assessment",
      "Evidence",
      "Diagnosis",
      "Repair",
      "Retest",
      "Readiness",
    ];
    let cursor = -1;
    for (const label of order) {
      const at = text.indexOf(label, cursor + 1);
      expect(at, `${label} should appear in order`).toBeGreaterThan(cursor);
      cursor = at;
    }
    expect(figure.querySelectorAll("circle").length).toBeGreaterThanOrEqual(24);
  });
});
