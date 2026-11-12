import { motion, AnimatePresence } from "framer-motion";
import { X, ArrowRight, Rocket } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface OnboardingSlideProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function OnboardingSlide({ isOpen, onClose }: OnboardingSlideProps) {
  const navigate = useNavigate();

  const handleChooseJourney = () => {
    onClose();
    navigate("/journey");
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm p-4" onClick={onClose}>
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-black/5"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-end mb-4">
              <button onClick={onClose} className="p-2 rounded-full text-gray-500 hover:text-gray-700 hover:bg-gray-100" aria-label="Close">
                <X size={20} />
              </button>
            </div>

            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-emerald-600 flex items-center justify-center shadow-lg">
                <Rocket size={24} className="text-white" />
              </div>
              <div>
                <h2 className="font-display font-bold text-xl text-text-primary">Welcome to BountyCode</h2>
                <p className="text-sm text-brand-secondary">Your path to placement prep and your first offer.</p>
              </div>
            </div>

            <div className="text-center space-y-4">
              <p className="font-semibold text-text-primary">Let's start your journey</p>
              <button
                onClick={handleChooseJourney}
                className="w-full flex items-center justify-center gap-2 rounded-xl bg-primary text-white font-semibold py-4 shadow-primary hover:bg-primary-dark active:scale-[0.97]"
              >
                <ArrowRight size={18} /> Choose Journey
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
