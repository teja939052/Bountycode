import { useState, useEffect } from "react";
import { BountyCodeLogo } from "./BountyCodeLogo";

export type BountyCodeSplashProps = {
  duration?: number;
  onComplete?: () => void;
  className?: string;
};

export function BountyCodeSplash({
  duration = 1800,
  onComplete,
  className = "",
}: BountyCodeSplashProps) {
  const [visible, setVisible] = useState(false);
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    const enterTimer = setTimeout(() => setVisible(true), 40);
    const exitTimer = setTimeout(() => {
      setExiting(true);
      setTimeout(() => onComplete?.(), 320);
    }, duration);
    return () => {
      clearTimeout(enterTimer);
      clearTimeout(exitTimer);
    };
  }, [duration, onComplete]);

  return (
    <div
      className={[
        "fixed inset-0 z-[200] flex items-center justify-center",
        "bg-[#0F1724]",
        exiting ? "bc-splash-exit" : visible ? "bc-splash-enter" : "bc-splash-enter",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      aria-live="polite"
      aria-label="Loading BountyCode"
    >
      <div className="relative flex flex-col items-center gap-6">
        <div className="bc-logo-reveal relative">
          <BountyCodeLogo variant="lockup" title="BountyCode" className="text-[#F7F5F0]" />

          {/* Subtle glitter */}
          <span
            aria-hidden="true"
            className="pointer-events-none absolute -top-3 left-1/2 h-2 w-2 -translate-x-1/2 rounded-full bg-[#C96F3D] bc-glitter-particle"
          />
          <span
            aria-hidden="true"
            className="pointer-events-none absolute top-1/2 -right-4 h-1.5 w-1.5 -translate-y-1/2 rounded-full bg-[#F7F5F0] bc-glitter-particle"
            style={{ animationDelay: "0.35s" }}
          />
          <span
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-2 left-1/3 h-1.5 w-1.5 rounded-full bg-[#C96F3D] bc-glitter-particle"
            style={{ animationDelay: "0.7s" }}
          />
        </div>
      </div>

      <style>{`
        @keyframes bc-splash-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes bc-splash-out {
          from { opacity: 1; }
          to { opacity: 0; }
        }
        @keyframes bc-logo-in {
          from { opacity: 0; transform: scale(0.96); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes bc-glitter {
          0%, 100% { opacity: 0.25; transform: translateY(0px); }
          50% { opacity: 1; transform: translateY(-2px); }
        }
        .bc-splash-enter {
          animation: bc-splash-in 180ms ease-out both;
        }
        .bc-splash-exit {
          animation: bc-splash-out 280ms ease-in both;
        }
        .bc-logo-reveal {
          animation: bc-logo-in 720ms cubic-bezier(.22, 1, .36, 1) both;
        }
        .bc-glitter-particle {
          box-shadow:
            0 0 7px rgba(255,255,255,.68),
            0 0 16px rgba(201,111,61,.16);
          animation: bc-glitter 1.15s ease-in-out infinite;
        }
        @media (prefers-reduced-motion: reduce) {
          .bc-splash-enter,
          .bc-splash-exit,
          .bc-logo-reveal,
          .bc-glitter-particle {
            animation: none !important;
          }
        }
      `}</style>
    </div>
  );
}

type BountyCodeLoaderProps = {
  size?: number;
  dark?: boolean;
  respectReducedMotion?: boolean;
  label?: string;
  className?: string;
};

export function BountyCodeLoader({
  size = 40,
  dark = false,
  respectReducedMotion: _respectReducedMotion = true,
  label = "Loading",
  className = "",
}: BountyCodeLoaderProps) {
  return (
    <span
      className={[
        "inline-flex items-center justify-center",
        dark ? "text-white" : "text-[#17263B]",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      role="status"
      aria-label={label}
    >
      <span
        className="bc-loader-pulse"
        style={{ width: size, height: size }}
      >
        <BountyCodeLogo variant="mark" title="" className="!h-full !w-full" />
      </span>

      <span className="sr-only">{label}</span>

      <style>{`
        @keyframes bc-loader-pulse {
          0%, 100% { opacity: .45; transform: scale(.96); }
          50% { opacity: 1; transform: scale(1); }
        }
        .bc-loader-pulse {
          display: inline-flex;
          animation: bc-loader-pulse 1.25s ease-in-out infinite;
          transform-origin: center;
        }
        @media (prefers-reduced-motion: reduce) {
          .bc-loader-pulse {
            animation: none !important;
          }
        }
      `}</style>
    </span>
  );
}
