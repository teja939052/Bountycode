import { requestWithRetry as request } from "./request.ts";
import type {
  InterviewStartResponse,
  InterviewResult,
  InterviewHistoryItem,
  BookingDetail,
  BookingSlot,
} from "./types.ts";

export const interviewApi = {
  startInterview(jobRole: string): Promise<InterviewStartResponse> {
    return request("/api/v1/interview/start", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  },

  startInterviewV2(
    jobRole: string,
    company = "general",
    interviewType = "mixed",
    difficulty = "medium",
  ): Promise<InterviewStartResponse> {
    return request("/api/v1/interview/start", {
      method: "POST",
      body: JSON.stringify({
        job_role: jobRole,
        company,
        interview_type: interviewType,
        difficulty,
      }),
    });
  },

  submitAnswer(
    interviewId: string,
    question: string,
    answer: string,
  ): Promise<{
    question: string;
    score: number;
    feedback: string;
    is_follow_up?: boolean;
    next_question?: string;
    finished?: boolean;
  }> {
    return request("/api/v1/interview/answer", {
      method: "POST",
      body: JSON.stringify({ interview_id: interviewId, question, answer }),
    });
  },

  getInterviewResult(interviewId: string): Promise<InterviewResult> {
    return request(`/api/v1/interview/${interviewId}/result`);
  },

  getInterviewHistory(): Promise<InterviewHistoryItem[]> {
    return request("/api/v1/interview/history");
  },
};

export const mockInterviewApi = {
  startMockInterview(
    config: Record<string, unknown> = {},
  ): Promise<{ session_id: string; questions?: unknown[] }> {
    return request("/api/v1/mock-interview/start", {
      method: "POST",
      body: JSON.stringify(config),
    });
  },

  submitAnswer(
    sessionId: string,
    questionIndex: number,
    code: string,
    language: string,
  ): Promise<{
    passed?: boolean;
    score?: number;
    output?: string;
    error?: string;
  }> {
    return request(`/api/v1/mock-interview/${sessionId}/submit`, {
      method: "POST",
      body: JSON.stringify({ question_index: questionIndex, code, language }),
    });
  },

  getStatus(
    sessionId: string,
  ): Promise<{ status: string; completed?: boolean; score?: number }> {
    return request(`/api/v1/mock-interview/${sessionId}/status`);
  },

  getHistory(): Promise<InterviewHistoryItem[]> {
    return request("/api/v1/mock-interview/history");
  },
};

export const bookingApi = {
  bookInterview(
    data: Record<string, unknown>,
  ): Promise<{ booking_id: string; status: string }> {
    return request("/api/v1/interview-booking/book", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getUpcomingBookings(): Promise<BookingDetail[]> {
    return request("/api/v1/interview-booking/upcoming");
  },

  getBookingHistory(
    page = 1,
    limit = 20,
    status: string | null = null,
  ): Promise<{
    bookings: BookingDetail[];
    total: number;
    page: number;
    pages: number;
  }> {
    let url = `/api/v1/interview-booking/history?page=${page}&limit=${limit}`;
    if (status) {
      url += `&status=${status}`;
    }
    return request(url);
  },

  getBookingDetail(bookingId: string): Promise<BookingDetail> {
    return request(`/api/v1/interview-booking/${bookingId}`);
  },

  startBooking(
    bookingId: string,
  ): Promise<{ session_id?: string; started?: boolean }> {
    return request(`/api/v1/interview-booking/${bookingId}/start`, {
      method: "POST",
    });
  },

  submitBookingAnswers(
    bookingId: string,
    answers: Record<string, unknown>,
  ): Promise<{ submitted?: boolean; message?: string }> {
    return request(`/api/v1/interview-booking/${bookingId}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    });
  },

  cancelBooking(
    bookingId: string,
    reason: string | null = null,
  ): Promise<{ canceled?: boolean }> {
    return request(`/api/v1/interview-booking/${bookingId}/cancel`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    });
  },

  getAvailableSlots(
    date: string,
    type: string | null = null,
  ): Promise<BookingSlot[]> {
    let url = `/api/v1/interview-booking/available-slots?date=${date}`;
    if (type) {
      url += `&type=${type}`;
    }
    return request(url);
  },

  getBookingStats(): Promise<Record<string, unknown>> {
    return request("/api/v1/interview-booking/stats");
  },

  markNoShow(bookingId: string): Promise<{ marked?: boolean }> {
    return request(`/api/v1/interview-booking/${bookingId}/no-show`, {
      method: "POST",
    });
  },
};
