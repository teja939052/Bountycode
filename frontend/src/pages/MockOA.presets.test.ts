import { describe, expect, it } from "vitest";
import { COMPANY_PRESETS } from "./MockOA";

describe("company-wise MockOA presets", () => {
  it("contains distinct TCS Foundation and Advanced tracks", () => {
    const foundation = COMPANY_PRESETS.find((preset) => preset.id === "tcs_foundation");
    const advanced = COMPANY_PRESETS.find((preset) => preset.id === "tcs_advanced");

    expect(foundation).toMatchObject({ backendCompany: "tcs", track: "foundation", duration: 75 });
    expect(advanced).toMatchObject({ backendCompany: "tcs", track: "advanced", duration: 115 });
    expect(foundation?.sourceUrl).toContain("tcs.com");
  });

  it("keeps Wipro and Accenture provenance visible", () => {
    const wipro = COMPANY_PRESETS.find((preset) => preset.id === "wipro");
    const accenture = COMPANY_PRESETS.find((preset) => preset.id === "accenture");

    expect(wipro).toMatchObject({ backendCompany: "wipro", duration: 80 });
    expect(accenture).toMatchObject({ backendCompany: "accenture" });
    expect(accenture?.sourceLabel).toMatch(/invitation-dependent/i);
    expect(accenture?.sections).toEqual(expect.arrayContaining(["Technical", "Coding"]));
  });
});
