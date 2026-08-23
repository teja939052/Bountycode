import type {
  MissionState,
  NovaMood,
  NovaDialogue,
  GuideState,
  LearnerProfile,
  MissionStepType,
} from "./missionTypes";

export class NovaGuide {
  private state: GuideState;
  private learnerProfile: LearnerProfile;
  private missionState: MissionState;

  constructor(learnerProfile: LearnerProfile, missionState: MissionState) {
    this.learnerProfile = learnerProfile;
    this.missionState = missionState;
    this.state = {
      currentMood: "encouraging",
      dialogueHistory: [],
      hintsGiven: 0,
      encouragementLevel: 3,
      lastIntervention: Date.now(),
    };
  }

  updateMissionState(missionState: MissionState) {
    this.missionState = missionState;
  }

  updateLearnerProfile(profile: LearnerProfile) {
    this.learnerProfile = profile;
  }

  getMood(): NovaMood {
    return this.state.currentMood;
  }

  getMoodEmoji(): string {
    const emojis: Record<NovaMood, string> = {
      encouraging: "🌱",
      curious: "🔍",
      challenging: "⚔️",
      proud: "🏆",
      patient: "🌿",
      serious: "🎯",
    };
    return emojis[this.state.currentMood] || "🌱";
  }

  shouldIntervene(stepType: MissionStepType): boolean {
    const { hintsGiven, encouragementLevel } = this.state;
    const { hintsRevealed, predictionsCorrect, predictionsTotal } = this.missionState;

    if (stepType === "build" && this.missionState.codeExecutions > 3) {
      return true;
    }
    if (stepType === "debug" && this.missionState.stepResults[this.missionState.currentStepIndex]?.debugResult?.attempts > 2) {
      return true;
    }
    if (stepType === "predict" && predictionsTotal > 0 && predictionsCorrect / predictionsTotal < 0.5) {
      return true;
    }
    if (hintsGiven >= 2 && this.missionState.hintsRevealed === hintsGiven) {
      return false;
    }
    return hintsGiven < 2;
  }

  getDialogue(stepType: MissionStepType, stepIndex: number, context?: any): NovaDialogue[] {
    const dialogues = this.generateDialogue(stepType, stepIndex, context);
    this.state.dialogueHistory.push(...dialogues.map(d => d.text));
    this.state.hintsGiven += dialogues.filter(d => d.mood === "patient").length;
    this.state.lastIntervention = Date.now();
    return dialogues;
  }

  private generateDialogue(stepType: MissionStepType, stepIndex: number, context?: any): NovaDialogue[] {
    const { masteryScore, hintsRevealed, predictionsCorrect, predictionsTotal, codeExecutions } = this.missionState;
    const { missionsCompleted, predictionAccuracy, averageHintsPerMission } = this.learnerProfile;

    const isFirstMission = missionsCompleted === 0;
    const isEarlyStep = stepIndex <= 1;
    const struggling = codeExecutions > 3 || (predictionsTotal > 0 && predictionsCorrect / predictionsTotal < 0.4);

    switch (stepType) {
      case "story":
        return this.getStoryDialogue(isFirstMission, isEarlyStep, context);

      case "discover":
        return this.getDiscoverDialogue(isEarlyStep, context);

      case "predict":
        return this.getPredictDialogue(predictionsCorrect, predictionsTotal, context);

      case "build":
        return this.getBuildDialogue(codeExecutions, masteryScore, context);

      case "break":
        return this.getBreakDialogue(context);

      case "debug":
        return this.getDebugDialogue(codeExecutions, context);

      case "prove":
        return this.getProveDialogue(masteryScore, context);

      case "reward":
        return this.getRewardDialogue(masteryScore, context);

      default:
        return [{ id: "default", text: "Let's continue.", mood: "encouraging" }];
    }
  }

  private getStoryDialogue(isFirstMission: boolean, isEarlyStep: boolean, context?: any): NovaDialogue[] {
    if (isFirstMission && isEarlyStep) {
      return [
        {
          id: "story-welcome",
          text: "Welcome to BountyCode. I'm Nova — your guide through these missions. You don't take courses here. You go on missions.",
          mood: "encouraging",
        },
        {
          id: "story-first-mission",
          text: "Your first mission is waiting. The bounty board is broken — every player's score is being reset to zero. Let's fix it.",
          mood: "curious",
        },
      ];
    }
    return [
      {
        id: "story-continue",
        text: "The story continues. Your next mission awaits.",
        mood: "encouraging",
      },
    ];
  }

  private getDiscoverDialogue(isEarlyStep: boolean, context?: any): NovaDialogue[] {
    if (isEarlyStep) {
      return [
        {
          id: "discover-welcome",
          text: "Let's explore. Run the code. See what breaks. That's how you learn.",
          mood: "curious",
        },
      ];
    }
    return [
      {
        id: "discover-continue",
        text: "Keep exploring. Change values. See what happens.",
        mood: "patient",
      },
    ];
  }

