import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Spinner from "./Spinner";

describe("Spinner", () => {
  it("renders with default size", () => {
    const { container } = render(<Spinner />);
    const spinner = container.querySelector(".animate-spin");
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass("w-8", "h-8");
  });

  it("renders with small size", () => {
    const { container } = render(<Spinner size="sm" />);
    const spinner = container.querySelector(".animate-spin");
    expect(spinner).toHaveClass("w-5", "h-5");
  });

  it("renders with large size", () => {
    const { container } = render(<Spinner size="lg" />);
    const spinner = container.querySelector(".animate-spin");
    expect(spinner).toHaveClass("w-12", "h-12");
  });

  it("renders with custom numeric size", () => {
    const { container } = render(<Spinner size={32} />);
    const spinner = container.querySelector(".animate-spin");
    expect(spinner).toHaveStyle({ width: "32px", height: "32px" });
  });

  it("applies custom className", () => {
    const { container } = render(<Spinner className="my-spinner" />);
    const wrapper = container.querySelector(".my-spinner");
    expect(wrapper).toBeInTheDocument();
  });
});
