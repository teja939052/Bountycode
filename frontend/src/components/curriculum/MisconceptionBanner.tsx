// @ts-nocheck
import { motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

interface MisconceptionBannerProps {
  misconception: {
    id: string;
    description: string;
    fix: string;
    confidence?: string;
  };
}

export default function MisconceptionBanner({ misconception }: MisconceptionBannerProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-amber-200 bg-amber-50/80 p-4"
    >
      <div className="flex items-start gap-3">
        <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
        <div className="flex-1">
          <p className="text-sm font-bold text-amber-900">{misconception.description}</p>
          <div className="mt-2 flex items-start gap-2 rounded-xl bg-amber-100/60 p-3">
            <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
            <p className="text-xs text-amber-900">{misconception.fix}</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
