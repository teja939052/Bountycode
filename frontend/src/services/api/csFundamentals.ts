// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export interface CsTheoryTopic {
  id: string;
  title: string;
  domain: string;
  definition: string;
  key_facts: string[];
  worked_example: { problem: string; solution: string };
  interview_ask: string;
  triggers: string[];
  practice_hint: string;
}

const DOMAIN_LABEL: Record<string, string> = {
  os: "Operating Systems",
  dbms: "DBMS",
  oop: "OOP",
  cn: "Computer Networks",
  sql: "SQL",
};

export const csFundamentalsApi = {
  domainLabel(domain: string): string {
    return DOMAIN_LABEL[domain] ?? domain;
  },

  index(): Promise<{
    domains: string[];
    topics: { id: string; title: string; domain: string }[];
    by_domain: Record<string, { id: string; title: string; domain: string }[]>;
    total: number;
  }> {
    return request("/api/v1/cs-fundamentals/theory");
  },

  detail(topicId: string): Promise<CsTheoryTopic> {
    return request(`/api/v1/cs-fundamentals/theory/${encodeURIComponent(topicId)}`);
  },

  forDomain(domain: string): Promise<{ domain: string; topics: CsTheoryTopic[]; total: number }> {
    return request(`/api/v1/cs-fundamentals/domain/${encodeURIComponent(domain)}`);
  },
};
