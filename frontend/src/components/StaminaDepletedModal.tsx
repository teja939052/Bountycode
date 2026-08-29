import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";

interface StaminaDepletedModalProps {
  visible: boolean;
  onClose: () => void;
  remaining: number;
}

export const StaminaDepletedModal: React.FC<StaminaDepletedModalProps> = ({ visible, onClose, remaining }) => {
  const navigate = useNavigate();

  const handleUpgrade = () => {
    navigate("/pricing");
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className="bg-space-panel border border-space-border rounded-2xl p-8 max-w-md w-full text-center"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
          >
            <div className="text-5xl mb-4">⚡</div>
            <h3 className="font-bold text-2xl text-text-primary mb-4 font-heading">
              Stamina Depleted!
            </h3>
            <p className="text-sm text-gray-400 font-mono mb-6">
              You've used all {3} free problems today. Upgrade to Pro for:
            </p>
            <ul className="space-y-2 mb-6 text-left">
              <li className="flex items-start gap-2 text-sm">
                <span className="text-cyber-green font-bold">✓</span>
                <span className="text-gray-300">Unlimited problems — no daily cap</span>
              </li>
              <li className="flex items-start gap-2 text-sm">
                <span className="text-cyber-green font-bold">✓</span>
                <span className="text-gray-300">53 company-specific question banks</span>
              </li>
              <li className="flex items-start gap-2 text-sm">
                <span className="text-cyber-green font-bold">✓</span>
                <span className="text-gray-300">Curated questions only (no templates)</span>
              </li>
            </ul>
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-3 mb-6">
              <p className="text-amber-800 font-bold font-mono text-sm">
                ₹99/mo — Less than 1 plate of samosas 🥟
              </p>
            </div>
            <button
              onClick={handleUpgrade}
              className="w-full py-3 px-4 bg-cyber-green text-white font-bold rounded-xl hover:shadow-lg transition-all border-b-2 border-cyber-green active:border-b-0 active:translate-y-[2px]"
            >
              Unlock Pro Pass
            </button>
            <button
              onClick={onClose}
              className="mt-3 text-xs text-gray-500 hover:text-gray-400 font-mono"
            >
              Keep browsing for now
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
