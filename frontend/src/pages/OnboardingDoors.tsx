import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, ArrowLeft, Check, Briefcase, GraduationCap, Sprout, Sparkles } from "lucide-react";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { MentorAvatar } from "../design-system/Mentor";
import { MasteryBar } from "../design-system/Progress";

/**
 * The 3-door onboarding. The learner never picks from a feature catalog —
 * they only answer "Where are you starting from?", then we take it from here.
 */

type Phase = "door" | "detail" | "handoff";

interface Door {
  key: string;
  emoji: string;
  title: string;
  subtitle: string;
  tagline: string;
}

interface DoorData {
  doors: Door[];
  job_roles: { key: string; label: string }[];
  career_stages: { key: string; label: string }[];
  dev_tracks: { key: string; label: string }[];
}

const FALLBACK_DOORS: Door[] = [
  {
    key: "job",
    emoji: "\u{1F4BC}",
    title: "I NEED A JOB",
    subtitle: "Graduate, job seeker, career switcher or working professional.",
    tagline: "Find your gaps, train for the role, get ready.",
  },
  {
    key: "dev",
    emoji: "\u{1F393}",
    title: "I WANT TO BECOME A DEVELOPER",
    subtitle: "Student or learner building coding and CS skills.",
    tagline: "One mission at a time. We'll turn learning into engineering ability.",
  },
  {
    key: "beginner",
    emoji: "\u{1F331}",
    title: "I'M NEW TO TECH",
    subtitle: "Coding, AI and technology feel confusing. Start from zero.",
    tagline: "You don't need to know anything yet. We'll teach you from zero.",
  },
];

const DOOR_MENTOR: Record<string, string> = {
  job: "Tell me the job you want. I'll find what you're missing and train you for exactly that role.",
  dev: "You're building a developer's mind. I'll show you exactly one mission at a time — no 50 tabs.",
  beginner: "Everyone started somewhere. You don't need to know anything yet — I'll teach you from zero.",
};

const DOOR_ICONS: Record<string, React.ReactNode> = {
  job: <Briefcase size={30} strokeWidth={1.6} className="text-ocean" />,
  dev: <GraduationCap size={30} strokeWidth={1.6} className="text-wood" />,
  beginner: <Sprout size={30} strokeWidth={1.6} className="text-wood" />,
};

const DOOR_TINT: Record<string, string> = {
  job: "bg-ocean-soft/70 border-ocean",
  dev: "bg-sand-soft border-sand",
  beginner: "bg-mint border-primary/30",
};

const DEFAULT_ROLES = [
  { key: "sde", label: "Software Developer" },
  { key: "ai_software_developer", label: "AI Software Developer" },
  { key: "data_analyst", label: "Data Analyst" },
  { key: "data_scientist", label: "Data Scientist" },
  { key: "qa_automation", label: "QA / Automation" },
  { key: "frontend", label: "Frontend Developer" },
  { key: "backend", label: "Backend Developer" },
  { key: "devops", label: "DevOps" },
  { key: "cybersecurity", label: "Cybersecurity" },
];

const DEFAULT_STAGES = [
  { key: "nothing", label: "I know nothing / very little" },
  { key: "code", label: "I can code" },
  { key: "degree", label: "I have a degree" },
  { key: "experience", label: "I have experience" },
  { key: "projects", label: "I have projects" },
  { key: "interviewed", label: "I've interviewed before" },
];

