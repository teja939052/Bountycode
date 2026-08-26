import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Skeleton, { CardSkeleton, StatsSkeleton, QuestionCardSkeleton, DashboardCardSkeleton } from "./Skeleton";

describe("Skeleton", () => {
  it("renders single line by default", () => {
    const { container } = render(<Skeleton />);
    const el = container.firstElementChild;
    expect(el).toBeInTheDocument();
    expect(el).toHaveClass("animate-pulse");
  });

  it("renders multiple lines", () => {
    const { container } = render(<Skeleton lines={3} />);
    const wrapper = container.firstElementChild;
    expect(wrapper).toHaveClass("space-y-3");
    const lines = wrapper!.querySelectorAll("div");
    expect(lines.length).toBe(3);
  });

  it("renders heading variant", () => {
    const { container } = render(<Skeleton variant="heading" />);
    const el = container.firstElementChild;
    expect(el).toHaveClass("h-8");
  });

  it("renders avatar variant", () => {
    const { container } = render(<Skeleton variant="avatar" />);
    const el = container.firstElementChild;
    expect(el).toHaveClass("h-12");
    expect(el).toHaveClass("w-12");
    expect(el).toHaveClass("rounded-full");
  });

  it("renders card variant", () => {
    const { container } = render(<Skeleton variant="card" />);
    const el = container.firstElementChild;
    expect(el).toHaveClass("h-40");
  });

  it("renders button variant", () => {
    const { container } = render(<Skeleton variant="button" />);
    const el = container.firstElementChild;
    expect(el).toHaveClass("h-12");
    expect(el).toHaveClass("w-32");
  });

  it("applies custom className", () => {
    const { container } = render(<Skeleton className="my-class" />);
    expect(container.firstElementChild).toHaveClass("my-class");
  });

  it("last line is shorter in multi-line mode", () => {
    const { container } = render(<Skeleton lines={2} />);
    const lines = container.firstElementChild!.querySelectorAll("div");
    expect(lines[0]).toHaveClass("w-full");
    expect(lines[1]).toHaveClass("w-3/4");
  });
});

describe("CardSkeleton", () => {
  it("renders a card skeleton", () => {
    const { container } = render(<CardSkeleton />);
    const card = container.querySelector(".card");
    expect(card).toBeInTheDocument();
    expect(card).toHaveClass("animate-pulse");
  });

  it("contains content skeleton elements", () => {
    const { container } = render(<CardSkeleton />);
    const innerDivs = container.querySelectorAll(".bg-brand-primary\\/10");
    expect(innerDivs.length).toBeGreaterThan(0);
  });
});

describe("StatsSkeleton", () => {
  it("renders 4 stat cards", () => {
    const { container } = render(<StatsSkeleton />);
    const cards = container.querySelectorAll(".card");
    expect(cards.length).toBe(4);
  });
});

describe("QuestionCardSkeleton", () => {
  it("renders default 5 rows", () => {
    const { container } = render(<QuestionCardSkeleton />);
    const rows = container.querySelectorAll(".animate-pulse");
    expect(rows.length).toBe(5);
  });

  it("renders custom count", () => {
    const { container } = render(<QuestionCardSkeleton count={2} />);
    const rows = container.querySelectorAll(".animate-pulse");
    expect(rows.length).toBe(2);
  });
});

describe("DashboardCardSkeleton", () => {
  it("renders default 4 cards", () => {
    const { container } = render(<DashboardCardSkeleton />);
    const cards = container.querySelectorAll(".card");
    expect(cards.length).toBe(4);
  });
});
