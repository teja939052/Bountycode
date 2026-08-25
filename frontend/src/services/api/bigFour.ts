import { requestWithRetry as request } from "./request.ts";

export interface Big4Firm {
  firm_id: string;
  name: string;
  tagline: string;
  values: string[];
  rounds: string[];
  prep_tips: string[];
}

export interface CaseMeta {
  case_id: string;
  firm_id: string;
  title: string;
}

export interface CaseDetail extends CaseMeta {
  context: string;
  task: string;
  framework: string[];
}

export interface CaseGrade {
  case_id: string;
  title: string;
  overall: number;
  max_overall?: number;
  dimensions: { name: string; score: number; note: string }[];
  feedback: string;
}

export interface SqlQuestion {
  id: string;
  topic: string;
  question: string;
  options: string[];
}

export const bigFourApi = {
  firms(): Promise<{ firms: Big4Firm[] }> {
    return request("/api/v1/big-four/firms");
  },

  cases(): Promise<{ cases: CaseMeta[] }> {
    return request("/api/v1/big-four/cases");
  },

  getCase(caseId: string): Promise<{ case: CaseDetail }> {
    return request(`/api/v1/big-four/cases/${caseId}`);
  },

  submitCase(caseId: string, response: string): Promise<CaseGrade> {
    return request(`/api/v1/big-four/cases/${caseId}/submit`, {
      method: "POST",
      body: JSON.stringify({ response }),
    });
  },

  sqlMeta(): Promise<{ total: number; topics: string[] }> {
    return request("/api/v1/big-four/sql/meta");
  },

  sqlQuestions(count = 8, topic = ""): Promise<{ questions: SqlQuestion[] }> {
    const params = new URLSearchParams({ count: String(count) });
    if (topic) params.set("topic", topic);
    return request(`/api/v1/big-four/sql/questions?${params.toString()}`);
  },

  sqlCheck(
    questionId: string,
    answer: string,
  ): Promise<{ correct: boolean; correct_answer: string; explanation: string }> {
    return request("/api/v1/big-four/sql/check", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer }),
    });
  },

  sqlComplete(correct: number, total: number): Promise<Record<string, unknown>> {
    return request("/api/v1/big-four/sql/complete", {
      method: "POST",
      body: JSON.stringify({ correct, total }),
    });
  },
};
