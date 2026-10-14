// @ts-nocheck
import React from "react";

type MemoryBoardProps = {
  variables: string[];
  initialValues: Record<string, any>;
  onStateChange: (state: Record<string, any>) => void;
};

export default function MemoryBoard({ variables, initialValues, onStateChange }: MemoryBoardProps) {
  const [state, setState] = React.useState(initialValues);

  React.useEffect(() => {
    onStateChange(state);
  }, [state, onStateChange]);

  const update = (key: string, value: any) => {
    setState((prev) => {
      const next = { ...prev, [key]: value };
      return next;
    });
  };

  return (
    <div className="grid gap-3">
      {variables.map((key) => (
        <div key={key} className="bg-white border-2 border-gray-200 rounded-xl p-4">
          <label className="text-xs font-mono text-gray-500 block mb-1">{key}</label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:border-brand-500"
            value={state[key] ?? ""}
            onChange={(e) => update(key, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
}