export default function OnboardingDoors() {
  const [phase, setPhase] = useState<Phase>("door");
  const [data, setData] = useState<DoorData | null>(null);
  const [selectedDoor, setSelectedDoor] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  const [selectedStage, setSelectedStage] = useState<string | null>(null);
  const [selectedTrack, setSelectedTrack] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const doors = data?.doors || FALLBACK_DOORS;
  const roles = data?.job_roles?.length ? data.job_roles : DEFAULT_ROLES;
  const stages = data?.career_stages?.length ? data.career_stages : DEFAULT_STAGES;
  const devTracks = data?.dev_tracks?.length
    ? data.dev_tracks
    : [
        { key: "programming", label: "Programming Village" },
        { key: "cs", label: "Computer Science Castle" },
        { key: "algorithms", label: "Algorithm Arena" },
        { key: "backend", label: "Backend Harbor" },
        { key: "ai", label: "AI Lab" },
      ];

  useEffect(() => {
    api.onboarding.getDoors().then(setData).catch(() => setData(null));
  }, []);

  const canContinue = useCallback(() => {
    if (!selectedDoor) return false;
    if (selectedDoor === "job") return !!selectedRole && !!selectedStage;
    if (selectedDoor === "dev") return !!selectedTrack;
    return true;
  }, [selectedDoor, selectedRole, selectedStage, selectedTrack]);

  const confirm = useCallback(async () => {
    if (!selectedDoor) return;
    setSubmitting(true);
    try {
      const res = await api.onboarding.completeDoor({
        door: selectedDoor,
        role: selectedDoor === "job" ? selectedRole : undefined,
        stage: selectedDoor === "job" ? selectedStage : undefined,
        track: selectedDoor === "dev" ? selectedTrack : undefined,
      });
      const target = res.redirect || "/dashboard";
      navigate(target.startsWith("/") ? target : `/${target}`);
    } catch {
      // On failure still land the user somewhere useful.
      navigate("/dashboard");
    } finally {
      setSubmitting(false);
    }
  }, [selectedDoor, selectedRole, selectedStage, selectedTrack, navigate]);

  const pickDoor = (key: string) => {
    setSelectedDoor(key);
    setPhase("detail");
  };

  const goBack = () => {
    if (phase === "detail") setPhase("door");
    else navigate(-1);
  };

  const activeDoor = doors.find((d) => d.key === selectedDoor);

  const progress = (() => {
    if (phase === "handoff") return 90;
    if (phase === "detail") return 50;
    return 15;
  })();

  return (
    <PageShell theme="adventure">
      <div className="flex min-h-screen items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          {/* Mentor greeting */}
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45 }}
            className="mb-5 flex items-center gap-3"
          >
            <MentorAvatar size={52} mood="briefing" />
            <p className="rounded-xl border border-border bg-surface px-4 py-2.5 text-sm leading-snug text-text-muted shadow-card">
              <span className="font-bold text-text">Captain Byte:</span>{" "}
              {phase === "detail" && activeDoor
                ? DOOR_MENTOR[activeDoor.key] || DOOR_MENTOR.job
                : phase === "handoff"
                ? "Perfect. We'll take it from here. Your path is being carved — see you on the other side."
                : "Before anything else: where are you starting from? Pick your doorway."}
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
                  {phase === "door" ? "Step 1 of 2" : phase === "detail" ? "Step 2 of 2" : "All set"}
                </span>
                <span className="text-xs font-bold text-primary-dark">{progress}%</span>
              </div>
              <MasteryBar value={progress} showValue={false} />
            </div>

            <AnimatePresence mode="wait">
              {/* ── DOOR PHASE ── */}
              {phase === "door" && (
                <motion.div
                  key="door"
                  initial={reduced ? {} : { opacity: 0, x: 30 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={reduced ? {} : { opacity: 0, x: -30 }}
                  transition={{ duration: 0.35 }}
                  className="space-y-5 px-6 py-6"
                >
                  <div className="text-center">
                    <h2 className="font-display mb-2 text-2xl font-extrabold text-text">
                      Where are you starting from?
                    </h2>
                    <p className="mx-auto max-w-md text-sm leading-relaxed text-text-muted">
                      Pick one door. We'll figure out the rest — you'll never have to guess
                      what to learn next.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                    {doors.map((d, idx) => (
                      <motion.button
                        key={d.key}
                        initial={reduced ? {} : { opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 * idx, duration: 0.4 }}
                        onClick={() => pickDoor(d.key)}
                        className="text-left group focus:outline-none"
                      >
                        <Card tone="default" className="h-full p-5 hover:border-primary/50">
                          <div className={`mb-3 inline-flex h-14 w-14 items-center justify-center rounded-2xl border ${DOOR_TINT[d.key]}`}>
                            {DOOR_ICONS[d.key]}
                          </div>
                          <p className="font-display text-base font-extrabold leading-tight text-text">
                            {d.title}
                          </p>
                          <p className="mt-1.5 text-xs leading-relaxed text-text-muted">{d.subtitle}</p>
                          <div className="mt-3 flex items-center gap-1.5 text-xs font-semibold text-primary-dark">
                            {d.tagline}
                            <ArrowRight size={13} className="transition-transform group-hover:translate-x-0.5" />
                          </div>
                        </Card>
                      </motion.button>
                    ))}
                  </div>

                  <p className="pt-1 text-center text-xs text-text-muted">
                    <Sparkles size={12} className="mr-1 inline text-reward" />
                    We'll take it from here. One path, one next mission, real progress.
                  </p>
                </motion.div>
              )}

              {/* ── DETAIL PHASE ── */}
              {phase === "detail" && activeDoor && (
                <motion.div
                  key={`detail-${activeDoor.key}`}
                  initial={reduced ? {} : { opacity: 0, x: 30 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={reduced ? {} : { opacity: 0, x: -30 }}
                  transition={{ duration: 0.35 }}
                  className="space-y-6 px-6 py-6"
                >
                  <div className="text-center">
                    <div className={`mx-auto mb-3 inline-flex h-14 w-14 items-center justify-center rounded-2xl border ${DOOR_TINT[activeDoor.key]}`}>
                      {DOOR_ICONS[activeDoor.key]}
                    </div>
                    <h2 className="font-display mb-1 text-xl font-extrabold text-text">
                      {activeDoor.key === "job"
                        ? "Your target role"
                        : activeDoor.key === "dev"
                        ? "Your developer adventure"
                        : "Start from zero"}
                    </h2>
                    <p className="text-xs text-text-muted">{activeDoor.tagline}</p>
                  </div>

                  {activeDoor.key === "job" && (
                    <>
                      <div>
                        <p className="adventure-label mb-2">What job are you targeting?</p>
                        <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3">
                          {roles.map((r) => (
                            <button
                              key={r.key}
                              onClick={() => setSelectedRole(r.key)}
                              className={`relative rounded-xl border-2 px-3 py-2.5 text-left text-sm font-semibold transition-all ${
                                selectedRole === r.key
                                  ? "border-primary bg-mint text-primary-dark"
                                  : "border-border bg-surface text-text hover:border-primary/40 hover:bg-surface-2"
                              }`}
                            >
                              {r.label}
                              {selectedRole === r.key && (
                                <Check size={15} className="absolute right-2 top-2 text-primary-dark" />
                              )}
                            </button>
                          ))}
                        </div>
                      </div>

                      <div>
                        <p className="adventure-label mb-2">Where are you right now?</p>
                        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                          {stages.map((s) => (
                            <button
                              key={s.key}
                              onClick={() => setSelectedStage(s.key)}
                              className={`relative rounded-xl border-2 px-3 py-2.5 text-left text-sm font-medium transition-all ${
                                selectedStage === s.key
                                  ? "border-primary bg-mint text-primary-dark"
                                  : "border-border bg-surface text-text hover:border-primary/40 hover:bg-surface-2"
                              }`}
                            >
                              {s.label}
                              {selectedStage === s.key && (
                                <Check size={15} className="absolute right-2 top-2 text-primary-dark" />
                              )}
                            </button>
                          ))}
                        </div>
                      </div>
                    </>
                  )}

                  {activeDoor.key === "dev" && (
                    <div className="space-y-4">
                      <p className="adventure-label mb-2">Where do you want to start?</p>
                      <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
                        {devTracks.map((t) => (
                          <button
                            key={t.key}
                            onClick={() => setSelectedTrack(t.key)}
                            className={`relative rounded-xl border-2 px-3 py-2.5 text-left text-sm font-semibold transition-all ${
                              selectedTrack === t.key
                                ? "border-primary bg-mint text-primary-dark"
                                : "border-border bg-surface text-text hover:border-primary/40 hover:bg-surface-2"
                            }`}
                          >
                            {t.label}
                            {selectedTrack === t.key && (
                              <Check size={15} className="absolute right-2 top-2 text-primary-dark" />
                            )}
                          </button>
                        ))}
                      </div>
                      <p className="text-xs leading-relaxed text-text-muted">
                        Don't worry about picking wrong — your path grows from wherever you
                        start, one mission at a time.
                      </p>
                    </div>
                  )}

                  {activeDoor.key === "beginner" && (
                    <div className="rounded-xl border border-border bg-surface-2 p-4 text-sm text-text-muted">
                      <span className="font-bold text-text">No prior knowledge needed.</span> We start from
                      the very first step — what happens when you press a button on a website — and build
                      up from there, one gentle mission at a time.
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Bottom navigation */}
            <div className="surface-border flex items-center justify-between border-t bg-surface-2 px-6 py-4">
              <Button variant="ghost" size="sm" onClick={goBack} leftIcon={<ArrowLeft size={14} />}>
                {phase === "detail" ? "Back" : "Skip"}
              </Button>

              {phase === "detail" && activeDoor ? (
                <Button
                  variant={activeDoor.key === "job" ? "primary" : "ocean"}
                  size="md"
                  onClick={confirm}
                  disabled={!canContinue() || submitting}
                  loading={submitting}
                  rightIcon={<ArrowRight size={15} />}
                >
                  {activeDoor.key === "job" ? "Build My Plan" : "Let's Go"}
                </Button>
              ) : (
                <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
                  Skip for now
                </Button>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </PageShell>
  );
}
