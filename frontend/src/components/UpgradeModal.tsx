import { motion, AnimatePresence } from "framer-motion";
import { Zap, ArrowRight, X, Check } from "lucide-react";

export default function UpgradeModal({ isOpen, onClose, feature, benefit, plan = "pro" }) {
  if (!isOpen) return null;

  const handleUpgrade = () => {
    window.location.href = `/pricing?selected=${plan}&from=${feature || "upgrade"}`;
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
          <motion.div
            className="bg-white dark:bg-gray-900 rounded-2xl p-6 max-w-md w-full shadow-2xl"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Zap className="text-cyber-blue" size={20} />
                <h2 className="text-xl font-bold dark:text-white">Unlock {feature}</h2>
              </div>
              <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
                <X size={20} />
              </button>
            </div>

            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">{benefit}</p>

            <div className="space-y-2 mb-6">
              {plan === "pro" ? (
                <>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Unlimited {feature.replace(/_/g, " ")}
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Full company question banks (10,000+)
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Semantic ATS scoring + rewrite
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Placement Predictor for 50+ companies
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Priority AI feedback
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> Everything in Pro
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> One-time payment — never billed again
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                    <Check size={16} className="text-green-500" /> All future updates included
                  </div>
                </>
              )}
            </div>

            <div className="flex gap-3">
              <button onClick={onClose} className="flex-1 btn-secondary">Not Now</button>
              <button onClick={handleUpgrade} className="flex-1 btn-primary flex items-center justify-center gap-2">
                Get {plan === "pro" ? "Pro" : "Lifetime"} <ArrowRight size={16} />
              </button>
            </div>

            <p className="text-xs text-gray-500 text-center mt-3">7-day free trial, cancel anytime</p>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
