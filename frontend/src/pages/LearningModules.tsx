import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import {
  BookOpen,
  CheckCircle2,
  Lock,
  ChevronRight,
  ChevronLeft,
  GraduationCap,
  Clock,
  Zap,
  Trophy,
  Target,
  ChevronDown,
  ChevronUp,
  Code2,
  Sparkles,
  Star,
  Award,
  ArrowLeft,
  Flame,
  RotateCcw,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";

const DIFFICULTY_COLORS = {
  beginner: { bg: "bg-green-100", text: "text-green-700", border: "border-green-300" },
  intermediate: { bg: "bg-yellow-100", text: "text-yellow-700", border: "border-yellow-300" },
  advanced: { bg: "bg-red-100", text: "text-red-700", border: "border-red-300" },
};

const STEP_TYPE_ICON = {
  theory: "📖",
  example: "💡",
  try_it: "🛠️",
  hint: "🔍",
  solution: "✅",
};

const STEP_TYPE_LABEL = {
  theory: "Theory",
  example: "Walkthrough",
  try_it: "Try It",
  hint: "Hint",
  solution: "Solution",
};

function ProgressRing({ pct, size = 80, stroke = 6, color = "#3B82F6" }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;

  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.10)" strokeWidth={stroke} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round"
        className="transition-all duration-1000 ease-out"
      />
      <text x={size / 2} y={size / 2} textAnchor="middle" dominantBaseline="central" className="fill-text-primary text-sm font-bold" style={{ transform: "rotate(90deg)" }}>
        {Math.round(pct)}%
      </text>
    </svg>
  );
}

function ModuleCard({ module, onClick }) {
  const diff = DIFFICULTY_COLORS[module.difficulty] || DIFFICULTY_COLORS["beginner"];
  const isStarted = module.is_started;
  const progress = module.user_progress || 0;
  const isComplete = progress === 100;

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="relative rounded-2xl border border-brand-primary/20 bg-surface-card/90 p-5 cursor-pointer transition-all duration-200 hover:shadow-soft-lg group"
    >
      {isComplete && (
        <div className="absolute top-3 right-3" aria-label="Module completed">
          <CheckCircle2 size={20} className="text-green-500" />
        </div>
      )}

      <div className="flex items-center gap-3 mb-3">
        <div className="h-10 w-10 rounded-xl bg-brand-sky/10 flex items-center justify-center text-lg" aria-hidden="true">
          {STEP_TYPE_ICON.theory}
        </div>
        <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase tracking-wider font-medium border ${diff.bg} ${diff.text} ${diff.border}`}>
          {module.difficulty}
        </span>
      </div>

      <h3 className="font-display font-bold text-text-primary mb-1 group-hover:text-brand-sky transition-colors">
        {module.title}
      </h3>
      <p className="text-xs text-brand-secondary mb-3 line-clamp-2" style={{ display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
        {module.description}
      </p>

      <div className="mb-3">
        <div className="flex justify-between text-[10px] text-brand-secondary mb-1">
          <span>Progress</span>
          <span>{progress}%</span>
        </div>
        <div className="h-1.5 w-full bg-surface-card/50 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-brand-sky to-brand-lavender rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 text-[10px] text-brand-secondary">
          <span className="flex items-center gap-1"><Clock size={10} /> {module.estimated_time_minutes}m</span>
          <span className="flex items-center gap-1"><Zap size={10} /> {module.xp_reward} XP</span>
        </div>
        <span className="text-xs font-medium text-brand-sky group-hover:underline">
          {isStarted ? (isComplete ? "Review" : "Continue") : "Start"} →
        </span>
      </div>

      <div className="flex flex-wrap gap-1 mt-3">
        {(module.company_tags || []).slice(0, 3).map((tag) => (
          <span key={tag} className="px-2 py-0.5 rounded-full bg-brand-sky/10 text-brand-sky text-[9px] font-mono">
            {tag}
          </span>
        ))}
      </div>
    </motion.div>
  );
}

function StepList({ steps, currentStep, completedSteps, onStepClick }) {
  return (
    <div className="space-y-1">
      {steps.map((step, index) => {
        const stepNum = step.step_number || index + 1;
        const isCompleted = completedSteps.includes(stepNum);
        const isCurrent = stepNum === currentStep;
        const isLocked = !isCompleted && stepNum > currentStep && !steps.slice(0, stepNum - 1).every((_, i) => completedSteps.includes(i + 1));

        return (
          <button
            key={stepNum}
            onClick={() => !isLocked && onStepClick(stepNum)}
            disabled={isLocked}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all duration-200 ${
              isCurrent
                ? "bg-brand-sky/10 border border-brand-sky/30 text-brand-sky"
                : isCompleted
                ? "bg-green-50 border border-green-200 text-text-secondary"
                : isLocked
                ? "bg-surface-base border border-brand-primary/5 text-brand-secondary cursor-not-allowed opacity-60"
                : "hover:bg-surface-base border border-transparent"
            }`}
          >
            <span className="flex-shrink-0 w-6 text-center">
              {isCompleted ? (
                <CheckCircle2 size={16} className="text-green-500" />
              ) : isLocked ? (
                <Lock size={14} className="text-gray-400" />
              ) : (
                <span className="text-xs font-mono font-bold">{stepNum}</span>
              )}
            </span>
            <span className="flex-1 text-xs font-medium truncate">{step.title}</span>
            <span className="text-[9px] font-mono uppercase text-brand-secondary hidden sm:inline">
              {STEP_TYPE_LABEL[step.type] || step.type}
            </span>
          </button>
        );
      })}
    </div>
  );
}

