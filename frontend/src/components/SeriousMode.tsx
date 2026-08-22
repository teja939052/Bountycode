import { ReactNode, useEffect } from "react";
import { motion } from "framer-motion";
import { X, Clock, Brain, BarChart3 } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

interface SeriousModeProps {
  title: string;
  timeRemaining: number | null;
  onExit: () => void;
  children: ReactNode;
}

export default function SeriousMode({ title, timeRemaining, onExit, children }: SeriousModeProps) {
  const reduced = useReducedMotion();

  useEffect(() => {
    document.documentElement.classList.add("serious-mode");
    return () => document.documentElement.classList.remove("serious-mode");
  }, []);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
      .toString()
      .padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={reduced ? {} : { opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="fixed inset-0 z-50 flex flex-col bg-surface text-text-primary overflow-hidden"
    >
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-surface/95 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <Brain size={20} className="text-primary" />
          <span className="font-medium text-text-primary">{title}</span>
        </div>

        <div className="flex items-center gap-4">
          {timeRemaining !== null && (
            <div className="flex items-center gap-2 px-3 py-1 rounded-[8px] bg-border/20">
              <Clock size={14} className="text-text-muted" />
              <span className="font-mono text-sm text-text-primary">{formatTime(timeRemaining)}</span>
            </div>
          )}
          <button
            onClick={onExit}
            className="p-1.5 rounded-[8px] text-text-muted hover:text-text-primary hover:bg-primary-soft transition-colors"
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {children}
      </div>

      {/* Status bar */}
      <div className="flex items-center justify-between px-4 py-2 border-t border-border bg-surface/95 text-xs text-text-muted">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full bg-primary" />
            <span>Serious mode active</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button className="hover:text-text-primary transition-colors">
            <BarChart3 size={14} />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
