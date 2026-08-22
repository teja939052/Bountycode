export default function Button({ children, variant = "primary", className = "", disabled, ...props }) {
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    ghost: "btn-ghost",
    danger: "btn-danger",
  };

  return (
    <button
      className={`${variants[variant]} inline-flex items-center justify-center gap-2 ${className}`}
      disabled={disabled}
      aria-disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
