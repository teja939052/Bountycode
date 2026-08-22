import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Input from "./Input";

describe("Input", () => {
  it("renders with label", () => {
    render(<Input label="Email" name="email" />);
    expect(screen.getByText("Email")).toBeInTheDocument();
    expect(screen.getByRole("textbox")).toHaveAttribute("name", "email");
  });

  it("generates id from name prop when id not provided", () => {
    render(<Input label="First Name" name="firstName" />);
    const input = screen.getByRole("textbox");
    expect(input).toHaveAttribute("id", "firstName");
  });

  it("uses provided id", () => {
    render(<Input label="Email" id="email-input" name="email" />);
    expect(screen.getByRole("textbox")).toHaveAttribute("id", "email-input");
  });

  it("shows error message", () => {
    render(<Input label="Email" error="Email is required" name="email" />);
    expect(screen.getByText("Email is required")).toBeInTheDocument();
    expect(screen.getByRole("textbox")).toHaveAttribute("aria-invalid", "true");
  });

  it("does not show error when error is not provided", () => {
    render(<Input label="Email" name="email" />);
    expect(screen.getByRole("textbox")).toHaveAttribute("aria-invalid", "false");
  });

  it("applies custom className to input", () => {
    render(<Input className="my-input" name="email" />);
    const input = screen.getByRole("textbox");
    expect(input).toHaveClass("my-input");
  });
});
