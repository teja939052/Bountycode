import { useState, useCallback } from "react";
import { ChevronLeft, ArrowRight, CheckCircle, Play, Target, Zap } from "lucide-react";
import { Card, Button, SectionHeader } from "../../design-system";
import { PageShell } from "../../design-system/PageShell";

export interface MissionStep {
  id: string;
  title: string;
  description: string;
  render: () => JSX.Element;
}

export interface MissionEvidence {
  skillId: string;
  stages: { stageId: string }[];
  finalPassed: boolean;
  timeSpentSeconds: number;
}

export interface FlagshipMissionProps {
  captainMessage: string;
  captainMood: string;
  xpReward: number;
  backTo: string;
  steps: MissionStep[];
  evidence: MissionEvidence;
}

const MOOD_LABEL: Record<string, string> = {
  briefing: "Briefing",
  encouraging: "Encouraging",
  curious: "Curious",
  challenging: "Challenge",
  serious: "Serious",
};

export default function FlagshipMissionShell({
  captainMessage,
  captainMood,
  xpReward,
  backTo,
  steps,
  evidence,
}: FlagshipMissionProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [completed, setCompleted] = useState<Set<string>>(new Set());
  const [finished, setFinished] = useState(false);

  const current = steps[activeIndex];
  const isLast = activeIndex >= steps.length - 1;
  const allDone = completed.size >= steps.length;

  const markDone = useCallback(() => {
    if (current && !completed.has(current.id)) {
      setCompleted((prev) => new Set([...prev, current.id]));
    }
  }, [current, completed]);

  const nextStep = useCallback(() => {
    if (current) markDone();
    if (activeIndex < steps.length - 1) {
      setActiveIndex((i) => i + 1);
    } else {
      setFinished(true);
    }
  }, [activeIndex, steps.length, current, markDone]);

  const progress = steps.length ? Math.round((completed.size / steps.length) * 100) : 0;

  return (
    <PageShell theme="adventure" className="max-w-4xl mx-auto">
      <div className="mb-6 flex items-center justify-between gap-4">
        <Button variant="ghost" size="sm" onClick={() => (window.location.href = backTo)}>
          <ChevronLeft className="w-4 h-4 mr-2" /> Back to placement
        </Button>
        <div className="flex items-center gap-3 text-sm font-medium text-text-muted">
          <Target className="w-4 h-4" />
          <span>Mission {activeIndex + 1} of {steps.length}</span>
        </div>
      </div>

      <Card pad="md" className="mb-6">
        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
              <Play className="w-5 h-5 text-primary" />
            </div>
            <div>
              <div className="font-semibold text-text">{captainMessage}</div>
              <div className="text-xs text-text-muted uppercase tracking-wider">
                {MOOD_LABEL[captainMood] || captainMood}
              </div>
            </div>
          </div>
          <div className="ml-auto flex items-center gap-2 text-sm">
            <Zap className="w-4 h-4 text-amber-500" />
            <span className="font-bold text-text">+{xpReward} XP</span>
          </div>
        </div>
      </Card>

      <Card pad="md">
        <SectionHeader
          eyebrow="Current step"
          title={current?.title || "Mission complete"}
          description={current?.description || ""}
        />

        {finished ? (
          <div className="py-8 text-center">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
            <h3 className="font-bold text-text mb-2">Mission complete</h3>
            <p className="text-text-muted mb-6">
              You traced, predicted, built, broke, fixed, recalled, and transferred.
            </p>
            <Button variant="gold" onClick={() => (window.location.href = backTo)}>
              Return to placement
            </Button>
          </div>
        ) : (
          <>
            {current && current.render && current.render()}
            <div className="mt-6 flex items-center justify-between">
              <div className="w-1/3">
                <div className="w-full bg-border rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs text-text-muted mt-1">
                  <span>{completed.size} / {steps.length}</span>
                  <span>{progress}%</span>
                </div>
              </div>
              <div className="w-2/3 flex gap-3">
                {!isLast && (
                  <Button variant="primary" onClick={nextStep} disabled={!completed.has(current.id)}>
                    Mark complete &rarr;
                  </Button>
                )}
                {isLast && (
                  <Button variant="gold" onClick={nextStep} disabled={!completed.has(current.id)}>
                    Prove it &rarr;
                  </Button>
                )}
              </div>
            </div>
          </>
        )}
      </Card>
    </PageShell>
  );
}
