import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { formatTime, formatMemory, parseErrorLine, detectErrorType, normalizeTopics, getStarterProblemType, CodeCache } from "./useCompiler";

describe("formatTime", () => {
  it("formats seconds only", () => {
    expect(formatTime(0)).toBe("0s");
    expect(formatTime(45)).toBe("45s");
    expect(formatTime(59)).toBe("59s");
  });

  it("formats minutes and seconds", () => {
    expect(formatTime(60)).toBe("1m 0s");
    expect(formatTime(90)).toBe("1m 30s");
    expect(formatTime(3599)).toBe("59m 59s");
  });

  it("formats hours, minutes, and seconds", () => {
    expect(formatTime(3600)).toBe("1h 0m 0s");
    expect(formatTime(3661)).toBe("1h 1m 1s");
    expect(formatTime(7200)).toBe("2h 0m 0s");
  });
});

describe("formatMemory", () => {
  it("returns N/A for null", () => {
    expect(formatMemory(null)).toBe("N/A");
  });

  it("formats bytes", () => {
    expect(formatMemory(512)).toBe("512 B");
  });

  it("formats kilobytes", () => {
    expect(formatMemory(1024)).toBe("1.0 KB");
    expect(formatMemory(1536)).toBe("1.5 KB");
  });

  it("formats megabytes", () => {
    expect(formatMemory(1048576)).toBe("1.0 MB");
    expect(formatMemory(2621440)).toBe("2.5 MB");
  });
});

describe("parseErrorLine", () => {
  it("returns null for empty message", () => {
    expect(parseErrorLine("")).toBeNull();
  });

  it("parses 'line N' pattern", () => {
    expect(parseErrorLine("SyntaxError at line 42")).toBe(42);
  });

  it("parses 'Line N' pattern (capitalized)", () => {
    expect(parseErrorLine("Line 15: unexpected token")).toBe(15);
  });

  it("parses 'at line N' pattern", () => {
    expect(parseErrorLine("at line 7")).toBe(7);
  });

  it("parses ':N:N' pattern", () => {
    expect(parseErrorLine("file.py:10:5: error")).toBe(10);
  });

  it("parses '(N,N)' pattern", () => {
    expect(parseErrorLine("error at (3,12)")).toBe(3);
  });

  it("returns null when no pattern matches", () => {
    expect(parseErrorLine("something went wrong")).toBeNull();
  });
});

describe("detectErrorType", () => {
  it("detects compile error", () => {
    expect(detectErrorType(undefined, "syntax error", undefined)).toBe("compile");
  });

  it("detects TLE", () => {
    expect(detectErrorType("Time Limit Exceeded", undefined, undefined)).toBe("tle");
  });

  it("detects timeout", () => {
    expect(detectErrorType("timeout occurred", undefined, undefined)).toBe("tle");
  });

  it("detects MLE", () => {
    expect(detectErrorType("Memory Limit Exceeded", undefined, undefined)).toBe("mle");
  });

  it("detects runtime error with non-zero exit", () => {
    expect(detectErrorType(undefined, undefined, 1)).toBe("runtime");
  });

  it("returns runtime as default", () => {
    expect(detectErrorType(undefined, undefined, undefined)).toBe("runtime");
  });
});

describe("normalizeTopics", () => {
  it("returns empty array for null", () => {
    expect(normalizeTopics(null)).toEqual([]);
  });

  it("normalizes topics array", () => {
    expect(normalizeTopics({ topics: ["Arrays", " Strings ", "DP"] })).toEqual(["Arrays", "Strings", "DP"]);
  });

  it("uses topic field as fallback", () => {
    expect(normalizeTopics({ topic: "Trees" })).toEqual(["Trees"]);
  });

  it("combines topics and topic", () => {
    expect(normalizeTopics({ topics: ["A"], topic: "B" })).toEqual(["A", "B"]);
  });

  it("filters empty strings", () => {
    expect(normalizeTopics({ topics: ["A", "", "  ", "B"] })).toEqual(["A", "B"]);
  });
});

describe("getStarterProblemType", () => {
  it("returns linked_list for linked list topics", () => {
    expect(getStarterProblemType(["Linked List"])).toBe("linked_list");
    expect(getStarterProblemType(["linked_list"])).toBe("linked_list");
  });

  it("returns binary_tree for tree topics", () => {
    expect(getStarterProblemType(["Binary Tree"])).toBe("binary_tree");
    expect(getStarterProblemType(["BST"])).toBe("binary_tree");
  });

  it("returns graph for graph topics", () => {
    expect(getStarterProblemType(["Graph"])).toBe("graph");
    expect(getStarterProblemType(["BFS"])).toBe("graph");
    expect(getStarterProblemType(["DFS"])).toBe("graph");
  });

  it("returns dp for dynamic programming topics", () => {
    expect(getStarterProblemType(["Dynamic Programming"])).toBe("dp");
    expect(getStarterProblemType(["DP"])).toBe("dp");
  });

  it("returns class as default", () => {
    expect(getStarterProblemType(["Arrays"])).toBe("class");
    expect(getStarterProblemType([])).toBe("class");
  });
});

describe("CodeCache", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("getKey generates correct key", () => {
    expect(CodeCache.getKey("p1", "python")).toBe("pp_code_p1_python");
    expect(CodeCache.getKey(undefined, "js")).toBe("pp_code_default_js");
  });

  it("save and load round-trip", () => {
    CodeCache.save("p1", "python", "print('hello')");
    const loaded = CodeCache.load("p1", "python");
    expect(loaded).toBe("print('hello')");
  });

  it("load returns null for missing key", () => {
    expect(CodeCache.load("nonexistent", "python")).toBeNull();
  });

  it("remove deletes cached code", () => {
    CodeCache.save("p1", "python", "code");
    CodeCache.remove("p1", "python");
    expect(CodeCache.load("p1", "python")).toBeNull();
  });

  it("load returns null for expired cache", () => {
    const expired = JSON.stringify({ code: "old", ts: Date.now() - 8 * 86400000 });
    localStorage.setItem("pp_code_p1_python", expired);
    expect(CodeCache.load("p1", "python")).toBeNull();
  });

  it("save does not throw on localStorage error", () => {
    const spy = vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("QuotaExceededError");
    });
    expect(() => CodeCache.save("p1", "python", "code")).not.toThrow();
    spy.mockRestore();
  });
});
