import { forwardRef } from "react";

const Input = forwardRef(({ label, error, className = "", ...props }, ref) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">
          {label}
        </label>
      )}
      <input
        ref={ref}
        className={`input ${error ? "!border-cyber-red" : ""} ${className}`}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-cyber-red font-mono">{error}</p>}
    </div>
  );
});

Input.displayName = "Input";
export default Input;
