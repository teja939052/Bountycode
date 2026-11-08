export default function Button({ children, variant = "primary", className = "", disabled, ...props }: { children?: React.ReactNode; variant?: string; className?: string; disabled?: boolean; [key: string]: any }) {
  const variants: Record<string, string> = {
    primary: "bg-primary text-white shadow-primary hover:bg-primary-dark active:scale-[0.97]",
    secondary: "bg-surface-2 text-primary border border-primary/20 hover:bg-primary/5 active:scale-[0.97]",
    ghost: "text-primary hover:bg-primary/10 active:scale-[0.97]",
    danger: "bg-red-500 text-white hover:bg-red-600 active:scale-[0.97]",
  };

  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-xl font-semibold px-5 py-3 text-sm transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap ${variants[variant]} ${className}`}
      disabled={disabled}
      aria-disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
