// @ts-nocheck
import { motion, AnimatePresence } from "framer-motion";

export function AccordionItem({
  title,
  children,
  open = false,
}: {
  title: string;
  children: React.ReactNode;
  open?: boolean;
}) {
  return (
    <div className="rounded-xl border border-brand-primary/10 bg-white">
      <div className="px-4 py-3 text-sm font-semibold text-text-primary">{title}</div>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="border-t border-brand-primary/5 px-4 py-3 text-sm text-text-secondary">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function ExpandableCard({ title, children, className = "" }: { title: string; children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      whileHover={{ scale: 1.01 }}
      className={`rounded-2xl border border-brand-primary/10 bg-white p-5 shadow-soft ${className}`}
    >
      <div className="text-sm font-semibold text-text-primary">{title}</div>
      <div className="mt-2 text-sm text-text-secondary">{children}</div>
    </motion.div>
  );
}

export function ScrollRevealCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.4 }}
      className={`rounded-2xl border border-brand-primary/10 bg-white p-5 shadow-soft ${className}`}
    >
      {children}
    </motion.div>
  );
}
