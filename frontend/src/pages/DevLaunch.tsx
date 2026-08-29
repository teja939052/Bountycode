import { useState, useEffect, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  ArrowLeft,
  Check,
  Sparkles,
  Route as RouteIcon,
  Compass,
  Map as MapIcon,
  Castle,
} from "lucide-react";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { MentorAvatar } from "../design-system/Mentor";
import { MasteryBar } from "../design-system/Progress";

/**
 * Door 2: developer adventure. The learner picked a track (Programming Village,
 * CS Castle, Algorithm Arena, Backend Harbor, AI Lab). We run a short real probe,
 * then hand them their adventure path (the world progression) and first 3 missions.
 */

interface Question {
  id: string;
  type: "explore" | "predict" | "break";
  title: string;
  prompt: string;
  code?: string;
  options?: { id: string; text: string }[];
  expected_output?: string;
  explanation?: string;
}

interface World {
  world_id: string;
  title: string;
  description: string;
  competency_count: number;
}

interface PathData {
  track: string;
  start_world: string;
  start_world_title: string;
  worlds: World[];
  current_world_idx: number;
}

interface Mission {
  mission_id: string;
  quest_type: string;
  title: string;
  description: string;
  difficulty: string;
  xp_reward: number;
  estimated_minutes: number;
}

interface DevResult {
  track: string;
  path: PathData;
  graded: { id: string; title: string; type: string; is_correct: boolean }[];
  correct_count: number;
  question_count: number;
  baseline_categories: Record<string, number>;
  first_missions: Mission[];
}

type Detail = "diagnostic" | "handoff";

const FALLBACK_TRACK = "programming";
const TRACKS: Record<string, string> = {
  programming: "Programming Village",
  cs: "Computer Science Castle",
  algorithms: "Algorithm Arena",
  backend: "Backend Harbor",
  ai: "AI Lab",
};

