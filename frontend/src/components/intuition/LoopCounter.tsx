import { useState, useCallback } from "react";
import { ArrowRight, RefreshCw, Play, StopCircle } from "lucide-react";
import { Card, Button } from "../../design-system";

export interface LoopCounterProps {
  limit: number;
  onComplete: () => void;
}

export default function LoopCounter({ limit, onComplete }: LoopCounterProps) {
  const [i, setI] = useState(0);
  const [running, setRunning] = useState(false);
  const [done, setDone] = useState(false);
  const [history, setHistory] = useState<number[]>([]);

  const tick = useCallback(() => {
    if (i < limit) {
      setHistory((h) => [...h, i]);
      setI((prev) => prev + 1);
    } else {
      setDone(true);
      setRunning(false);
      onComplete();
    }
  }, [i, limit, onComplete]);

  const reset = useCallback(() => {
    setI(0);
    setDone(false);
    setRunning(false);
    setHistory([]);
  }, []);

  return (
    <Card pad="md" className="bg-[#0f0f0f] border-[#2a2a2a]">
      <div className="flex items-center gap-2 mb-4">
        <Play className="w-4 h-4 text-amber-500" />
        <span className="font-mono text-sm text-text">for (let i = 0; i &lt; {limit}; i++)</span>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-4">
        <div className="p-3 rounded-lg border border-[#2a2a2a] bg-[#1a1a1a]">
          <div className="text-xs text-[#9a9a9a]">Current i</div>
          <div className="font-mono text-lg text-text">{i}</div>
        </div>
        <div className="p-3 rounded-lg border border-[#2a2a2a] bg-[#1a1a1a]">
          <div className="text-xs text-[#9a9a9a]">Iterations run</div>
          <div className="font-mono text-lg text-text">{history.length}</div>
        </div>
      </div>

      {history.length > 0 && (
        <div className="mb-4">
          <div className="text-xs text-[#9a9a9a] mb-2">Trace</div>
          <div className="flex gap-1">
            {history.map((v, idx) => (
              <div key={idx} className="px-2 py-1 rounded border border-[#333] bg-[#16161a] text-xs font-mono text-[#e9e9e9]">
                i={v}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-3">
        {done ? (
          <Button variant="outline" onClick={reset} size="sm">
            <RefreshCw className="w-4 h-4" /> Reset
          </Button>
        ) : (
          <>
            <Button
              variant={running ? "secondary" : "primary"}
              onClick={() => setRunning((r) => !r)}
              size="sm"
            >
              {running ? <StopCircle className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {running ? "Pause" : "Step"}
            </Button>
            <Button variant="ghost" onClick={tick} size="sm" disabled={running}>
              <ArrowRight className="w-4 h-4" /> Next
            </Button>
          </>
        )}
      </div>

      {done && (
        <p className="mt-3 text-sm text-green-400 font-medium">
          Loop finished after {limit} iterations (i = 0..{limit - 1}).
        </p>
      )}
    </Card>
  );
}
