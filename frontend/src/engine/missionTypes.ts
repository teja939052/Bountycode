export type MissionStepType =
  | "story"
  | "discover"
  | "predict"
  | "build"
  | "break"
  | "debug"
  | "prove"
  | "reward";

export type NovaMood =
  | "encouraging"
  | "curious"
  | "challenging"
  | "proud"
  | "patient"
  | "serious";

export interface NovaDialogue {
  id: string;
  text: string;
  mood: NovaMood;
  condition?: (state: MissionState) => boolean;
}

export interface MissionStep {
  id: string;
  type: MissionStepType;
  title: string;
  content: string;
  novaDialogue?: NovaDialogue[];
  config: StepConfig;
  xp: number;
  required?: string[];
}

export interface StepConfig {
  // Discover
  codeSnippet?: string;
  expectedOutput?: string;
  interactive?: boolean;

  // Predict
  question?: string;
  options?: PredictOption[];
  correctAnswer?: string;
  explanation?: string;

  // Build
  functionName?: string;
  signature?: string;
  description?: string;
  testCases?: TestCase[];
  hiddenTests?: number;
  starterCode?: string;

  // Break
  inputsToTry?: string[];
  question?: string;
  correctSet?: string[];
  explanation?: string;

  // Debug
  buggyCode?: string;
  failingInput?: any;
  error?: string;
  hint?: string;

  // Prove
  timed?: boolean;
  timeLimitMinutes?: number;
  masteryThreshold?: number;
}

export interface PredictOption {
  id: string;
  text: string;
  correct: boolean;
}

export interface TestCase {
  input: any[];
  expected: any;
}

export interface Mission {
  id: string;
  worldId: string;
  worldTitle: string;
  worldIcon: string;
  order: number;
  title: string;
  description: string;
  scenario: string;
  goal: string;
  skillsTaught: string[];
  prerequisites: string[];
  steps: MissionStep[];
  bossStep: MissionStep;
  reinforcementMissions: ReinforcementMission[];
  masteryThreshold: number;
  masteryXp: number;
  nextMissionId?: string;
}

export interface ReinforcementMission {
  id: string;
  title: string;
  description: string;
  targetSkill: string;
  steps: MissionStep[];
  xp: number;
}

export interface MissionState {
  missionId: string;
  currentStepIndex: number;
  completedSteps: Set<number>;
  stepResults: Record<number, StepResult>;
  hintsUsed: number;
  predictionsCorrect: number;
  predictionsTotal: number;
  codeExecutions: number;
  hintsRevealed: number;
  timeSpentSeconds: number;
  masteryScore: number;
  isComplete: boolean;
  currentStepType?: MissionStepType;
}

export interface StepResult {
  stepIndex: number;
  type: MissionStepType;
  completed: boolean;
  score: number;
  timeSpent: number;
  hintsUsed: number;
  predictionCorrect?: boolean;
  codeResult?: CodeResult;
  debugResult?: DebugResult;
}

export interface CodeResult {
  passed: boolean;
  output: string;
  expected: string;
  stderr?: string;
}

export interface DebugResult {
  fixed: boolean;
  timeToFix: number;
  attempts: number;
}

export interface World {
  id: string;
  title: string;
  icon: string;
  description: string;
  order: number;
  missions: Mission[];
  prerequisites: string[];
}

export interface GuideState {
  currentMood: NovaMood;
  dialogueHistory: string[];
  hintsGiven: number;
  encouragementLevel: number;
  lastIntervention: number;
}

export interface LearnerProfile {
  masteryBySkill: Record<string, number>;
  predictionAccuracy: number;
  hintsPerMission: number;
  averageHintsPerMission: number;
  debuggingSpeed: number;
  missionsCompleted: number;
  currentMissionId?: string;
  currentWorldId?: string;
  totalXp: number;
  level: number;
}