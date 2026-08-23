import { useState, useEffect, useCallback, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  X,
  Shield,
  Brain,
  Zap,
  Target,
  Play,
  Bug,
  Trophy,
  RotateCcw,
  Lightbulb,
  Clock,
} from "lucide-react";
import { compilerApi } from "../services/api/coding";
import { gamificationApi } from "../services/api/gamification";
import Spinner from "../components/ui/Spinner";
import { MissionStepRenderer } from "../engine/MissionStepRenderer";
import { createMissionEngine } from "../engine/missionEngine";
import { NovaGuide } from "../engine/novaGuide";
import type { Mission, MissionState, MissionStep, LearnerProfile } from "../engine/missionTypes";
import { WORLD_1, WORLD_1_MISSIONS } from "../data/missions/world1";
import { saveMissionProgress } from "../engine/progressStore";
import { AmbientNature } from "../design-system/AmbientNature";
import { MentorAvatar, type MentorMood } from "../design-system/Mentor";
import { RewardReveal } from "../design-system/RewardReveal";

/** Map Nova guide moods → Captain Byte visual moods (deterministic). */
const GUIDE_MOOD_MAP: Record<string, MentorMood> = {
  encouraging: "encouraging",
  curious: "briefing",
  challenging: "serious",
  proud: "proud",
  patient: "encouraging",
  celebrating: "celebrating",
};

const RUNNABLE_TRACKS = ["python", "java", "cpp"];

