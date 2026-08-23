/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: {
          DEFAULT: "#F7FAF7",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          2: "#F0F7F1",
          hover: "#F0EDE6",
        },
        border: {
          DEFAULT: "#E3EBE4",
        },
        text: {
          DEFAULT: "#17211B",
          muted: "#68736B",
          light: "#68736B",
          inverse: "#FFFFFF",
        },
        primary: {
          DEFAULT: "#22C55E",
          dark: "#16A34A",
          soft: "#DCFCE7",
          hover: "#16A34A",
        },
        blue: {
          DEFAULT: "#3B82F6",
          soft: "#DBEAFE",
        },
        gold: {
          DEFAULT: "#F59E0B",
          soft: "#FEF3C7",
        },
        purple: {
          DEFAULT: "#8B5CF6",
          soft: "#EDE9FE",
        },
        red: {
          DEFAULT: "#EF4444",
          soft: "#FEE2E2",
        },
        success: "#22C55E",
        warning: "#F59E0B",
        error: "#EF4444",
        info: "#3B82F6",

        /* Bounty palette (used for accents, not primary) */
        navy: {
          DEFAULT: "#0A0E17",
          50: "#E8EDF5",
          100: "#D1DBEB",
          200: "#A3B7D7",
          300: "#7593C3",
          400: "#476FAF",
          500: "#1A4B9B",
          600: "#153C7C",
          700: "#102D5D",
          800: "#0A1E3E",
          900: "#050F1F",
        },
        amber: {
          DEFAULT: "#FFD700",
          50: "#FFF8E6",
          100: "#FFF1CC",
          200: "#FFE399",
          300: "#FFD566",
          400: "#FFC733",
          500: "#FFB900",
          600: "#E6A700",
          700: "#CC9500",
          800: "#B38300",
          900: "#997100",
        },
        cream: {
          DEFAULT: "#F5E6D3",
          50: "#FDF8F3",
          100: "#FBF1E8",
        },
        rust: {
          DEFAULT: "#B45309",
        },
        smoke: {
          DEFAULT: "#6B7280",
        },
        pearl: {
          DEFAULT: "#F8FAFC",
        },
      },
      boxShadow: {
        "soft": "0 1px 3px rgba(17, 33, 27, 0.04), 0 4px 12px rgba(17, 33, 27, 0.03)",
        "soft-md": "0 2px 8px rgba(17, 33, 27, 0.06), 0 8px 24px rgba(17, 33, 27, 0.04)",
        "soft-lg": "0 4px 16px rgba(17, 33, 27, 0.08), 0 16px 48px rgba(17, 33, 27, 0.06)",
        "card": "0 1px 3px rgba(17, 33, 27, 0.04), 0 2px 8px rgba(17, 33, 27, 0.02)",
        "card-hover": "0 4px 12px rgba(17, 33, 27, 0.06), 0 8px 24px rgba(17, 33, 27, 0.04)",
        "primary": "0 4px 20px rgba(34, 197, 94, 0.12)",
        "primary-lg": "0 8px 40px rgba(34, 197, 94, 0.18)",
        "modal": "0 20px 60px rgba(17, 33, 27, 0.12)",
        "coral": "0 4px 20px rgba(34, 197, 94, 0.12)",
        "coral-lg": "0 8px 40px rgba(34, 197, 94, 0.18)",
        "teal": "0 4px 20px rgba(34, 197, 94, 0.12)",
        "teal-lg": "0 8px 40px rgba(34, 197, 94, 0.18)",
        "navy": "0 4px 20px rgba(10, 14, 23, 0.12)",
        "gold": "0 4px 20px rgba(245, 158, 11, 0.15)",
        "bounty": "0 0 40px rgba(255, 215, 0, 0.15)",
      },
      fontFamily: {
        display: ["Manrope", "Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 20s linear infinite",
        "float": "float 6s ease-in-out infinite",
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.3s ease-out",
        "scale-in": "scaleIn 0.3s ease-out",
        "glow-pulse": "glowPulse 3s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideDown: {
          "0%": { opacity: "0", transform: "translateY(-8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.96)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        glowPulse: {
          "0%, 100%": { opacity: "0.4" },
          "50%": { opacity: "1" },
        },
      },
    },
  },
  safelist: [
    { pattern: /bg-(primary|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover))?(\/\d+)?/ },
    { pattern: /text-(primary|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover))?/ },
    { pattern: /border-(primary|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover))?(\/\d+)?/ },
    { pattern: /from-(primary|blue|gold|purple|red|amber)(-(DEFAULT|dark|soft))?/ },
    { pattern: /to-(primary|blue|gold|purple|red|amber)(-(DEFAULT|dark|soft))?/ },
    { pattern: /bg-(canvas|surface|border|text|navy|smoke|pearl)(-(DEFAULT|2|muted|light|inverse|900|800))?(\/\d+)?/ },
    { pattern: /text-(canvas|surface|border|text|navy|smoke|pearl|cream)(-(DEFAULT|2|muted|light|inverse|900|100))?/ },
    { pattern: /border-(canvas|surface|border|text|navy|smoke|pearl)(-(DEFAULT|2|muted|light|inverse))?(\/\d+)?/ },
  ],
  plugins: [],
};
