import { forwardRef, type ReactNode } from "react";

interface PageShellProps extends React.HTMLAttributes<HTMLDivElement> {
  theme?: "default" | "focus" | "dark";
  container?: boolean;
  maxWidth?: string;
  padding?: string;
}

export const PageShell = forwardRef<HTMLDivElement, PageShellProps>(
  ({ theme = "default", container = true, maxWidth = "7xl", padding = "py-8 px-6 sm:px-8", className = "", children, ...props }, ref) => {
    const themeStyles: Record<string, string> = {
      default: "bg-canvas min-h-screen",
      focus: "bg-[#0d1117] min-h-screen text-text-primary",
      dark: "bg-charcoal min-h-screen text-text-primary",
    };

    return (
      <div
        ref={ref}
        className={`${themeStyles[theme]} ${container ? `max-w-${maxWidth} mx-auto ${padding}` : ""} ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

PageShell.displayName = "PageShell";
export default PageShell;
