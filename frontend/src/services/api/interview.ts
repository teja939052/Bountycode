import { requestWithRetry as request } from "./request.ts";
export const interviewApi = {
  startInterview(jobRole) {
    return request("/api/v1/interview/start", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  },

  startInterviewV2(jobRole, company = "general", interviewType = "mixed", difficulty = "medium") {
    return request("/api/v1/interview/start", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole, company, interview_type: interviewType, difficulty }),
    });
  },

  submitAnswer(interviewId, question, answer) {
    return request("/api/v1/interview/answer", {
      method: "POST",
      body: JSON.stringify({ interview_id: interviewId, question, answer }),
    });
  },

  getInterviewResult(interviewId) {
    return request(`/api/v1/interview/${interviewId}/result`);
  },

  getInterviewHistory() {
    return request("/api/v1/interview/history");
  },
};

export const mockInterviewApi = {
  startMockInterview(config: Record<string, any> = {}) {
    return request("/api/v1/mock-interview/start", {
      method: "POST",
      body: JSON.stringify(config),
    });
  },

  submitAnswer(sessionId, questionIndex, code, language) {
    return request(`/api/v1/mock-interview/${sessionId}/submit`, {
      method: "POST",
      body: JSON.stringify({ question_index: questionIndex, code, language }),
    });
  },

  getStatus(sessionId) {
    return request(`/api/v1/mock-interview/${sessionId}/status`);
  },

  getHistory() {
    return request("/api/v1/mock-interview/history");
  },
};

export const bookingApi = {
  bookInterview(data) {
    return request("/api/v1/interview-booking/book", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getUpcomingBookings() {
    return request("/api/v1/interview-booking/upcoming");
  },

  getBookingHistory(page = 1, limit = 20, status = null) {
    let url = `/api/v1/interview-booking/history?page=${page}&limit=${limit}`;
    if (status) {
      url += `&status=${status}`;
    }
    return request(url);
  },

  getBookingDetail(bookingId) {
    return request(`/api/v1/interview-booking/${bookingId}`);
  },

  startBooking(bookingId) {
    return request(`/api/v1/interview-booking/${bookingId}/start`, {
      method: "POST",
    });
  },

  submitBookingAnswers(bookingId, answers) {
    return request(`/api/v1/interview-booking/${bookingId}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    });
  },

  cancelBooking(bookingId, reason = null) {
    return request(`/api/v1/interview-booking/${bookingId}/cancel`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    });
  },

  getAvailableSlots(date, type = null) {
    let url = `/api/v1/interview-booking/available-slots?date=${date}`;
    if (type) {
      url += `&type=${type}`;
    }
    return request(url);
  },

  getBookingStats() {
    return request("/api/v1/interview-booking/stats");
  },

  markNoShow(bookingId) {
    return request(`/api/v1/interview-booking/${bookingId}/no-show`, {
      method: "POST",
    });
  },
};