import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger" | "success";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  fullWidth?: boolean;
}

const baseStyles =
  "inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition-all duration-200 active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap";

const variantStyles: Record<string, string> = {
  primary:
    "bg-primary text-white shadow-primary hover:bg-primary-dark",
  secondary:
    "bg-surface-2 text-primary border border-primary/20 hover:bg-primary/5",
  outline:
    "border border-primary text-primary hover:bg-primary/5",
  ghost:
    "text-primary hover:bg-primary/10",
  danger:
    "bg-red-500 text-white hover:bg-red-600 shadow-red/10 hover:shadow-red/20",
  success:
    "bg-success text-white hover:bg-success-dark shadow-success hover:shadow-success-lg",
};

const sizeStyles: Record<string, string> = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-5 py-3 text-sm",
  lg: "px-8 py-4 text-base",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = "primary",
      size = "md",
      loading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className = "",
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        type="button"
        disabled={disabled || loading}
        className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${
          fullWidth ? "w-full" : ""
        } ${className}`}
        {...props}
      >
        {loading ? (
          <svg
            className="w-4 h-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        ) : leftIcon ? (
          <span className="flex-shrink-0">{leftIcon}</span>
        ) : null}
        {children}
        {rightIcon ? (
          <span className="flex-shrink-0">{rightIcon}</span>
        ) : null}
      </button>
    );
  }
);

Button.displayName = "Button";
export default Button;
