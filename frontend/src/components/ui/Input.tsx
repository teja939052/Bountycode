import { forwardRef, type InputHTMLAttributes, type ReactNode } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: ReactNode;
  error?: ReactNode;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = "", id, ...props }, ref) => {
    const inputId = id || props.name || (typeof label === "string" ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="mb-1.5 block text-[11px] font-mono uppercase tracking-[0.2em] text-text-muted">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : undefined}
          className={`input ${error ? "!border-red-400 !ring-red-100" : ""} ${className}`}
          {...props}
        />
        {error && <p id={`${inputId}-error`} className="mt-1 text-xs text-red-500 font-mono" role="alert">{error}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";
export default Input;
