/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        space: {
          void: "#05050A",
          titanium: "#0B0C10",
          panel: "#111318",
          border: "#1a1d26",
        },
        cyber: {
          blue: "#4CC9F0",
          "blue-dim": "#2a7a97",
          "blue-glow": "rgba(76,201,240,0.15)",
          purple: "#7209B7",
          "purple-dim": "#4a0677",
          "purple-glow": "rgba(114,9,183,0.15)",
          green: "#4BB543",
          "green-dim": "#2d6e2a",
          "green-glow": "rgba(75,181,67,0.15)",
          red: "#EF4444",
          amber: "#F59E0B",
        },
        primary: {
          50: "#e0f7ff",
          100: "#b3ecff",
          200: "#80dfff",
          300: "#4dd2ff",
          400: "#26c8ff",
          500: "#4CC9F0",
          600: "#0099cc",
          700: "#007399",
          800: "#004d66",
          900: "#002633",
        },
      },
      fontFamily: {
        display: ["Orbitron", "Rajdhani", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Geist Mono", "monospace"],
        body: ["Rajdhani", "Inter", "system-ui", "sans-serif"],
      },
      boxShadow: {
        "cyber-blue": "0 0 20px rgba(76,201,240,0.15), 0 0 60px rgba(76,201,240,0.05)",
        "cyber-purple": "0 0 20px rgba(114,9,183,0.15), 0 0 60px rgba(114,9,183,0.05)",
        "cyber-green": "0 0 20px rgba(75,181,67,0.15), 0 0 60px rgba(75,181,67,0.05)",
        "cyber-blue-intense": "0 0 30px rgba(76,201,240,0.3), 0 0 80px rgba(76,201,240,0.1)",
        "cyber-purple-intense": "0 0 30px rgba(114,9,183,0.3), 0 0 80px rgba(114,9,183,0.1)",
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 20s linear infinite",
        "glow-pulse": "glowPulse 3s ease-in-out infinite",
        "scan-line": "scanLine 2s linear infinite",
        "float": "float 6s ease-in-out infinite",
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.3s ease-out",
        "scale-in": "scaleIn 0.3s ease-out",
        "border-flow": "borderFlow 3s linear infinite",
      },
      keyframes: {
        glowPulse: {
          "0%, 100%": { opacity: "0.4" },
          "50%": { opacity: "1" },
        },
        scanLine: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideDown: {
          "0%": { opacity: "0", transform: "translateY(-10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        borderFlow: {
          "0%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
          "100%": { backgroundPosition: "0% 50%" },
        },
      },
      backgroundImage: {
        "grid-pattern": "linear-gradient(rgba(76,201,240,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(76,201,240,0.03) 1px, transparent 1px)",
        "radial-glow": "radial-gradient(ellipse at center, rgba(76,201,240,0.08) 0%, transparent 70%)",
      },
      backgroundSize: {
        "grid-lg": "4rem 4rem",
      },
    },
  },
  plugins: [],
};
