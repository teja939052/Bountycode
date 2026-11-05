import { useEffect, useState, useCallback } from "react";
import { Clock, AlertCircle } from "lucide-react";
import { Card } from "../../design-system";

export interface PlacementTimerProps {
  seconds: number;
  onExpire: () => void;
}

export default function PlacementTimer({ seconds, onExpire }: PlacementTimerProps) {
  const [timeLeft, setTimeLeft] = useState(seconds);
  const [locked, setLocked] = useState(false);

  useEffect(() => {
    if (locked || timeLeft <= 0) return;
    const id = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          setLocked(true);
          onExpire();
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [timeLeft, locked, onExpire]);

  const minutes = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const display = `${minutes}:${secs.toString().padStart(2, "0")}`;

  return (
    <Card
      pad="sm"
      className="flex items-center gap-3 border-amber-500/30 bg-amber-500/5"
    >
      <Clock className="w-4 h-4 text-amber-500" />
      <span className="font-mono text-amber-400 font-bold">{display}</span>
      {locked && (
        <span className="text-xs text-red-400 flex items-center gap-1">
          <AlertCircle className="w-3 h-3" /> Time expired
        </span>
      )}
    </Card>
  );
}
