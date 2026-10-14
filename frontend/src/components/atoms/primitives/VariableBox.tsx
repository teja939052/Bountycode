// @ts-nocheck
import { motion } from "framer-motion";

type VariableBoxProps = {
  label: string;
  value: string | number;
  onChange?: (value: string) => void;
  readOnly?: boolean;
};

export default function VariableBox({ label, value, onChange, readOnly }: VariableBoxProps) {
  return (
    <div className="inline-flex items-center gap-2 bg-gray-50 border rounded-xl px-4 py-3 shadow-sm">
      <span className="font-mono text-sm text-gray-500">{label}</span>
      <span className="text-gray-400">=</span>
      <motion.input
        type="text"
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        readOnly={readOnly}
        className="w-24 rounded-lg border px-3 py-1 text-center font-mono text-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
        whileFocus={{ scale: 1.05 }}
      />
    </div>
  );
}
