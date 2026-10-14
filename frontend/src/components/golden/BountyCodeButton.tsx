// @ts-nocheck
import { motion, type MotionProps } from "framer-motion";
import { useMotion } from "../../hooks/useMotion";
import { motion as motionTokens } from "../../design-system/motion";
const { scale: scaleToken } = motionTokens;

type ButtonState = "rest" | "hover" | "press" | "success" | "loading" | "disabled" | "locked";

interface BountyCodeButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  state?: ButtonState;
  children: React.ReactNode;
  className?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  variant?: "primary" | "secondary" | "gold" | "ocean";
}

const VARIANT_CLASS: Record<NonNullable<BountyCodeButtonProps["variant"]>, string> = {
  primary: "btn-primary",
  secondary: "btn-secondary",
  gold: "btn-gold",
  ocean: "btn-ocean",
};

export function BountyCodeButton({
  state = "rest",
  children,
  className = "",
  leftIcon,
  rightIcon,
  variant = "primary",
  disabled,
  ...rest
}: BountyCodeButtonProps) {
  const { scale, springTransition } = useMotion();

  const scaleValue = (() => {
    if (disabled || state === "disabled" || state === "locked") return 1;
    switch (state) {
      case "press":
        return scaleToken.press;
      case "hover":
        return scaleToken.hover;
      case "success":
        return scaleToken.success;
      default:
        return 1;
    }
  })();

  const motionProps: MotionProps = {
    whileHover: disabled || state === "disabled" || state === "locked" ? {} : { scale: scaleToken.hover },
    whileTap: disabled || state === "disabled" || state === "locked" ? {} : { scale: scaleToken.press },
    transition: springTransition("interaction"),
  };

  return (
    <motion.button
      {...motionProps}
      disabled={disabled || state === "disabled" || state === "loading" || state === "locked"}
      className={`${VARIANT_CLASS[variant]} ${className}`}
      style={{
        transform: state === "press" ? `scale(${scaleValue})` : undefined,
      }}
      {...rest}
    >
      {state === "loading" && (
        <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {leftIcon && <span className="inline-flex shrink-0">{leftIcon}</span>}
      <span>{children}</span>
      {rightIcon && <span className="inline-flex shrink-0">{rightIcon}</span>}
    </motion.button>
  );
}
