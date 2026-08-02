import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";

export default function AnimatedCard({ children, className = "", delay = 0, ...props }) {
  const reduced = useReducedMotion();

  return (
    <motion.div
      className={className}
      initial={reduced ? false : { opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.4, delay, ease: "easeOut" }}
      whileHover={reduced ? {} : { y: -4, transition: { type: "spring", stiffness: 400, damping: 25 } }}
      {...props}
    >
      {children}
    </motion.div>
  );
}
