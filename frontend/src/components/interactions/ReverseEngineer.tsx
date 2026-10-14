// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type ReverseEngineerProps = {
  input: number;
  output: number;
  rules: string[];
  onRuleSelected: (rule: string) => void;
};

export default function ReverseEngineer({ input, output, rules, onRuleSelected }: ReverseEngineerProps) {
  const [selected, setSelected] = React.useState<string | null>(null);

  return (
    <div className="space-y-4">
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <p className="text-sm text-blue-800">
          Input: {input} → Output: {output}
        </p>
      </div>
      <p className="text-sm text-gray-600">What rule could produce this?</p>
      <div className="grid gap-2">
        {rules.map((rule) => (
          <motion.button
            key={rule}
            className={`px-4 py-3 rounded-xl border-2 text-left text-sm ${
              selected === rule ? "border-brand-500 bg-brand-50" : "border-gray-200 bg-white"
            }`}
            whileHover={{ scale: 1.01 }}
            onClick={() => { setSelected(rule); onRuleSelected(rule); }}
          >
            {rule}
          </motion.button>
        ))}
      </div>
      {selected && (
        <p className="text-xs text-gray-500">Now apply this rule to a new input.</p>
      )}
    </div>
  );
}
