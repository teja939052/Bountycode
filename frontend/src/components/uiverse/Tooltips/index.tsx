// @ts-nocheck
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function Tooltip({
  text,
  children,
  position = "top",
}: {
  text: string;
  children: React.ReactNode;
  position?: "top" | "bottom" | "left" | "right";
}) {
  const [visible, setVisible] = useState(false);
  const positionClasses: Record<string, string> = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2",
  };

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      <AnimatePresence>
        {visible && (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 4 }}
            className={`absolute z-50 whitespace-nowrap rounded-lg bg-black/80 px-3 py-1.5 text-xs text-white ${positionClasses[position]}`}
          >
            {text}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function RichTooltip({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div className="relative inline-block" onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}>
      {children}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="absolute z-50 w-72 rounded-xl border border-brand-primary/10 bg-white p-4 shadow-lg"
          >
            <div className="text-sm font-semibold text-text-primary">{title}</div>
            <div className="mt-1 text-xs text-text-secondary">{description}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
