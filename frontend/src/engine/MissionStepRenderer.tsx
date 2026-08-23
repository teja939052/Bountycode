import { useState, useEffect } from "react";
import { Play, Pause, RotateCcw, Check, X, Lightbulb, Target, Bug, Zap, Shield, Clock, Brain } from "lucide-react";
import { compilerApi } from "../services/api/coding";

interface MissionStepRendererProps {
  step: any;
  state: any;
  guideDialogue: any[];
  guideMood: string;
  onSubmitPrediction: (answer: string) => Promise<any>;
  onRunCode: (code: string) => Promise<any>;
  onSubmitDebugFix: (code: string) => Promise<any>;
  onRequestHint: () => string;
  onNextStep: () => void;
  onPreviousStep: () => void;
  canGoNext: boolean;
  canGoPrevious: boolean;
  isRunning: boolean;
  runOutput: any;
  checkResult: any;
  code: string;
  setCode: (code: string) => void;
  showHints: boolean;
  hintCount: number;
  setShowHints: (show: boolean) => void;
  setHintCount: (count: number) => void;
}

export function MissionStepRenderer({
  step,
  state,
  guideDialogue,
  guideMood,
  onSubmitPrediction,
  onRunCode,
  onSubmitDebugFix,
  onRequestHint,
  onNextStep,
  onPreviousStep,
  canGoNext,
  canGoPrevious,
  isRunning,
  runOutput,
  checkResult,
  code,
  setCode,
  showHints,
  hintCount,
  setShowHints,
  setHintCount,
}: MissionStepRendererProps) {
  const moodEmojis: Record<string, string> = {
    encouraging: "🌱",
    curious: "🔍",
    challenging: "⚔️",
    proud: "🏆",
    patient: "🌿",
    serious: "🎯",
  };

  const stepIcons: Record<string, any> = {
    story: Brain,
    discover: Zap,
    predict: Target,
    build: Play,
    break: Bug,
    debug: Bug,
    prove: Shield,
    reward: Zap,
  };

  const StepIcon = stepIcons[step.type] || Brain;

  if (!guideDialogue || guideDialogue.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Nova Guide Panel */}
      <div className="rounded-2xl bg-gradient-to-r from-[#EEF5E7] to-[#F0FDF4] border border-[#D1FAE5] p-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-white/80 flex items-center justify-center text-2xl">
            {moodEmojis[guideMood] || "🌱"}
          </div>
          <div className="flex-1 space-y-2">
            {guideDialogue.map((dialogue, i) => (
              <div key={i} className="text-text-primary leading-relaxed">
                <span className="font-semibold text-nature-blossom">Nova:</span> {dialogue.text}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Step Content */}
      <div className="rounded-2xl border border-[#E5E7EB] bg-white p-6 shadow-[0_1px_2px_rgba(31,41,55,0.04)]">
        <div className="mb-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary-soft flex items-center justify-center">
            <StepIcon size={20} className="text-primary" />
          </div>
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-wider text-nature-blossom">
              {step.type.toUpperCase()}
            </p>
            <h3 className="font-display text-lg font-bold text-text-primary">{step.title}</h3>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <span className="rounded-full bg-primary-soft px-3 py-1 text-xs font-semibold text-primary">
              +{step.xp} XP
            </span>
          </div>
        </div>

        <div className="prose prose-sm max-w-none text-text-secondary">
          {step.content}
        </div>

        {/* Step-specific UI */}
        {step.type === "discover" && (
          <DiscoverStep step={step} code={code} setCode={setCode} runOutput={runOutput} isRunning={isRunning} onRunCode={onRunCode} />
        )}

        {step.type === "predict" && (
          <PredictStep step={step} state={state} onSubmitPrediction={onSubmitPrediction} checkResult={checkResult} />
        )}

        {step.type === "build" && (
          <BuildStep
            step={step}
            code={code}
            setCode={setCode}
            runOutput={runOutput}
            checkResult={checkResult}
            isRunning={isRunning}
            onRunCode={onRunCode}
            showHints={showHints}
            hintCount={hintCount}
            setShowHints={setShowHints}
            setHintCount={setHintCount}
            onRequestHint={onRequestHint}
          />
        )}

        {step.type === "break" && (
          <BreakStep step={step} />
        )}

        {step.type === "debug" && (
          <DebugStep
            step={step}
            code={code}
            setCode={setCode}
            runOutput={runOutput}
            checkResult={checkResult}
            isRunning={isRunning}
            onSubmitDebugFix={onSubmitDebugFix}
            showHints={showHints}
            hintCount={hintCount}
            setShowHints={setShowHints}
            setHintCount={setHintCount}
            onRequestHint={onRequestHint}
          />
        )}

        {step.type === "prove" && (
          <ProveStep
            step={step}
            code={code}
            setCode={setCode}
            runOutput={runOutput}
            checkResult={checkResult}
            isRunning={isRunning}
            onRunCode={onRunCode}
          />
        )}

        {step.type === "reward" && (
          <RewardStep step={step} />
        )}

        {step.type === "story" && (
          <StoryStep step={step} />
        )}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between pt-4 border-t border-[#E5E7EB]">
        <button
          onClick={onPreviousStep}
          disabled={!canGoPrevious}
          className="px-4 py-2 text-sm text-text-muted hover:text-text-primary disabled:opacity-50 transition-colors"
        >
          ← Back
        </button>
        {canGoNext && (
          <button
            onClick={onNextStep}
            className="px-6 py-3 rounded-[10px] bg-primary text-text-primary font-medium text-sm transition-all hover:bg-primary-dark"
          >
            Next →
          </button>
        )}
      </div>
    </div>
  );
}

function DiscoverStep({ step, code, setCode, runOutput, isRunning, onRunCode }: any) {
  const config = step.config;
  return (
    <div className="mt-6 space-y-4">
      <p className="text-sm text-text-secondary">Run the code and observe what happens.</p>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        className="h-48 w-full resize-y rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed text-text-primary outline-none focus:border-nature-leaf focus:ring-2 focus:ring-nature-leaf/20"
        defaultValue={config.codeSnippet || ""}
      />
      <div className="flex gap-2">
        <button
          onClick={onRunCode}
          disabled={isRunning}
          className="rounded-full bg-[#1F2937] px-5 py-2 text-sm font-bold text-white transition-colors hover:bg-[#374151] disabled:opacity-60"
        >
          {isRunning ? "Running…" : "Run Code"}
        </button>
      </div>
      {runOutput && (
        <div className={`rounded-xl p-4 font-mono text-[13px] ${runOutput.ok ? "bg-green-50 border border-green-200 text-green-700" : "bg-red-50 border border-red-200 text-red-700"}`}>
          <pre className="whitespace-pre-wrap">{runOutput.text || runOutput.output || "(no output)"}</pre>
          {runOutput.expected && (
            <p className="mt-2 text-green-700">Expected: {runOutput.expected}</p>
          )}
        </div>
      )}
      {config.expectedOutput && (
        <p className="text-xs text-text-muted">Expected: {config.expectedOutput}</p>
      )}
    </div>
  );
}

function PredictStep({ step, state, onSubmitPrediction, checkResult }: any) {
  const config = step.config;
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (answer: string) => {
    setSelectedAnswer(answer);
    setSubmitted(true);
    await onSubmitPrediction(answer);
  };

  return (
    <div className="mt-6 space-y-4">
      <p className="font-semibold text-text-primary">{config.question}</p>
      <div className="space-y-2">
        {config.options?.map((option: any, i: number) => (
          <button
            key={i}
            onClick={() => !submitted && setSelectedAnswer(option.id)}
            disabled={submitted}
            className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition-colors ${
              submitted
                ? option.correct
                  ? "border-green-300 bg-green-50 text-green-700"
                  : option.id === selectedAnswer
                  ? "border-red-300 bg-red-50 text-red-700"
                  : "border-[#E5E7EB] bg-white text-text-secondary"
                : option.id === selectedAnswer
                ? "border-[#4F8F57] bg-[#EEF5E7] text-text-primary"
                : "border-[#E5E7EB] bg-white text-text-secondary hover:bg-[#F9FAFB]"
            }`}
          >
            {option.text}
          </button>
        ))}
      </div>
      {submitted && config.explanation && (
        <div className={`rounded-xl p-4 ${selectedAnswer === config.correctAnswer ? "bg-green-50 border border-green-200 text-green-700" : "bg-red-50 border border-red-200 text-red-700"}`}>
          {selectedAnswer === config.correctAnswer ? "Correct! " : "Not quite. "}{config.explanation}
        </div>
      )}
    </div>
  );
}

function BuildStep({
  step,
  code,
  setCode,
  runOutput,
  checkResult,
  isRunning,
  onRunCode,
  showHints,
  hintCount,
  setShowHints,
  setHintCount,
  onRequestHint,
}: any) {
  const config = step.config;
  return (
    <div className="mt-6 space-y-4">
      <p className="text-sm text-text-secondary">{config.description}</p>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        className="h-56 w-full resize-y rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed text-text-primary outline-none focus:border-nature-leaf focus:ring-2 focus:ring-nature-leaf/20"
        defaultValue={config.starterCode || ""}
        placeholder={config.signature}
      />
      <div className="flex flex-wrap gap-2">
        <button
          onClick={onRunCode}
          disabled={isRunning}
          className="rounded-full bg-[#1F2937] px-5 py-2 text-sm font-bold text-white transition-colors hover:bg-[#374151] disabled:opacity-60"
        >
          {isRunning ? "Running…" : "Run Tests"}
        </button>
        {config.hints?.length > 0 && (
          <button
            onClick={() => { setShowHints(!showHints); if (!showHints) { setHintCount(c => Math.min(c + 1, config.hints?.length || 1)); onRequestHint(); }}}
            className="flex items-center gap-1.5 rounded-full border border-[#EAB308]/40 bg-[#FEFCE8] px-4 py-2 text-sm font-semibold text-[#854D0E] hover:bg-[#FEF9C3]"
          >
            <Lightbulb size={15} /> Hint
          </button>
        )}
      </div>
      {showHints && config.hints?.length > 0 && (
        <div className="rounded-xl border border-[#EAB308]/30 bg-[#FEFCE8] p-4">
          {config.hints.slice(0, hintCount).map((h: string, i: number) => (
            <p key={i} className="text-sm text-[#854D0E]">{h}</p>
          ))}
        </div>
      )}
      {runOutput && (
        <div className={`rounded-xl p-4 font-mono text-[13px] ${runOutput.ok ? "bg-green-50 border border-green-200 text-green-700" : "bg-red-50 border border-red-200 text-red-700"}`}>
          <pre className="whitespace-pre-wrap">{runOutput.text || "(no output)"}</pre>
          {runOutput.expected && <p className="mt-2 text-green-700">Expected: {runOutput.expected}</p>}
          {runOutput.mismatch && <p className="mt-2 text-red-700">{runOutput.mismatch}</p>}
        </div>
      )}
      {checkResult === true && (
        <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-semibold text-green-700 flex items-center gap-2">
          <Check size={16} /> All tests passed!
        </div>
      )}
      {checkResult === false && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700 flex items-center gap-2">
          <X size={16} /> Not quite — check the requirements and try again.
        </div>
      )}
    </div>
  );
}

function BreakStep({ step }: any) {
  const config = step.config;
  return (
    <div className="mt-6 space-y-4">
      <p className="text-sm text-text-secondary">{config.question}</p>
      <div className="space-y-2">
        {config.inputsToTry?.map((input: string, i: number) => (
          <button key={i} className="w-full rounded-xl border border-[#E5E7EB] bg-white px-4 py-3 text-left text-sm font-mono text-text-primary hover:bg-[#F9FAFB]">
            {input}
          </button>
        ))}
      </div>
      {config.explanation && (
        <div className="rounded-xl bg-[#FEFCE8] border border-[#EAB308]/30 p-4 text-sm text-[#854D0E]">
          {config.explanation}
        </div>
      )}
    </div>
  );
}

function DebugStep({
  step,
  code,
  setCode,
  runOutput,
  checkResult,
  isRunning,
  onSubmitDebugFix,
  showHints,
  hintCount,
  setShowHints,
  setHintCount,
  onRequestHint,
}: any) {
  const config = step.config;
  return (
    <div className="mt-6 space-y-4">
      <div className="rounded-xl border border-red-200 bg-red-50 p-4">
        <p className="font-semibold text-red-700 mb-2">Buggy Code:</p>
        <pre className="rounded-lg bg-red-50/50 p-3 font-mono text-[13px] text-red-700 overflow-x-auto">{config.buggyCode}</pre>
        <p className="mt-2 text-sm text-red-600">Error: {config.error}</p>
        {config.failingInput && (
          <p className="text-sm text-text-muted">Failing input: <code>{JSON.stringify(config.failingInput)}</code></p>
        )}
      </div>
      <p className="text-sm text-text-secondary">Fix the bug and run the tests.</p>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        className="h-56 w-full resize-y rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed text-text-primary outline-none focus:border-nature-leaf focus:ring-2 focus:ring-nature-leaf/20"
        defaultValue={config.buggyCode}
      />
      <div className="flex flex-wrap gap-2">
        <button
          onClick={onSubmitDebugFix}
          disabled={isRunning}
          className="rounded-full bg-[#1F2937] px-5 py-2 text-sm font-bold text-white transition-colors hover:bg-[#374151] disabled:opacity-60"
        >
          {isRunning ? "Testing Fix…" : "Test Fix"}
        </button>
        {config.hints?.length > 0 && (
          <button
            onClick={() => { setShowHints(!showHints); if (!showHints) { setHintCount(c => Math.min(c + 1, config.hints?.length || 1)); onRequestHint(); }}}
            className="flex items-center gap-1.5 rounded-full border border-[#EAB308]/40 bg-[#FEFCE8] px-4 py-2 text-sm font-semibold text-[#854D0E] hover:bg-[#FEF9C3]"
          >
            <Lightbulb size={15} /> Hint
          </button>
        )}
      </div>
      {showHints && config.hints?.length > 0 && (
        <div className="rounded-xl border border-[#EAB308]/30 bg-[#FEFCE8] p-4">
          {config.hints.slice(0, hintCount).map((h: string, i: number) => (
            <p key={i} className="text-sm text-[#854D0E]">{h}</p>
          ))}
        </div>
      )}
      {runOutput && (
        <div className={`rounded-xl p-4 font-mono text-[13px] ${runOutput.ok ? "bg-green-50 border border-green-200 text-green-700" : "bg-red-50 border border-red-200 text-red-700"}`}>
          <pre className="whitespace-pre-wrap">{runOutput.text || "(no output)"}</pre>
        </div>
      )}
      {checkResult === true && (
        <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm font-semibold text-green-700 flex items-center gap-2">
          <Check size={16} /> Bug fixed! All tests pass.
        </div>
      )}
    </div>
  );
}

function ProveStep({
  step,
  code,
  setCode,
  runOutput,
  checkResult,
  isRunning,
  onRunCode,
}: any) {
  const config = step.config;
  return (
    <div className="mt-6 space-y-4">
      <div className="rounded-xl border-2 border-red-200 bg-red-50 p-4">
        <div className="flex items-center gap-2 mb-2">
          <Shield size={20} className="text-red-500" />
          <span className="font-bold text-red-700">BOSS BOUNTY</span>
          {config.timed && (
            <span className="ml-auto flex items-center gap-1 text-red-600">
              <Clock size={14} /> {config.timeLimitMinutes} min
            </span>
          )}
        </div>
        <p className="text-text-secondary">{config.description}</p>
      </div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        className="h-64 w-full resize-y rounded-xl border border-[#E5E7EB] bg-[#F9FAFB] p-4 font-mono text-[13px] leading-relaxed text-text-primary outline-none focus:border-red-400 focus:ring-2 focus:ring-red-400/20"
        placeholder={config.signature}
      />
      <button
        onClick={onRunCode}
        disabled={isRunning}
        className="w-full rounded-full bg-red-600 px-6 py-3 text-sm font-bold text-white transition-colors hover:bg-red-700 disabled:opacity-60"
        disabled={isRunning}
      >
        {isRunning ? "Running Tests…" : "Submit for Review"}
      </button>
      {runOutput && (
        <div className={`rounded-xl p-4 font-mono text-[13px] ${runOutput.ok ? "bg-green-50 border border-green-200 text-green-700" : "bg-red-50 border border-red-200 text-red-700"}`}>
          <pre className="whitespace-pre-wrap">{runOutput.text || "(no output)"}</pre>
        </div>
      )}
      {checkResult === true && (
        <div className="rounded-xl border-2 border-green-400 bg-green-50 px-4 py-3 text-sm font-bold text-green-700 flex items-center gap-2">
          <Shield size={16} className="text-green-500" /> Boss defeated! Mastery achieved.
        </div>
      )}
    </div>
  );
}

function RewardStep({ step }: any) {
  return (
    <div className="mt-6 space-y-4 text-center">
      <div className="text-6xl">🏆</div>
      <h3 className="font-display text-2xl font-bold text-text-primary">Mission Complete!</h3>
      <p className="text-text-secondary">{step.content}</p>
      <div className="rounded-xl bg-gradient-to-r from-primary to-primary-dark px-6 py-4 text-text-primary">
        <p className="font-bold">+{step.xp} XP</p>
        <p className="text-sm opacity-80">Mastery unlocked</p>
      </div>
    </div>
  );
}

function StoryStep({ step }: any) {
  return (
    <div className="mt-6 space-y-4">
      <div className="prose prose-sm max-w-none text-text-secondary">
        {step.content}
      </div>
    </div>
  );
}