/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      // ══════════════════════════════════════════════════════════════════════
      // BOUNTYCODE DESIGN SYSTEM V3 — "Golden Hour Academy"
      // Warm, vibrant, mobile-first palette — high contrast, sunny gradients
      // ══════════════════════════════════════════════════════════════════════
      colors: {
        // ── Base (warm dark canvas, not pure black) ──
        canvas: {
          DEFAULT: "#0F172A",   // deep slate-900
          soft: "#1E293B",      // slate-800 elevated
          surface: "#334155",   // slate-700 cards
          surfaceHover: "#64748B", // slate-500 hover (more visible)
        },
        border: {
          DEFAULT: "#64748B",   // slate-500 (more visible borders)
          soft: "#334155",      // slate-700
          focus: "#F97316",     // orange-500
          primary: "#F97316/30",
        },
        text: {
          DEFAULT: "#F8FAFC",   // slate-50
          primary: "#F8FAFC",
          secondary: "#E2E8F0", // slate-200 (better contrast)
          muted: "#CBD5E1",     // slate-300 (WCAG AA on surfaces)
          dim: "#94A3B8",       // slate-400
          inverse: "#0F172A",   // canvas
        },

        // ── Primary brand (vibrant orange — energetic, student-friendly) ──
        primary: {
          DEFAULT: "#F97316",   // orange-500
          dark: "#EA580C",      // orange-600
          deep: "#C2410C",      // orange-700
          soft: "rgba(249, 115, 22, 0.10)",
          softer: "rgba(249, 115, 22, 0.05)",
          glow: "rgba(249, 115, 22, 0.25)",
          text: "#FFFFFF",
        },

        // ── Subject accent colors (warm, distinct per subject) ──
        subject: {
          coding: {
            DEFAULT: "#06B6D4",  // cyan-500
            soft: "rgba(6, 182, 212, 0.10)",
            glow: "rgba(6, 182, 212, 0.25)",
          },
          aptitude: {
            DEFAULT: "#F59E0B",  // amber-500
            soft: "rgba(245, 158, 11, 0.10)",
            glow: "rgba(245, 158, 11, 0.25)",
          },
          reasoning: {
            DEFAULT: "#EC4899",  // pink-500
            soft: "rgba(236, 72, 153, 0.10)",
            glow: "rgba(236, 72, 153, 0.25)",
          },
          verbal: {
            DEFAULT: "#10B981",  // emerald-500
            soft: "rgba(16, 185, 129, 0.10)",
            glow: "rgba(16, 185, 129, 0.25)",
          },
          interview: {
            DEFAULT: "#8B5CF6",  // violet-500
            soft: "rgba(139, 92, 246, 0.10)",
            glow: "rgba(139, 92, 246, 0.25)",
          },
          boss: {
            DEFAULT: "#EF4444",  // red-500
            soft: "rgba(239, 68, 68, 0.10)",
            glow: "rgba(239, 68, 68, 0.25)",
          },
        },

        // ── Semantic ──
        success: {
          DEFAULT: "#22C55E",
          soft: "rgba(34, 197, 94, 0.10)",
          text: "#86EFAC",
        },
        warning: {
          DEFAULT: "#F59E0B",
          soft: "rgba(245, 158, 11, 0.10)",
          text: "#FCD34D",
        },
        error: {
          DEFAULT: "#EF4444",
          soft: "rgba(239, 68, 68, 0.10)",
          text: "#FCA5A5",
        },
        info: {
          DEFAULT: "#3B82F6",
          soft: "rgba(59, 130, 246, 0.10)",
          text: "#93C5FD",
        },

        // ── Legacy aliases (backward compat) ──
        blue: { DEFAULT: "#3B82F6", soft: "rgba(59, 130, 246, 0.10)" },
        gold: { DEFAULT: "#F59E0B", soft: "rgba(245, 158, 11, 0.10)" },
        purple: { DEFAULT: "#8B5CF6", soft: "rgba(139, 92, 246, 0.10)" },
        red: { DEFAULT: "#EF4444", soft: "rgba(239, 68, 68, 0.10)" },

        // ── Coddy compat (kept for existing references) ──
        coddy: { DEFAULT: "#29ABE2", dark: "#34B4E4", button: "#0077FF", buttonShadow: "#005DC8", deep: "#007ACCC", darkTheme: "#1B78A0" },
        streak: { DEFAULT: "#E85A18", light: "#F4C4B4", 500: "#E85A18", 600: "#C94E15", 900: "#7B2E0C" },
        score: { DEFAULT: "#FCAD00", light: "#FDE6A5", 500: "#FCAD00", 600: "#E69A00", 900: "#8B6A00" },
        energy: { DEFAULT: "#3E39B8", light: "#D6D4EC", 500: "#3E39B8", 600: "#332FA8", 900: "#23217A" },
        bugsy: { DEFAULT: "#D31D65", light: "#F4A9C4", 500: "#D31D65" },
        pro: { DEFAULT: "#CF7F26", light: "#EAC89C", 500: "#CF7F26" },
        hearts: { DEFAULT: "#FF4B4B", light: "#FFCCCC", 500: "#FF4B4B", 600: "#E63A3A", 900: "#992727" },
        streakFreeze: { DEFAULT: "#69AEFF", light: "#D3E3FF", 500: "#69AEFF" },
        successLegacy: { DEFAULT: "#05B20C", light: "#DFF8DB", 500: "#05B20C" },
        mist: "#F1F5F9",
        skyWash: "#DDF4FF",
        charcoal: "#252627",
        graphite: "#2D2E2F",
        editor: "#1E1E1E",
      },
      boxShadow: {
        "soft": "0 1px 3px rgba(15, 23, 42, 0.12), 0 4px 12px rgba(15, 23, 42, 0.08)",
        "card": "0 1px 3px rgba(15, 23, 42, 0.15), 0 2px 8px rgba(15, 23, 42, 0.10)",
        "card-hover": "0 12px 32px rgba(15, 23, 42, 0.25), 0 6px 16px rgba(15, 23, 42, 0.12)",
        "primary": "0 0 20px rgba(249, 115, 22, 0.25)",
        "primary-lg": "0 0 40px rgba(249, 115, 22, 0.35)",
        "modal": "0 20px 60px rgba(15, 23, 42, 0.35)",
        "coding": "0 0 20px rgba(6, 182, 212, 0.15)",
        "aptitude": "0 0 20px rgba(245, 158, 11, 0.15)",
        "reasoning": "0 0 20px rgba(236, 72, 153, 0.15)",
        "verbal": "0 0 20px rgba(16, 185, 129, 0.15)",
        "boss": "0 0 20px rgba(239, 68, 68, 0.15)",
        "bounty": "0 0 40px rgba(245, 158, 11, 0.25)",
      },
      fontFamily: {
        display: ["Manrope", "Inter", "system-ui", "sans-serif"],
        round: ['"Baloo 2"', "Nunito", "Quicksand", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 20s linear infinite",
        "float": "float 6s ease-in-out infinite",
        "float-slow": "float 8s ease-in-out infinite",
        "float-gentle": "float 10s ease-in-out infinite",
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.3s ease-out",
        "scale-in": "scaleIn 0.3s ease-out",
        "glow-pulse": "glowPulse 3s ease-in-out infinite",
        "drift": "drift 12s ease-in-out infinite",
        "drift-slow": "drift 20s ease-in-out infinite",
        "sway": "sway 6s ease-in-out infinite",
        "shimmer": "shimmer 3s ease-in-out infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
        drift: {
          "0%, 100%": { transform: "translateX(0px) translateY(0px)" },
          "25%": { transform: "translateX(10px) translateY(-5px)" },
          "50%": { transform: "translateX(-5px) translateY(-10px)" },
          "75%": { transform: "translateX(-10px) translateY(-5px)" },
        },
        sway: {
          "0%, 100%": { transform: "rotate(-1deg)" },
          "50%": { transform: "rotate(1deg)" },
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
        shimmer: {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 225deg, var(--tw-gradient-stops))",
        "grid-academy": "linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px)",
        "sunset-gradient": "linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%)",
      },
      backgroundSize: {
        "grid-academy": "24px 24px",
      },
    },
  },
  safelist: [
    { pattern: /bg-(canvas|primary|subject|success|warning|error|info|blue|gold|purple|red)(-(DEFAULT|dark|deep|soft|softer|glow|text))?(\/\d+)?/ },
    { pattern: /text-(canvas|primary|subject|success|warning|error|info|blue|gold|purple|red)(-(DEFAULT|dark|deep|soft|softer|glow|text))?/ },
    { pattern: /border-(canvas|primary|subject|success|warning|error|info|blue|gold|purple|red)(-(DEFAULT|soft|focus|primary))?(\/\d+)?/ },
    { pattern: /from-(primary|subject|success|warning|error|info|blue|gold|purple|red)(-(DEFAULT|dark|deep))?/ },
    { pattern: /to-(primary|subject|success|warning|error|info|blue|gold|purple|red)(-(DEFAULT|dark|deep))?/ },
    { pattern: /shadow-(card|primary|modal|coding|aptitude|reasoning|verbal|boss|bounty)/ },
    { pattern: /bg-(coding|aptitude|reasoning|verbal|interview|boss)(-(DEFAULT|soft|glow))?/ },
    { pattern: /text-(coding|aptitude|reasoning|verbal|interview|boss)(-(DEFAULT|soft|glow))?/ },
    { pattern: /shadow-(coding|aptitude|reasoning|verbal|boss)/ },
    { pattern: /bg-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?(\/\d+)?/ },
    { pattern: /text-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?/ },
    { pattern: /border-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?(\/\d+)?/ },
    { pattern: /from-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success)(-(DEFAULT|dark|light|500|600))?/ },
    { pattern: /to-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success)(-(DEFAULT|dark|light|500|600))?/ },
  ],
  plugins: [],
};
