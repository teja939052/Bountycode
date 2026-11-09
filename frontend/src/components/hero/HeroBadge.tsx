import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

function HeroBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
      className="mx-auto inline-flex items-center gap-2 rounded-full border border-white/70 bg-white/55 px-3.5 py-1.5 text-[11px] font-bold uppercase tracking-[0.16em] backdrop-blur-[2px] shadow-lg shadow-white/20"
      style={{ color: "#33453B" }}
    >
      <Sparkles size={11} style={{ color: "#D4A843" }} aria-hidden="true" />
      Built for the service-company pipeline
    </motion.div>
  );
}

export { HeroBadge };
export default HeroBadge;