  private getPredictDialogue(predictionsCorrect: number, predictionsTotal: number, context?: any): NovaDialogue[] {
    if (predictionsTotal === 0) {
      return [
        {
          id: "predict-first",
          text: "Before you run it, predict what will happen. This trains your mental model — the most important skill a developer has.",
          mood: "challenging",
        },
      ];
    }
    const accuracy = predictionsCorrect / predictionsTotal;
    if (accuracy < 0.4) {
      return [
        {
          id: "predict-struggling",
          text: "You're struggling to predict outcomes. That's okay — this is exactly what we're training. Slow down. Read the code line by line.",
          mood: "patient",
        },
      ];
    }
    if (accuracy > 0.8) {
      return [
        {
          id: "predict-strong",
          text: "Your mental model is sharp. Keep trusting it.",
          mood: "proud",
        },
      ];
    }
    return [
      {
        id: "predict-continue",
        text: "Good. Now predict the next one.",
        mood: "curious",
      },
    ];
  }

  private getBuildDialogue(codeExecutions: number, masteryScore: number, context?: any): NovaDialogue[] {
    if (codeExecutions === 0) {
      return [
        {
          id: "build-start",
          text: "Now you build. Write the code. The tests will tell you if it works.",
          mood: "challenging",
        },
      ];
    }
    if (codeExecutions > 3) {
      return [
        {
          id: "build-struggling",
          text: "You've run the code a few times. Remember: read the error. Read the test case. Think before you type.",
          mood: "patient",
        },
      ];
    }
    if (masteryScore > 80) {
      return [
        {
          id: "build-strong",
          text: "Clean code. Solid thinking.",
          mood: "proud",
        },
      ];
    }
    return [
      {
        id: "build-continue",
        text: "Keep iterating. The tests are your compass.",
        mood: "encouraging",
      },
    ];
  }

  private getBreakDialogue(context?: any): NovaDialogue[] {
    return [
      {
        id: "break-intro",
        text: "Now break it on purpose. Find the edge cases. That's how you make code bulletproof.",
        mood: "challenging",
      },
    ];
  }

  private getDebugDialogue(codeExecutions: number, context?: any): NovaDialogue[] {
    if (codeExecutions <= 1) {
      return [
        {
          id: "debug-start",
          text: "Here's broken code. The test fails. Your job: find the bug and fix it. This is where real developers earn their keep.",
          mood: "serious",
        },
      ];
    }
    if (codeExecutions > 2) {
      return [
        {
          id: "debug-stuck",
          text: "Stuck? Read the error message. Trace the logic. What did the code *actually* do vs what you *expected* it to do?",
          mood: "patient",
        },
      ];
    }
    return [
      {
        id: "debug-continue",
        text: "Close. Trace one more line.",
        mood: "curious",
      },
    ];
  }

  private getProveDialogue(masteryScore: number, context?: any): NovaDialogue[] {
    return [
      {
        id: "prove-boss",
        text: "No hints. No scaffolding. Just you and the requirements. This is the boss bounty. Prove you've mastered this.",
        mood: "serious",
      },
    ];
  }

  private getRewardDialogue(masteryScore: number, context?: any): NovaDialogue[] {
    if (masteryScore >= 90) {
      return [
        {
          id: "reward-mastery",
          text: "Mastery achieved. You didn't just complete the mission — you owned it. The next mission is unlocked.",
          mood: "proud",
        },
      ];
    }
    if (masteryScore >= 70) {
      return [
        {
          id: "reward-pass",
          text: "Mission complete. You've proven the basics. But there are gaps — I'll give you a side quest to close them before the next mission.",
          mood: "encouraging",
        },
      ];
    }
    return [
      {
        id: "reward-retry",
        text: "Not quite there yet. Let's run a reinforcement mission first. You'll be ready.",
        mood: "patient",
      },
    ];
  }

  getGuidanceForMastery(masteryScore: number): string {
    if (masteryScore >= 90) return "You've mastered this. Moving on.";
    if (masteryScore >= 70) return "Good foundation. One side quest to close the gaps.";
    return "Let's reinforce this skill before moving forward.";
  }

  getNextMissionRecommendation(): string {
    if (this.learnerProfile.missionsCompleted === 0) {
      return "Your first mission: The First Command. Learn to make the computer do exactly what you tell it.";
    }
    if (this.learnerProfile.predictionAccuracy < 0.5) {
      return "You're coding fine, but predicting outcomes needs work. Next mission focuses on mental models.";
    }
    if (this.learnerProfile.averageHintsPerMission > 2) {
      return "You're relying on hints. Next mission: fewer hints, more independence.";
    }
    return "Ready for the next challenge.";
  }
}

export function createNovaGuide(learnerProfile: LearnerProfile, missionState: MissionState): NovaGuide {
  return new NovaGuide(learnerProfile, missionState);
}