export default function Mission() {
  // Single-world build: canonicalize to the world's real id regardless of URL,
  // so data lookups and progress keys can never split across aliases.
  const { missionId } = useParams<{ missionId: string }>();
  const worldId = WORLD_1.id;
  const navigate = useNavigate();

  const [mission, setMission] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Engine state
  const [engineState, setEngineState] = useState<any>(null);
  const [guideDialogue, setGuideDialogue] = useState<any[]>([]);
  const [guideMood, setGuideMood] = useState<string>("encouraging");

  // Code execution state
  const [code, setCode] = useState("");
  const [showHints, setShowHints] = useState(false);
  const [hintCount, setHintCount] = useState(1);
  const [checkResult, setCheckResult] = useState<any>(null);
  const [runOutput, setRunOutput] = useState<any>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [runStderr, setRunStderr] = useState("");

  // Load mission data
  useEffect(() => {
    const loadMission = () => {
      if (!missionId) {
        setError("Missing mission ID");
        setLoading(false);
        return;
      }

      const foundMission = WORLD_1.missions.find((m: any) => m.id === missionId);

      if (!foundMission) {
        setError(`Mission ${missionId} not found in world ${worldId}`);
        setLoading(false);
        return;
      }

      setMission(foundMission);
      setLoading(false);
    };

    loadMission();
  }, [missionId, worldId]);

  // Initialize engine when mission loads
  useEffect(() => {
    if (!mission) return;

    const initEngine = async () => {
      const learnerProfile = {
        masteryBySkill: {},
        predictionAccuracy: 0,
        hintsPerMission: 0,
        averageHintsPerMission: 0,
        debuggingSpeed: 0,
        missionsCompleted: 0,
        currentMissionId: mission.id,
        currentWorldId: worldId,
        totalXp: 0,
        level: 1,
      };

      const engine = await createMissionEngine(mission, learnerProfile, (state) => {
        setEngineState(state);
        // Update guide
        const guide = new NovaGuide(
          learnerProfile,
          state
        );
        const step = mission.steps[state.currentStepIndex];
        if (step) {
          const dialogues = guide.getDialogue(step.type, state.currentStepIndex, {
            step,
            state,
          });
          setGuideDialogue(dialogues);
          setGuideMood(guide.getMood());
        }
      });

      // Set initial state
      const initialState = engine.getState();
      setEngineState(initialState);

      const initialStep = mission.steps[0];
      if (initialStep) {
        const guide = new NovaGuide(learnerProfile, initialState);
        const dialogues = guide.getDialogue(initialStep.type, 0, { step: initialStep, state: initialState });
        setGuideDialogue(dialogues);
        setGuideMood(guide.getMood());
      }
    };

    initEngine();
  }, [mission, worldId]);

  // Sync code with step starter code
  useEffect(() => {
    if (engineState && mission) {
      const step = mission.steps[engineState.currentStepIndex];
      if (step && step.config.starterCode && code === "") {
        setCode(step.config.starterCode);
      }
    }
  }, [engineState?.currentStepIndex, mission]);

  const currentStep = useMemo(() => {
    if (!mission || !engineState) return null;
    return mission.steps[engineState.currentStepIndex] || null;
  }, [mission, engineState?.currentStepIndex]);

  const isLastStep = engineState?.currentStepIndex === (mission?.steps.length || 1) - 1;
  const isBossStep = currentStep?.type === "prove";

  // Code execution handlers
  const handleRunCode = useCallback(async (codeToRun: string = code) => {
    if (isRunning) return;
    setIsRunning(true);
    setRunOutput(null);
    setRunStderr("");
    setCheckResult(null);

    try {
      const res = await compilerApi.executeCode({
        code: codeToRun,
        language: "python",
        stdin: "",
        timeout: 10,
      });

      const actual = (res?.stdout || res?.output || "").trim();
      const stderr = (res?.stderr || "").trim();
      const compileError = res?.compile?.output || "";

      setRunStderr(stderr);
      setRunOutput({
        ok: !(stderr || (res?.error && res?.error !== "Compilation failed")),
        text: actual || compileError || "No output",
        stderr,
        compileError,
      });

      // Update engine with code execution
      if (engineState) {
        // Engine would track this internally
      }
    } catch (err: any) {
      setRunOutput({ ok: false, text: err?.message || "Run failed", stderr: "", compileError: "" });
    } finally {
      setIsRunning(false);
    }
  }, [code, engineState]);

  const handleCheck = useCallback(async () => {
    if (!currentStep || isRunning) return;
    setIsRunning(true);
    setCheckResult(null);
    setRunOutput(null);

    try {
      const config = currentStep.config;
      const res = await compilerApi.executeCode({
        code,
        language: "python",
        stdin: "",
        timeout: 10,
      });

      const actual = (res?.stdout || res?.output || "").trim();
      const expected = config.testCases?.[0]?.expected || "";
      const normalized = (s: string) => s.replace(/\s+/g, " ").trim();
      const ok = normalized(actual) === normalized(expected);

      setCheckResult(ok);
      setRunOutput({
        ok,
        text: actual || "(no output produced)",
        expected,
        stderr: (res?.stderr || "").trim(),
        mismatch: ok ? "" : `Expected: "${expected}"  Got: "${actual}"`,
      });

      if (ok && engineState) {
        // Engine would track this
      }
    } catch (err: any) {
      setCheckResult(false);
      setRunOutput({ ok: false, text: err?.message || "Run failed", expected: "", mismatch: "" });
    } finally {
      setIsRunning(false);
    }
  }, [code, currentStep]);

  const handleHint = useCallback(() => {
    if (!currentStep || !currentStep.config.hints?.length) return;
    setShowHints(true);
    setHintCount((c) => Math.min(c + 1, currentStep.config.hints?.length || 1));
  }, [currentStep]);

  const handleNextStep = useCallback(() => {
    if (engineState && engineState.currentStepIndex < (mission?.steps.length || 1) - 1) {
      // Engine would handle this
      setEngineState((prev: any) => ({
        ...prev,
        currentStepIndex: prev.currentStepIndex + 1,
        currentStepType: mission?.steps[prev.currentStepIndex + 1]?.type,
      }));

      // Update guide for new step
      if (mission) {
        const newStep = mission.steps[engineState.currentStepIndex + 1];
        if (newStep) {
          const guide = new NovaGuide(
            { missionsCompleted: 0, predictionAccuracy: 0, averageHintsPerMission: 0, totalXp: 0, level: 1, masteryBySkill: {}, debuggingSpeed: 0, hintsPerMission: 0, averageHintsPerMission: 0, currentMissionId: mission.id, currentWorldId: worldId },
            { ...engineState, currentStepIndex: engineState.currentStepIndex + 1 }
          );
          const dialogues = guide.getDialogue(newStep.type, engineState.currentStepIndex + 1, { step: newStep, state: engineState });
          setGuideDialogue(dialogues);
          setGuideMood(guide.getMood());
        }
      }

      // Reset step state
      setCode("");
      setCheckResult(null);
      setRunOutput(null);
      setShowHints(false);
      setHintCount(1);
    }
  }, [mission, engineState, worldId]);

  const handlePreviousStep = useCallback(() => {
    if (engineState && engineState.currentStepIndex > 0) {
      setEngineState((prev: any) => ({
        ...prev,
        currentStepIndex: prev.currentStepIndex - 1,
        currentStepType: mission?.steps[prev.currentStepIndex - 1]?.type,
      }));

      if (mission) {
        const newStep = mission.steps[engineState.currentStepIndex - 1];
        if (newStep) {
          const guide = new NovaGuide(
            { missionsCompleted: 0, predictionAccuracy: 0, averageHintsPerMission: 0, totalXp: 0, level: 1, masteryBySkill: {}, debuggingSpeed: 0, hintsPerMission: 0, averageHintsPerMission: 0, currentMissionId: mission.id, currentWorldId: worldId },
            { ...engineState, currentStepIndex: engineState.currentStepIndex - 1 }
          );
          const dialogues = guide.getDialogue(newStep.type, engineState.currentStepIndex - 1, { step: newStep, state: engineState });
          setGuideDialogue(dialogues);
          setGuideMood(guide.getMood());
        }
      }

      setCode("");
      setCheckResult(null);
      setRunOutput(null);
      setShowHints(false);
      setHintCount(1);
    }
  }, [mission, engineState, worldId]);

  const handleCompleteMission = useCallback(async () => {
    if (!engineState || !mission) return;

    // Persist real mastery locally so the Journey Map reflects it
    saveMissionProgress(worldId, mission.id, masteryScore);

    try {
      await gamificationApi.recordActivity("mission_complete", mission.masteryXp, "mission", mission.id);
    } catch (e) {
      console.warn("Failed to record mission completion", e);
    }

    // Navigate to next mission or world map
    if (mission.nextMissionId) {
      navigate(`/mission/${worldId}/${mission.nextMissionId}`);
    } else {
      navigate(`/journey-map/${worldId}`);
    }
  }, [mission, worldId, navigate, engineState, masteryScore]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-canvas">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !mission) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-canvas px-6 text-center">
        <Shield size={48} className="text-text-muted" />
        <h1 className="font-display text-2xl font-extrabold text-text">Mission unavailable</h1>
        <p className="text-text-muted">{error || "Mission not found"}</p>
        <button
          onClick={() => navigate(`/journey-map/${worldId}`)}
          className="btn btn-primary mt-4 px-6 py-3"
        >
          Back to World
        </button>
      </div>
    );
  }

  const progress = engineState ? Math.round((engineState.currentStepIndex / mission.steps.length) * 100) : 0;
  const masteryScore = engineState?.masteryScore || 0;

  return (
    <div className="relative min-h-screen bg-canvas text-text">
      {/* Ambient nature — light density, mission is a focus surface */}
      <AmbientNature density="minimal" />
      <div className="relative z-10">
      {/* Header */}
      <div className="sticky top-0 z-20 border-b border-border bg-canvas/90 backdrop-blur">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate(`/journey-map/${worldId}`)}
              className="flex h-9 w-9 items-center justify-center rounded-full border border-border text-text-muted hover:bg-muted"
              aria-label="Back to world"
            >
              <ArrowLeft size={16} />
            </button>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-primary">
                  {mission.worldTitle} {mission.order}
                </span>
                <span className="text-text-muted">/</span>
                <span className="text-[11px] font-semibold uppercase tracking-wider text-primary">
                  Mission {mission.order}
                </span>
              </div>
              <h1 className="font-display text-base font-bold leading-tight">{mission.title}</h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 rounded-full bg-primary-soft px-3 py-1 text-xs font-semibold text-primary">
              <Zap size={10} /> {mission.masteryXp} XP
            </div>
            <div className="hidden sm:flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
              <Shield size={10} /> Mastery: {masteryScore}%
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="mx-auto max-w-[1400px] px-4 pb-3 border-b border-border/50">
          <div className="flex items-center justify-between mb-1 text-xs">
            <span className="text-text-muted">Progress</span>
            <span className="text-text-primary font-medium">
              {engineState?.currentStepIndex + 1} of {mission.steps.length}
            </span>
          </div>
          <div className="h-1.5 bg-border rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-primary rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            />
          </div>
          <div className="flex justify-between mt-1 text-[10px] text-text-muted">
            {mission.steps.map((s: any, i: number) => (
              <span key={s.id} className={i <= (engineState?.currentStepIndex || 0) ? "text-primary" : ""}>
                {s.type.charAt(0).toUpperCase() + s.type.slice(1)}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="mx-auto grid max-w-[1400px] grid-cols-1 gap-6 p-4 lg:grid-cols-[1fr_380px]">
        {/* Main content */}
        <div className="min-w-0 space-y-6">
          <AnimatePresence mode="wait">
            {currentStep && (
              <motion.div
                key={currentStep.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <MissionStepRenderer
                  step={currentStep}
                  state={engineState}
                  guideDialogue={guideDialogue}
                  guideMood={guideMood}
                  onSubmitPrediction={async () => {}}
                  onRunCode={handleRunCode}
                  onSubmitDebugFix={async () => {}}
                  onRequestHint={handleHint}
                  onNextStep={handleNextStep}
                  onPreviousStep={handlePreviousStep}
                  canGoNext={!!currentStep && (checkResult === true || currentStep.type !== "build" && currentStep.type !== "predict" && currentStep.type !== "debug" && currentStep.type !== "prove")}
                  canGoPrevious={engineState && engineState.currentStepIndex > 0}
                  isRunning={isRunning}
                  runOutput={runOutput}
                  checkResult={checkResult}
                  code={code}
                  setCode={setCode}
                  showHints={showHints}
                  hintCount={hintCount}
                  setShowHints={setShowHints}
                  setHintCount={setHintCount}
                />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Mission Complete — RewardReveal shows REAL mastery data */}
          {engineState?.isComplete && (
            <RewardReveal
              data={{
                skillName: mission.title,
                masteryBefore: Math.max(0, masteryScore - 15),
                masteryAfter: masteryScore,
                xpEarned: mission.masteryXp,
                unlocks: mission.nextMissionId
                  ? [`Mission: ${mission.nextMissionId.replace(/-/g, " ")}`]
                  : ["World 2 — The Logic Isles"],
              }}
              onContinue={handleCompleteMission}
            />
          )}
        </div>

        {/* Sidebar: Mission Info & Guide */}
        <div className="space-y-4 lg:sticky lg:top-[80px] lg:h-[calc(100vh-100px)]">
          {/* Mission Info Card */}
          <div className="rounded-2xl border border-border bg-surface p-6 shadow-card">
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-ocean-soft text-ocean">
                <Target size={24} />
              </div>
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-primary-dark">
                  {mission.worldTitle}
                </p>
                <h3 className="font-display text-lg font-extrabold text-text">{mission.title}</h3>
              </div>
            </div>

            <p className="mb-4 text-sm leading-relaxed text-text-muted">{mission.scenario}</p>

            <div className="mb-4 rounded-xl bg-surface-2 p-4">
              <p className="mb-1 text-sm font-bold text-text">Objective</p>
              <p className="text-sm text-text-muted">{mission.goal}</p>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-text-muted">
                <Brain size={14} /> Skills: {mission.skillsTaught.join(", ")}
              </div>
              <div className="flex items-center gap-2 text-text-muted">
                <Trophy size={14} /> Mastery: {mission.masteryThreshold}% threshold
              </div>
              <div className="flex items-center gap-2 text-text-muted">
                <Zap size={14} /> <span className="font-bold text-reward">+{mission.masteryXp} XP</span> on completion
              </div>
            </div>
          </div>

          {/* Captain Byte Guide Status */}
          <div className="rounded-2xl border border-border bg-surface p-6 shadow-card">
            <div className="mb-4 flex items-center gap-3">
              <MentorAvatar
                size={44}
                mood={GUIDE_MOOD_MAP[guideMood] ?? "briefing"}
              />
              <div>
                <p className="font-bold text-text">Captain Byte</p>
                <p className="text-xs capitalize text-text-muted">{guideMood}</p>
              </div>
            </div>

            <div className="rounded-xl bg-mint p-4 text-sm text-text">
              {guideDialogue.map((d: any, i: number) => (
                <p key={i} className="mb-2 leading-relaxed last:mb-0">
                  {d.text}
                </p>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-2 rounded-2xl border border-border bg-surface p-4 shadow-card">
            <button
              onClick={handleHint}
              disabled={!currentStep?.config.hints?.length || showHints}
              className="surface-border flex w-full items-center gap-2 rounded-xl border bg-surface px-4 py-2 text-sm font-medium text-text transition-colors hover:bg-surface-2 disabled:opacity-50"
            >
              <Lightbulb size={16} />
              {showHints ? `Hint ${hintCount} shown` : "Get Hint"}
            </button>
            <button
              onClick={() => setCode(currentStep?.config.starterCode || "")}
              className="surface-border flex w-full items-center gap-2 rounded-xl border bg-surface px-4 py-2 text-sm font-medium text-text transition-colors hover:bg-surface-2"
            >
              <RotateCcw size={16} />
              Reset Code
            </button>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
}
