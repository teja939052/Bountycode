import { motion } from "framer-motion";
import useReducedMotion from "../../hooks/useReducedMotion";

export default function AnimatedButton({ children, className = "", whileHover: hoverProp, whileTap: tapProp, ...props }) {
  const reduced = useReducedMotion();

  const defaultHover = reduced ? {} : { scale: 1.03 };
  const defaultTap = reduced ? {} : { scale: 0.97 };

  return (
    <motion.button
      className={className}
      whileHover={hoverProp ?? defaultHover}
      whileTap={tapProp ?? defaultTap}
      transition={{ type: "spring", stiffness: 400, damping: 20 }}
      {...props}
    >
      {children}
    </motion.button>
  );
}
