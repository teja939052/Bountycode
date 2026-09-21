import { useRef } from "react";
import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";

export default function ScrollingText({
  text,
  className = "",
}: {
  text: string;
  className?: string;
}) {
  const reducedMotion = useReducedMotion();
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const x = useTransform(scrollYProgress, [0, 1], ["-10%", "10%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.2, 1, 1, 0.2]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.92, 1, 0.92]);

  if (reducedMotion) {
    return (
      <div ref={ref} className={`overflow-hidden ${className}`}>
        <p className="text-center font-display text-2xl font-extrabold text-primary/90">{text}</p>
      </div>
    );
  }

  return (
    <div ref={ref} className={`overflow-hidden ${className}`}>
      <motion.p
        style={{ x, opacity, scale }}
        className="text-center font-display text-2xl font-extrabold text-primary/90"
      >
        {text}
      </motion.p>
    </div>
  );
}
