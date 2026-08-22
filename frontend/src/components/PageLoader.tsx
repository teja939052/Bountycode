import { motion } from "framer-motion";
import Spinner from "../components/ui/Spinner";
import useReducedMotion from "../hooks/useReducedMotion";

export default function PageLoader() {
  const reduced = useReducedMotion();

  return (
    <div className="min-h-screen flex items-center justify-center bg-[radial-gradient(circle_at_top,rgba(79,143,87,0.08),transparent_34%),linear-gradient(180deg,#FAFAF6_0%,#F4EFE4_100%)]">
      <motion.div
        className="text-center"
        initial={reduced ? {} : { opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.2 }}
      >
        <Spinner size="lg" />
        <motion.p
          className="mt-4 text-sm text-brand-muted"
          initial={reduced ? {} : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          Loading...
        </motion.p>
      </motion.div>
    </div>
  );
}
