// @ts-nocheck
import { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, Lightbulb, RefreshCw, Trophy, Loader2 } from "lucide-react";
import { lessonApi } from "../services/api/lesson";
import MissionPackRenderer from "../components/mission/MissionPackRenderer";
import { BountyCodeLoader } from "../components/brand/BountyCodeBrandMotion";

export default function MissionPackPlayer() {
  const { packId } = useParams<{ packId: string }>();
  const [pack, setPack] = useState(null);
  const [session, setSession] = useState(null);
  const [currentStep, setCurrentStep] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [answerResult, setAnswerResult] = useState(null);
  const [hint, setHint] = useState("");
  const [showHint, setShowHint] = useState(false);
  const [diamondsEarned, setDiamondsEarned] = useState(0);
  const [mistakeCount, setMistakeCount] = useState(0);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (!packId) return;
    setLoading(true);
    lessonApi.getLessonPlayerSession
      ? lessonApi.getLessonPlayerReteach(packId).catch(() => {})
      : Promise.resolve();

    // Fetch mission pack from backend
    fetch(`/api/v1/mission-packs/${encodeURIComponent(packId)}`)
      .then((r) => r.json())
      .then((data) => {
        if (data?.pack) {
          setPack(data.pack);
          startLesson(data.pack);
        } else {
          setLoading(false);
        }
      })
      .catch(() => setLoading(false));
  }, [packId]);

  const startLesson = async (packData) => {
    try {
      const domain = packData.domain || "aptitude";
      const params: any = {
        domain,
        mastery_threshold: packData.mastery_threshold || 75,
      };
      if (domain === "aptitude") {
        params.topic = packData.concept || packData.skill_id;
        params.difficulty = packData.difficulty || "medium";
      } else if (domain === "coding") {
        params.world_id = "foundations";
        params.level_id = "level-1";
      } else if (domain === "company") {
        params.company = packData.tags?.[0] || "general";
        params.role = "sde";
      }

      const res = await lessonApi.startLessonPlayer(params);
      if (res?.session_id) {
        setSession(res);
        setCurrentStep(res.step);
      }
    } catch (e) {
      console.error("Failed to start lesson:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = useCallback(async (payload) => {
    if (!session) return;
    setSubmitting(true);
    setAnswerResult(null);
    setShowHint(false);

    try {
      const res = await lessonApi.submitLessonPlayer(session.session_id, payload);
      if (res) {
        setAnswerResult({
          passed: res.passed || false,
          score: res.score || 0,
          message: res.message || "",
          mastery_unlocked: res.mastery_unlocked || false,
          reward: res.reward || {},
          reteach_required: res.reteach_required || false,
          next_step: res.next_step || null,
        });

        if (res.passed) {
          if (res.mastery_unlocked) {
            setDiamondsEarned((p) => p + (res.reward?.diamonds || 0));
            setCompleted(true);
          }
        } else {
          setMistakeCount((p) => p + 1);
        }

        if (res.next_step && !res.reteach_required) {
          setCurrentStep(res.next_step.step);
        }
      }
    } catch (e) {
      console.error("Submit failed:", e);
      setAnswerResult({
        passed: false,
        score: 0,
        message: "Submission failed. Please try again.",
        mastery_unlocked: false,
        reward: {},
        reteach_required: false,
        next_step: null,
      });
    } finally {
      setSubmitting(false);
    }
  }, [session]);

  const handleHint = useCallback(async () => {
    if (!session || !currentStep) return;
    try {
      const res = await lessonApi.requestLessonPlayerHint(session.session_id, currentStep.step_index);
      if (res?.hint) {
        setHint(res.hint);
        setShowHint(true);
      }
    } catch (e) {
      setHint("Review the step content and try again.");
      setShowHint(true);
    }
  }, [session, currentStep]);

  const handleRetry = useCallback(() => {
    setAnswerResult(null);
    setShowHint(false);
  }, []);

  const handleReteach = useCallback(async () => {
    if (!session) return;
    try {
      const res = await lessonApi.getLessonPlayerReteach(session.session_id);
      if (res?.plan) {
        setHint(`Reteach: ${res.reteach_action || "Review the concept again."}`);
        setShowHint(true);
      }
    } catch (e) {
      console.error("Reteach failed:", e);
    }
  }, [session]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <BountyCodeLoader size={32} />
          <p className="mt-3 text-sm text-text-muted">Loading mission pack...</p>
        </div>
      </div>
    );
  }

  if (!pack || !session || !currentStep) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="text-center">
          <p className="font-bold text-text-primary">Failed to load mission pack</p>
          <Link to="/journey" className="btn-primary mt-4 inline-block text-sm">
            Back to Journey
          </Link>
        </div>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-emerald-200 bg-emerald-50 p-8 text-center"
        >
          <Trophy className="mx-auto h-16 w-16 text-yellow-500 mb-4" />
          <h1 className="text-3xl font-bold mb-2">Mission Complete!</h1>
          <p className="text-text-secondary mb-1">{pack.title}</p>
          <p className="text-2xl font-bold text-emerald-700 mt-2">💎 {diamondsEarned} Diamonds</p>
          <p className="text-sm text-text-muted mt-1">Diamonds earned</p>
          <div className="mt-4 flex justify-center gap-3">
            <Link to="/journey" className="btn-primary text-sm">
              Back to Journey
            </Link>
            <Link to={`/mission/${packId}`} className="btn-secondary text-sm">
              Review Pack
            </Link>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-base px-4 pb-32 pt-4 md:pb-16">
      <div className="mx-auto w-full max-w-2xl space-y-4">
        <div className="flex items-center justify-between gap-2">
          <Link to="/journey" className="inline-flex min-h-[44px] items-center gap-1 font-mono text-xs text-text-muted">
            <ArrowLeft size={14} /> Journey
          </Link>
          <div className="flex items-center gap-3">
            <span className="font-mono text-[11px] text-text-muted">
              {pack.title} · Step {currentStep.step_index + 1}/{session.total_steps || 9}
            </span>
            <span className="font-mono text-[11px] text-text-muted">💎 {diamondsEarned}</span>
          </div>
        </div>

        {mistakeCount > 0 && (
          <div className="flex items-center gap-2 rounded-2xl border border-orange-200 bg-orange-50 p-3 text-sm text-orange-700">
            <Lightbulb size={16} />
            <span>{mistakeCount} mistake{mistakeCount !== 1 ? "s" : ""} — that's data, not failure.</span>
          </div>
        )}

        {showHint && hint && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-blue-200 bg-blue-50 p-4"
          >
            <div className="flex items-start gap-2">
              <Lightbulb size={18} className="shrink-0 text-blue-600" />
              <div>
                <p className="text-sm font-semibold text-blue-900">Hint</p>
                <p className="mt-1 text-sm text-blue-700">{hint}</p>
              </div>
            </div>
          </motion.div>
        )}

        {answerResult && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-2xl border p-4 ${
              answerResult.passed
                ? "border-emerald-200 bg-emerald-50"
                : "border-red-200 bg-red-50"
            }`}
          >
            <div className="flex items-start gap-2">
              {answerResult.passed ? (
                <span className="text-emerald-600">✅</span>
              ) : (
                <span className="text-red-600">❌</span>
              )}
              <div className="flex-1">
                <p className={`text-sm font-semibold ${answerResult.passed ? "text-emerald-900" : "text-red-900"}`}>
                  {answerResult.passed ? "Correct!" : "Not quite right"}
                </p>
                {answerResult.message && (
                  <p className="mt-1 text-sm text-text-secondary">{answerResult.message}</p>
                )}
                {answerResult.mastery_unlocked && (
                  <div className="mt-3 rounded-xl bg-emerald-100 p-3">
                    <p className="text-sm font-bold text-emerald-900">🎉 Mastery Unlocked!</p>
                    {answerResult.reward?.diamonds && (
                      <p className="mt-1 font-mono text-xs text-emerald-700">
                        💎 +{answerResult.reward.diamonds}
                      </p>
                    )}
                  </div>
                )}
                {answerResult.reteach_required && (
                  <button
                    onClick={handleReteach}
                    className="mt-3 inline-flex items-center gap-2 rounded-xl bg-orange-500 px-4 py-2 text-sm font-bold text-white"
                  >
                    <RefreshCw size={14} /> Get Reteach Plan
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        )}

        <MissionPackRenderer
          pack={pack}
          step={currentStep}
          onSubmit={handleSubmit}
          onHint={handleHint}
          onRetry={handleRetry}
          answerResult={answerResult}
          loading={submitting}
          hint={hint}
          showHint={showHint}
          diamondsEarned={diamondsEarned}
          mistakeCount={mistakeCount}
        />
      </div>
    </div>
  );
}
