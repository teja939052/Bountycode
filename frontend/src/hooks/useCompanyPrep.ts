import { useQuery, useMutation } from "@tanstack/react-query";
import api from "../services/api";

const COMPANIES_KEY = ["company-prep", "companies"] as const;

export function companyGuideKey(companyId: string) {
  return ["company-prep", "guide", companyId] as const;
}

export function companyBehavioralKey(company: string, role: string) {
  return ["company-prep", "behavioral", company, role] as const;
}

export function companyQuestionsKey(companyId: string) {
  return ["company-prep", "questions", companyId] as const;
}

export function companyQuestionListKey(companyId: string, category: string) {
  return ["company-prep", "question-list", companyId, category] as const;
}

export function useCompanyPrep() {
  const companies = useQuery<{ companies: Array<{ id: string; name: string; focus_areas?: string[]; interview_rounds?: string[] }> }>({
    queryKey: COMPANIES_KEY,
    queryFn: () => api.getCompanies(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });

  const useGuide = (companyId: string | null) =>
    useQuery({
      queryKey: companyGuideKey(companyId || ""),
      queryFn: () => api.getCompanyGuide(companyId),
      enabled: Boolean(companyId),
      retry: 1,
      staleTime: 120_000,
      refetchOnWindowFocus: false,
    });

  const useBehavioral = (company: string | null, role: string) =>
    useQuery({
      queryKey: companyBehavioralKey(company || "", role),
      queryFn: () => api.getBehavioralQuestion(company, role),
      enabled: Boolean(company),
      retry: 1,
      staleTime: 60_000,
      refetchOnWindowFocus: false,
    });

  const useQuestions = (companyId: string | null) =>
    useQuery({
      queryKey: companyQuestionsKey(companyId || ""),
      queryFn: () => api.getCompanyQuestions(companyId),
      enabled: Boolean(companyId),
      retry: 1,
      staleTime: 120_000,
      refetchOnWindowFocus: false,
    });

  const useQuestionList = (companyId: string | null, category: string | null) =>
    useQuery({
      queryKey: companyQuestionListKey(companyId || "", category || ""),
      queryFn: () => api.getCompanyQuestionList(companyId, category, 1, 50),
      enabled: Boolean(companyId && category),
      retry: 1,
      staleTime: 120_000,
      refetchOnWindowFocus: false,
    });

  const practiceMutation = useMutation({
    mutationFn: (payload: { company: string; role: string }) =>
      api.createPracticeSession(payload),
  });

  const isLoading = companies.isLoading;

  const refetch = async () => {
    await companies.refetch();
  };

  return {
    companies: companies.data?.companies ?? [],
    isLoading,
    isError: companies.isError,
    useGuide,
    useBehavioral,
    useQuestions,
    useQuestionList,
    practiceMutation,
    refetch,
  };
}
