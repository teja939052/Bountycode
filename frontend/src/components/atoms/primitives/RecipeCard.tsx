// @ts-nocheck
import { motion } from "framer-motion";

type RecipeCardProps = {
  steps: string[];
  activeStep?: number;
};

export default function RecipeCard({ steps, activeStep = 0 }: RecipeCardProps) {
  return (
    <div className="bg-white border rounded-xl p-4 shadow-sm max-w-md">
      <p className="text-xs font-mono text-gray-500 mb-2">Recipe</p>
      <div className="flex flex-col gap-2">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            className={`flex items-center gap-3 px-3 py-2 rounded-lg ${
              idx === activeStep ? "bg-brand-50 border border-brand-200" : "bg-gray-50"
            }`}
            animate={{ x: idx === activeStep ? [0, 4, 0] : 0 }}
            transition={{ duration: 0.3 }}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
              idx === activeStep ? "bg-brand-500 text-white" : "bg-gray-200 text-gray-600"
            }`}>
              {idx + 1}
            </span>
            <span className={`text-sm ${idx === activeStep ? "text-gray-900 font-medium" : "text-gray-600"}`}>
              {step}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
