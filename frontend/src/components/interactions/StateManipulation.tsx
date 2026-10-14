// @ts-nocheck
import React from "react";

type StateManipulationProps = {
  variable: string;
  initial: any;
  onStateChange: (state: any) => void;
};

export default function StateManipulation({ variable, initial, onStateChange }: StateManipulationProps) {
  const [value, setValue] = React.useState(initial);

  React.useEffect(() => {
    onStateChange({ [variable]: value });
  }, [variable, value]);

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-gray-700">{variable}</label>
      <input
        type="number"
        className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500"
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
      />
    </div>
  );
}
