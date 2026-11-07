/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // ============ BASE LIGHT SYSTEM ============
        canvas: {
          DEFAULT: "#F7FAF7",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          2: "#F0F7F1",
          hover: "#F0EDE6",
          // Sub-tokens referenced by pages/design-system components.
          base: "#FAFAF6",
          card: "#FFFFFF",
          elevated: "#FFFFFF",
          raised: "#FFFFFF",
          muted: "#F0F7F1",
          100: "#F0F7F1",
          border: "#DCE8DE",
        },
        border: {
          DEFAULT: "#DCE8DE",
          primary: "#DCE8DE",
          muted: "#E6EDE7",
        },
        text: {
          DEFAULT: "#17211B",
          primary: "#17211B",
          secondary: "#3F4A43",
          muted: "#68736B",
          light: "#68736B",
          dim: "#8A948D",
          inverse: "#FFFFFF",
        },

        // ============ PRIMARY GREEN (ACCENT, NOT BACKGROUND) ============
        primary: {
          DEFAULT: "#22C55E",
          50: "#F0FDF4",
          100: "#DCFCE7",
          400: "#4ADE80",
          500: "#22C55E",
          600: "#16A34A",
          700: "#15803D",
          900: "#14532D",
          dark: "#16A34A",
          soft: "#DCFCE7",
          hover: "#16A34A",
        },

        // ============ LEGACY ALIASES ============
        // `brand-*`, `surface-card`, `nature-*`, `cyber-*` and `space-*` are
        // referenced across the app. They are aliases onto the light system
        // above so every usage renders with the front-page palette.
        brand: {
          50: "#EAF7ED", 200: "#BFE6C9", 500: "#22C55E", 600: "#16A34A",
          700: "#15803D", 900: "#14532D",
          DEFAULT: "#22C55E", primary: "#22C55E", secondary: "#5BA7A0",
          tertiary: "#EAB74D", accent: "#8BC9D5", deep: "#15803D",
          dim: "#68736B", muted: "#68736B", mint: "#EAF7ED",
          sky: "#8BC9D5", gold: "#EAB74D", emerald: "#22C55E",
          lavender: "#E8A9B8", teal: "#5BA7A0",
          amber: "#EAB74D", coral: "#E96A5B", rose: "#D4839A",
          bg: "#FAFAF6", vibe: "#E8A9B8",
          "vibe-accent": "#E8A9B8",
          "sky-pale": "#E8F5FA",
          "coral-pale": "#FDEDEC", "gold-pale": "#FFF3D0",
          "emerald-dark": "#16A34A", "gold-dark": "#C9992F",
          "lavender-dark": "#D4839A", "rose-dark": "#B96A80",
        },
        cyber: {
          blue: "#4A90E2", green: "#22C55E", purple: "#8B6BD9",
          red: "#E96A5B", amber: "#EAB74D", yellow: "#EAB74D",
          orange: "#E96A5B",
        },
        // Kept light on purpose: the app ships a single bright theme.
        space: {
          void: "#F7FAF7", panel: "#FFFFFF", border: "#DCE8DE",
          titanium: "#F0F0EB", cosmos: "#F7FAF7", nebula: "#F3F0FA",
        },
        nature: {
          blossom: { DEFAULT: "#E8A9B8", soft: "#FBE4EC", deep: "#D4839A" },
          moss: { DEFAULT: "#6E9E78", soft: "#E4EFE6", deep: "#4F7D5A" },
          leaf: { DEFAULT: "#8FBF7F", soft: "#EDF6EA" },
          bark: { DEFAULT: "#8B6B4F", soft: "#F3EDE6" },
          stone: { DEFAULT: "#A8A29A", soft: "#F2F1EF" },
          sand: { DEFAULT: "#D9C9A3", soft: "#FAF6EC" },
          sun: { DEFAULT: "#E8B04D", soft: "#FDF3DC" },
          sky: { DEFAULT: "#9CC7D9", soft: "#EAF4F8" },
          ink: { DEFAULT: "#1C2A22" },
          glow: { DEFAULT: "#E8A9B8" },
        },
        background: {
          surface: "#FFFFFF",
          secondary: "#F0F7F1",
          base: "#F7FAF7",
          card: "#FFFFFF",
        },
        accent: {
          DEFAULT: "#22C55E",
          primary: "#22C55E",
          secondary: "#5BA7A0",
          warm: "#EAB74D",
          coral: "#E96A5B",
          light: "#DCFCE7",
          hover: "#16A34A",
        },
        // Bare aliases some call sites use (`text-muted`, `border-default`).
        muted: "#68736B",
        secondary: "#3F4A43",
        default: "#DCE8DE",
        base: "#F7FAF7",
        card: "#FFFFFF",
        mint: "#EAF7ED",
        diamonds: "#5BA7A0",
        achievement: "#EAB74D",
        boss: "#E96A5B",
        "vibe-accent": "#E8A9B8",

        // ============ ADVENTURE PALETTE ============
        ocean: {
          DEFAULT: "#5BA7A0",
          soft: "#E0F2F1",
        },
        sky: {
          DEFAULT: "#8BC9D5",
          soft: "#E8F5FA",
        },
        sand: {
          DEFAULT: "#E9D6A3",
          soft: "#FDF6EB",
        },
        wood: {
          DEFAULT: "#A8754F",
          soft: "#F5EFE8",
        },

        // ============ REWARD GOLD ============
        reward: {
          DEFAULT: "#EAB74D",
          soft: "#FFF3D0",
          muted: "#E8B03D",
        },

        // ============ SEMANTIC ============
        tech: {
          DEFAULT: "#4A90E2",
          soft: "#E8F0FE",
        },
        coral: {
          DEFAULT: "#E96A5B",
          soft: "#FDEDEC",
        },
        rare: {
          DEFAULT: "#8B6BD9",
          soft: "#F3F0FA",
        },

        // ============ LEGACY (kept for backward compat) ============
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

        // ============ BOUNTY PALETTE (legacy, kept for compat) ============
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
        "ocean": "0 4px 20px rgba(91, 167, 160, 0.12)",
        "coral": "0 4px 20px rgba(233, 106, 91, 0.15)",
        "gold": "0 4px 20px rgba(234, 183, 77, 0.18)",
        "bounty": "0 0 40px rgba(255, 215, 0, 0.15)",
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
      },
    },
  },
  safelist: [
    { pattern: /bg-(primary|ocean|sky|sand|wood|reward|tech|coral|rare|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover|muted))?(\/\d+)?/ },
    { pattern: /text-(primary|ocean|sky|sand|wood|reward|tech|coral|rare|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover|muted))?/ },
    { pattern: /border-(primary|ocean|sky|sand|wood|reward|tech|coral|rare|blue|gold|purple|red|success|warning|error|info)(-(DEFAULT|dark|soft|hover|muted))?(\/\d+)?/ },
    { pattern: /from-(primary|ocean|sky|sand|wood|reward|tech|coral|rare|blue|gold|purple|red|amber)(-(DEFAULT|dark|soft))?/ },
    { pattern: /to-(primary|ocean|sky|sand|wood|reward|tech|coral|rare|blue|gold|purple|amber)(-(DEFAULT|dark|soft))?/ },
    { pattern: /bg-(canvas|surface|border|text|navy|smoke|pearl)(-(DEFAULT|2|muted|light|inverse|900|800))?(\/\d+)?/ },
    { pattern: /text-(canvas|surface|border|text|navy|smoke|pearl|cream)(-(DEFAULT|2|primary|muted|light|inverse|900|100))?/ },
    { pattern: /border-(canvas|surface|border|text|navy|smoke|pearl)(-(DEFAULT|2|muted|light|inverse))?(\/\d+)?/ },
    { pattern: /(bg|text|border|from|via|to|ring|shadow)-(brand|nature|cyber|space|surface|background|accent)(-[a-zA-Z0-9]+)*(\/\d+)?/ },
  ],
  plugins: [],
};