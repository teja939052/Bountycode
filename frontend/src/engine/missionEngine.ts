import type {
  Mission,
  MissionState,
  MissionStep,
  MissionStepType,
  StepResult,
  StepConfig,
  CodeResult,
  DebugResult,
  LearnerProfile,
  MissionState as MissionStateType,
} from "./missionTypes";
import { NovaGuide } from "./novaGuide";

export class MissionEngine {
  private mission: Mission;
  private state: MissionState;
  private guide: NovaGuide;
  private onStateChange: (state: MissionState) => void;
  private startTime: number;
  private stepStartTime: number;

  constructor(
    mission: Mission,
    learnerProfile: any,
    onStateChange: (state: MissionState) => void
  ) {
    this.mission = mission;
    this.state = this.createInitialState();
    this.guide = new NovaGuide(learnerProfile, this.state);
    this.onStateChange = onStateChange;
    this.startTime = Date.now();
    this.stepStartTime = Date.now();
  }

  private async init(learnerProfile: any) {
    const { NovaGuide } = await import("./novaGuide");
    this.guide = new NovaGuide(
      learnerProfile,
      this.state
    );
  }

  private createInitialState(): MissionState {
    return {
      missionId: this.mission.id,
      currentStepIndex: 0,
      completedSteps: new Set(),
      stepResults: {},
      hintsUsed: 0,
      predictionsCorrect: 0,
      predictionsTotal: 0,
      codeExecutions: 0,
      hintsRevealed: 0,
      timeSpentSeconds: 0,
      masteryScore: 0,
      isComplete: false,
      currentStepType: this.mission.steps[0]?.type,
    };
  }

  getState(): MissionState {
    return { ...this.state };
  }

  getCurrentStep(): MissionStep | null {
    return this.mission.steps[this.state.currentStepIndex] || null;
  }

  getGuideDialogue(): any[] {
    const step = this.getCurrentStep();
    if (!step) return [];
    return this.guide.getDialogue(step.type, this.state.currentStepIndex, {
      step: this.getCurrentStep(),
      state: this.state,
    });
  }

  getGuideMood(): string {
    return this.guide.getMood();
  }

  async submitPrediction(answer: string): Promise<{ correct: boolean; explanation: string }> {
    const step = this.getCurrentStep();
    if (!step || step.type !== "predict") {
      throw new Error("Not a predict step");
    }

    const config = step.config as any;
    const correct = answer === config.correctAnswer;
    this.state.predictionsTotal++;
    if (correct) this.state.predictionsCorrect++;

    const timeSpent = Math.floor((Date.now() - this.stepStartTime) / 1000);
    this.recordStepResult({
      stepIndex: this.state.currentStepIndex,
      type: "predict",
      completed: true,
      score: correct ? 100 : 0,
      timeSpent,
      hintsUsed: this.state.hintsUsed,
      predictionCorrect: correct,
    });

    return { correct, explanation: config.explanation || "" };
  }

  async runCode(code: string, language: string = "python"): Promise<CodeResult> {
    this.state.codeExecutions++;
    const step = this.getCurrentStep();
    if (!step || step.type !== "build" && step.type !== "debug") {
      throw new Error("Not a code execution step");
    }

    // This would call the compiler API
    // For now, return a mock result
    const result: CodeResult = {
      passed: false,
      output: "",
      expected: "",
    };

    const config = step.config as any;
    if (config.testCases) {
      // In real implementation, call compiler API
      // For now, simulate
      result.passed = true;
      result.output = "Test output";
      result.expected = "Expected output";
    }

    const timeSpent = Math.floor((Date.now() - this.stepStartTime) / 1000);
    this.recordStepResult({
      stepIndex: this.state.currentStepIndex,
      type: step.type,
      completed: result.passed,
      score: result.passed ? 100 : 50,
      timeSpent,
      hintsUsed: this.state.hintsUsed,
      codeResult: result,
    });

    this.stepStartTime = Date.now();
    return result;
  }

