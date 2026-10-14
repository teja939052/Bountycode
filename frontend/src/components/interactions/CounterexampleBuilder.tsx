// @ts-nocheck
import React from "react";
import { motion } from "framer-motion";

type CounterexampleBuilderProps = {
  claim: string;
  variables: Record<string, { min: number; max: number }>;
  onCounterexample: (values: Record<string, number>) => void;
};

export default function CounterexampleBuilder({ claim, variables, onCounterexample }: CounterexampleBuilderProps) {
  const [values, setValues] = React.useState<Record<string, number>>({});
  const [submitted, setSubmitted] = React.useState(false);

  const update = (key: string, value: number) => {
    setValues((prev) => ({ ...prev, [key]: value }));
    setSubmitted(false);
  };

  const submit = () => {
    setSubmitted(true);
    onCounterexample(values);
  };

  return (
    <div className="space-y-4">
      <p className="text-gray-800">Claim: "{claim}"</p>
      <p className="text-sm text-gray-600">Set values to find a counterexample:</p>
      <div className="grid gap-3">
        {Object.entries(variables).map(([key, range]) => (
          <div key={key}>
            <label className="text-sm font-medium text-gray-700 block mb-1">{key}</label>
            <input
              type="range"
              min={range.min}
              max={range.max}
              value={values[key] ?? range.min}
              onChange={(e) => update(key, Number(e.target.value))}
              className="w-full"
            />
            <span className="text-xs text-gray-500">{values[key] ?? range.min}</span>
          </div>
        ))}
      </div>
      <motion.button
        className="bg-brand-500 text-white px-6 py-2 rounded-full"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={submit}
      >
        Test claim
      </motion.button>
      {submitted && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
          <p className="text-sm text-yellow-800">Does this break the claim? Analyze the result.</p>
        </div>
      )}
    </div>
  );
}
