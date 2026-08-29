import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import {
  ArrowLeft, CheckCircle2, XCircle, Play, Lightbulb, Trophy,
  BookOpen, Code, Zap, Target, Sparkles, Star, Crown,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import ArcadeBackdrop from "../components/learning/ArcadeBackdrop";
import { candyGradient } from "../components/candy/palette";
import type { CandyColor } from "../components/candy/palette";

const MEMORY_COLORS: Record<number, CandyColor> = {
  0: "strawberry",
  1: "grape",
  2: "lemon",
  3: "mint",
  4: "blueberry",
  5: "tangerine",
  6: "cherry",
  7: "gold",
};

type DiscoveryStep = {
  type: "observation" | "manipulation" | "mutation" | "bulb_reveal";
  prompt: string;
  memory_state?: number[];
  question: string;
  correct_answer?: number | string;
  hint_level_1?: string;
  hint_level_2?: string;
  hint_level_3?: string;
  insight?: string;
};

type StoryWorld = {
  title: string;
  emoji: string;
  narration: string[];
  character: { name: string; emoji: string; quote: string };
};

type Sandbox = {
  language: string;
  starter_code: string;
  test_cases: Array<{ description: string; expected_output: string }>;
  scaffolded_hints: Array<{ level: number; text: string }>;
};

type TransferChallenge = {
  title: string;
  description: string;
  difficulty: string;
  starter_code: string;
  expected_output: string;
  scaffolded_hints: Array<{ level: number; text: string }>;
};

type BossBattle = {
  title: string;
  emoji: string;
  description: string;
  health: number;
  rounds: Array<{
    question: string;
    correct_answer: string;
    explanation: string;
  }>;
  reward_xp: number;
  reward_badge: string;
};

type VariableDiscoveryContent = {
  story_world: StoryWorld;
  discovery: { title: string; steps: DiscoveryStep[] };
  code_sandbox: Sandbox;
  transfer_challenge: TransferChallenge;
  boss_battle: BossBattle;
  xp_reward: number;
  next_steps: string;
};

type LessonPhase = "story" | "discovery" | "sandbox" | "transfer" | "boss" | "celebration";

const VariableDiscovery = () => {
  const [loading, setLoading] = useState(true);
  const [content, setContent] = useState<VariableDiscoveryContent | null>(null);
  const [phase, setPhase] = useState<LessonPhase>("story");
  const [narrationIndex, setNarrationIndex] = useState(0);
  const [discoveryStep, setDiscoveryStep] = useState(0);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [checkResult, setCheckResult] = useState<"pass" | "fail" | null>(null);
  const [hintLevel, setHintLevel] = useState(0);
  const [bossRound, setBossRound] = useState(0);
  const [bossHealth, setBossHealth] = useState(3);
  const [bossAnswers, setBossAnswers] = useState<Record<number, string>>({});
  const [xpResult, setXpResult] = useState<any>(null);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    api
      .get("/api/v1/learning/lesson/variable-discovery")
      .then((d) => {
        setContent(d);
        setCode(d.code_sandbox.starter_code);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading || !content) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  const story = content.story_world;
  const discovery = content.discovery;
  const sandbox = content.code_sandbox;
  const transfer = content.transfer_challenge;
  const boss = content.boss_battle;

  const nextPhase = () => {
    const order: LessonPhase[] = ["story", "discovery", "sandbox", "transfer", "boss", "celebration"];
    const idx = order.indexOf(phase);
    if (idx < order.length - 1) {
      setPhase(order[idx + 1]);
    }
  };

  const handleDiscoveryAnswer = (answer: string) => {
    const step = discovery.steps[discoveryStep];
    const expected = String(step.correct_answer);
    const isCorrect = answer.trim() === expected || Number(answer.trim()) === Number(step.correct_answer);

    if (isCorrect) {
      if (discoveryStep < discovery.steps.length - 1) {
        setDiscoveryStep(discoveryStep + 1);
        setHintLevel(0);
      } else {
        nextPhase();
      }
    }
  };

  const revealHint = () => {
    const step = discovery.steps[discoveryStep];
    const hints = [step.hint_level_1, step.hint_level_2, step.hint_level_3];
    if (hintLevel < hints.length - 1) {
      setHintLevel(hintLevel + 1);
    }
  };

  const handleRunCode = useCallback(async () => {
    setRunning(true);
    setOutput("");
    setCheckResult(null);
    try {
      const result = await api.post("/api/v1/compiler/execute", {
        code,
        language: sandbox.language,
        stdin: "",
        timeout: 10,
      });
      if (result.success) {
        setOutput(result.stdout || "(no output)");
      } else {
        setOutput(result.stderr || result.error || "Execution failed");
      }
    } catch (err: any) {
      setOutput(err.message || "Failed to execute");
    } finally {
      setRunning(false);
    }
  }, [code, sandbox.language]);

  const checkSandboxAnswer = useCallback(async () => {
    const expected = sandbox.test_cases[0].expected_output.trim();
    const result = await handleRunCode();
    const actual = (result?.stdout || "").trim();
    const passed = result?.success === true && actual === expected;
    setCheckResult(passed ? "pass" : "fail");
  }, [handleRunCode, sandbox.test_cases]);

  const checkTransferAnswer = useCallback(async () => {
    const expected = transfer.expected_output.trim();
    const result = await handleRunCode();
    const actual = (result?.stdout || "").trim();
    const passed = result?.success === true && actual === expected;
    setCheckResult(passed ? "pass" : "fail");
    if (passed) {
      setTimeout(() => nextPhase(), 1500);
    }
  }, [handleRunCode, transfer.expected_output]);

  const handleBossAnswer = (answer: string) => {
    const round = boss.rounds[bossRound];
    const expected = round.correct_answer.trim();
    const isCorrect = answer.trim() === expected;

    setBossAnswers((prev) => ({ ...prev, [bossRound]: answer }));

    if (isCorrect) {
      setBossHealth(bossHealth - 1);
      if (bossRound < boss.rounds.length - 1) {
        setBossRound(bossRound + 1);
      } else if (bossHealth <= 1) {
        handleCompleteLesson();
      }
    } else {
      window.dispatchEvent(
        new CustomEvent("xp-gained", { detail: { xp: 0 } })
      );
    }
  };

  const handleCompleteLesson = useCallback(async () => {
    setCompleting(true);
    try {
      const result = await api.post("/api/v1/learning/lesson/variable-discovery/complete", {});
      setXpResult(result);
      setPhase("celebration");
      window.dispatchEvent(
        new CustomEvent("xp-gained", { detail: { xp: result.xp_gained || content.xp_reward } })
      );
    } catch (err) {
      console.error(err);
    } finally {
      setCompleting(false);
    }
  }, [content.xp_reward]);

  const resetSandbox = () => {
    setCode(sandbox.starter_code);
    setOutput("");
    setCheckResult(null);
    setHintLevel(0);
  };

  return (
    <div className="relative min-h-screen px-4 py-8">
      <ArcadeBackdrop variant="candy" />
      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Back button */}
        <button
          onClick={() => (phase === "story" ? (window.location.href = "/learn") : setPhase("story"))}
          className="flex items-center gap-2 text-brand-muted hover:text-text-primary transition-colors text-sm font-mono mb-4"
        >
          <ArrowLeft size={14} /> {phase === "story" ? "Back to Learn" : "Back to Story"}
        </button>

        {/* Phase indicator */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          {(["story", "discovery", "sandbox", "transfer", "boss", "celebration"] as LessonPhase[]).map(
            (p, i) => {
              const labels = ["Story", "Discovery", "Code", "Transfer", "Boss", "Done"];
              const active = p === phase;
              return (
                <div
                  key={p}
                  className={`px-3 py-1 rounded-full text-xs font-mono transition-all ${
                    active
                      ? "bg-yellow-400 text-yellow-900"
                      : "bg-surface-2 text-text-primary/40"
                  }`}
                >
                  {i + 1}. {labels[i]}
                </div>
              );
            }
          )}
        </div>

        {/* STORY PHASE */}
        {phase === "story" && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-4">
              <span className="text-5xl">{story.emoji}</span>
              <h1 className="text-3xl font-display font-black text-text-primary">
                {story.title}
              </h1>
            </div>

            <div className="glass rounded-xl p-6 space-y-4">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{story.character.emoji}</span>
                <div>
                  <p className="font-display font-bold text-yellow-400">
                    {story.character.name} says:
                  </p>
                  <p className="text-sm font-mono text-brand-secondary mt-1">
                    "{story.character.quote}"
                  </p>
                </div>
              </div>

              <AnimatePresence mode="wait">
                <motion.p
                  key={narrationIndex}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="text-lg font-mono text-brand-secondary leading-relaxed"
                >
                  {story.narration[narrationIndex]}
                </motion.p>
              </AnimatePresence>

              <div className="flex justify-between items-center pt-4">
                <div className="flex gap-1">
                  {story.narration.map((_, i) => (
                    <div
                      key={i}
                      className={`h-1.5 rounded-full transition-all ${
                        i === narrationIndex
                          ? "w-8 bg-yellow-400"
                          : "w-2 bg-text-primary/20"
                      }`}
                    />
                  ))}
                </div>

                <button
                  onClick={() => {
                    if (narrationIndex < story.narration.length - 1) {
                      setNarrationIndex(narrationIndex + 1);
                    } else {
                      nextPhase();
                    }
                  }}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all"
                >
                  <Play size={14} />
                  {narrationIndex < story.narration.length - 1 ? "Next" : "Begin Discovery"}
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* DISCOVERY PHASE */}
        {phase === "discovery" && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <h2 className="text-2xl font-display font-bold text-text-primary flex items-center gap-2">
              <Lightbulb size={24} className="text-yellow-400" />
              {discovery.title}
            </h2>

            <AnimatePresence mode="wait">
              {discovery.steps[discoveryStep] && (
                <motion.div
                  key={discoveryStep}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="space-y-4"
                >
                  {discovery.steps[discoveryStep].type === "bulb_reveal" ? (
                    <div className="glass rounded-xl p-6 border border-yellow-500/20 bg-yellow-500/5">
                      <p className="text-sm font-mono text-brand-secondary leading-relaxed">
                        {discovery.steps[discoveryStep].prompt}
                      </p>
                      <div className="mt-4 p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                        <p className="text-sm font-mono text-yellow-300">
                          {discovery.steps[discoveryStep].insight}
                        </p>
                      </div>
                      <button
                        onClick={() => {
                          setDiscoveryStep(discoveryStep + 1);
                          setHintLevel(0);
                        }}
                        disabled={discoveryStep >= discovery.steps.length - 1}
                        className="mt-4 flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all disabled:opacity-50"
                      >
                        <Zap size={14} />
                        {discoveryStep >= discovery.steps.length - 1
                          ? "Continue to Code Sandbox"
                          : "Next Step"}
                      </button>
                    </div>
                  ) : (
                    <>
                      {(discovery.steps[discoveryStep] as any).memory_state && (
                        <div className="flex gap-2 flex-wrap">
                          {(discovery.steps[discoveryStep] as any).memory_state.map(
                            (val: number, i: number) => (
                              <div
                                key={i}
                                className="flex flex-col items-center gap-1"
                              >
                                <div
                                  className="w-12 h-16 rounded-lg border-2 flex items-center justify-center text-sm font-mono"
                                  style={{
                                    background: candyGradient(MEMORY_COLORS[i % 8]),
                                    borderColor: "rgba(255,255,255,0.2)",
                                  }}
                                >
                                  {val}
                                </div>
                                <span className="text-xs text-brand-muted">
                                  addr {i}
                                </span>
                              </div>
                            )
                          )}
                        </div>
                      )}

                      <p className="text-lg font-mono text-brand-secondary">
                        {discovery.steps[discoveryStep].prompt}
                      </p>

                      <div className="bg-surface-card/30 rounded-lg p-4 border border-white/5">
                        <p className="text-sm font-mono text-text-primary mb-3">
                          {discovery.steps[discoveryStep].question}
                        </p>

                        {discovery.steps[discoveryStep].type === "observation" ||
                        discovery.steps[discoveryStep].type === "mutation" ? (
                          <NumberInput onSubmit={handleDiscoveryAnswer} hintLevel={hintLevel} step={discovery.steps[discoveryStep]} />
                        ) : (
                          <TextInput onSubmit={handleDiscoveryAnswer} hintLevel={hintLevel} step={discovery.steps[discoveryStep]} />
                        )}

                        {(discovery.steps[discoveryStep].hint_level_1 ||
                          discovery.steps[discoveryStep].hint_level_2 ||
                          discovery.steps[discoveryStep].hint_level_3) && (
                          <HintReveal
                            level={hintLevel}
                            step={discovery.steps[discoveryStep]}
                            onReveal={revealHint}
                          />
                        )}
                      </div>
                    </>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )}

        {/* SANDBOX PHASE */}
        {phase === "sandbox" && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <h2 className="text-2xl font-display font-bold text-text-primary flex items-center gap-2">
              <Code size={24} className="text-cyan-400" />
              Interactive Code Sandbox
            </h2>

            <div className="glass rounded-xl p-4">
              <p className="text-sm font-mono text-brand-secondary mb-4">
                {sandbox.test_cases[0].description}
              </p>

              <div className="rounded-lg overflow-hidden border border-white/5">
                <Editor
                  height="200px"
                  language={sandbox.language === "c" ? "c" : sandbox.language}
                  theme="vs-dark"
                  value={code}
                  onChange={(val) => setCode(val || "")}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 13,
                    tabSize: 4,
                    lineNumbers: "on",
                    wordWrap: "on",
                    padding: { top: 8 },
                  }}
                />
              </div>

              <div className="flex gap-2 mt-4">
                <button
                  onClick={handleRunCode}
                  disabled={running}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all disabled:opacity-50"
                >
                  {running ? <Spinner size="sm" /> : <Play size={14} />}
                  {running ? "Running..." : "Run Code"}
                </button>
                <button
                  onClick={checkSandboxAnswer}
                  disabled={running}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500/20 border border-green-400/30 text-green-400 font-mono text-sm hover:bg-green-500/30 transition-all"
                >
                  Check Answer
                </button>
                <button
                  onClick={resetSandbox}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-card/30 border border-white/5 text-brand-muted font-mono text-sm hover:bg-surface-card/50"
                >
                  Reset
                </button>

                {sandbox.scaffolded_hints.length > 0 && (
                  <HintReveal
                    level={hintLevel}
                    step={{
                      hint_level_1: sandbox.scaffolded_hints[0]?.text,
                      hint_level_2: sandbox.scaffolded_hints[1]?.text,
                      hint_level_3: sandbox.scaffolded_hints[2]?.text,
                    }}
                    onReveal={() =>
                      setHintLevel(
                        Math.min(
                          hintLevel + 1,
                          sandbox.scaffolded_hints.length
                        )
                      )
                    }
                  />
                )}
              </div>
            </div>

            {output && (
              <div className="bg-[#0d1117] rounded-lg p-3 border border-white/5">
                <pre className={`text-sm font-mono ${checkResult === "pass" ? "text-green-400" : checkResult === "fail" ? "text-red-400" : "text-green-400"}`}>
                  {output}
                </pre>
              </div>
            )}

            {checkResult && (
              <motion.div
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                className={`p-3 rounded-lg flex items-center gap-2 ${
                  checkResult === "pass"
                    ? "bg-green-500/10 border border-green-500/20 text-green-400"
                    : "bg-red-500/10 border border-red-500/20 text-red-400"
                }`}
              >
                {checkResult === "pass" ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                {checkResult === "pass"
                  ? "Correct! Variables can be declared, printed, and reassigned."
                  : "Output doesn't match. Check your format specifiers and \\n characters."}
              </motion.div>
            )}

            {checkResult === "pass" && (
              <button
                onClick={() => {
                  setCheckResult(null);
                  resetSandbox();
                  setHintLevel(0);
                  nextPhase();
                }}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-yellow-500/20 border border-yellow-400/30 text-yellow-400 font-mono text-sm hover:bg-yellow-500/30 transition-all"
              >
                <Star size={14} /> Continue to Transfer Challenge
              </button>
            )}
          </motion.div>
        )}

        {/* TRANSFER CHALLENGE PHASE */}
        {phase === "transfer" && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <h2 className="text-2xl font-display font-bold text-text-primary flex items-center gap-2">
              <Target size={24} className="text-purple-400" />
              {transfer.title}
            </h2>

            <div className="glass rounded-xl p-6 border border-purple-500/20">
              <p className="text-sm font-mono text-brand-secondary leading-relaxed mb-4">
                {transfer.description}
              </p>

              <p className="text-xs font-mono text-yellow-400/70 uppercase tracking-wider mb-2">
                Difficulty: {transfer.difficulty}
              </p>

              <div className="rounded-lg overflow-hidden border border-white/5">
                <Editor
                  height="200px"
                  language="c"
                  theme="vs-dark"
                  value={code}
                  onChange={(val) => setCode(val || "")}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 13,
                    tabSize: 4,
                    lineNumbers: "on",
                    wordWrap: "on",
                    padding: { top: 8 },
                  }}
                />
              </div>

              <div className="flex gap-2 mt-4">
                <button
                  onClick={handleRunCode}
                  disabled={running}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all disabled:opacity-50"
                >
                  {running ? <Spinner size="sm" /> : <Play size={14} />}
                  Run
                </button>
                <button
                  onClick={checkTransferAnswer}
                  disabled={running}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500/20 border border-green-400/30 text-green-400 font-mono text-sm hover:bg-green-500/30 transition-all"
                >
                  Check Answer
                </button>

                <HintReveal
                  level={hintLevel}
                  step={{
                    hint_level_1: transfer.scaffolded_hints[0]?.text,
                    hint_level_2: transfer.scaffolded_hints[1]?.text,
                    hint_level_3: transfer.scaffolded_hints[2]?.text,
                  }}
                  onReveal={() => setHintLevel(Math.min(hintLevel + 1, 3))}
                />
              </div>

              {checkResult === "pass" && (
                <motion.div
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-3 p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 flex items-center gap-2"
                >
                  <CheckCircle2 size={16} />
                  Transfer complete! You applied variables to a new context.
                </motion.div>
              )}
            </div>
          </motion.div>
        )}

        {/* BOSS BATTLE PHASE */}
        {phase === "boss" && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <h2 className="text-2xl font-display font-bold text-text-primary flex items-center gap-2">
              <span className="text-3xl">{boss.emoji}</span> {boss.title}
            </h2>

            <div className="glass rounded-xl p-6 border border-red-500/20">
              <p className="text-sm font-mono text-brand-secondary mb-4">
                {boss.description}
              </p>

              <div className="flex items-center gap-3 mb-4">
                <span className="text-sm font-mono text-brand-muted">Boss Health:</span>
                {Array.from({ length: boss.health }).map((_, i) => (
                  <HeartKey key={i} filled={i < bossHealth} />
                ))}
              </div>

              <AnimatePresence mode="wait">
                {bossRound < boss.rounds.length && (
                  <motion.div
                    key={bossRound}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    className="space-y-4"
                  >
                    <p className="text-lg font-mono text-text-primary">
                      {boss.rounds[bossRound].question}
                    </p>

                    <BossAnswerInput
                      onSubmit={(answer) => handleBossAnswer(answer)}
                      correctAnswer={boss.rounds[bossRound].correct_answer}
                      round={bossRound + 1}
                      totalRounds={boss.rounds.length}
                      explanation={boss.rounds[bossRound].explanation}
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        )}

        {/* CELEBRATION PHASE */}
        {phase === "celebration" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-12"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="text-6xl mb-6"
            >
              🏆
            </motion.div>
            <h2 className="text-3xl font-display font-black text-text-primary mb-4">
              Boss Defeated!
            </h2>
            <p className="text-lg font-mono text-brand-secondary mb-6">
              {boss.title} has been vanquished.
            </p>
            <div className="flex justify-center gap-8 mb-6">
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                <p className="text-3xl font-bold text-green-400">
                  +{xpResult?.xp_gained || content.xp_reward}
                </p>
                <p className="text-xs text-brand-muted font-mono">XP EARNED</p>
              </motion.div>
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <Trophy size={32} className="text-yellow-400 mx-auto" />
                <p className="text-xs text-brand-muted font-mono">Badge Unlocked</p>
              </motion.div>
            </div>

            {xpResult?.srs_state && (
              <p className="text-sm font-mono text-cyan-400 mb-4">
                Concept "{xpResult.srs_concept_enrolled}" enrolled in spaced repetition.
              </p>
            )}

            <button
              onClick={() => (window.location.href = "/learn")}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all"
            >
              <BookOpen size={16} />
              Return to Learning Hub
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
};

function NumberInput({ onSubmit, hintLevel, step }: {
  onSubmit: (answer: string) => void;
  hintLevel: number;
  step: any;
}) {
  const [value, setValue] = useState("");
  const [showHint, setShowHint] = useState(false);

  const hints = [step.hint_level_1, step.hint_level_2, step.hint_level_3].filter(Boolean);

  const handleSubmit = () => {
    if (!value.trim()) return;
    onSubmit(value.trim());
    setValue("");
  };

  return (
    <div className="space-y-3">
      <input
        type="number"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Enter address..."
        className="w-full px-3 py-2 rounded-lg bg-surface-card/30 border border-white/5 text-text-primary font-mono text-sm focus:outline-none focus:border-cyan-300/30"
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
      />
      <button
        onClick={handleSubmit}
        className="w-full px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all"
      >
        Submit
      </button>

      {hints.length > 0 && (
        <HintStrip
          level={hintLevel}
          hints={hints}
          onReveal={() => setShowHint(true)}
        />
      )}
    </div>
  );
}

function TextInput({ onSubmit, hintLevel, step }: {
  onSubmit: (answer: string) => void;
  hintLevel: number;
  step: any;
}) {
  const [value, setValue] = useState("");

  const hints = [step.hint_level_1, step.hint_level_2, step.hint_level_3].filter(Boolean);

  const handleSubmit = () => {
    if (!value.trim()) return;
    onSubmit(value.trim());
    setValue("");
  };

  return (
    <div className="space-y-3">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Enter value..."
        className="w-full px-3 py-2 rounded-lg bg-surface-card/30 border border-white/5 text-text-primary font-mono text-sm focus:outline-none focus:border-cyan-300/30"
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
      />
      <button
        onClick={handleSubmit}
        className="w-full px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-300/30 text-cyan-300 font-mono text-sm hover:bg-cyan-500/30 transition-all"
      >
        Submit
      </button>

      {hints.length > 0 && (
        <HintStrip
          level={hintLevel}
          hints={hints}
          onReveal={() => {}}
        />
      )}
    </div>
  );
}

function HintReveal({ level, step, onReveal }: {
  level: number;
  step: any;
  onReveal: () => void;
}) {
  const hints = [step.hint_level_1, step.hint_level_2, step.hint_level_3].filter(Boolean);

  if (level === 0) {
    return (
      <button
        onClick={onReveal}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-mono hover:bg-purple-500/20 transition-all"
      >
        <Lightbulb size={12} /> Show Hint
      </button>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-2 p-3 rounded-lg bg-purple-500/5 border border-purple-500/20 space-y-1"
    >
      {hints.slice(0, level + 1).map((h: string, i: number) => (
        <p key={i} className="text-xs font-mono text-purple-300 flex items-start gap-2">
          <span className="text-purple-500">💡</span> {h}
        </p>
      ))}
    </motion.div>
  );
}

function HintStrip({ level, hints, onReveal }: {
  level: number;
  hints: string[];
  onReveal: () => void;
}) {
  if (level === 0 && hints.length > 0) {
    return (
      <button
        onClick={onReveal}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-mono hover:bg-purple-500/20 transition-all"
      >
        <Lightbulb size={12} /> Hint ({hints.length})
      </button>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -5 }}
      animate={{ opacity: 1, y: 0 }}
      className="mt-2 p-3 rounded-lg bg-purple-500/5 border border-purple-500/20 space-y-1"
    >
      {hints.slice(0, Math.max(1, level)).map((h: string, i: number) => (
        <p key={i} className="text-xs font-mono text-purple-300 flex items-start gap-2">
          <span className="text-purple-500">💡</span> {h}
        </p>
      ))}
    </motion.div>
  );
}

function HeartKey({ filled }: { filled: boolean }) {
  return (
    <motion.div
      animate={{ scale: filled ? [1, 1.2, 1] : 1 }}
      transition={{ duration: 0.3 }}
    >
      {filled ? (
        <span className="text-red-400 text-xl">❤️</span>
      ) : (
        <span className="text-red-400/30 text-xl">♥</span>
      )}
    </motion.div>
  );
}

function BossAnswerInput({
  onSubmit,
  correctAnswer,
  round,
  totalRounds,
  explanation,
}: {
  onSubmit: (answer: string) => void;
  correctAnswer: string;
  round: number;
  totalRounds: number;
  explanation: string;
}) {
  const [answer, setAnswer] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmit = () => {
    if (!answer.trim()) return;
    const correct = answer.trim() === correctAnswer.trim();
    setIsCorrect(correct);
    setSubmitted(true);

    setTimeout(() => {
      onSubmit(answer.trim());
      setAnswer("");
      setSubmitted(false);
    }, 1500);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-xs font-mono text-brand-muted">
        <span>Round {round} of {totalRounds}</span>
        <span>•</span>
        <span>HP: {3 - (round - 1)}</span>
      </div>

      {!submitted ? (
        <>
          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Enter your answer..."
            className="w-full px-3 py-2 rounded-lg bg-surface-card/30 border border-white/5 text-text-primary font-mono text-sm focus:outline-none focus:border-red-400/30"
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />
          <button
            onClick={handleSubmit}
            className="w-full px-4 py-2 rounded-lg bg-red-500/20 border border-red-500/30 text-red-400 font-mono text-sm hover:bg-red-500/30 transition-all"
          >
            Strike the Boss!
          </button>
        </>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          className={`p-3 rounded-lg flex items-start gap-2 ${
            isCorrect
              ? "bg-green-500/10 border border-green-500/20 text-green-400"
              : "bg-red-500/10 border border-red-500/20 text-red-400"
          }`}
        >
          {isCorrect ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
          <div>
            <p>{isCorrect ? "Correct!" : "Wrong!"}</p>
            <p className="text-sm mt-1">{explanation}</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default VariableDiscovery;
