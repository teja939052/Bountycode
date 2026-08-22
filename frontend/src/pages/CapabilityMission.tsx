import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, CheckCircle2, XCircle, Code2, Bug, Target, Zap } from 'lucide-react';

const api = {
  mission: (world: string, comp: string) => fetch(`/api/v1/curriculum/mission/${world}/${comp}`, { credentials: 'include' }).then(r => r.json()),
  completeStep: (data: Record<string, unknown>) => fetch('/api/v1/curriculum/complete-step', {
    method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(r => r.json()),
};

interface Step {
  type: string; title: string; content?: string; code?: string;
  expected_output?: string; hint?: string; question?: string;
  options?: Array<{ id: string; text: string; correct: boolean }>;
  explanation?: string; function_name?: string; signature?: string;
  description?: string; test_cases?: Array<Record<string, unknown>>;
  hidden_tests?: number; xp?: number; timed?: boolean;
  time_limit_minutes?: number; buggy_code?: string;
  failing_input?: Record<string, unknown>; simulation?: Record<string, unknown>;
}

export default function CapabilityMission() {
  const { worldId, competencyId } = useParams<{ worldId: string; competencyId: string }>();
  const navigate = useNavigate();
  const [comp, setComp] = useState<Record<string, unknown> | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, unknown>>({});
  const [stepScores, setStepScores] = useState<Record<number, number>>({});
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [showHint, setShowHint] = useState(false);
  const [code, setCode] = useState('');
  const [reward, setReward] = useState<{ xp: number; readiness: number | null } | null>(null);

  useEffect(() => {
    if (worldId && competencyId) {
      api.mission(worldId, competencyId).then(r => { setComp(r.competency); setLoading(false); });
    }
  }, [worldId, competencyId]);

  const steps: Step[] = (comp?.steps as Step[]) || [];
  const step = steps[currentStep];
  const totalSteps = steps.length;

  const handleAnswer = useCallback((stepIdx: number, answer: unknown, score: number) => {
    setAnswers(prev => ({ ...prev, [stepIdx]: answer }));
    setStepScores(prev => ({ ...prev, [stepIdx]: score }));
    setCompletedSteps(prev => new Set(prev).add(stepIdx));
    if (worldId && competencyId) {
      api.completeStep({ world_id: worldId, competency_id: competencyId, step_index: stepIdx, score, time_spent_seconds: 0 })
        .then(r => {
          if (r && (r.xp_awarded > 0 || r.readiness_score != null)) {
            setReward({ xp: r.xp_awarded || 0, readiness: r.readiness_score });
            setTimeout(() => setReward(null), 5000);
          }
        })
        .catch(() => {});
    }
  }, [worldId, competencyId]);

  if (loading) return (
    <div className="min-h-screen bg-[#0a0e17] flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" />
    </div>
  );

  if (!step) return (
    <div className="min-h-screen bg-[#0a0e17] flex items-center justify-center text-white">
      <div className="text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-2xl font-bold mb-2">Mission Complete!</h2>
        <p className="text-gray-400 mb-6">{completedSteps.size} / {totalSteps} steps done.</p>
        <button onClick={() => navigate('/capability-worlds')} className="px-6 py-3 bg-emerald-500/20 hover:bg-emerald-500/30 rounded-xl text-emerald-300 font-medium">
          Back to Worlds
        </button>
      </div>
    </div>
  );

  const stepIcons: Record<string, React.ComponentType<{ className?: string }>> = {
    context: Target, explore: Code2, predict: Zap, build: Zap, break: Bug,
    debug: Bug, real_world: Zap, assessment: CheckCircle2, reflection: Target, goal: Target,
  };
  const Icon = stepIcons[step.type] || Target;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e17] via-[#0d1525] to-[#0f172a] text-white">
      {reward && (
        <motion.div initial={{ opacity: 0, y: -30 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
          className="fixed top-6 left-1/2 -translate-x-1/2 z-50 px-6 py-3 bg-gradient-to-r from-purple-500/30 to-cyan-500/30 border border-purple-500/40 rounded-2xl backdrop-blur-lg flex items-center gap-4 shadow-xl">
          {reward.xp > 0 && <span className="text-amber-300 font-bold">+{reward.xp} XP</span>}
          {reward.readiness != null && (
            <span className="text-cyan-300 text-sm">Job Readiness: <strong>{Math.round(reward.readiness)}%</strong></span>
          )}
        </motion.div>
      )}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-6 flex items-center gap-4">
          <button onClick={() => navigate(-1)} className="text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
            <motion.div className="h-full bg-gradient-to-r from-purple-500 to-cyan-500 rounded-full"
              animate={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }} />
          </div>
          <span className="text-sm text-gray-400">{currentStep + 1}/{totalSteps}</span>
        </div>

        <motion.div key={currentStep} initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center">
              <Icon className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <div className="text-xs text-purple-400 uppercase tracking-wider font-medium">{step.type}</div>
              <h2 className="text-xl font-bold">{step.title}</h2>
            </div>
          </div>
          {step.content && step.type !== 'context' && step.type !== 'goal' && (
            <p className="text-gray-300 ml-13">{step.content}</p>
          )}
        </motion.div>

        <AnimatePresence mode="wait">
          <motion.div key={currentStep} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
            <StepRenderer step={step} stepIndex={currentStep} onAnswer={handleAnswer}
              answer={answers[currentStep]} completed={completedSteps.has(currentStep)}
              code={code} setCode={setCode} stepScores={stepScores} />
          </motion.div>
        </AnimatePresence>

        {step.hint && (
          <div className="mt-6">
            {!showHint ? (
              <button onClick={() => setShowHint(true)} className="text-sm text-amber-400 hover:text-amber-300">Need a hint?</button>
            ) : (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-200 text-sm">
                {step.hint}
              </motion.div>
            )}
          </div>
        )}

        <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/10">
          <button onClick={() => { if (currentStep > 0) { setCurrentStep(currentStep - 1); setShowHint(false); } }}
            disabled={currentStep === 0}
            className="px-5 py-2.5 text-sm text-gray-400 hover:text-white disabled:opacity-30">
            Previous
          </button>
          <div className="text-sm text-gray-500">
            {step.xp ? `${step.xp} XP` : ''} {step.timed ? `${step.time_limit_minutes} min` : ''}
          </div>
          <button onClick={() => { if (currentStep < totalSteps - 1) { setCurrentStep(currentStep + 1); setShowHint(false); setCode(''); } }}
            className="px-5 py-2.5 bg-white/10 hover:bg-white/15 rounded-xl text-sm font-medium flex items-center gap-2">
            {currentStep === totalSteps - 1 ? 'Complete' : 'Next'} <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

function StepRenderer({ step, stepIndex, onAnswer, answer, completed, code, setCode, stepScores }: {
  step: Step; stepIndex: number; onAnswer: (idx: number, answer: unknown, score: number) => void;
  answer: unknown; completed: boolean; code: string; setCode: (v: string) => void; stepScores: Record<number, number>;
}) {
  if (step.type === 'context' || step.type === 'goal') {
    return (
      <div className="p-6 bg-white/5 border border-white/10 rounded-2xl">
        {step.simulation && (
          <div className="mb-4 p-4 bg-black/40 rounded-xl font-mono text-sm text-green-400 whitespace-pre-wrap">
            {String((step.simulation as Record<string, unknown>).initial_state || '')}
          </div>
        )}
        {step.type === 'goal' && step.content && (
          <div className="text-lg font-semibold text-emerald-400">{step.content}</div>
        )}
        {step.content && step.type === 'context' && (
          <div className="text-gray-300">{step.content}</div>
        )}
      </div>
    );
  }

  if (step.type === 'explore') {
    return (
      <div className="space-y-4">
        <div className="p-4 bg-black/40 rounded-xl font-mono text-sm text-green-400 whitespace-pre-wrap overflow-x-auto">
          {step.code}
        </div>
        <div className="text-xs text-gray-500">Expected output:</div>
        <div className="p-3 bg-white/5 rounded-lg font-mono text-sm text-cyan-300">{step.expected_output}</div>
        {completed && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> Explored
          </div>
        )}
      </div>
    );
  }

  if (step.type === 'predict' && step.options) {
    const selected = answer as string | undefined;
    return (
      <div className="space-y-3">
        <div className="text-lg font-medium mb-4">{step.question}</div>
        {step.options.map(opt => (
          <button key={opt.id} disabled={completed}
            onClick={() => onAnswer(stepIndex, opt.id, opt.correct ? 100 : 0)}
            className={`w-full p-4 rounded-xl border text-left transition-all ${
              selected === opt.id
                ? opt.correct ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-red-500/10 border-red-500/30 text-red-300'
                : 'bg-white/5 border-white/10 hover:border-white/20'
            }`}>
            <span className="font-medium mr-3">{opt.id.toUpperCase()}.</span> {opt.text}
            {selected === opt.id && opt.correct && <CheckCircle2 className="w-4 h-4 inline ml-2 text-emerald-400" />}
            {selected === opt.id && !opt.correct && <XCircle className="w-4 h-4 inline ml-2 text-red-400" />}
          </button>
        ))}
        {completed && step.explanation && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-xl text-cyan-200 text-sm mt-4">
            {step.explanation}
          </motion.div>
        )}
      </div>
    );
  }

  if (step.type === 'build' || step.type === 'real_world') {
    return (
      <div className="space-y-4">
        <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="text-sm text-gray-400 mb-2">
            Function: <code className="text-cyan-300">{step.function_name}</code>
          </div>
          {step.signature && (
            <pre className="p-3 bg-black/40 rounded-lg font-mono text-sm text-green-400 overflow-x-auto">{step.signature}</pre>
          )}
          {step.description && <p className="text-sm text-gray-300 mt-3">{step.description}</p>}
        </div>
        {step.test_cases && (
          <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
            <div className="text-sm font-medium text-gray-400 mb-3">Test Cases</div>
            <div className="space-y-2">
              {step.test_cases.slice(0, 4).map((tc, i) => (
                <div key={i} className="p-3 bg-black/30 rounded-lg font-mono text-xs">
                  <div className="text-green-400">Input: {JSON.stringify(tc.input)}</div>
                  <div className="text-cyan-300">Expected: {JSON.stringify(tc.expected)}</div>
                </div>
              ))}
              {step.hidden_tests ? <div className="text-xs text-gray-500">+ {step.hidden_tests} hidden tests</div> : null}
            </div>
          </div>
        )}
        {!completed && (
          <textarea value={code} onChange={e => setCode(e.target.value)}
            placeholder="Write your solution here..."
            className="w-full h-40 bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-sm text-green-400 placeholder-gray-600 resize-none focus:outline-none focus:border-purple-500/50" />
        )}
        {!completed && (
          <button onClick={() => onAnswer(stepIndex, code, code.length > 20 ? 85 : 50)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 rounded-xl font-medium text-sm">
            Submit Solution
          </button>
        )}
        {completed && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> Completed — Score: {stepScores[stepIndex]}%
          </div>
        )}
      </div>
    );
  }

  if (step.type === 'debug') {
    return (
      <div className="space-y-4">
        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
          <div className="text-sm text-red-400 font-medium mb-2">Buggy Code</div>
          <pre className="p-3 bg-black/40 rounded-lg font-mono text-sm text-red-300 overflow-x-auto">{step.buggy_code}</pre>
          {step.failing_input && (
            <div className="mt-2 text-xs text-gray-400">Fails on: {JSON.stringify(step.failing_input)}</div>
          )}
        </div>
        <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="text-sm font-medium mb-2">{step.question}</div>
          <textarea value={code} onChange={e => setCode(e.target.value)} placeholder="Describe the bug and provide the fix..."
            className="w-full h-24 bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-sm text-green-400 placeholder-gray-600 resize-none focus:outline-none focus:border-purple-500/50" />
        </div>
        {!completed && (
          <button onClick={() => onAnswer(stepIndex, code, code.length > 10 ? 85 : 40)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 rounded-xl font-medium text-sm">
            Submit Fix
          </button>
        )}
        {completed && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> Debugged — Score: {stepScores[stepIndex]}%
          </div>
        )}
      </div>
    );
  }

  if (step.type === 'break') {
    return (
      <div className="space-y-4">
        <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="text-sm font-medium text-amber-400 mb-2">Break It</div>
          {step.content && <p className="text-gray-300 text-sm">{step.content}</p>}
        </div>
        <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="text-sm font-medium mb-2">{step.question}</div>
          <textarea value={code} onChange={e => setCode(e.target.value)} placeholder="Your answer..."
            className="w-full h-24 bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-sm text-green-400 placeholder-gray-600 resize-none focus:outline-none focus:border-purple-500/50" />
        </div>
        {!completed && (
          <button onClick={() => onAnswer(stepIndex, code, code.length > 5 ? 85 : 40)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 rounded-xl font-medium text-sm">
            Submit
          </button>
        )}
      </div>
    );
  }

  if (step.type === 'assessment') {
    return (
      <div className="space-y-4">
        <div className="p-6 bg-gradient-to-br from-purple-500/10 to-cyan-500/10 border border-purple-500/20 rounded-2xl text-center">
          <div className="text-3xl mb-3">⚔️</div>
          <h3 className="text-xl font-bold mb-2">{step.title}</h3>
          {step.timed && <div className="text-amber-400 text-sm mb-2">⏱ {step.time_limit_minutes} minutes</div>}
          {step.description && <p className="text-gray-300 text-sm">{step.description}</p>}
        </div>
        {step.test_cases && (
          <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
            <div className="text-sm font-medium text-gray-400 mb-3">Test Cases</div>
            <div className="space-y-2">
              {step.test_cases.slice(0, 3).map((tc, i) => (
                <div key={i} className="p-3 bg-black/30 rounded-lg font-mono text-xs">
                  <div className="text-green-400">Input: {JSON.stringify(tc.input)}</div>
                  <div className="text-cyan-300">Expected: {JSON.stringify(tc.expected)}</div>
                </div>
              ))}
              {step.hidden_tests ? <div className="text-xs text-gray-500">+ {step.hidden_tests} hidden tests</div> : null}
            </div>
          </div>
        )}
        {!completed && (
          <textarea value={code} onChange={e => setCode(e.target.value)} placeholder="Write your solution..."
            className="w-full h-48 bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-sm text-green-400 placeholder-gray-600 resize-none focus:outline-none focus:border-purple-500/50" />
        )}
        {!completed && (
          <button onClick={() => onAnswer(stepIndex, code, code.length > 20 ? 80 : 30)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 rounded-xl font-medium text-sm">
            Submit Assessment
          </button>
        )}
        {completed && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-300 text-sm flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> Assessment Complete — Score: {stepScores[stepIndex]}%
          </div>
        )}
      </div>
    );
  }

  if (step.type === 'reflection') {
    return (
      <div className="space-y-4">
        <div className="p-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="text-sm font-medium text-purple-400 mb-2">Reflect</div>
          {step.content && <p className="text-gray-300 text-sm">{step.content}</p>}
        </div>
        <textarea value={code} onChange={e => setCode(e.target.value)} placeholder="What did you learn? What was hard?"
          className="w-full h-32 bg-black/40 border border-white/10 rounded-xl p-4 text-sm text-green-400 placeholder-gray-600 resize-none focus:outline-none focus:border-purple-500/50" />
        {!completed && (
          <button onClick={() => onAnswer(stepIndex, code, code.length > 5 ? 90 : 50)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-400 hover:to-cyan-400 rounded-xl font-medium text-sm">
            Complete Reflection
          </button>
        )}
      </div>
    );
  }

  return <div className="p-4 bg-white/5 border border-white/10 rounded-xl text-gray-400">Step type: {step.type}</div>;
}
