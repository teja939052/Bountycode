import { describe, it, expect } from "vitest";
import { validateEmail, validatePassword, validateRequired, validateForm } from "./validation";

describe("validateEmail", () => {
  it("accepts valid email", () => {
    expect(validateEmail("user@example.com")).toBe(true);
  });

  it("rejects email without @", () => {
    expect(validateEmail("userexample.com")).toBe(false);
  });

  it("rejects email without domain", () => {
    expect(validateEmail("user@")).toBe(false);
  });

  it("rejects empty string", () => {
    expect(validateEmail("")).toBe(false);
  });

  it("rejects email with spaces", () => {
    expect(validateEmail("user @example.com")).toBe(false);
  });
});

describe("validatePassword", () => {
  it("accepts valid password", () => {
    expect(validatePassword("Strong123")).toBe(true);
  });

  it("rejects password shorter than 8 chars", () => {
    expect(validatePassword("Ab1")).toBe(false);
  });

  it("rejects password without uppercase", () => {
    expect(validatePassword("strong123")).toBe(false);
  });

  it("rejects password without number", () => {
    expect(validatePassword("StrongPass")).toBe(false);
  });

  it("accepts password with special chars", () => {
    expect(validatePassword("Strong1!")).toBe(true);
  });
});

describe("validateRequired", () => {
  it("accepts non-empty string", () => {
    expect(validateRequired("hello")).toBe(true);
  });

  it("rejects empty string", () => {
    expect(validateRequired("")).toBe(false);
  });

  it("rejects whitespace-only string", () => {
    expect(validateRequired("   ")).toBe(false);
  });

  it("rejects null", () => {
    expect(validateRequired(null)).toBe(false);
  });

  it("rejects undefined", () => {
    expect(validateRequired(undefined)).toBe(false);
  });

  it("accepts zero", () => {
    expect(validateRequired(0)).toBe(true);
  });

  it("accepts array with items", () => {
    expect(validateRequired([1, 2, 3])).toBe(true);
  });
});

describe("validateForm", () => {
  it("returns null when all validations pass", () => {
    const result = validateForm([
      { name: "email", value: "user@example.com", rules: [{ type: "email", message: "Invalid email" }] },
      { name: "password", value: "Strong123", rules: [{ type: "password" }] },
    ]);
    expect(result).toBeNull();
  });

  it("returns errors for missing required fields", () => {
    const result = validateForm([
      { name: "name", value: "", rules: [{ type: "required", message: "Name is required" }] },
    ]);
    expect(result).toEqual({ name: "Name is required" });
  });

  it("returns error for invalid email", () => {
    const result = validateForm([
      { name: "email", value: "bad", rules: [{ type: "email", message: "Invalid email" }] },
    ]);
    expect(result).toEqual({ email: "Invalid email" });
  });

  it("returns error for too-short value", () => {
    const result = validateForm([
      { name: "username", value: "ab", rules: [{ type: "minLength", value: 3, message: "Too short" }] },
    ]);
    expect(result).toEqual({ username: "Too short" });
  });

  it("skips validation for empty optional fields", () => {
    const result = validateForm([
      { name: "bio", value: "", rules: [{ type: "minLength", value: 5 }] },
    ]);
    expect(result).toBeNull();
  });

  it("uses default messages when none provided", () => {
    const result = validateForm([
      { name: "email", value: "", rules: [{ type: "required" }] },
    ]);
    expect(result).toEqual({ email: "email is required" });
  });

  it("returns first error per field only", () => {
    const result = validateForm([
      {
        name: "email",
        value: "",
        rules: [
          { type: "required", message: "Required" },
          { type: "email", message: "Invalid" },
        ],
      },
    ]);
    expect(result).toEqual({ email: "Required" });
  });
});
