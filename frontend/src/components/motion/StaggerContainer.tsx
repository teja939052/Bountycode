import { motion, type Variants } from "framer-motion";
import type { ReactNode } from "react";
import useReducedMotion from "../../hooks/useReducedMotion";

const container: Variants = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } },
};

export default function StaggerContainer({ children, className = "" }: { children?: ReactNode; className?: string }) {
  const reduced = useReducedMotion();

  return (
    <motion.div
      className={className}
      initial={reduced ? false : "hidden"}
      whileInView="show"
      viewport={{ once: true, margin: "-50px" }}
      variants={reduced ? {} : container}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({ children, className = "" }: { children?: ReactNode; className?: string }) {
  const reduced = useReducedMotion();

  return (
    <motion.div className={className} variants={reduced ? {} : item}>
      {children}
    </motion.div>
  );
}
