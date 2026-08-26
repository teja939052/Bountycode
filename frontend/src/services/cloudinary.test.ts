import { describe, it, expect } from "vitest";
import { cloudinaryImage, cloudinaryVideo, optimizeImage, CLOUDINARY_CLOUD_NAME } from "./cloudinary";

describe("CLOUDINARY_CLOUD_NAME", () => {
  it("is defined", () => {
    expect(CLOUDINARY_CLOUD_NAME).toBe("bountycode");
  });
});

describe("cloudinaryImage", () => {
  it("generates URL with default options", () => {
    const url = cloudinaryImage("test-image");
    expect(url).toContain("https://res.cloudinary.com/bountycode/image/upload/");
    expect(url).toContain("w_auto");
    expect(url).toContain("h_auto");
    expect(url).toContain("q_auto");
    expect(url).toContain("f_auto");
    expect(url).toContain("test-image");
  });

  it("generates URL with custom width", () => {
    const url = cloudinaryImage("logo", { width: 200 });
    expect(url).toContain("w_200");
  });

  it("generates URL with custom height", () => {
    const url = cloudinaryImage("banner", { height: 400 });
    expect(url).toContain("h_400");
  });

  it("generates URL with custom quality", () => {
    const url = cloudinaryImage("photo", { quality: 80 });
    expect(url).toContain("q_80");
  });

  it("generates URL with custom format", () => {
    const url = cloudinaryImage("icon", { format: "webp" });
    expect(url).toContain("f_webp");
  });

  it("combines multiple options", () => {
    const url = cloudinaryImage("hero", { width: 1200, height: 600, quality: 90, format: "png" });
    expect(url).toContain("w_1200");
    expect(url).toContain("h_600");
    expect(url).toContain("q_90");
    expect(url).toContain("f_png");
  });
});

describe("cloudinaryVideo", () => {
  it("generates video URL with default options", () => {
    const url = cloudinaryVideo("lesson-1");
    expect(url).toContain("https://res.cloudinary.com/bountycode/video/upload/");
    expect(url).toContain("w_auto");
    expect(url).toContain("h_auto");
    expect(url).toContain("q_auto");
    expect(url).toContain("lesson-1");
  });

  it("generates video URL with custom dimensions", () => {
    const url = cloudinaryVideo("tutorial", { width: 1920, height: 1080 });
    expect(url).toContain("w_1920");
    expect(url).toContain("h_1080");
  });
});

describe("optimizeImage", () => {
  it("returns external URLs unchanged", () => {
    const url = "https://example.com/photo.jpg";
    expect(optimizeImage(url)).toBe(url);
  });

  it("converts local png path to cloudinary URL", () => {
    const url = optimizeImage("images/logo.png", 200);
    expect(url).toContain("cloudinary.com");
    expect(url).toContain("w_200");
    expect(url).toContain("f_webp");
  });

  it("converts local jpg path to cloudinary URL", () => {
    const url = optimizeImage("photos/avatar.jpg");
    expect(url).toContain("cloudinary.com");
    expect(url).toContain("w_300");
  });

  it("uses auto format for jpg/jpeg", () => {
    const url = optimizeImage("photo.jpeg");
    expect(url).toContain("f_auto");
  });

  it("uses webp format for png", () => {
    const url = optimizeImage("icon.png");
    expect(url).toContain("f_webp");
  });

  it("uses webp format for gif", () => {
    const url = optimizeImage("animation.gif");
    expect(url).toContain("f_webp");
  });

  it("uses auto format for webp", () => {
    const url = optimizeImage("image.webp");
    expect(url).toContain("f_auto");
  });
});
