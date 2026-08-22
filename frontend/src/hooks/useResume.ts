import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export interface ResumeScore {
  overall_score: number;
  section_scores: Record<string, number>;
  recommendations: string[];
  ats_score: number;
  missing_keywords: string[];
}

export interface ResumeAnalysis {
  credit_score: number;
  card: string[];
  report: string[];
}

export interface ResumeUploadResult {
  resume_id: string;
  analysis: ResumeAnalysis;
  score: ResumeScore;
}

export interface AptitudeQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
}

export interface AptitudeTestResult {
  score: number;
  total_questions: number;
  correct: number;
  incorrect: number;
  by_section: Record<string, number>;
  feedback: string;
}

export function useResumeScore() {
  return useQuery<ResumeScore>({
    queryKey: ["resume", "score"],
    queryFn: () => api.resume.getScore(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useResumeAnalysis() {
  return useQuery<ResumeAnalysis>({
    queryKey: ["resume", "analysis"],
    queryFn: () => api.resume.getAnalysis(),
    retry: 1,
    staleTime: 300_000,
    refetchOnWindowFocus: false,
  });
}

export function useResumeUpload() {
  const queryClient = useQueryClient();

  return useMutation<ResumeUploadResult, Error, File>({
    mutationFn: (file) => api.resume.upload(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resume"] });
    },
  });
}

export function useResumeGenerate() {
  const queryClient = useQueryClient();

  return useMutation<ResumeUploadResult, Error, { resume_data: any }>({
    mutationFn: ({ resume_data }) => api.resume.generate(resume_data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resume"] });
    },
  });
}

export function useResumeOptimize() {
  const queryClient = useQueryClient();

  return useMutation<ResumeUploadResult, Error, { job_description: any }>({
    mutationFn: ({ job_description }) => api.resume.optimize(job_description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resume"] });
    },
  });
}

export function useResumeExport() {
  const queryClient = useQueryClient();

  return useMutation<Blob, Error, { format: "pdf" | "docx" }>({
    mutationFn: ({ format }) => api.resume.export(format),
    onSuccess: (blob) => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    },
  });
}

export function useAptitudeStart() {
  const queryClient = useQueryClient();

  return useMutation<{ test_id: string }, Error, { test_type: string }>({
    mutationFn: ({ test_type }) => api.aptitude.start(test_type),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}

export function useAptitudeSubmit() {
  const queryClient = useQueryClient();

  return useMutation<{
    correct: boolean;
    explanation: string;
  }, Error, { question_id: string; answer: string; time_taken?: number }>({
    mutationFn: ({ question_id, answer, time_taken }) =>
      api.aptitude.submit(question_id, answer, time_taken),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}

export function useAptitudeComplete() {
  const queryClient = useQueryClient();

  return useMutation<{ result: AptitudeTestResult }, Error, { test_id: string }>({
    mutationFn: ({ test_id }) => api.aptitude.complete(test_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["aptitude"] });
    },
  });
}