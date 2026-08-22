export const typography = {
  fontFamilies: {
    display: '"Manrope", "Inter", system-ui, sans-serif',
    body: '"Inter", system-ui, sans-serif',
    mono: '"JetBrains Mono", "Fira Code", monospace',
  },
  fontSizes: {
    xs: "0.75rem",     // 12px
    sm: "0.875rem",    // 14px
    base: "1rem",      // 16px
    lg: "1.125rem",    // 18px
    xl: "1.25rem",     // 20px
    "2xl": "1.5rem",   // 24px
    "3xl": "1.875rem", // 30px
    "4xl": "2.25rem",  // 36px
    "5xl": "3rem",     // 48px
  },
  fontWeights: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  lineHeights: {
    tight: 1.1,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
  },
  letterSpacing: {
    tight: "-0.015em",
    normal: "0",
    wide: "0.025em",
    wider: "0.1em",
    widest: "0.2em",
  },
  headings: {
    h1: { size: "4xl", weight: "black", lineHeight: "tight", letterSpacing: "tight" },
    h2: { size: "3xl", weight: "extrabold", lineHeight: "tight", letterSpacing: "tight" },
    h3: { size: "2xl", weight: "bold", lineHeight: "snug", letterSpacing: "tight" },
    h4: { size: "xl", weight: "bold", lineHeight: "snug", letterSpacing: "normal" },
    h5: { size: "lg", weight: "semibold", lineHeight: "normal", letterSpacing: "normal" },
    h6: { size: "base", weight: "semibold", lineHeight: "normal", letterSpacing: "normal" },
  },
  body: {
    large: { size: "lg", weight: "normal", lineHeight: "relaxed" },
    base: { size: "base", weight: "normal", lineHeight: "relaxed" },
    small: { size: "sm", weight: "normal", lineHeight: "normal" },
    caption: { size: "xs", weight: "medium", lineHeight: "normal", letterSpacing: "wider" },
  },
};