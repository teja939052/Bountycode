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
        },
        border: {
          DEFAULT: "#DCE8DE",
        },
        text: {
          DEFAULT: "#17211B",
          primary: "#17211B",
          muted: "#68736B",
          light: "#68736B",
          inverse: "#FFFFFF",
        },

        // ============ PRIMARY GREEN (ACCENT, NOT BACKGROUND) ============
        primary: {
          DEFAULT: "#22C55E",
          dark: "#16A34A",
          soft: "#DCFCE7",
          hover: "#16A34A",
        },

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

        // ============ CODDY TECH SEMANTIC PALETTE (reverse-engineered from coddy.tech/brand/colors) ============
        // One brand color: Coddy Blue. Every other color means something.
        coddy: {
          DEFAULT: "#29ABE2",
          dark: "#34B4E4",
          button: "#0077FF",
          buttonShadow: "#005DC8",
          deep: "#007ACCC",
          darkTheme: "#1B78A0",
        },
        streak: {
          DEFAULT: "#E85A18",
          light: "#F4C4B4",
          50: "#FDF1EB",
          100: "#FBE2D4",
          400: "#F07B4A",
          500: "#E85A18",
          600: "#C94E15",
          900: "#7B2E0C",
        },
        score: {
          DEFAULT: "#FCAD00",
          light: "#FDE6A5",
          50: "#FEFBF0",
          100: "#FEF3C7",
          500: "#FCAD00",
          600: "#E69A00",
          900: "#8B6A00",
        },
        energy: {
          DEFAULT: "#3E39B8",
          light: "#D6D4EC",
          500: "#3E39B8",
          600: "#332FA8",
          900: "#23217A",
        },
        bugsy: {
          DEFAULT: "#D31D65",
          light: "#F4A9C4",
          500: "#D31D65",
        },
        pro: {
          DEFAULT: "#CF7F26",
          light: "#EAC89C",
          500: "#CF7F26",
        },
        hearts: {
          DEFAULT: "#FF4B4B",
          light: "#FFCCCC",
          500: "#FF4B4B",
          600: "#E63A3A",
          900: "#992727",
        },
        streakFreeze: {
          DEFAULT: "#69AEFF",
          light: "#D3E3FF",
          500: "#69AEFF",
        },
        success: {
          DEFAULT: "#05B20C",
          light: "#DFF8DB",
          500: "#05B20C",
        },

        // Backgrounds (coddy)
        mist: "#F1F5F9",
        skyWash: "#DDF4FF",
        charcoal: "#252627",
        graphite: "#2D2E2F",
        editor: "#1E1E1E",
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
    { pattern: /bg-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?(\/\d+)?/ },
    { pattern: /text-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?/ },
    { pattern: /border-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success|mist|skyWash|charcoal|graphite|editor)(-(DEFAULT|dark|button|buttonShadow|deep|darkTheme|light|50|100|400|500|600|900))?(\/\d+)?/ },
    { pattern: /from-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success)(-(DEFAULT|dark|light|500|600))?/ },
    { pattern: /to-(coddy|streak|score|energy|bugsy|pro|hearts|streakFreeze|success)(-(DEFAULT|dark|light|500|600))?/ },
  ],
  plugins: [],
};