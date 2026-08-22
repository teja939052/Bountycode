import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft, ArrowRight, BookOpen, Lightbulb, Code2, Bug,
  Zap, Clock, Target, CheckCircle2, XCircle, Flame, Trophy,
  SkipForward, Loader2, Sparkles, Eye, Play, Square,
} from "lucide-react";
import Editor from "@monaco-editor/react";
import { missionApi } from "../services/api/missions";
import { useJuice } from "../juice/JuiceProvider";
import MasteryRadar from "../components/MasteryRadar";
import Skeleton from "../components/ui/Skeleton";

const LAYER_META = [
  { key: "story", name: "Story", icon: BookOpen, color: "#3B82F6", description: "Why this matters" },
  { key: "concept", name: "Concept", icon: Lightbulb, color: "#A855F7", description: "The idea explained" },
  { key: "interact", name: "Interact", icon: Eye, color: "#F59E0B", description: "Play with it" },
  { key: "code", name: "Code", icon: Code2, color: "#22C55E", description: "Build it" },
  { key: "mastery", name: "Mastery", icon: Trophy, color: "#EF4444", description: "Prove it" },
];

const INTERACTION_ICONS: Record<string, any> = {
  predict: Eye, trace: Target, bug_hunt: Bug, challenge: Code2, test_lab: Zap, speed_run: Clock,
};

const INTERACTION_COLORS: Record<string, string> = {
  predict: "#A855F7", trace: "#3B82F6", bug_hunt: "#EF4444", challenge: "#22C55E", test_lab: "#F59E0B", speed_run: "#EC4899",
};

interface MissionData {
  topic: string;
  layers: {
    story: { title: string; narrative: string; motivation: string; };
    concept: { title: string; explanation: string; examples: Array<{ code: string; output: string; explanation: string; }>; visualization?: string; };
    interact: { challenges: Array<{ type: string; prompt: string; code?: string; options?: string[]; answer: string; explanation: string; }>; };
    code: { challenge: string; boilerplate?: string; tests: Array<{ input: string; expected: string; }>; hints: string[]; };
    mastery: { boss_name: string; challenges: Array<{ type: string; prompt: string; code?: string; answer: string; difficulty: string; }>; pass_score: number; };
  };
  mastery?: any;
}