export default function DevLaunch() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const track = params.get("track") || FALLBACK_TRACK;

  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<string, unknown>>({});
  const [detail, setDetail] = useState<Detail>("diagnostic");
  const [result, setResult] = useState<DevResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.onboarding
      .startDevLaunch(track)
      .then((d) => {
        setQuestions(d.questions || []);
        setLoading(false);
      })
      .catch(() => {
        setError("We couldn't load your launch. Please try again.");
        setLoading(false);
      });
  }, [track]);

  const q = questions[current];
  const progress = (() => {
    if (detail === "handoff") return 100;
    if (questions.length === 0) return 10;
    return Math.round(((current + 1) / questions.length) * 65);
  })();

  const canContinue = useCallback(() => {
    if (!q) return false;
    if (q.type === "explore") {
      const v = (answers[q.id] as string) || "";
      return v.trim().length > 0;
    }
    return answers[q.id] != null;
  }, [q, answers]);

  const next = useCallback(() => {
    if (!q) return;
    if (current + 1 < questions.length) {
      setCurrent((c) => c + 1);
    } else {
      submit();
    }
  }, [q, current, questions.length]);

  const submit = useCallback(async () => {
    setSubmitting(true);
    try {
      const res = await api.onboarding.completeDevLaunch({ track, answers });
      setResult(res);
      setDetail("handoff");
    } catch {
      setError("We hit a snag saving your results. Try again.");
    } finally {
      setSubmitting(false);
    }
  }, [track, answers]);

  if (loading) {
    return (
      <PageShell theme="adventure">
        <div className="flex min-h-screen items-center justify-center">
          <div className="flex items-center gap-3 text-sm text-text-muted">
            <Compass className="animate-spin text-wood" size={22} />
            Captain Byte is mapping your adventure…
          </div>
        </div>
      </PageShell>
    );
  }

  if (error && !result) {
    return (
      <PageShell theme="adventure">
        <div className="flex min-h-screen items-center justify-center px-4">
          <Card className="max-w-md p-8 text-center">
            <p className="font-display mb-3 text-lg font-extrabold text-text">{error}</p>
            <Button variant="ocean" onClick={() => navigate("/journey")}>
              Back to Journey
            </Button>
          </Card>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell theme="adventure">
      <div className="flex min-h-screen items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45 }}
            className="mb-5 flex items-center gap-3"
          >
            <MentorAvatar size={52} mood={detail === "handoff" ? "celebrating" : "briefing"} />
            <p className="rounded-xl border border-border bg-surface px-4 py-2.5 text-sm leading-snug text-text-muted shadow-card">
              <span className="font-bold text-text">Captain Byte:</span>{" "}
              {detail === "handoff"
                ? "Your adventure has a map now. Take the first mission — one focused step deeper into your world."
                : `We're entering ${TRACKS[track] || track}. Answer a few short questions so I know exactly where your journey begins — no prior knowledge needed.`}
            </p>
          </motion.div>

          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="overflow-hidden rounded-2xl border border-border bg-surface shadow-soft-lg"
          >
            {/* Progress */}
            <div className="surface-border border-b px-6 pb-4 pt-5">
              <div className="mb-3 flex items-center justify-between">
                <span className="adventure-label">
                  {detail === "handoff" ? "Your adventure is ready" : `${TRACKS[track] || track} · Question ${current + 1} of ${questions.length}`}
                </span>
                <span className="text-xs font-bold text-primary-dark">{progress}%</span>
              </div>
              <MasteryBar value={progress} showValue={false} />
            </div>

            <AnimatePresence mode="wait">
              {detail === "diagnostic" && q && (
                <motion.div
                  key={`q-${current}`}
                  initial={reduced ? {} : { opacity: 0, x: 30 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={reduced ? {} : { opacity: 0, x: -30 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-5 px-6 py-6"
                >
                  <div>
                    <span className="adventure-label mb-1 block">
                      {q.type === "explore"
                        ? "Predict the output"
                        : "Choose one"}
                    </span>
                    <h2 className="font-display text-xl font-extrabold text-text">{q.title}</h2>
                    <p className="mt-1 text-sm leading-relaxed text-text-muted">{q.prompt}</p>
                  </div>

                  {q.code && (
                    <pre className="overflow-x-auto rounded-xl border border-border bg-surface-2 p-4 text-sm leading-relaxed text-text">
                      {q.code}
                    </pre>
                  )}

                  {q.type === "explore" && (
                    <textarea
                      value={(answers[q.id] as string) || ""}
                      onChange={(e) => setAnswers((a) => ({ ...a, [q.id]: e.target.value }))}
                      placeholder="Type what you think this prints…"
                      rows={3}
                      className="w-full rounded-xl border border-border bg-surface-2 p-3 text-sm text-text outline-none focus:border-primary"
                    />
                  )}

                  {q.type === "predict" && q.options && (
                    <div className="grid grid-cols-1 gap-2.5">
                      {q.options.map((o) => (
                        <button
                          key={o.id}
                          onClick={() => setAnswers((a) => ({ ...a, [q.id]: o.id }))}
                          className={`relative flex items-start gap-2 rounded-xl border-2 px-3 py-2.5 text-left text-sm font-medium transition-all ${
                            answers[q.id] === o.id
                              ? "border-primary bg-mint text-primary-dark"
                              : "border-border bg-surface text-text hover:border-primary/40 hover:bg-surface-2"
                          }`}
                        >
                          <span className="mt-0.5 font-bold">{o.id.toUpperCase()})</span>
                          <span>{o.text}</span>
                          {answers[q.id] === o.id && (
                            <Check size={15} className="ml-auto text-primary-dark" />
                          )}
                        </button>
                      ))}
                    </div>
                  )}
                </motion.div>
              )}

              {detail === "handoff" && result && (
                <motion.div
                  key="handoff"
                  initial={reduced ? {} : { opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  className="space-y-6 px-6 py-6"
                >
                  <div className="text-center">
                    <div className="mx-auto mb-3 inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-sand bg-sand-soft">
                      <MapIcon size={28} className="text-wood" />
                    </div>
                    <h2 className="font-display text-2xl font-extrabold text-text">
                      Your {TRACKS[track] || track} adventure is mapped
                    </h2>
                    <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-text-muted">
                      You got {result.correct_count} of {result.question_count} right. Enough to
                      start from exactly where you are — the rest unfolds one mission at a time.
                    </p>
                  </div>

                  {/* Adventure path */}
                  <div>
                    <h3 className="adventure-label mb-2 flex items-center gap-1.5">
                      <RouteIcon size={14} className="text-wood" /> Your adventure path
                    </h3>
                    <div className="space-y-2.5">
                      {result.path.worlds.map((w, i) => (
                        <div key={w.world_id} className="flex items-start gap-3">
                          <div
                            className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-[11px] font-bold text-white ${
                              i === 0
                                ? "bg-ocean"
                                : i === 1
                                ? "bg-sand text-primary-dark"
                                : i === 2
                                ? "bg-wood"
                                : "bg-reward"
                            }`}
                          >
                            {i + 1}
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-semibold text-text">
                              {w.title}{" "}
                              {i === 0 && (
                                <span className="ml-1 rounded-full bg-mint px-2 py-0.5 text-[10px] font-bold text-primary-dark">
                                  You start here
                                </span>
                              )}
                            </p>
                            <p className="text-xs leading-relaxed text-text-muted">{w.description}</p>
                          </div>
                          <Castle size={15} className="mt-1 shrink-0 text-wood/50" />
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* First missions */}
                  <div>
                    <h3 className="adventure-label mb-2 flex items-center gap-1.5">
                      <Sparkles size={14} className="text-reward" /> Your first missions
                    </h3>
                    <div className="space-y-2.5">
                      {result.first_missions.map((m, i) => (
                        <Card key={m.mission_id} tone="default" className="flex items-center gap-3 p-4">
                          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-mint text-sm font-bold text-primary-dark">
                            {i + 1}
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-semibold text-text">{m.title}</p>
                            <p className="text-xs leading-relaxed text-text-muted">{m.description}</p>
                          </div>
                          <div className="shrink-0 text-right">
                            <p className="text-sm font-bold text-reward">+{m.xp_reward} XP</p>
                            <p className="text-[11px] text-text-muted">~{m.estimated_minutes} min</p>
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Bottom navigation */}
            <div className="surface-border flex items-center justify-between border-t bg-surface-2 px-6 py-4">
              {detail === "diagnostic" ? (
                <>
                  <Button
                    variant="ghost"
                    size="sm"
                    leftIcon={<ArrowLeft size={14} />}
                    onClick={() =>
                      current > 0 ? setCurrent((c) => c - 1) : navigate("/dashboard")
                    }
                  >
                    Back
                  </Button>
                  <Button
                    variant="ocean"
                    size="md"
                    rightIcon={<ArrowRight size={15} />}
                    disabled={!canContinue() || submitting}
                    loading={submitting}
                    onClick={next}
                  >
                    {current + 1 === questions.length ? "Finish & Map My Adventure" : "Next"}
                  </Button>
                </>
              ) : (
                <Button
                  variant="ocean"
                  size="md"
                  rightIcon={<Sparkles size={15} />}
                  onClick={() => navigate("/lesson/variables-state")}
                >
                  Start My First Mission
                </Button>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </PageShell>
  );
}
