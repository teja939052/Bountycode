import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Modal from "./Modal";

describe("Modal", () => {
  it("does not render when isOpen is false", () => {
    render(<Modal isOpen={false} onClose={vi.fn()} title="Test"><p>Content</p></Modal>);
    expect(screen.queryByText("Test")).not.toBeInTheDocument();
  });

  it("renders when isOpen is true", () => {
    render(<Modal isOpen={true} onClose={vi.fn()} title="Test Modal"><p>Modal content</p></Modal>);
    expect(screen.getByText("Test Modal")).toBeInTheDocument();
    expect(screen.getByText("Modal content")).toBeInTheDocument();
  });

  it("calls onClose when backdrop is clicked", () => {
    const onClose = vi.fn();
    render(<Modal isOpen={true} onClose={onClose} title="Test"><p>Content</p></Modal>);
    const backdrop = document.querySelector('[aria-hidden="true"]');
    expect(backdrop).toBeInTheDocument();
    fireEvent.click(backdrop!);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when X button is clicked", () => {
    const onClose = vi.fn();
    render(<Modal isOpen={true} onClose={onClose} title="Test"><p>Content</p></Modal>);
    const closeBtn = screen.getByRole("button", { name: /close dialog/i });
    fireEvent.click(closeBtn);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("has correct ARIA attributes", () => {
    render(<Modal isOpen={true} onClose={vi.fn()} title="Accessible"><p>Content</p></Modal>);
    const dialog = screen.getByRole("dialog");
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(dialog).toHaveAttribute("aria-labelledby", "modal-title");
  });

  it("renders children inside scrollable area", () => {
    render(
      <Modal isOpen={true} onClose={vi.fn()} title="With Children">
        <div data-testid="child-1">First</div>
        <div data-testid="child-2">Second</div>
      </Modal>
    );
    expect(screen.getByTestId("child-1")).toBeInTheDocument();
    expect(screen.getByTestId("child-2")).toBeInTheDocument();
  });
});