export default function MissionView() {
  const { topic } = useParams<{ topic: string }>();
  const navigate = useNavigate();
  const { showXP, play } = useJuice();

  const [mission, setMission] = useState<MissionData | null>(null);
  const [mastery, setMastery] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [layer, setLayer] = useState(0);
  const [interactIdx, setInteractIdx] = useState(0);
  const [masteryIdx, setMasteryIdx] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [resultCorrect, setResultCorrect] = useState(false);
  const [hintLevel, setHintLevel] = useState(0);
  const [hintText, setHintText] = useState("");
  const [combo, setCombo] = useState(0);
  const [totalXP, setTotalXP] = useState(0);
  const [masteryResults, setMasteryResults] = useState<Record<number, { correct: boolean; score: number }>>({});
  const [timer, setTimer] = useState(0);
  const timerRef = useRef<any>(null);
  const editorRef = useRef<any>(null);

  useEffect(() => {
    if (!topic) return;
    setLoading(true);
    missionApi.missionContent(topic)
      .then((data) => {
        setMission(data);
        setLoading(false);
      })
      .catch(() => {
        setMission(null);
        setLoading(false);
      });
    missionApi.topicMastery(topic).then(setMastery).catch(() => {});
  }, [topic]);

  useEffect(() => {
    if (layer >= 2 && !showResult) {
      timerRef.current = setInterval(() => setTimer((t) => t + 1), 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [layer, showResult]);

  const currentChallenge = mission?.layers.interact.challenges[interactIdx];
  const currentBoss = mission?.layers.mastery.challenges[masteryIdx];

  const submitInteract = (correct: boolean) => {
    setShowResult(true);
    setResultCorrect(correct);
    if (correct) {
      setCombo((c) => c + 1);
      const xp = 15 + combo * 5;
      setTotalXP((t) => t + xp);
      showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
      play("xpCollect");
    } else {
      setCombo(0);
    }
    if (topic && currentChallenge) {
      missionApi.submitInteraction({ topic, interaction_type: currentChallenge.type, score: correct ? 100 : 0, is_correct: correct }).catch(() => {});
    }
  };

  const nextInteract = () => {
    if (!mission) return;
    const challenges = mission.layers.interact.challenges;
    if (interactIdx < challenges.length - 1) {
      setInteractIdx((i) => i + 1);
      setShowResult(false);
      setUserAnswer("");
      setHintLevel(0);
      setHintText("");
    } else {
      setLayer(3);
      setTimer(0);
    }
  };

  const submitBoss = (correct: boolean) => {
    setShowResult(true);
    setResultCorrect(correct);
    setMasteryResults((prev) => ({ ...prev, [masteryIdx]: { correct, score: correct ? 100 : 0 } }));
    if (correct) {
      const xp = 25 + combo * 5;
      setTotalXP((t) => t + xp);
      showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
      play("xpCollect");
      setCombo((c) => c + 1);
    }
  };

  const nextBoss = () => {
    if (!mission) return;
    const challenges = mission.layers.mastery.challenges;
    if (masteryIdx < challenges.length - 1) {
      setMasteryIdx((i) => i + 1);
      setShowResult(false);
      setUserAnswer("");
    } else {
      const total = Object.values(masteryResults).length + 1;
      const correct = Object.values(masteryResults).filter((r) => r.correct).length + (resultCorrect ? 1 : 0);
      const pct = Math.round((correct / total) * 100);
      if (pct >= (mission.layers.mastery.pass_score || 70)) {
        play("levelUp");
      }
    }
  };

  const requestHint = async () => {
    if (!topic || !currentChallenge) return;
    const next = Math.min(hintLevel + 1, 3);
    try {
      const res = await missionApi.requestHint({ topic, interaction_type: currentChallenge.type, hint_level: next });
      setHintText(res.text);
      setHintLevel(next);
    } catch { /* ignore */ }
  };

  const handleEditorMount = (editor: any) => {
    editorRef.current = editor;
    if (mission?.layers.code.boilerplate) {
      editor.setValue(mission.layers.code.boilerplate);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-4xl mx-auto">
        <Skeleton className="h-10 w-64 mb-3 bg-white/5" />
        <Skeleton className="h-60 w-full rounded-2xl bg-white/5" />
      </div>
    );
  }

  if (!mission) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <p className="text-6xl mb-4">🔮</p>
          <h2 className="text-2xl font-display font-black text-white mb-2">Mission Not Found</h2>
          <p className="text-gray-400 text-sm mb-4">This mission hasn't been unlocked yet.</p>
          <button onClick={() => navigate("/journey")} className="px-4 py-2 rounded-xl bg-white/10 text-white text-sm border border-white/10 hover:bg-white/15 transition-all">
            Back to Career RPG
          </button>
        </div>
      </div>
    );
  }

  const layerInfo = LAYER_META[layer];

  return (
    <div className="min-h-screen bg-black px-4 py-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button onClick={() => navigate("/journey")} className="flex items-center gap-2 text-gray-400 hover:text-white text-sm transition-all">
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
        <div className="flex items-center gap-3">
          {combo >= 3 && (
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-orange-500/20 border border-orange-500/30">
              <Flame className="w-3.5 h-3.5 text-orange-400" />
              <span className="text-[10px] font-mono text-orange-400">{combo}x Combo</span>
            </motion.div>
          )}
          <span className="text-xs font-mono text-gray-500">{totalXP} XP</span>
        </div>
      </div>

      {/* Layer Progress */}
      <div className="flex gap-1 mb-6">
        {LAYER_META.map((l, i) => {
          const Icon = l.icon;
          return (
            <button key={l.key} onClick={() => i <= layer && setLayer(i)}
              className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-[10px] font-mono transition-all ${
                i === layer ? "text-white border border-white/15 bg-white/10" :
                i < layer ? "text-green-400 border border-green-500/20 bg-green-500/5" :
                "text-gray-600 border border-white/5 bg-transparent"
              }`}>
              {i < layer ? <CheckCircle2 className="w-3 h-3" /> : <Icon className="w-3 h-3" />}
              <span className="hidden sm:inline">{l.name}</span>
            </button>
          );
        })}
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        <motion.div key={layer} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>

          {/* LAYER 0: Story */}
          {layer === 0 && (
            <div className="rounded-3xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-transparent p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center bg-blue-500/20 border border-blue-500/30">
                  <BookOpen className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <h2 className="text-xl font-display font-black text-white">{mission.layers.story.title}</h2>
                  <p className="text-xs text-gray-400">Mission Briefing</p>
                </div>
              </div>
              <p className="text-sm text-gray-300 leading-relaxed mb-6 whitespace-pre-line">{mission.layers.story.narrative}</p>
              <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-4 mb-6">
                <p className="text-xs font-mono text-blue-400 mb-1">WHY THIS MATTERS</p>
                <p className="text-sm text-gray-300">{mission.layers.story.motivation}</p>
              </div>
              <button onClick={() => setLayer(1)} className="w-full py-3 rounded-xl bg-blue-500/20 text-blue-400 text-sm font-medium border border-blue-500/30 hover:bg-blue-500/30 transition-all flex items-center justify-center gap-2">
                Continue to Concept <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* LAYER 1: Concept */}
          {layer === 1 && (
            <div className="rounded-3xl border border-purple-500/20 bg-gradient-to-br from-purple-500/10 to-transparent p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center bg-purple-500/20 border border-purple-500/30">
                  <Lightbulb className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <h2 className="text-xl font-display font-black text-white">{mission.layers.concept.title}</h2>
                  <p className="text-xs text-gray-400">Core Concept</p>
                </div>
              </div>
              <div className="prose-invert text-sm text-gray-300 leading-relaxed mb-6 whitespace-pre-line">
                {mission.layers.concept.explanation}
              </div>
              {mission.layers.concept.visualization && (
                <div className="rounded-xl border border-purple-500/20 bg-black/40 p-4 mb-6 font-mono text-xs text-purple-300 whitespace-pre">
                  {mission.layers.concept.visualization}
                </div>
              )}
              {mission.layers.concept.examples.map((ex, i) => (
                <div key={i} className="rounded-xl border border-white/10 bg-white/5 p-4 mb-3">
                  <code className="text-xs text-green-400 font-mono block mb-2">{ex.code}</code>
                  <p className="text-[10px] font-mono text-gray-500">Output: <span className="text-white">{ex.output}</span></p>
                  <p className="text-[10px] text-gray-400 mt-1">{ex.explanation}</p>
                </div>
              ))}
              <button onClick={() => setLayer(2)} className="w-full py-3 rounded-xl bg-purple-500/20 text-purple-400 text-sm font-medium border border-purple-500/30 hover:bg-purple-500/30 transition-all flex items-center justify-center gap-2 mt-4">
                Start Interacting <Play className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* LAYER 2: Interact */}
          {layer === 2 && currentChallenge && (
            <div className="rounded-3xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-transparent p-6 sm:p-8">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${INTERACTION_COLORS[currentChallenge.type]}22`, border: `1px solid ${INTERACTION_COLORS[currentChallenge.type]}44` }}>
                    {(() => { const I = INTERACTION_ICONS[currentChallenge.type] || Target; return <I className="w-5 h-5" style={{ color: INTERACTION_COLORS[currentChallenge.type] }} />; })()}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">{currentChallenge.prompt}</h3>
                    <p className="text-[10px] font-mono" style={{ color: INTERACTION_COLORS[currentChallenge.type] }}>{currentChallenge.type.replace("_", " ")}</p>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-gray-500">{interactIdx + 1}/{mission.layers.interact.challenges.length}</span>
              </div>

              {currentChallenge.code && (
                <div className="rounded-xl border border-white/10 bg-black/40 p-4 mb-4 font-mono text-xs text-green-400 whitespace-pre">{currentChallenge.code}</div>
              )}

              {!showResult ? (
                <>
                  <input value={userAnswer} onChange={(e) => setUserAnswer(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && userAnswer.trim() && submitInteract(userAnswer.trim().toLowerCase() === currentChallenge.answer.toLowerCase())}
                    placeholder="Your answer..."
                    className="w-full bg-black/40 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-gray-600 font-mono focus:outline-none focus:border-white/25 transition-all mb-4" />

                  <div className="flex gap-3">
                    <button onClick={() => userAnswer.trim() && submitInteract(userAnswer.trim().toLowerCase() === currentChallenge.answer.toLowerCase())}
                      disabled={!userAnswer.trim()}
                      className="flex-1 py-2.5 rounded-xl bg-amber-500/20 text-amber-400 text-sm font-medium border border-amber-500/30 hover:bg-amber-500/30 transition-all disabled:opacity-30">
                      Submit
                    </button>
                    <button onClick={requestHint} disabled={hintLevel >= 3}
                      className="px-4 py-2.5 rounded-xl bg-white/5 text-gray-400 text-sm border border-white/5 hover:text-white transition-all disabled:opacity-30">
                      <Lightbulb className="w-4 h-4" /> {hintLevel > 0 && <span className="text-[10px] ml-1">{hintLevel}/3</span>}
                    </button>
                  </div>

                  {hintText && (
                    <motion.div initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}
                      className="mt-3 p-3 rounded-xl border border-amber-500/20 bg-amber-500/5 text-xs text-amber-300">
                      {hintText}
                    </motion.div>
                  )}
                </>
              ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <div className={`p-3 rounded-xl border text-sm font-mono mb-4 ${resultCorrect ? "border-green-500/30 bg-green-500/10 text-green-400" : "border-red-500/30 bg-red-500/10 text-red-400"}`}>
                    {resultCorrect ? "Correct!" : `Answer: ${currentChallenge.answer}`}
                  </div>
                  <p className="text-xs text-gray-400 mb-4">{currentChallenge.explanation}</p>
                  <button onClick={nextInteract}
                    className="w-full py-2.5 rounded-xl bg-white/10 text-white text-sm font-medium border border-white/10 hover:bg-white/15 transition-all flex items-center justify-center gap-2">
                    {interactIdx < mission.layers.interact.challenges.length - 1 ? "Next Challenge" : "Start Coding"}
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>
              )}
            </div>
          )}

          {/* LAYER 3: Code — Monaco Editor */}
          {layer === 3 && (
            <div className="rounded-3xl border border-green-500/20 bg-gradient-to-br from-green-500/10 to-transparent p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center bg-green-500/20 border border-green-500/30">
                  <Code2 className="w-6 h-6 text-green-400" />
                </div>
                <div>
                  <h2 className="text-xl font-display font-black text-white">Code Challenge</h2>
                  <p className="text-xs text-gray-400">Write real code · {Math.floor(timer / 60)}:{String(timer % 60).padStart(2, "0")}</p>
                </div>
              </div>
              <p className="text-sm text-gray-300 mb-4">{mission.layers.code.challenge}</p>

              {/* Monaco Editor */}
              <div className="rounded-xl border border-white/10 bg-[#1e1e1e] overflow-hidden mb-4">
                <div className="flex items-center justify-between px-4 py-2 bg-[#252526] border-b border-white/5">
                  <span className="text-[10px] font-mono text-gray-500">main.py</span>
                  <span className="text-[10px] font-mono text-green-400/60">Python</span>
                </div>
                <Editor
                  height="260px"
                  defaultLanguage="python"
                  theme="vs-dark"
                  defaultValue={mission.layers.code.boilerplate || "# Write your solution here\n"}
                  onMount={handleEditorMount}
                  options={{
                    fontSize: 13,
                    fontFamily: "'Fira Code', 'Cascadia Code', monospace",
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    lineNumbers: "on",
                    roundedSelection: true,
                    padding: { top: 12, bottom: 12 },
                    tabSize: 4,
                    automaticLayout: true,
                    wordWrap: "on",
                    scrollbar: { vertical: "hidden" },
                    overviewRulerLanes: 0,
                    hideCursorInOverviewRuler: true,
                  }}
                />
              </div>

              {mission.layers.code.tests.length > 0 && (
                <div className="rounded-xl border border-white/10 bg-white/5 p-3 mb-4">
                  <p className="text-[10px] font-mono text-gray-500 mb-1">TEST CASES</p>
                  {mission.layers.code.tests.map((t, i) => (
                    <div key={i} className="text-[11px] font-mono text-gray-400">
                      Input: <span className="text-white">{t.input || "(none)"}</span> → Expected: <span className="text-green-400">{t.expected}</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex gap-3">
                <button onClick={() => { setLayer(4); setMasteryIdx(0); setMasteryResults({}); setTimer(0); }}
                  className="flex-1 py-2.5 rounded-xl bg-green-500/20 text-green-400 text-sm font-medium border border-green-500/30 hover:bg-green-500/30 transition-all flex items-center justify-center gap-2">
                  Take Mastery Trial <Trophy className="w-4 h-4" />
                </button>
                <button onClick={requestHint} disabled={hintLevel >= 3}
                  className="px-4 py-2.5 rounded-xl bg-white/5 text-gray-400 text-sm border border-white/5 hover:text-white transition-all">
                  <Lightbulb className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* LAYER 4: Mastery Trial */}
          {layer === 4 && currentBoss && (
            <div className="rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-transparent p-6 sm:p-8">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">⚔️</div>
                  <div>
                    <h3 className="text-sm font-bold text-white">{mission.layers.mastery.boss_name}</h3>
                    <p className="text-[10px] font-mono text-gray-500">Mastery Trial · {masteryIdx + 1}/{mission.layers.mastery.challenges.length}</p>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-gray-500">Pass: {mission.layers.mastery.pass_score}%</span>
              </div>

              <div className="flex gap-1 mb-4">
                {mission.layers.mastery.challenges.map((_: any, i: number) => {
                  const r = masteryResults[i];
                  return (
                    <div key={i} className={`h-1.5 flex-1 rounded-full transition-all ${
                      r ? (r.correct ? "bg-green-500" : "bg-red-500") : (i === masteryIdx ? "bg-white" : "bg-white/10")
                    }`} />
                  );
                })}
              </div>

              <AnimatePresence mode="wait">
                <motion.div key={masteryIdx} initial={{ opacity: 0, x: 15 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -15 }}>
                  <p className="text-sm text-white mb-3">{currentBoss.prompt}</p>
                  {currentBoss.code && (
                    <div className="rounded-xl border border-white/10 bg-black/40 p-3 mb-4 font-mono text-xs text-green-400 whitespace-pre">{currentBoss.code}</div>
                  )}
                  {!showResult ? (
                    <>
                      <input value={userAnswer} onChange={(e) => setUserAnswer(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && userAnswer.trim() && submitBoss(userAnswer.trim().toLowerCase().includes(currentBoss.answer.toLowerCase()))}
                        placeholder="Your answer..."
                        className="w-full bg-black/40 border border-white/10 rounded-xl p-3 text-sm text-white placeholder-gray-600 font-mono focus:outline-none focus:border-white/25 transition-all mb-3" />
                      <button onClick={() => userAnswer.trim() && submitBoss(userAnswer.trim().toLowerCase().includes(currentBoss.answer.toLowerCase()))}
                        disabled={!userAnswer.trim()}
                        className="w-full py-2.5 rounded-xl bg-red-500/20 text-red-400 text-sm font-medium border border-red-500/30 hover:bg-red-500/30 transition-all disabled:opacity-30">
                        Attack
                      </button>
                    </>
                  ) : (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                      <div className={`p-3 rounded-xl border text-sm font-mono mb-3 ${resultCorrect ? "border-green-500/30 bg-green-500/10 text-green-400" : "border-red-500/30 bg-red-500/10 text-red-400"}`}>
                        {resultCorrect ? "Hit!" : `Answer: ${currentBoss.answer}`}
                      </div>
                      <button onClick={nextBoss}
                        className="w-full py-2.5 rounded-xl bg-white/10 text-white text-sm font-medium border border-white/10 hover:bg-white/15 transition-all">
                        {masteryIdx < mission.layers.mastery.challenges.length - 1 ? "Next Challenge" : "View Results"}
                      </button>
                    </motion.div>
                  )}
                </motion.div>
              </AnimatePresence>

              {mastery && (
                <div className="mt-6 pt-6 border-t border-white/10">
                  <p className="text-xs font-mono text-gray-500 mb-3">Current Mastery</p>
                  <div className="flex justify-center">
                    <MasteryRadar dimensions={mastery.dimensions} overall={mastery.overall} size={180} />
                  </div>
                </div>
              )}
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
