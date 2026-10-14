// @ts-nocheck
import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mentor } from "../../design-system/Mentor";
import CelebrationOverlay from "../CelebrationOverlay";
import { ArrowRight, Trophy } from "lucide-react";
import { Link } from "react-router-dom";
import { missionApi } from "../../services/api/missions";

export type MissionStepId =
  | "captain"
  | "visual"
  | "manipulate"
  | "predict"
  | "change"
  | "build"
  | "break"
  | "fix"
  | "recall"
  | "transfer"
  | "placement"
  | "prove"
  | "reward";

export type MissionStep = {
  id: MissionStepId;
  title: string;
  description: string;
  render: () => React.ReactNode;
};

export type StageEvidence = {
  stageId: string;
  passed?: boolean;
  diagnosisCode?: string;
  attemptCount?: number;
};

export type MissionEvidence = {
  skillId: string;
  stages: StageEvidence[];
  finalPassed: boolean;
  timeSpentSeconds: number;
};

export type FlagshipMissionProps = {
  captainMessage: string;
  captainMood?: "briefing" | "encouraging" | "celebrating" | "stuck";
  steps: MissionStep[];
  xpReward: number;
  backTo?: string;
  evidence?: MissionEvidence;
  onEvidenceUpdate?: (evidence: MissionEvidence) => void;
};

export default function FlagshipMissionShell({
  captainMessage,
  captainMood = "briefing",
  steps,
  xpReward,
  backTo = "/placement",
  evidence,
  onEvidenceUpdate,
}: FlagshipMissionProps) {
  const [step, setStep] = useState<MissionStepId>("captain");
  const [showCelebration, setShowCelebration] = useState(false);
  const [currentXp, setCurrentXp] = useState(0);
  const [startTime] = useState(() => Date.now());
  const [stageEvidence, setStageEvidence] = useState<Record<string, StageEvidence>>({});
  const [finalPassed, setFinalPassed] = useState(false);

  const currentStepIndex = steps.findIndex((s) => s.id === step);
  const progress = ((currentStepIndex + 1) / steps.length) * 100;

  const recordStage = useCallback(
    (stageId: string, patch: Partial<StageEvidence>) => {
      setStageEvidence((prev) => {
        const next = {
          ...prev,
          [stageId]: { ...prev[stageId], ...patch },
        };
        onEvidenceUpdate?.({
          skillId: evidence?.skillId || "general",
          stages: Object.values(next),
          finalPassed,
          timeSpentSeconds: Math.round((Date.now() - startTime) / 1000),
        });
        return next;
      });
    },
    [evidence?.skillId, finalPassed, onEvidenceUpdate, startTime],
  );

  const next = () => {
    const idx = steps.findIndex((s) => s.id === step);
    if (idx < steps.length - 1) {
      setStep(steps[idx + 1].id);
    }
  };

  const handleComplete = async () => {
    const timeSpent = Math.round((Date.now() - startTime) / 1000);
    const stages = Object.values(stageEvidence);
    const passedCount = stages.filter((s) => s.passed).length;
    const score = stages.length ? Math.round((passedCount / stages.length) * 100) : 0;

    const payload = {
      type: "learn",
      skill_id: evidence?.skillId || "general",
      passed: finalPassed || score >= 60,
      score,
      attempts: stages.reduce((sum, s) => sum + (s.attemptCount || 1), 0),
      time_spent: timeSpent,
      diagnosis_codes: stages
        .filter((s) => s.diagnosisCode)
        .map((s) => s.diagnosisCode),
    };

    try {
      await missionApi.recordActivity(payload);
    } catch {
      // fail-open: still show celebration locally
    }

    setCurrentXp(xpReward);
    setShowCelebration(true);
    setStep("reward");
  };

  const currentStep = steps[currentStepIndex];

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono uppercase tracking-wider text-[#9a9a9a]">
              Mission Progress
            </span>
            <span className="text-xs font-mono text-[#ffa116]">
              {currentStepIndex + 1}/{steps.length}
            </span>
          </div>
          <div className="h-2 rounded-full bg-[#2a2a2a]">
            <motion.div
              className="h-2 rounded-full bg-[#ffa116]"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          <div className="mt-2 text-xs text-[#9a9a9a]">{currentStep?.title}</div>
        </div>

        <AnimatePresence mode="wait">
          {step === "captain" && (
            <motion.div
              key="captain"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <Mentor mood={captainMood} message={captainMessage} />
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Let&apos;s begin <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {currentStep && step !== "captain" && step !== "reward" && (
            <motion.div
              key={step}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              {currentStep.render()}

              <div className="flex items-center justify-between">
                <div className="text-xs text-[#9a9a9a]">{currentStep.description}</div>
                <button
                  onClick={step === "prove" ? handleComplete : next}
                  className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
                >
                  {step === "prove" ? "Claim Reward" : "Next"}
                  {step !== "prove" && <ArrowRight size={16} />}
                  {step === "prove" && <Trophy size={16} />}
                </button>
              </div>
            </motion.div>
          )}

          {step === "reward" && (
            <motion.div
              key="reward"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="rounded-xl border border-[#ffa11655] bg-[#141414] p-8 text-center"
            >
              <Trophy className="mx-auto text-[#ffa116] mb-4" size={48} />
              <h2 className="text-2xl font-bold mb-2">Mission Complete!</h2>
              <p className="text-sm text-[#9a9a9a] mb-4">
                You earned {currentXp} XP. Tomorrow&apos;s mission will test whether this skill transfers.
              </p>
              <Link
                to={backTo}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Back to campaign <ArrowRight size={16} />
              </Link>
            </motion.div>
          )}
        </AnimatePresence>

        <CelebrationOverlay
          show={showCelebration}
          type="perfect"
          title={`+${xpReward} XP`}
          onClose={() => setShowCelebration(false)}
        />
      </div>
    </div>
  );
}
