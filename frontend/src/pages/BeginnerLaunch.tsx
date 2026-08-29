import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  Sparkles,
  Route as RouteIcon,
  Compass,
  Terminal,
  Hand,
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
 * Door 3: brand-new learner. No diagnostic — you get one tiny, reassuring first
 * step (what a program really is) and then the path ahead. Zero pressure, zero
 * failure; only the start of a gentle climb.
 */

interface Step {
  type: string;
  title: string;
  content?: string;
  code?: string;
  simulation?: string;
}

interface World {
  world_id: string;
  title: string;
  description: string;
  competency_count: number;
}

interface BeginnerData {
  title: string;
  intro: string;
  steps: Step[];
  path: {
    start_world: string;
    start_world_title: string;
    worlds: World[];
  };
}

type Phase = "intro" | "steps" | "handoff";

export default function BeginnerLaunch() {
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const [data, setData] = useState<BeginnerData | null>(null);
  const [loading, setLoading] = useState(true);
  const [phase, setPhase] = useState<Phase>("intro");
  const [stepIdx, setStepIdx] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.onboarding
      .startBeginner()
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => {
        setError("We couldn't load your first step. Please try again.");
        setLoading(false);
      });
  }, []);

  const begin = useCallback(async () => {
    if (!data) return;
    setPhase("steps");
  }, [data]);

  const finish = useCallback(async () => {
    setSubmitting(true);
    try {
      await api.onboarding.completeBeginner();
    } catch {
      /* landing somewhere is fine even if persistence hiccups */
    } finally {
      setSubmitting(false);
      setPhase("handoff");
    }
  }, []);

  const progress = (() => {
    if (phase === "handoff") return 100;
    if (phase === "intro" || !data) return 10;
    return Math.round(((stepIdx + 1) / Math.max(1, data.steps.length)) * 70);
  })();

  const step = data?.steps?.[stepIdx];

  if (loading) {
    return (
      <PageShell theme="adventure">
        <div className="flex min-h-screen items-center justify-center">
          <div className="flex items-center gap-3 text-sm text-text-muted">
            <Compass className="animate-spin text-ocean" size={22} />
            Captain Byte is warming up your very first step…
          </div>
        </div>
      </PageShell>
    );
  }

  if (error && !data) {
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
            <MentorAvatar size={52} mood={phase === "handoff" ? "proud" : "welcome"} />
            <p className="rounded-xl border border-border bg-surface px-4 py-2.5 text-sm leading-snug text-text-muted shadow-card">
              <span className="font-bold text-text">Captain Byte:</span>{" "}
              {phase === "intro"
                ? "Welcome to tech. You don't need to know a single thing yet — I promise. Let me show you your very first tiny step."
                : phase === "steps"
                ? "This is it — your first step from zero. Take it at your own pace. No pressure, no failing."
                : "There you go. You've taken your first step. From here we climb, one gentle mission at a time."}
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
                  {phase === "intro"
                    ? "Your very first step"
                    : phase === "steps"
                    ? `Step ${stepIdx + 1} of ${data?.steps.length || 0}`
                    : "You're on your way"}
                </span>
                <span className="text-xs font-bold text-primary-dark">{progress}%</span>
              </div>
              <MasteryBar value={progress} showValue={false} />
            </div>

            <AnimatePresence mode="wait">
              {/* INTRO */}
              {phase === "intro" && data && (
                <motion.div
                  key="intro"
                  initial={reduced ? {} : { opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={reduced ? {} : { opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-5 px-6 py-6"
                >
                  <div className="text-center">
                    <div className="mx-auto mb-3 inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-mint bg-mint">
                      <Terminal size={26} className="text-primary-dark" />
                    </div>
                    <h2 className="font-display text-2xl font-extrabold text-text">{data.title}</h2>
                    <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-text-muted">
                      {data.intro}
                    </p>
                  </div>

                  <Card tone="mint" className="p-5">
                    <p className="mb-2 flex items-center gap-1.5 text-sm font-bold text-primary-dark">
                      <Hand size={16} /> What to expect
                    </p>
                    <ul className="space-y-1.5 text-sm text-text">
                      <li>· One tiny step at a time — nothing overwhelming.</li>
                      <li>· No tests, no scores, nothing to get wrong.</li>
                      <li>· A real first taste of how programs actually work.</li>
                    </ul>
                  </Card>
                </motion.div>
              )}

              {/* STEPS */}
              {phase === "steps" && step && (
                <motion.div
                  key={`step-${stepIdx}`}
                  initial={reduced ? {} : { opacity: 0, x: 30 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={reduced ? {} : { opacity: 0, x: -30 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-5 px-6 py-6"
                >
                  <div>
                    <span className="adventure-label mb-1 block">
                      {step.type === "context"
                        ? "The big picture"
                        : step.type === "explore"
                        ? "Watch it happen"
                        : "A gentle idea"}
                    </span>
                    <h2 className="font-display text-xl font-extrabold text-text">{step.title}</h2>
                    {step.content && (
                      <p className="mt-2 text-sm leading-relaxed text-text-muted">{step.content}</p>
                    )}
                  </div>

                  {step.code && (
                    <pre className="overflow-x-auto rounded-xl border border-border bg-surface-2 p-4 text-sm leading-relaxed text-text">
                      {step.code}
                    </pre>
                  )}

                  {step.simulation && (
                    <Card tone="sand" className="p-4">
                      <p className="mb-1 flex items-center gap-1.5 text-xs font-bold text-wood">
                        <Terminal size={13} /> Watch this example
                      </p>
                      <p className="text-sm leading-relaxed text-text">{step.simulation}</p>
                    </Card>
                  )}
                </motion.div>
              )}

              {/* HANDOFF */}
              {phase === "handoff" && data && (
                <motion.div
                  key="handoff"
                  initial={reduced ? {} : { opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  className="space-y-6 px-6 py-6"
                >
                  <div className="text-center">
                    <div className="mx-auto mb-3 inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-ocean bg-ocean-soft/70">
                      <Sparkles size={26} className="text-ocean" />
                    </div>
                    <h2 className="font-display text-2xl font-extrabold text-text">
                      You just crossed into tech
                    </h2>
                    <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-text-muted">
                      That was your first real step — and it wasn't scary at all. Here's the gently
                      rising path ahead. One mission at a time.
                    </p>
                  </div>

                  <div>
                    <h3 className="adventure-label mb-2 flex items-center gap-1.5">
                      <RouteIcon size={14} className="text-wood" /> The path ahead
                    </h3>
                    <div className="space-y-2.5">
                      {data.path.worlds.map((w, i) => (
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
                            <p className="text-sm font-semibold text-text">{w.title}</p>
                            <p className="text-xs leading-relaxed text-text-muted">{w.description}</p>
                          </div>
                          <Castle size={15} className="mt-1 shrink-0 text-wood/50" />
                        </div>
                      ))}
                    </div>
                  </div>

                  <Card tone="mint" className="p-4">
                    <p className="text-sm leading-relaxed text-text">
                      <span className="font-bold text-primary-dark">Your first mission:</span>{" "}
                      open the <span className="font-semibold">Memory Box</span> — learn how
                      variables hold data — then we unlock the world ahead.
                    </p>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Bottom navigation */}
            <div className="surface-border flex items-center justify-between border-t bg-surface-2 px-6 py-4">
              {phase === "intro" ? (
                <>
                  <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
                    Maybe later
                  </Button>
                  <Button
                    variant="ocean"
                    size="md"
                    rightIcon={<ArrowRight size={15} />}
                    onClick={begin}
                  >
                    Let's Try My First Step
                  </Button>
                </>
              ) : phase === "steps" ? (
                <>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                      stepIdx > 0 ? setStepIdx((i) => i - 1) : navigate("/dashboard")
                    }
                  >
                    Back
                  </Button>
                  <Button
                    variant="ocean"
                    size="md"
                    rightIcon={<ArrowRight size={15} />}
                    onClick={() => {
                      if (stepIdx + 1 < (data?.steps.length || 0)) {
                        setStepIdx((i) => i + 1);
                      } else {
                        finish();
                      }
                    }}
                    loading={submitting}
                  >
                    {stepIdx + 1 === data?.steps.length ? "I've Got It" : "Next"}
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
