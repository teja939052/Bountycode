interface SpinnerProps {
  size?: string | number;
  className?: string;
}

export default function Spinner({ size = "md", className = "" }: SpinnerProps) {
  const sizes = {
    sm: "w-5 h-5",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };
  const cls = typeof size === "number" ? "" : sizes[size] || sizes.md;
  const style = typeof size === "number" ? { width: size, height: size } : undefined;

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div
        style={style}
        className={`${cls} rounded-full border-4 border-slate-200 border-t-brand-sky text-brand-sky animate-spin`}
      />
    </div>
  );
}
