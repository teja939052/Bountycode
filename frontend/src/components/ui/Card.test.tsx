import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { getRarityEmoji, getRarityStars, getRarityColor } from "./Card";

describe("getRarityEmoji", () => {
  it("returns correct emoji for each rarity", () => {
    expect(getRarityEmoji("common")).toBe("⬜");
    expect(getRarityEmoji("uncommon")).toBe("🟢");
    expect(getRarityEmoji("rare")).toBe("🔵");
    expect(getRarityEmoji("epic")).toBe("🟣");
    expect(getRarityEmoji("legendary")).toBe("🟡");
    expect(getRarityEmoji("mythic")).toBe("🩷");
  });

  it("returns default for unknown rarity", () => {
    expect(getRarityEmoji("unknown")).toBe("⬜");
  });
});

describe("getRarityStars", () => {
  it("returns correct star count", () => {
    expect(getRarityStars("common")).toBe("★");
    expect(getRarityStars("uncommon")).toBe("★★");
    expect(getRarityStars("rare")).toBe("★★★");
    expect(getRarityStars("epic")).toBe("★★★★");
    expect(getRarityStars("legendary")).toBe("★★★★★");
    expect(getRarityStars("mythic")).toBe("★★★★★★");
  });

  it("returns default star for unknown rarity", () => {
    expect(getRarityStars("unknown")).toBe("★");
  });
});

describe("getRarityColor", () => {
  it("returns correct color for each rarity", () => {
    expect(getRarityColor("common")).toBe("#9CA3AF");
    expect(getRarityColor("uncommon")).toBe("#22C55E");
    expect(getRarityColor("rare")).toBe("#3B82F6");
    expect(getRarityColor("epic")).toBe("#A855F7");
    expect(getRarityColor("legendary")).toBe("#EAB308");
    expect(getRarityColor("mythic")).toBe("#EC4899");
  });

  it("returns default gray for unknown rarity", () => {
    expect(getRarityColor("unknown")).toBe("#9CA3AF");
  });
});