  async submitDebugFix(code: string): Promise<DebugResult> {
    this.state.codeExecutions++;
    const timeSpent = Math.floor((Date.now() - this.stepStartTime) / 1000);

    // In real implementation, run the fixed code against test cases
    const result: DebugResult = {
      fixed: true,
      timeToFix: timeSpent,
      attempts: this.state.codeExecutions,
    };

    this.recordStepResult({
      stepIndex: this.state.currentStepIndex,
      type: "debug",
      completed: result.fixed,
      score: result.fixed ? 100 : 50,
      timeSpent,
      hintsUsed: this.state.hintsUsed,
      debugResult: result,
    });

    this.stepStartTime = Date.now();
    return result;
  }

  requestHint(): string {
    this.state.hintsRevealed++;
    this.state.hintsUsed++;
    const step = this.getCurrentStep();
    const config = step?.config as any;
    return config.hint || "Read the error carefully. What did the code actually do vs what you expected?";
  }

  nextStep(): boolean {
    if (this.state.currentStepIndex >= this.mission.steps.length - 1) {
      return this.completeMission();
    }

    this.state.currentStepIndex++;
    this.state.currentStepType = this.mission.steps[this.state.currentStepIndex]?.type;
    this.stepStartTime = Date.now();
    this.notifyStateChange();
    return true;
  }

  previousStep(): boolean {
    if (this.state.currentStepIndex > 0) {
      this.state.currentStepIndex--;
      this.state.currentStepType = this.mission.steps[this.state.currentStepIndex]?.type;
      this.stepStartTime = Date.now();
      this.notifyStateChange();
      return true;
    }
    return false;
  }

  private completeMission(): boolean {
    this.state.isComplete = true;
    this.calculateMastery();
    this.notifyStateChange();
    return true;
  }

  private calculateMastery() {
    const results = Object.values(this.state.stepResults);
    if (results.length === 0) {
      this.state.masteryScore = 0;
      return;
    }

    let totalScore = 0;
    let totalWeight = 0;

    results.forEach(result => {
      let weight = 1;
      if (result.type === "prove") weight = 3;
      else if (result.type === "build" || result.type === "debug") weight = 2;
      else if (result.type === "predict") weight = 1.5;

      totalScore += result.score * weight;
      totalWeight += weight;
    });

    this.state.masteryScore = Math.round(totalScore / totalWeight);
  }

  getMasteryScore(): number {
    return this.state.masteryScore;
  }

  isMastered(): boolean {
    return this.state.masteryScore >= this.mission.masteryThreshold;
  }

  getReinforcementMission(): any | null {
    if (this.isMastered()) return null;

    // Find the weakest skill
    const weakSkills = this.identifyWeakSkills();
    if (weakSkills.length === 0) return null;

    const targetSkill = weakSkills[0];
    const reinforcement = this.mission.reinforcementMissions.find(
      m => m.targetSkill === targetSkill
    );

    return reinforcement || null;
  }

  private identifyWeakSkills(): string[] {
    const skillScores: Record<string, { total: number; count: number }> = {};

    Object.values(this.state.stepResults).forEach(result => {
      const step = this.mission.steps[result.stepIndex];
      if (!step) return;

      step.skillsTaught?.forEach(skill => {
        if (!skillScores[skill]) {
          skillScores[skill] = { total: 0, count: 0 };
        }
        skillScores[skill].total += result.score;
        skillScores[skill].count++;
      });
    });

    return Object.entries(skillScores)
      .filter(([_, v]) => v.count > 0 && v.total / v.count < 70)
      .sort((a, b) => (a[1].total / a[1].count) - (b[1].total / b[1].count))
      .map(([skill]) => skill);
  }

  getProgress(): number {
    return Math.round((this.state.currentStepIndex / this.mission.steps.length) * 100);
  }

  getTimeSpent(): number {
    return Math.floor((Date.now() - this.startTime) / 1000);
  }

  private recordStepResult(result: StepResult) {
    this.state.stepResults[result.stepIndex] = result;
    this.state.completedSteps.add(result.stepIndex);
    this.notifyStateChange();
  }

  private notifyStateChange() {
    this.onStateChange({ ...this.state });
  }
}

export function createMissionEngine(
  mission: any,
  learnerProfile: any,
  onStateChange: (state: any) => void
): MissionEngine {
  return new MissionEngine(mission, learnerProfile, onStateChange);
}