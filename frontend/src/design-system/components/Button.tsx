import { forwardRef, ButtonHTMLAttributes } from "react";
import { colors, radii, shadows, motion, spacing } from "..";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "outline" | "destructive" | "success";
  size?: "sm" | "md" | "lg" | "xl";
  fullWidth?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const variantStyles: Record<ButtonProps["variant"], string> = {
  primary: `
    background: linear-gradient(135deg, ${colors.brand.primary} 0%, ${colors.brand.deep} 100%);
    color: ${colors.text.inverse};
    border: none;
    box-shadow: ${shadows.sm};
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, ${colors.brand.deep} 0%, ${colors.brand.darkest} 100%);
      box-shadow: ${shadows.md};
      transform: translateY(-1px);
    }
    &:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: ${shadows.xs};
    }
  `,
  secondary: `
    background: ${colors.background.surfaceSecondary};
    color: ${colors.text.primary};
    border: 1px solid ${colors.border.primary};
    &:hover:not(:disabled) {
      background: ${colors.background.secondary};
      border-color: ${colors.border.secondary};
    }
  `,
  ghost: `
    background: transparent;
    color: ${colors.brand.primary};
    border: 1px solid transparent;
    &:hover:not(:disabled) {
      background: ${colors.brand.mint};
    }
  `,
  outline: `
    background: transparent;
    color: ${colors.text.primary};
    border: 1px solid ${colors.border.primary};
    &:hover:not(:disabled) {
      background: ${colors.background.surfaceSecondary};
      border-color: ${colors.border.secondary};
    }
  `,
  destructive: `
    background: ${colors.semantic.error};
    color: ${colors.text.inverse};
    border: none;
    box-shadow: ${shadows.sm};
    &:hover:not(:disabled) {
      background: #DC2626;
      box-shadow: ${shadows.md};
    }
  `,
  success: `
    background: ${colors.semantic.success};
    color: ${colors.text.inverse};
    border: none;
    box-shadow: ${shadows.sm};
    &:hover:not(:disabled) {
      background: ${colors.brand.deep};
      box-shadow: ${shadows.md};
    }
  `,
};

const sizeStyles: Record<ButtonProps["size"], string> = {
  sm: `px-${spacing.scale[3]} py-${spacing.scale[1.5]} text-sm gap-1.5`,
  md: `px-${spacing.scale[4]} py-${spacing.scale[2]} text-base gap-2`,
  lg: `px-${spacing.scale[6]} py-${spacing.scale[3]} text-lg gap-2.5`,
  xl: `px-${spacing.scale[8]} py-${spacing.scale[4]} text-xl gap-3`,
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = "primary",
      size = "md",
      fullWidth = false,
      loading = false,
      leftIcon,
      rightIcon,
      disabled,
      className = "",
      children,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        className={`
          inline-flex items-center justify-center font-semibold tracking-wide
          rounded-${radii.button} transition-all duration-200 ease-out
          focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2
          disabled:opacity-50 disabled:cursor-not-allowed
          ${fullWidth ? "w-full" : ""}
          ${sizeStyles[size]}
          ${variantStyles[variant]}
          ${className}
        `}
        disabled={isDisabled}
        aria-busy={loading}
        {...props}
      >
        {loading && (
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="3"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        )}
        {!loading && leftIcon && <span aria-hidden="true">{leftIcon}</span>}
        {children}
        {!loading && rightIcon && <span aria-hidden="true">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = "Button";