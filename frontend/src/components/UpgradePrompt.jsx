import { Link } from "react-router-dom";
import { Crown, Zap, Lock, ArrowRight } from "lucide-react";

export default function UpgradePrompt({ feature, description, compact = false }) {
  if (compact) {
    return (
      <div className="bg-gradient-to-r from-primary-50 to-purple-50 border border-primary-200 rounded-lg p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Lock size={18} className="text-primary-600" />
          <div>
            <p className="font-semibold text-sm">{feature}</p>
            <p className="text-xs text-gray-500">{description || "Upgrade to Pro to unlock"}</p>
          </div>
        </div>
        <Link
          to="/pricing"
          className="flex items-center gap-1 text-primary-600 font-semibold text-sm hover:text-primary-700 whitespace-nowrap"
        >
          Upgrade
          <ArrowRight size={14} />
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-8 text-white">
      <div className="flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
            <Crown size={28} />
          </div>
          <div>
            <h3 className="text-xl font-bold mb-1">{feature || "Unlock Full Power"}</h3>
            <p className="text-primary-100">
              {description || "Upgrade to Pro for unlimited access to all features"}
            </p>
          </div>
        </div>
        <Link
          to="/pricing"
          className="bg-white text-primary-700 px-6 py-3 rounded-lg font-bold hover:bg-primary-50 transition-colors shrink-0 flex items-center gap-2"
        >
          <Zap size={18} />
          Upgrade to Pro — $19/mo
        </Link>
      </div>
    </div>
  );
}