function renderContent(content) {
  if (!content) return null;
  return (
    <div className="text-text-secondary leading-relaxed [&_h1]:font-display [&_h1]:text-text-primary [&_h1]:text-xl [&_h1]:font-bold [&_h1]:mt-6 [&_h1]:mb-3 [&_h2]:font-display [&_h2]:text-text-primary [&_h2]:text-lg [&_h2]:font-bold [&_h2]:mt-4 [&_h2]:mb-2 [&_p]:mb-3 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:pl-5 [&_li]:mb-1 [&_code]:bg-surface-card/50 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-sm [&_pre]:bg-surface-base [&_pre]:rounded-xl [&_pre]:p-4 [&_pre]:my-3 [&_pre]:overflow-x-auto [&_pre]:text-gray-100 [&_pre]:text-sm [&_pre]:font-mono [&_a]:text-brand-sky [&_a]:underline"
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
}

export default function LearningModules() {
  const [view, setView] = useState("list");
  const [modules, setModules] = useState([]);
  const [selectedModule, setSelectedModule] = useState(null);
  const [progress, setProgress] = useState(null);
  const [currentStepView, setCurrentStepView] = useState(1);
  const [loading, setLoading] = useState(true);
  const [stepLoading, setStepLoading] = useState(false);
  const [difficultyFilter, setDifficultyFilter] = useState("all");
  const [topicFilter, setTopicFilter] = useState("all");
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationData, setCelebrationData] = useState(null);

  const fetchModules = useCallback(async () => {
    try {
      const res = await api.learningModules.list({
        difficulty: difficultyFilter !== "all" ? difficultyFilter : undefined,
        topic: topicFilter !== "all" ? topicFilter : undefined,
      });
      setModules(res.modules || []);
    } catch (err) {
      console.error("Failed to load modules:", err);
    } finally {
      setLoading(false);
    }
  }, [difficultyFilter, topicFilter]);

  useEffect(() => {
    fetchModules();
  }, [fetchModules]);

  const handleSelectModule = useCallback(async (mod) => {
    setLoading(true);
    try {
      const res = await api.learningModules.get(mod.id);
      setSelectedModule(res.module);
      setProgress(res.progress);
      setCurrentStepView(res.progress?.current_step || 1);
      setView("detail");
    } catch (err) {
      console.error("Failed to load module:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleStartModule = useCallback(async () => {
    if (!selectedModule) return;
    try {
      const res = await api.learningModules.start(selectedModule.id);
      setProgress(res.progress);
    } catch (err) {
      console.error("Failed to start module:", err);
    }
  }, [selectedModule]);

  const handleCompleteStep = useCallback(async (stepNumber) => {
    if (!selectedModule) return;
    setStepLoading(true);
    try {
      const res = await api.learningModules.completeStep(selectedModule.id, stepNumber);
      setProgress((prev) => ({
        ...prev,
        completed_steps: res.completed_steps || (prev?.completed_steps || []).concat([stepNumber]),
        progress_pct: res.progress_pct,
        xp_earned: res.total_xp,
        completed_at: res.message.includes("Module complete") ? new Date().toISOString() : prev?.completed_at,
      }));

      if (res.badge_unlocked) {
        setCelebrationData({
          type: "badge",
          title: res.badge_unlocked,
          subtitle: "Badge Earned!",
          xp: res.xp_earned,
          message: `Badge unlocked: ${res.badge_unlocked}`,
        });
        setShowCelebration(true);
      } else if (res.message.includes("Module complete")) {
        setCelebrationData({
          type: "levelup",
          title: "Module Complete!",
          subtitle: `+${res.xp_earned} XP`,
          xp: res.xp_earned,
        });
        setShowCelebration(true);
      }

      if (res.completed_steps?.length < selectedModule.steps?.length) {
        const modRes = await api.learningModules.get(selectedModule.id);
        setSelectedModule(modRes.module);
        setProgress(modRes.progress);
      }
    } catch (err) {
      console.error("Failed to complete step:", err);
    } finally {
      setStepLoading(false);
    }
  }, [selectedModule]);

  const currentStep = currentStepView;

  const isModuleComplete = progress?.progress_pct === 100;

  if (loading && view === "list") {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base">
      <CelebrationOverlay
        show={showCelebration}
        type={celebrationData?.type || "confetti"}
        title={celebrationData?.title || ""}
        subtitle={celebrationData?.subtitle || ""}
        xp={celebrationData?.xp || 0}
        onClose={() => {
          setShowCelebration(false);
          setCelebrationData(null);
        }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          {view === "detail" && (
            <button
              onClick={() => setView("list")}
              className="flex items-center gap-2 text-sm font-medium text-brand-secondary hover:text-brand-sky transition-colors"
            >
              <ArrowLeft size={16} />
              Back to Modules
            </button>
          )}
          <div>
            <h1 className="font-display font-extrabold text-2xl text-text-primary">
              {view === "detail" ? selectedModule?.title : "Learning Modules"}
            </h1>
            <p className="text-sm text-brand-secondary mt-1">
              {view === "detail"
                ? "Master concepts step by step with interactive lessons"
                : "Choose a topic and start your learning journey"}
            </p>
          </div>
        </div>

        {/* Module List View */}
        {view === "list" && (
          <>
            {/* Filters */}
            <div className="flex flex-wrap gap-3 mb-8">
              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="quest-chip text-sm"
              >
                <option value="all">All Levels</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
              <select
                value={topicFilter}
                onChange={(e) => setTopicFilter(e.target.value)}
                className="quest-chip text-sm"
              >
                <option value="all">All Topics</option>
                <option value="arrays">Arrays</option>
                <option value="strings">Strings</option>
                <option value="search">Search</option>
                <option value="linked-lists">Linked Lists</option>
                <option value="sorting">Sorting</option>
                <option value="dynamic-programming">DP</option>
                <option value="trees">Trees</option>
              </select>
            </div>

            {/* Module Grid */}
            {modules.length === 0 ? (
              <div className="text-center py-16">
                <GraduationCap size={48} className="mx-auto text-gray-300 mb-4" />
                <p className="text-brand-secondary">No modules found for this filter.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {modules.map((mod) => (
                  <ModuleCard
                    key={mod.id}
                    module={mod}
                    onClick={() => handleSelectModule(mod)}
                  />
                ))}
              </div>
            )}
          </>
        )}

        {/* Module Detail View */}
        {view === "detail" && selectedModule && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Sidebar: Progress + Step List */}
            <div className="lg:col-span-1 space-y-6">
              {/* Progress Ring */}
              <div className="arena-card p-6 text-center">
                <ProgressRing
                  pct={progress?.progress_pct || 0}
                  size={100}
                  stroke={8}
                  color={isModuleComplete ? "#22C55E" : "#3B82F6"}
                />
                <h3 className="font-display font-bold text-text-primary mt-4">
                  {isModuleComplete ? "Complete!" : "In Progress"}
                </h3>
                <p className="text-xs text-brand-secondary mt-1">
                  {progress?.completed_steps?.length || 0} of {selectedModule.steps?.length} steps
                </p>
                <div className="flex items-center justify-center gap-4 mt-3 text-xs text-brand-secondary">
                  <span className="flex items-center gap-1"><Zap size={12} /> {progress?.xp_earned || 0} XP</span>
                  {progress?.badge_unlocked && <span className="flex items-center gap-1"><Trophy size={12} /> {progress.badge_unlocked}</span>}
                </div>
              </div>

              {/* Step List */}
              <div className="arena-card p-4">
                <h4 className="font-display font-bold text-sm text-text-primary mb-3">Steps</h4>
                <StepList
                  steps={selectedModule.steps || []}
                  currentStep={currentStep}
                  completedSteps={progress?.completed_steps || []}
                  onStepClick={(stepNum) => {
                    const stepIndex = stepNum - 1;
                    const steps = selectedModule.steps || [];
                    if (stepNum <= currentStep || steps.slice(0, stepNum - 1).every((_, i) => (progress?.completed_steps || []).includes(i + 1))) {
                      setCurrentStepView(stepNum);
                    }
                  }}
                />
              </div>

              {/* Start/Resume Button */}
              {!progress && (
                <button
                  onClick={handleStartModule}
                  className="w-full btn-primary py-3 text-sm font-bold"
                >
                  Start Module
                </button>
              )}
            </div>

            {/* Main Content Area */}
            <div className="lg:col-span-3">
              {/* Current Step Content */}
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="arena-card p-8"
              >
                {(() => {
                  const steps = selectedModule.steps || [];
                  const stepIndex = Math.min(currentStep - 1, steps.length - 1);
                  const step = steps[stepIndex];
                  if (!step) return <p>No steps available.</p>;

                  return (
                    <>
                      {/* Step Header */}
                      <div className="flex items-center gap-3 mb-6">
                        <span className="text-2xl" aria-hidden="true">{STEP_TYPE_ICON[step.type] || "📋"}</span>
                        <div>
                          <span className="text-[10px] font-mono uppercase tracking-wider text-brand-sky font-medium">
                            Step {step.step_number || stepIndex + 1} of {steps.length}
                          </span>
                          <h2 className="font-display font-bold text-xl text-text-primary">{step.title}</h2>
                        </div>
                      </div>

                      {/* Step Type Badge */}
                      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-sky/10 text-brand-sky text-xs font-mono mb-6">
                        {STEP_TYPE_LABEL[step.type] || step.type}
                      </div>

                      {/* Content */}
                      <div className="mb-8">{renderContent(step.content)}</div>

                      {/* Code Snippet */}
                      {step.code_snippet && (
                        <div className="mb-8">
                          <div className="flex items-center gap-2 mb-3">
                            <Code2 size={14} className="text-brand-sky" />
                            <span className="text-xs font-mono font-medium text-brand-secondary">
                              {step.language ? `${step.language} — ` : ""}Code
                            </span>
                          </div>
                          <pre className="bg-surface-2 text-text-primary rounded-xl p-4 text-sm font-mono overflow-x-auto leading-relaxed">
                            <code>{step.code_snippet}</code>
                          </pre>
                        </div>
                      )}

                      {/* Try It Button */}
                      {step.type === "try_it" && (
                        <div className="mb-6">
                          <Link
                            to={`/compiler`}
                            state={{ code: step.code_snippet || "", language: step.language || "python" }}
                            className="btn-primary inline-flex items-center gap-2 py-2.5 px-5 text-sm"
                          >
                            <Code2 size={14} /> Open Editor
                          </Link>
                        </div>
                      )}

                      {/* Navigation Buttons */}
                      <div className="flex items-center justify-between pt-6 border-t border-brand-primary/5">
                        <button
                          onClick={() => {
                            const prev = Math.max(1, currentStep - 1);
                            setCurrentStepView(prev);
                          }}
                          disabled={currentStep <= 1}
                          className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium text-brand-secondary hover:text-brand-sky transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                        >
                          <ChevronLeft size={16} /> Previous
                        </button>

                        {(progress?.completed_steps || []).includes(currentStep) ? (
                          <button
                            onClick={() => {
                              const next = Math.min(steps.length, currentStep + 1);
                              if (next > currentStep) {
                                setCurrentStepView(next);
                              }
                            }}
                            disabled={currentStep >= steps.length}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium text-brand-sky hover:bg-brand-sky/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                          >
                            Next <ChevronRight size={16} />
                          </button>
                        ) : (
                          <button
                            onClick={() => handleCompleteStep(currentStep)}
                            disabled={stepLoading}
                            className="btn-primary px-5 py-2.5 flex items-center gap-2 text-sm"
                          >
                            {stepLoading ? <Spinner size={14} /> : <CheckCircle2 size={16} />}
                            Mark Complete
                          </button>
                        )}
                      </div>
                    </>
                  );
                })()}
              </motion.div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}