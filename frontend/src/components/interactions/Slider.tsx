// @ts-nocheck
import React from "react";

type SliderProps = {
  variable: string;
  min: number;
  max: number;
  step: number;
  onValueChange: (value: number) => void;
};

export default function Slider({ variable, min, max, step, onValueChange }: SliderProps) {
  const [value, setValue] = React.useState(min);

  React.useEffect(() => {
    onValueChange(value);
  }, [value, onValueChange]);

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-gray-700">{variable}: {value}</label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => setValue(Number(e.target.value))}
        className="w-full"
      />
      <div className="flex justify-between text-xs text-gray-500">
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  );
}
