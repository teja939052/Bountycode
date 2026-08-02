import { useState, useEffect } from "react";
import api from "../services/api";
import UpgradeModal from "../components/UpgradeModal";

const FEATURE_DEFAULT_LIMITS = {
  interview: { limit: 5, label: "AI Interviews", upgrade: "Unlimited mock interviews with AI feedback" },
  resume: { limit: 3, label: "Resume Reviews", upgrade: "Unlimited resume analysis & optimization" },
  aptitude: { limit: 5, label: "Aptitude Tests", upgrade: "Unlimited aptitude practice with weak area analysis" },
  cover_letter: { limit: 3, label: "Cover Letters", upgrade: "Unlimited cover letters + LinkedIn About" },
  company_mock: { limit: 1, label: "Company Mocks", upgrade: "TCS/Infosys/Wipro/Accenture mock papers" },
  predictor: { limit: 3, label: "Predictions", upgrade: "Placement probability for 50+ companies" },
  question_bank: { limit: 5, label: "Question Bank", upgrade: "10,000+ company-tagged questions" },
};

export function useFeatureGate(feature) {
  const [allowed, setAllowed] = useState(true);
  const [remaining, setRemaining] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [usage, setUsage] = useState({ used: 0, limit: 0 });

  useEffect(() => {
    let cancelled = false;
    const check = async () => {
      try {
        const data = await api.getUsageStats();
        const featureLimits = data.features?.[feature];
        if (!featureLimits || cancelled) return;

        const limit = featureLimits.monthly_limit;
        const used = featureLimits.monthly_used;
        const isPro = data.plan === "pro" || data.plan === "lifetime";

        setUsage({ used, limit: limit === "unlimited" ? -1 : limit });
        setRemaining(isPro ? -1 : (limit === "unlimited" ? -1 : limit - used));

        if (!isPro && limit !== "unlimited" && used >= limit) {
          setAllowed(false);
        } else {
          setAllowed(true);
        }
      } catch {
        setAllowed(true);
      }
    };
    check();
    return () => { cancelled = true; };
  }, [feature]);

  const triggerUpgrade = () => {
    setShowModal(true);
  };

  const closeModal = () => setShowModal(false);

  const meta = FEATURE_DEFAULT_LIMITS[feature] || { label: feature, upgrade: "Upgrade to unlock" };

  return {
    allowed,
    remaining,
    usage,
    triggerUpgrade,
    modal: (
      <UpgradeModal
        isOpen={showModal}
        onClose={closeModal}
        feature={meta.label}
        benefit={meta.upgrade}
        plan="pro"
      />
    ),
  };
}
