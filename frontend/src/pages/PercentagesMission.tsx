// @ts-nocheck
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mentor } from "../design-system/Mentor";
import CelebrationOverlay from "../components/CelebrationOverlay";
import {
  ArrowRight,
  RotateCcw,
  CheckCircle,
  XCircle,
  Sparkles,
  Trophy,
} from "lucide-react";

type Step =
  | "captain"
  | "visual"
  | "manipulate"
  | "predict"
  | "change"
  | "build"
  | "break"
  | "fix"
  | "transfer"
  | "placement"
  | "prove"
  | "reward";

const STEPS: { id: Step; title: string; description: string }[] = [
  { id: "captain", title: "Welcome", description: "Captain Byte introduces the mission" },
  { id: "visual", title: "Visual", description: "See percentages in action" },
  { id: "manipulate", title: "Manipulate", description: "Change values and observe" },
  { id: "predict", title: "Predict", description: "What happens if...?" },
  { id: "change", title: "Change", description: "Change one thing" },
  { id: "build", title: "Build", description: "Write the formula" },
  { id: "break", title: "Break", description: "Introduce a bug" },
  { id: "fix", title: "Fix", description: "Debug and repair" },
  { id: "transfer", title: "Transfer", description: "Apply to a new problem" },
  { id: "placement", title: "Placement", description: "Real placement question" },
  { id: "prove", title: "Prove", description: "Submit your answer" },
  { id: "reward", title: "Reward", description: "Claim your XP" },
];

export default function PercentagesMission() {
  const [step, setStep] = useState<Step>("captain");
  const [showCelebration, setShowCelebration] = useState(false);
  const [xp, setXp] = useState(0);
  const [captainMessage, setCaptainMessage] = useState(
    "Today we're mastering percentages. This is one of the most common topics in placement tests. Let's build real understanding, not just memorization."
  );

  const currentStepIndex = STEPS.findIndex((s) => s.id === step);
  const progress = ((currentStepIndex + 1) / STEPS.length) * 100;

  const next = () => {
    const idx = STEPS.findIndex((s) => s.id === step);
    if (idx < STEPS.length - 1) {
      setStep(STEPS[idx + 1].id);
    }
  };

  const handleComplete = () => {
    setXp(150);
    setShowCelebration(true);
    setStep("reward");
  };

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
              {currentStepIndex + 1}/{STEPS.length}
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
          <div className="mt-2 text-xs text-[#9a9a9a]">{STEPS[currentStepIndex]?.title}</div>
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
              <Mentor mood="briefing" message={captainMessage} />
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Let's begin <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "visual" && (
            <motion.div
              key="visual"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Visual Explanation</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  A percentage is a fraction out of 100. If you have 25 out of 100, that's 25%.
                </p>
                <div className="grid grid-cols-10 gap-1 mb-4">
                  {Array.from({ length: 100 }).map((_, i) => (
                    <div
                      key={i}
                      className={`h-8 rounded ${
                        i < 25 ? "bg-[#ffa116]" : "bg-[#2a2a2a]"
                      }`}
                    />
                  ))}
                </div>
                <p className="text-xs text-[#9a9a9a]">
                  Orange = 25 items out of 100 total = 25%
                </p>
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Got it <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "manipulate" && (
            <motion.div
              key="manipulate"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Manipulate</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  Change the percentage and see what happens.
                </p>
                <PercentSlider />
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Next <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "predict" && (
            <motion.div
              key="predict"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Predict</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  If you increase 25% by 20%, what's the new percentage?
                </p>
                <input
                  type="number"
                  placeholder="Your answer"
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
                />
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Check <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "change" && (
            <motion.div
              key="change"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Change One Thing</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  Change the base from 100 to 200. What happens to the percentage?
                </p>
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                I see it <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "build" && (
            <motion.div
              key="build"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Tiny Build</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  Write the formula: percentage = (part / total) × 100
                </p>
                <input
                  type="text"
                  placeholder="(part / total) * 100"
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none font-mono"
                />
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Next <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "break" && (
            <motion.div
              key="break"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Break It</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  What if total = 0? Try it.
                </p>
                <div className="rounded-lg bg-[#0f0f0f] border border-red-500/30 p-4">
                  <code className="text-sm text-red-400">Error: Division by zero</code>
                </div>
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Fix it <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "fix" && (
            <motion.div
              key="fix"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Fix</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  Add a guard: if total === 0, return 0.
                </p>
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                  Fixed <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "transfer" && (
            <motion.div
              key="transfer"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Transfer</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  A shirt costs ₹800. After a 15% discount, what's the final price?
                </p>
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                I can do this <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "placement" && (
            <motion.div
              key="placement"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <h2 className="text-xl font-bold mb-4">Placement Question</h2>
                <p className="text-sm text-[#9a9a9a] mb-4">
                  If 40% of a number is 80, what is 60% of the same number?
                </p>
                <input
                  type="number"
                  placeholder="Your answer"
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2 text-sm text-[#e9e9e9] placeholder:text-[#9a9a9a] focus:border-[#ffa116] focus:outline-none"
                />
              </div>
              <button
                onClick={next}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Submit <ArrowRight size={16} />
              </button>
            </motion.div>
          )}

          {step === "prove" && (
            <motion.div
              key="prove"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              <div className="rounded-xl border border-[#2a2a2a] bg-[#141414] p-6">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle className="text-green-400" size={24} />
                  <h2 className="text-xl font-bold">Correct!</h2>
                </div>
                <p className="text-sm text-[#9a9a9a]">
                  If 40% = 80, then 1% = 2, so 60% = 120.
                </p>
              </div>
              <button
                onClick={handleComplete}
                className="inline-flex items-center gap-2 rounded-lg bg-[#ffa116] px-5 py-2 text-sm font-semibold text-black hover:brightness-110"
              >
                Claim Reward <Trophy size={16} />
              </button>
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
                You earned {xp} XP. Tomorrow's mission will test whether this skill transfers.
              </p>
              <Link
                to="/placement"
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
          title="+150 XP"
          onClose={() => setShowCelebration(false)}
        />
      </div>
    </div>
  );
}

function PercentSlider() {
  const [percent, setPercent] = useState(25);

  return (
    <div className="space-y-4">
      <input
        type="range"
        min="0"
        max="100"
        value={percent}
        onChange={(e) => setPercent(Number(e.target.value))}
        className="w-full"
      />
      <div className="text-center">
        <span className="text-3xl font-bold text-[#ffa116]">{percent}%</span>
      </div>
      <div className="grid grid-cols-10 gap-1">
        {Array.from({ length: 100 }).map((_, i) => (
          <div
            key={i}
            className={`h-6 rounded ${
              i < percent ? "bg-[#ffa116]" : "bg-[#2a2a2a]"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
