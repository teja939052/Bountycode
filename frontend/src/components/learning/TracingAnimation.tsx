// @ts-nocheck
import { useState, useEffect, useRef } from "react";

export type TraceStep = {
  pc: number;
  line: string;
  vars?: Record<string, any>;
  return?: any;
  output?: string;
  error?: string;
  handler?: string;
  break?: boolean;
};

type Props = {
  steps: TraceStep[];
  cardId: string;
  autoPlay?: boolean;
  delayMs?: number;
};

export default function TracingAnimation({ steps, cardId, autoPlay = false, delayMs = 700 }: Props) {
  const [idx, setIdx] = useState(0);
  const timer = useRef<number | null>(null);

  const clearTimer = () => {
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = null;
    }
  };

  useEffect(() => {
    clearTimer();
    setIdx(0);
    if (autoPlay && steps.length) {
      timer.current = window.setInterval(() => {
        setIdx((i) => {
          if (i >= steps.length - 1) {
            clearTimer();
            return i;
          }
          return i + 1;
        });
      }, delayMs);
    }
    return clearTimer;
  }, [autoPlay, cardId, steps.length, delayMs]);

  const step = steps[idx] || steps[0];
  const vars = step?.vars || {};
  const line = step?.line || "";
  const error = step?.error;
  const output = step?.output;
  const ret = step?.return;
  const handler = step?.handler;
  const isBreak = step?.break;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold text-text-secondary">
          Frame {idx + 1} / {steps.length}
        </div>
        <div className="flex items-center gap-2">
          <button
            className="rounded-md border border-border-muted px-2 py-1 text-xs text-text-secondary hover:border-brand hover:text-brand"
            onClick={() => setIdx((i) => Math.min(i + 1, steps.length - 1))}
          >
            Next
          </button>
          <button
            className="rounded-md border border-border-muted px-2 py-1 text-xs text-text-secondary hover:border-brand hover:text-brand"
            onClick={() => setIdx(0)}
          >
            Reset
          </button>
        </div>
      </div>
      <div className="rounded-xl border border-border-muted bg-surface-raised p-4">
        <div className="space-y-2">
          <div className="rounded-lg bg-surface p-2">
            <span className="text-xs font-semibold text-text-secondary">pc {step?.pc}</span>
            <span className="ml-2 rounded-full bg-surface-raised px-2 py-1 font-mono text-sm text-text-primary">
              {line}
            </span>
          </div>
          {error && (
            <div className="rounded-lg border border-red-300 bg-red-50 p-2 text-xs text-red-700">
              <span className="font-semibold">Error:</span> {error}
            </div>
          )}
          {handler && (
            <div className="rounded-lg border border-amber-300 bg-amber-50 p-2 text-xs text-amber-800">
              <span className="font-semibold">Caught:</span> {handler}
            </div>
          )}
          {isBreak && (
            <div className="rounded-lg border border-purple-300 bg-purple-50 p-2 text-xs text-purple-800">
              <span className="font-semibold">Loop ended</span>
            </div>
          )}
        </div>
      </div>
      <div className="rounded-xl border border-border-muted bg-surface-raised p-4">
        <div className="text-xs font-semibold text-text-secondary">Variables</div>
        <div className="mt-2 flex flex-wrap gap-2">
          {Object.entries(vars).map(([key, value]) => (
            <span
              key={key}
              className="rounded-full border border-brand/40 bg-brand/10 px-2 py-1 font-mono text-xs text-brand"
            >
              {key} = {typeof value === "object" ? JSON.stringify(value) : value}
            </span>
          ))}
        </div>
      </div>
      {(output || ret !== undefined) && (
        <div className="rounded-xl border border-emerald-300 bg-emerald-50 p-3 text-xs text-emerald-900">
          <span className="font-semibold">Return:</span> {JSON.stringify(ret ?? output)}
        </div>
      )}
    </div>
  );
}
