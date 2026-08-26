import type { ReactNode } from "react";
import { AmbientNature } from "./AmbientNature";

/**
 * PageShell — standard page wrapper enforcing the DESIGN FREEZE V2 theme matrix.
 *
 * Themes:
 *  - nature     : Ambient leaves only (default for learning/community pages)
 *  - adventure  : Leaves + faint map contours (landing, journey map, home)
 *  - focus      : NO decorative background. Compiler, OA, resume, admin.
 *  - celebration: Leaves + warm gold wash (reward reveals)
 *  - spring     : Sakura petal overlay (landing page hero)
 */

export type PageTheme = "nature" | "adventure" | "focus" | "celebration" | "spring";

interface PageShellProps {
  theme?: PageTheme;
  children: ReactNode;
  className?: string;
}

export function PageShell({ theme = "nature", children, className = "" }: PageShellProps) {
  // pb clears the fixed mobile BottomNav (64px bar + optional 28px league strip)
  const pad = "pb-28 md:pb-10";
  if (theme === "focus") {
    return (
      <div className={`relative min-h-screen bg-canvas ${className}`}>
        <div className={`relative z-10 ${pad}`}>{children}</div>
      </div>
    );
  }

  return (
    <div className={`relative min-h-screen bg-canvas ${className}`}>
      {theme === "adventure" && (
        <div
          aria-hidden="true"
          className="map-contours pointer-events-none fixed inset-0"
          style={{ zIndex: 0 }}
        />
      )}
      {theme === "celebration" && (
        <div
          aria-hidden="true"
          className="pointer-events-none fixed inset-0"
          style={{
            zIndex: 0,
            background:
              "radial-gradient(ellipse at 50% -10%, rgba(234,183,77,0.12), transparent 55%)",
          }}
        />
      )}
      {theme !== "spring" && (
        <AmbientNature density={theme === "adventure" ? "normal" : "normal"} />
      )}
      <div className={`relative z-10 ${pad}`}>{children}</div>
    </div>
  );
}
