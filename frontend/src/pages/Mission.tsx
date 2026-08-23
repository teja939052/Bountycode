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

const RUNNABLE_TRACKS = ["python", "java", "cpp"];

export default function Mission() {
  const { worldId, missionId } = useParams<{ worldId: string; missionId: string }>();
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
      if (!worldId || !missionId) {
        setError("Missing world or mission ID");
        setLoading(false);
        return;
      }

      const world = (WORLD_1 as any)[worldId] || WORLD_1;
      const foundMission = world.missions.find((m: any) => m.id === missionId);

      if (!foundMission) {
        setError(`Mission ${missionId} not found in world ${worldId}`);
        setLoading(false);
        return;
      }

      setMission(foundMission);
      setLoading(false);
    };

    loadMission();
  }, [worldId, missionId]);

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

    try {
      await gamificationApi.recordActivity("mission_complete", mission.masteryXp, "mission", mission.id);
    } catch (e) {
      console.warn("Failed to record mission completion", e);
    }

    // Navigate to next mission or world
    if (mission.nextMissionId) {
      navigate(`/mission/${worldId}/${mission.nextMissionId}`);
    } else if (mission.worldId) {
      navigate(`/world/${mission.worldId}`);
    }
  }, [mission, worldId, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-base">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !mission) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-surface-base px-6 text-center">
        <Shield size={48} className="text-text-muted" />
        <h1 className="text-2xl font-bold text-text-primary">Mission unavailable</h1>
        <p className="text-text-muted">{error || "Mission not found"}</p>
        <button
          onClick={() => navigate(`/world/${worldId}`)}
          className="mt-4 px-6 py-3 rounded-xl bg-primary text-white font-medium hover:bg-primary-dark"
        >
          Back to World
        </button>
      </div>
    );
  }

  const progress = engineState ? Math.round((engineState.currentStepIndex / mission.steps.length) * 100) : 0;
  const masteryScore = engineState?.masteryScore || 0;

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      {/* Header */}
      <div className="sticky top-0 z-20 border-b border-border bg-surface-base/90 backdrop-blur">
        <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate(`/world/${worldId}`)}
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

          {/* Mission Complete */}
          {engineState?.isComplete && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="rounded-2xl bg-gradient-to-r from-primary to-primary-dark p-8 text-center text-text-primary"
            >
              <div className="text-6xl mb-4">🏆</div>
              <h2 className="font-display text-3xl font-bold mb-2">Mission Complete!</h2>
              <p className="text-lg opacity-90 mb-6">You've mastered {mission.title}.</p>
              <div className="flex items-center justify-center gap-4 mb-6">
                <div className="rounded-xl bg-white/20 px-6 py-3">
                  <p className="font-bold text-xl">+{mission.masteryXp} XP</p>
                  <p className="text-sm opacity-80">Mastery XP</p>
                </div>
                <div className="rounded-xl bg-white/20 px-6 py-3">
                  <p className="font-bold text-xl">{masteryScore}%</p>
                  <p className="text-sm opacity-80">Mastery Score</p>
                </div>
              </div>
              <button
                onClick={handleCompleteMission}
                className="px-8 py-3 rounded-xl bg-white text-primary font-bold hover:bg-white/90 transition-colors"
              >
                {mission.nextMissionId ? "Next Mission →" : "View World Progress"}
              </button>
            </motion.div>
          )}
        </div>

        {/* Sidebar: Mission Info & Guide */}
        <div className="lg:sticky lg:top-[80px] lg:h-[calc(100vh-100px)] space-y-4">
          {/* Mission Info Card */}
          <div className="rounded-2xl border border-border bg-surface-base p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-primary-soft flex items-center justify-center text-2xl">
                {mission.worldIcon}
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-primary">
                  {mission.worldTitle}
                </p>
                <h3 className="font-display text-lg font-bold">{mission.title}</h3>
              </div>
            </div>

            <p className="text-text-secondary mb-4">{mission.scenario}</p>

            <div className="rounded-xl bg-muted p-4 mb-4">
              <p className="text-sm font-semibold text-text-primary mb-1">Objective</p>
              <p className="text-sm text-text-secondary">{mission.goal}</p>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-text-secondary">
                <Brain size={14} /> Skills: {mission.skillsTaught.join(", ")}
              </div>
              <div className="flex items-center gap-2 text-text-secondary">
                <Trophy size={14} /> Mastery: {mission.masteryThreshold}% threshold
              </div>
              <div className="flex items-center gap-2 text-text-secondary">
                <Zap size={14} /> {mission.masteryXp} XP on completion
              </div>
            </div>
          </div>

          {/* Nova Guide Status */}
          <div className="rounded-2xl border border-border bg-surface-base p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-primary-soft flex items-center justify-center">
                <span className="text-2xl">{guideMood === "encouraging" ? "🌱" : guideMood === "curious" ? "🔍" : guideMood === "challenging" ? "⚔️" : guideMood === "proud" ? "🏆" : guideMood === "patient" ? "🌿" : "🎯"}</span>
              </div>
              <div>
                <p className="font-semibold text-text-primary">Nova</p>
                <p className="text-xs text-text-muted capitalize">{guideMood}</p>
              </div>
            </div>

            <div className="rounded-xl bg-primary-soft/50 p-4 text-sm text-primary">
              {guideDialogue.map((d: any, i: number) => (
                <p key={i} className="mb-2 last:mb-0">
                  <span className="font-semibold">Nova:</span> {d.text}
                </p>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="rounded-2xl border border-border bg-surface-base p-4 space-y-2">
            <button
              onClick={handleHint}
              disabled={!currentStep?.config.hints?.length || showHints}
              className="w-full flex items-center gap-2 rounded-xl border border-border bg-surface-base px-4 py-2 text-sm font-medium text-text-primary hover:bg-muted transition-colors disabled:opacity-50"
            >
              <Lightbulb size={16} />
              {showHints ? `Hint ${hintCount} shown` : "Get Hint"}
            </button>
            <button
              onClick={() => setCode(currentStep?.config.starterCode || "")}
              className="w-full flex items-center gap-2 rounded-xl border border-border bg-surface-base px-4 py-2 text-sm font-medium text-text-primary hover:bg-muted transition-colors"
            >
              <RotateCcw size={16} />
              Reset Code
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}