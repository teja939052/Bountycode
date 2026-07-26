import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        <motion.p
          className="text-8xl font-display font-black text-cyber-blue mb-4 glow-blue"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ repeat: Infinity, duration: 3 }}
        >
          404
        </motion.p>
        <h1 className="text-2xl font-display font-bold text-white mb-2">Signal Lost</h1>
        <p className="text-gray-500 font-mono text-sm mb-6">
          Target coordinates not found in system database.
        </p>
        <Link to="/" className="btn-primary inline-block">
          Return to Base
        </Link>
      </motion.div>
    </div>
  );
}
