import { requestWithRetry as request } from "./request.ts";
import type { ATSScoreResponse, ResumeAnalysis } from "./types.ts";

export const enhancedApi = {
  improveBullet(bullet: string, jobRole = ""): Promise<{ improved: string }> {
    return request("/api/v1/enhanced/resume/improve-bullet", {
      method: "POST",
      body: JSON.stringify({ bullet, job_role: jobRole }),
    });
  },

  improveBullets(
    bullets: string[],
    jobRole = "",
  ): Promise<{ improved: string[] }> {
    return request("/api/v1/enhanced/resume/improve-bullets", {
      method: "POST",
      body: JSON.stringify({ bullets, job_role: jobRole }),
    });
  },

  getATSChecklist(resumeText: string): Promise<ResumeAnalysis> {
    return request("/api/v1/enhanced/resume/ats-checklist", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  },

  tailorResume(
    resumeText: string,
    jobDescription: string,
    jobRole = "",
  ): Promise<ResumeAnalysis> {
    return request("/api/v1/enhanced/resume/tailor", {
      method: "POST",
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
        job_role: jobRole,
      }),
    });
  },

  getCompanyChallenge(
    company: string,
    role = "SDE",
    difficulty: string | null = null,
  ): Promise<Record<string, unknown>> {
    return request("/api/v1/enhanced/coding/company-challenge", {
      method: "POST",
      body: JSON.stringify({ company, role, difficulty }),
    });
  },

  getCodeReviewerFeedback(
    code: string,
    language: string,
    problemDescription: string,
  ): Promise<{ review: string; score?: number; suggestions?: string[] }> {
    return request("/api/v1/enhanced/coding/interviewer-feedback", {
      method: "POST",
      body: JSON.stringify({
        code,
        language,
        problem_description: problemDescription,
      }),
    });
  },

  explainConcept(
    concept: string,
    level = "intermediate",
  ): Promise<{ explanation: string }> {
    return request("/api/v1/enhanced/coding/explain", {
      method: "POST",
      body: JSON.stringify({ concept, level }),
    });
  },

  getHint(
    problemDescription: string,
    currentCode = "",
    hintLevel = 1,
  ): Promise<{ hint: string }> {
    return request("/api/v1/enhanced/coding/hint", {
      method: "POST",
      body: JSON.stringify({
        problem_description: problemDescription,
        current_code: currentCode,
        hint_level: hintLevel,
      }),
    });
  },

  evaluateSTAR(
    question: string,
    answer: string,
    company = "",
    leadershipPrinciples: string[] = [],
  ): Promise<{ score: number; feedback: string }> {
    return request("/api/v1/enhanced/behavioral/evaluate-star", {
      method: "POST",
      body: JSON.stringify({
        question,
        answer,
        company,
        leadership_principles: leadershipPrinciples,
      }),
    });
  },

  getSTARTemplate(
    question: string,
    company = "",
    role = "",
  ): Promise<{ template: string }> {
    return request("/api/v1/enhanced/behavioral/star-template", {
      method: "POST",
      body: JSON.stringify({ question, company, role }),
    });
  },

  getBehavioralQuestions(
    company: string,
    role: string,
    count = 5,
  ): Promise<{ questions: Array<{ question: string; category?: string }> }> {
    return request("/api/v1/enhanced/behavioral/practice-questions", {
      method: "POST",
      body: JSON.stringify({ company, role, count }),
    });
  },

  getSemanticATS(
    resumeText: string,
    jobDescription = "",
  ): Promise<ATSScoreResponse> {
    return request("/api/v1/enhanced/ats/semantic", {
      method: "POST",
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });
  },
};

export const freePracticeApi = {
  quickInterview(
    jobRole = "Software Engineer",
  ): Promise<Record<string, unknown>> {
    return request("/api/v1/free/quick-interview", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  },

  quickEvaluate(
    question: string,
    answer: string,
    jobRole = "Software Engineer",
  ): Promise<{ score: number; feedback: string }> {
    return request("/api/v1/free/quick-evaluate", {
      method: "POST",
      body: JSON.stringify({ question, answer, job_role: jobRole }),
    });
  },
};
