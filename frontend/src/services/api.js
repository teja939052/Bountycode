const API_BASE = import.meta.env.VITE_API_URL || "";

const MEMORY_CACHE_TTL = 60000;
const memoryCache = new Map();

class ApiService {
  constructor() {
    this.baseUrl = API_BASE;
  }

  _cacheKey(endpoint, options) {
    return `${options.method || 'GET'}:${endpoint}:${JSON.stringify(options.body || '')}`;
  }

  async request(endpoint, options = {}) {
    const cacheKey = this._cacheKey(endpoint, options);
    const now = Date.now();

    if (memoryCache.has(cacheKey)) {
      const cached = memoryCache.get(cacheKey);
      if (now - cached.timestamp < MEMORY_CACHE_TTL) {
        return cached.data;
      }
      memoryCache.delete(cacheKey);
    }

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "/login";
      throw new Error("Session expired");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || "Request failed");
    }

    const data = await response.json();
    memoryCache.set(cacheKey, { data, timestamp: now });
    return data;
  }

  async requestBlob(endpoint, options = {}) {
    const headers = {
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });

    if (response.status === 401) {
      window.location.href = "/login";
      throw new Error("Session expired");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || "Request failed");
    }

    return response.blob();
  }

  async get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  }

  async post(endpoint, body) {
    return this.request(endpoint, { method: "POST", body: JSON.stringify(body) });
  }

  async put(endpoint, body) {
    return this.request(endpoint, { method: "PUT", body: JSON.stringify(body) });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: "DELETE" });
  }

  async register(email, password, name) {
    return this.request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    });
  }

  async login(email, password) {
    return this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  async logout() {
    return this.request("/api/auth/logout", { method: "POST" });
  }

  async getMe() {
    return this.request("/api/auth/me");
  }

  async updateProfile(name, email) {
    const data = await this.request("/api/auth/update-profile", {
      method: "POST",
      body: JSON.stringify({ name, email }),
    });
    memoryCache.delete(this._cacheKey("/api/auth/me", { method: "GET" }));
    return data;
  }

  async changePassword(currentPassword, newPassword) {
    return this.request("/api/auth/change-password", {
      method: "POST",
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    });
  }

  async forgotPassword(email) {
    return this.request("/api/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  }

  async resetPassword(email, token, newPassword) {
    return this.request("/api/auth/reset-password", {
      method: "POST",
      body: JSON.stringify({ email, token, new_password: newPassword }),
    });
  }

  async startInterview(jobRole) {
    return this.request("/api/interview/start", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  }

  async startInterviewV2(jobRole, company = "general", interviewType = "mixed", difficulty = "medium") {
    return this.request("/api/interview/start", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole, company, interview_type: interviewType, difficulty }),
    });
  }

  async submitAnswer(interviewId, question, answer) {
    return this.request("/api/interview/answer", {
      method: "POST",
      body: JSON.stringify({ interview_id: interviewId, question, answer }),
    });
  }

  async getInterviewResult(interviewId) {
    return this.request(`/api/interview/${interviewId}/result`);
  }

  async getInterviewHistory() {
    return this.request("/api/interview/history");
  }

  async uploadResume(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseUrl}/api/resume/upload`, {
      method: "POST",
      credentials: "include",
      body: formData,
    });

    if (response.status === 401) {
      window.location.href = "/login";
      throw new Error("Session expired");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Upload failed" }));
      throw new Error(error.detail || "Upload failed");
    }

    return response.json();
  }

  async generateResume(details) {
    return this.request("/api/resume/generate", {
      method: "POST",
      body: JSON.stringify(details),
    });
  }

  async optimizeResume(resumeId, jobDescription) {
    return this.request("/api/resume/optimize", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription }),
    });
  }

  async exportResume(resumeId, format) {
    return this.requestBlob(`/api/resume/${resumeId}/export/${format}`);
  }

  async getResumeHistory() {
    return this.request("/api/resume/history");
  }

  async createCheckout(country = "US") {
    return this.request("/api/billing/checkout", {
      method: "POST",
      body: JSON.stringify({ country }),
    });
  }

  async createLifetimeCheckout(country = "US") {
    return this.request("/api/billing/checkout/lifetime", {
      method: "POST",
      body: JSON.stringify({ country }),
    });
  }

  async createYearlyCheckout(country = "US") {
    return this.request("/api/billing/checkout/yearly", {
      method: "POST",
      body: JSON.stringify({ country }),
    });
  }

  async captureOrder(orderId) {
    return this.request("/api/billing/capture", {
      method: "POST",
      body: JSON.stringify({ order_id: orderId }),
    });
  }

  async getBillingStatus() {
    return this.request("/api/billing/status");
  }

  // Aptitude Test
  async getAptitudeCategories() {
    return this.request("/api/aptitude/categories");
  }

  async startAptitudeTest(category, difficulty = "medium", questionCount = 10) {
    return this.request("/api/aptitude/start", {
      method: "POST",
      body: JSON.stringify({ category, difficulty, question_count: questionCount }),
    });
  }

  async submitAptitudeAnswer(testId, questionIndex, answer) {
    return this.request("/api/aptitude/answer", {
      method: "POST",
      body: JSON.stringify({ test_id: testId, question_index: questionIndex, answer }),
    });
  }

  async completeAptitudeTest(testId, timeTaken = 0) {
    return this.request(`/api/aptitude/${testId}/complete?time_taken=${timeTaken}`, {
      method: "POST",
    });
  }

  async getAptitudeHistory() {
    return this.request("/api/aptitude/history");
  }

  // Cover Letter & Tools
  async generateCoverLetter(resumeId, jobDescription, companyName = "") {
    return this.request("/api/tools/cover-letter", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription, company_name: companyName }),
    });
  }

  async generateLinkedInAbout(resumeId, targetRole = "") {
    return this.request("/api/tools/linkedin-about", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, target_role: targetRole }),
    });
  }

  async getSalaryNegotiationTips(jobTitle, offeredSalary, location, yearsExperience = 0, companySize = "", benefits = []) {
    return this.request("/api/tools/salary-negotiation", {
      method: "POST",
      body: JSON.stringify({ job_title: jobTitle, offered_salary: offeredSalary, location, years_experience: yearsExperience, company_size: companySize, benefits }),
    });
  }

  async getCoverLetterHistory() {
    return this.request("/api/tools/cover-letter/history");
  }

  // System Design
  async startSystemDesign(difficulty = "medium", topic = "") {
    return this.request("/api/system-design/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic }),
    });
  }

  async submitSystemDesignAnswer(sessionId, question, answer, diagramDescription = "") {
    return this.request("/api/system-design/answer", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, question, answer, diagram_description: diagramDescription }),
    });
  }

  async getSystemDesignResult(sessionId) {
    return this.request(`/api/system-design/${sessionId}/result`);
  }

  async getSystemDesignHistory() {
    return this.request("/api/system-design/history");
  }

  // Company Prep
  async getCompanies() {
    return this.request("/api/company/companies");
  }

  async getBehavioralQuestion(company, role) {
    return this.request("/api/company/behavioral", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  }

  async getInterviewTips(company, role, roundType) {
    return this.request("/api/company/tips", {
      method: "POST",
      body: JSON.stringify({ company, role, round_type: roundType }),
    });
  }

  async getCompanyGuide(company) {
    return this.request(`/api/company/${company}/guide`);
  }

  // Coding Challenges
  async getCodingTopics() {
    return this.request("/api/coding/topics");
  }

  async startCodingChallenge(difficulty = "medium", topic = "arrays", language = "python") {
    return this.request("/api/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language }),
    });
  }

  async startCodingChallengeV2(difficulty = "medium", topic = "arrays", language = "python", company = "", role = "SDE") {
    return this.request("/api/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language, company, role }),
    });
  }

  async getCodingHint(challengeId, hintLevel = 1) {
    return this.request("/api/coding/hint", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, hint_level: hintLevel }),
    });
  }

  async getInterviewerReview(challengeId, code, language = "python") {
    return this.request("/api/coding/interviewer-review", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, language }),
    });
  }

  async submitCodingAnswer(challengeId, code, timeTaken = 0) {
    return this.request("/api/coding/submit", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, time_taken: timeTaken }),
    });
  }

  async getCodingSolution(challengeId) {
    return this.request(`/api/coding/${challengeId}/solution`);
  }

  async getCodingHistory() {
    return this.request("/api/coding/history");
  }

  // Salary Benchmark
  async getSalaryBenchmark(jobTitle, location, company = "", yearsExperience = 0, level = "") {
    return this.request("/api/salary/benchmark", {
      method: "POST",
      body: JSON.stringify({ job_title: jobTitle, location, company, years_experience: yearsExperience, level }),
    });
  }

  async compareOffers(offers) {
    return this.request("/api/salary/compare", {
      method: "POST",
      body: JSON.stringify({ offers }),
    });
  }

  // Gamification
  async getGamificationProfile() {
    return this.request("/api/gamification/profile");
  }

  async recordActivity(activityType, score = 0, category = null, skill = null) {
    const params = new URLSearchParams({ activity_type: activityType, score: score.toString() });
    if (category) params.append("category", category);
    if (skill) params.append("skill", skill);
    return this.request(`/api/gamification/record?${params.toString()}`, {
      method: "POST",
    });
  }

  async getLeaderboard(limit = 10) {
    return this.request(`/api/gamification/leaderboard?limit=${limit}`);
  }

  async getAllBadges() {
    return this.request("/api/gamification/badges");
  }

  // Skill Assessment
  async getSkillGraph() {
    return this.request("/api/gamification/skills");
  }

  async getWeakAreas(topN = 5) {
    return this.request(`/api/gamification/skills/weak?top_n=${topN}`);
  }

  async getReadinessScore(company = null) {
    const params = company ? `?company=${company}` : "";
    return this.request(`/api/gamification/skills/readiness${params}`);
  }

  // Hook Model - Mystery Box & Rewards
  async openMysteryBox() {
    return this.request("/api/hook/mystery-box", { method: "POST" });
  }

  async checkDoubleXP(activityType, score) {
    return this.request(`/api/hook/double-xp-check?activity_type=${activityType}&score=${score}`, {
      method: "POST",
    });
  }

  async getSavageFeedback(score) {
    return this.request(`/api/hook/savage-feedback?score=${score}`);
  }

  async useStreakFreeze() {
    return this.request("/api/hook/streak-freeze", { method: "POST" });
  }

  async getDailyBonus() {
    return this.request("/api/hook/daily-bonus");
  }

  // Enhanced ATS
  async analyzeATSEnhanced(resumeText, jobDescription = null) {
    const params = new URLSearchParams({ resume_text: resumeText });
    if (jobDescription) params.append("job_description", jobDescription);
    return this.request(`/api/hook/ats-analyze?${params.toString()}`, {
      method: "POST",
    });
  }

  // Social - Study Groups
  async createStudyGroup(name, description = "") {
    return this.request(`/api/hook/study-groups/create?name=${name}&description=${description}`, {
      method: "POST",
    });
  }

  async joinStudyGroup(groupId) {
    return this.request(`/api/hook/study-groups/${groupId}/join`, { method: "POST" });
  }

  async getStudyGroups() {
    return this.request("/api/hook/study-groups");
  }

  // Social - Contests
  async getActiveContests() {
    return this.request("/api/hook/contests");
  }

  async enterContest(contestId, score) {
    return this.request(`/api/hook/contests/${contestId}/enter?score=${score}`, {
      method: "POST",
    });
  }

  async getContestLeaderboard(contestId) {
    return this.request(`/api/hook/contests/${contestId}/leaderboard`);
  }

  // Free Practice Hook
  async quickInterview(jobRole = "Software Engineer") {
    return this.request("/api/free/quick-interview", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  }

  async quickEvaluate(question, answer, jobRole = "Software Engineer") {
    return this.request("/api/free/quick-evaluate", {
      method: "POST",
      body: JSON.stringify({ question, answer, job_role: jobRole }),
    });
  }

  // Enhanced Features - Resume
  async improveBullet(bullet, jobRole = "") {
    return this.request("/api/enhanced/resume/improve-bullet", {
      method: "POST",
      body: JSON.stringify({ bullet, job_role: jobRole }),
    });
  }

  async improveBullets(bullets, jobRole = "") {
    return this.request("/api/enhanced/resume/improve-bullets", {
      method: "POST",
      body: JSON.stringify({ bullets, job_role: jobRole }),
    });
  }

  async getATSChecklist(resumeText) {
    return this.request("/api/enhanced/resume/ats-checklist", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  }

  async tailorResume(resumeText, jobDescription, jobRole = "") {
    return this.request("/api/enhanced/resume/tailor", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription, job_role: jobRole }),
    });
  }

  // Enhanced Features - Coding
  async getCompanyCodingChallenge(company, role = "SDE", difficulty = null) {
    return this.request("/api/enhanced/coding/company-challenge", {
      method: "POST",
      body: JSON.stringify({ company, role, difficulty }),
    });
  }

  async getCodeReviewerFeedback(code, language, problemDescription) {
    return this.request("/api/enhanced/coding/interviewer-feedback", {
      method: "POST",
      body: JSON.stringify({ code, language, problem_description: problemDescription }),
    });
  }

  async explainConcept(concept, level = "intermediate") {
    return this.request("/api/enhanced/coding/explain", {
      method: "POST",
      body: JSON.stringify({ concept, level }),
    });
  }

  async getEnhancedCodingHint(problemDescription, currentCode = "", hintLevel = 1) {
    return this.request("/api/enhanced/coding/hint", {
      method: "POST",
      body: JSON.stringify({ problem_description: problemDescription, current_code: currentCode, hint_level: hintLevel }),
    });
  }

  // Enhanced Features - Behavioral
  async evaluateSTAR(question, answer, company = "", leadershipPrinciples = []) {
    return this.request("/api/enhanced/behavioral/evaluate-star", {
      method: "POST",
      body: JSON.stringify({ question, answer, company, leadership_principles: leadershipPrinciples }),
    });
  }

  async getSTARTemplate(question, company = "", role = "") {
    return this.request("/api/enhanced/behavioral/star-template", {
      method: "POST",
      body: JSON.stringify({ question, company, role }),
    });
  }

  async getBehavioralQuestions(company, role, count = 5) {
    return this.request("/api/enhanced/behavioral/practice-questions", {
      method: "POST",
      body: JSON.stringify({ company, role, count }),
    });
  }

  // Free ATS Tool (No auth required)
  async freeATSCheck(resumeText) {
    return fetch(`${this.baseUrl}/api/enhanced/free/ats-check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: resumeText }),
    }).then(r => r.json());
  }

  // Missing Bullet Generator (Pro only)
  async generateMissingBullet(resumeText, jobDescription, missingSkill) {
    return this.request("/api/enhanced/resume/missing-bullet", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription, missing_skill: missingSkill }),
    });
  }

  // Student Features - Cheat Sheets
  async getCheatSheet(company, topic) {
    return this.request("/api/student/cheatsheet", {
      method: "POST",
      body: JSON.stringify({ company, topic }),
    });
  }

  async getCheatSheetTemplates() {
    return this.request("/api/student/cheatsheet/templates");
  }

  // Student Features - Anti-Plagiarism
  async humanizeBullet(bullet) {
    return this.request("/api/student/humanize/bullet", {
      method: "POST",
      body: JSON.stringify({ bullet }),
    });
  }

  async humanizeResume(resumeText) {
    return this.request("/api/student/humanize/resume", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  }

  // Student Features - Application Tracker
  async createApplication(company, role, jobUrl = "", notes = "") {
    return this.request("/api/student/applications", {
      method: "POST",
      body: JSON.stringify({ company, role, job_url: jobUrl, notes }),
    });
  }

  async getApplicationPipeline() {
    return this.request("/api/student/applications/pipeline");
  }

  async updateApplicationStage(applicationId, newStage) {
    return this.request("/api/student/applications/stage", {
      method: "PUT",
      body: JSON.stringify({ application_id: applicationId, new_stage: newStage }),
    });
  }

  async getApplicationStats() {
    return this.request("/api/student/applications/stats");
  }

  async deleteApplication(applicationId) {
    return this.request(`/api/student/applications/${applicationId}`, {
      method: "DELETE",
    });
  }

  async getPipelineStages() {
    return this.request("/api/student/applications/stages");
  }

  // Student Features - Daily Drill
  async getDailyDrill() {
    return this.request("/api/student/drill/daily", { method: "POST" });
  }

  async submitDrill(drillId, answers) {
    return this.request("/api/student/drill/submit", {
      method: "POST",
      body: JSON.stringify({ drill_id: drillId, answers }),
    });
  }

  // Student Features - Profile Sync
  async syncGitHub(githubUrl) {
    return this.request("/api/student/sync/github", {
      method: "POST",
      body: JSON.stringify({ github_url: githubUrl }),
    });
  }

  async generateBulletsFromProjects(projects, role = "Software Engineer") {
    return this.request("/api/student/sync/generate-bullets", {
      method: "POST",
      body: JSON.stringify({ projects, role }),
    });
  }

  // Placement Predictor (Math-driven, zero AI cost)
  async predictOffer(company, role = "SDE") {
    return this.post("/api/predictor/predict", { company, role });
  }

  async predictOfferByCompany(company, role = "SDE") {
    return this.get(`/api/predictor/predict/${company}?role=${role}`);
  }

  async getPredictionHistory() {
    return this.get("/api/predictor/history");
  }

  async getSupportedCompanies() {
    return this.get("/api/predictor/companies");
  }

  async getCompaniesByTier(tier) {
    return this.get(`/api/predictor/companies/${tier}`);
  }

  async getTierWeights() {
    return this.get("/api/predictor/tiers");
  }

  async getSubSkills() {
    return this.get("/api/predictor/sub-skills");
  }

  // Company Mocks
  async getMockCompanies() {
    return this.get("/api/placement/mocks/companies");
  }

  async startMockTest(company) {
    return this.post("/api/placement/mocks/start", { company });
  }

  async submitMockAnswer(testId, questionIndex, answer) {
    return this.post("/api/placement/mocks/answer", {
      test_id: testId,
      question_index: questionIndex,
      answer,
    });
  }

  async completeMockTest(testId, answers = null) {
    return this.post("/api/placement/mocks/complete", {
      test_id: testId,
      answers,
    });
  }

  async getMockHistory() {
    return this.get("/api/placement/mocks/history");
  }

  // Gap Analysis
  async getGapAnalysis(company, targetProbability = 75) {
    return this.post("/api/placement/gap-analysis", {
      company,
      target_probability: targetProbability,
    });
  }

  async getCompanyProbability(company, target = 75) {
    return this.get(`/api/placement/probability/${encodeURIComponent(company)}?target=${target}`);
  }

  // Dashboard Insights
  async getDashboardInsights() {
    return this.get("/api/placement/dashboard-insights");
  }

  // Alumni Experiences
  async getAlumniExperiences(company = null, role = null, limit = 20) {
    const params = new URLSearchParams();
    if (company) params.set("company", company);
    if (role) params.set("role", role);
    params.set("limit", limit.toString());
    return this.get(`/api/placement/alumni?${params.toString()}`);
  }

  // Placement Drives
  async getPlacementDrives(limit = 10) {
    return this.get(`/api/placement/drives?limit=${limit}`);
  }

  // Career Profile
  async getCareerProfile() {
    return this.get("/api/profile");
  }

  async updateCareerProfile(payload) {
    return this.put("/api/profile", payload);
  }

  async createProfileFromResume(resumeText, resumeId = null) {
    return this.post("/api/profile/from-resume", { resume_text: resumeText, resume_id: resumeId });
  }

  async uploadResumeToProfile(file) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${this.baseUrl}/api/profile/upload-resume`, {
      method: "POST",
      credentials: "include",
      body: formData,
    });
    if (response.status === 401) {
      window.location.href = "/login";
      throw new Error("Session expired");
    }
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Upload failed" }));
      throw new Error(error.detail || "Upload failed");
    }
    return response.json();
  }

  async addProfileSectionItem(section, { item }) {
    return this.post(`/api/profile/sections/${section}/items`, { item });
  }

  async removeProfileSectionItem(section, index) {
    return this.delete(`/api/profile/sections/${section}/items/${index}`);
  }

  // Practice for This Role (Phase 4 workflow)
  async createPracticeSession(company, role = "SDE", focusAreas = null) {
    return this.post("/api/practice/session", {
      company,
      role,
      focus_areas: focusAreas,
    });
  }

  async completePracticeSession(sessionId) {
    return this.post(`/api/practice/session/${encodeURIComponent(sessionId)}/complete`);
  }

  async getPracticeSessions() {
    return this.get("/api/practice/sessions");
  }

  // Analytics
  async getAnalyticsOverview() {
    return this.get("/api/analytics/overview");
  }

  async getAnalyticsFunnel() {
    return this.get("/api/analytics/funnel");
  }

  async getAnalyticsSkills() {
    return this.get("/api/analytics/skills");
  }

  async getAnalyticsCompanies() {
    return this.get("/api/analytics/companies");
  }

  async getAnalyticsInsights() {
    return this.get("/api/analytics/insights");
  }

  async createEnterpriseCohort(name, institution) {
    return this.post("/api/enterprise/cohorts", { name, institution });
  }

  async getEnterpriseCohorts() {
    return this.get("/api/enterprise/cohorts");
  }

  async getCohortProgress(cohortId) {
    return this.get(`/api/enterprise/cohorts/${encodeURIComponent(cohortId)}/progress`);
  }

  // Trial
  async startTrial() {
    return this.post("/api/trial/start");
  }

  async getTrialStatus() {
    return this.get("/api/trial/status");
  }

  async cancelTrial() {
    return this.post("/api/trial/cancel");
  }

  // Student Discount
  async verifyStudentDiscount(email) {
    return this.post("/api/discount/student/verify", { email });
  }

  async getStudentDiscountStatus() {
    return this.get("/api/discount/student/status");
  }

  // Compiler
  async executeCompilerCode({ code, language, stdin = "", timeout = 5 }) {
    return this.post("/api/compiler/execute", { code, language, stdin, timeout });
  }

  async executeCompilerTestCases({ code, language, test_cases, timeout = 5 }) {
    return this.post("/api/compiler/execute-test-cases", { code, language, test_cases, timeout });
  }

  async getCompilerLanguages() {
    return this.get("/api/compiler/languages");
  }

  async getCompilerBoilerplate(language, topics = []) {
    return this.post("/api/compiler/boilerplate", { language, topics });
  }

  // Profile Stats
  async getProfileStats() {
    return this.get("/api/profile/stats");
  }

  async updateIntegration(platform, username) {
    return this.put("/api/profile/integrations", { platform, username });
  }

  // Usage / Conversion helpers
  async getUsageStats() {
    return this.get("/api/usage/stats");
  }

  async getSentenceLevelFeedback(answer, topic = "", ideal = "") {
    return this.post("/api/feedback/sentence-level", {
      answer,
      topic,
      ideal,
    });
  }

  // Real Features - ATS Scanner (No auth required)
  async realATSScan(resumeText, jobDescription = "") {
    return fetch(`${this.baseUrl}/api/real/ats/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
    }).then(r => r.json());
  }

  // Real Features - Code Execution
  async executeCode(code, language, stdin = "") {
    return this.request("/api/real/code/execute", {
      method: "POST",
      body: JSON.stringify({ code, language, stdin }),
    });
  }

  async runTestCases(code, language, testCases) {
    return this.request("/api/real/code/run-tests", {
      method: "POST",
      body: JSON.stringify({ code, language, test_cases: testCases }),
    });
  }

  async getBoilerplate(language, problemType = "general") {
    return this.get(`/api/real/code/boilerplate/${language}?problem_type=${problemType}`);
  }

  // Real Features - Smart Interview
  async getSmartInterviewQuestion(jobRole, company, difficulty = "medium", history = []) {
    return this.request("/api/real/interview/question", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole, company, difficulty, history }),
    });
  }

  async evaluateAnswerSmart(question, answer, jobRole, company, questionType = "technical") {
    return this.request("/api/real/interview/evaluate", {
      method: "POST",
      body: JSON.stringify({ question, answer, job_role: jobRole, company, question_type: questionType }),
    });
  }

  // Real Features - Smart Resume
  async improveBulletSmart(bullet, jobRole = "", company = "", industry = "tech") {
    return this.request("/api/real/resume/improve-bullet", {
      method: "POST",
      body: JSON.stringify({ bullet, job_role: jobRole, company, industry }),
    });
  }

  // Real Features - Smart Behavioral
  async getSTARTemplateSmart(question, company, role) {
    return this.request("/api/real/behavioral/star-template", {
      method: "POST",
      body: JSON.stringify({ question, company, role }),
    });
  }

  // Real Features - Smart System Design
  async getSystemDesignQuestionSmart(topic, difficulty = "medium", company = "google") {
    return this.request("/api/real/system-design/question", {
      method: "POST",
      body: JSON.stringify({ topic, difficulty, company }),
    });
  }

  // Question Bank
  async browseQuestions(params = {}) {
    const qs = new URLSearchParams();
    if (params.company) qs.set("company", params.company);
    if (params.role) qs.set("role", params.role);
    if (params.topic) qs.set("topic", params.topic);
    if (params.sub_topic) qs.set("sub_topic", params.sub_topic);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.type) qs.set("type", params.type);
    if (params.search) qs.set("search", params.search);
    if (params.page) qs.set("page", params.page);
    if (params.limit) qs.set("limit", params.limit);
    return this.get(`/api/questions/browse?${qs.toString()}`);
  }

  async getQuestionFilters() {
    return this.get("/api/questions/filters");
  }

  async submitQuestionAnswer(questionId, answer, timeTaken = null) {
    return this.post("/api/questions/answer", {
      question_id: questionId,
      answer,
      time_taken: timeTaken,
    });
  }

  async submitNewQuestion(payload) {
    return this.post("/api/questions/submit", payload);
  }

  async upvoteQuestion(questionId, vote = 1) {
    return this.post("/api/questions/upvote", { question_id: questionId, vote });
  }

  async getQuestionStats() {
    return this.get("/api/questions/stats");
  }

  async getRecentAnswers(limit = 20) {
    return this.get(`/api/questions/recent?limit=${limit}`);
  }

  async getRandomQuestion(type = null, difficulty = null, topic = null) {
    const qs = new URLSearchParams();
    if (type) qs.set("type", type);
    if (difficulty) qs.set("difficulty", difficulty);
    if (topic) qs.set("topic", topic);
    return this.get(`/api/questions/random?${qs.toString()}`);
  }

  async getCompanyQuestions(company, page = 1, limit = 20) {
    return this.get(`/api/questions/company/${encodeURIComponent(company)}?page=${page}&limit=${limit}`);
  }

  async getQuestionTopics() {
    return this.get("/api/questions/topics");
  }

  async getQuestionFull(questionId) {
    return this.get(`/api/questions/${encodeURIComponent(questionId)}`);
  }

  async isQuestionSolved(questionId) {
    return this.get(`/api/questions/${encodeURIComponent(questionId)}/solved`);
  }

  async submitQuestionCode(questionId, payload) {
    return this.post(`/api/questions/${encodeURIComponent(questionId)}/submit`, payload);
  }

  async submitMockTest(testId, answers) {
    return this.post(`/api/questions/mock-test/${encodeURIComponent(testId)}/submit`, answers);
  }

  async getSemanticAtsScore(resumeText, jobDescription = "") {
    return this.post("/api/resume/semantic-score", {
      resume_text: resumeText,
      job_description: jobDescription,
    });
  }

  // Semantic ATS (Phase 5)
  async getSemanticATS(resumeText, jobDescription = "") {
    return this.post("/api/enhanced/ats/semantic", { resume_text: resumeText, job_description: jobDescription });
  }

  // Batch operations - reduce round trips
  async batch(operations) {
    return this.post("/api/batch", { operations });
  }

  // ==================== Problems Navigation ====================

  async getTopics() {
    return this.get("/api/problems/topics");
  }

  async getTopicProblems(topic, sort = "order", difficulty = null, company = null) {
    let params = new URLSearchParams({ sort });
    if (difficulty) params.append("difficulty", difficulty);
    if (company) params.append("company", company);
    return this.get(`/api/problems/topics/${encodeURIComponent(topic)}?${params.toString()}`);
  }

  async getPatterns() {
    return this.get("/api/problems/patterns");
  }

  async getPatternProblems(patternName, sort = "order", difficulty = null) {
    let params = new URLSearchParams({ sort });
    if (difficulty) params.append("difficulty", difficulty);
    return this.get(`/api/problems/pattern/${encodeURIComponent(patternName)}?${params.toString()}`);
  }

  async getProblemProgress() {
    return this.get("/api/problems/progress");
  }

  async getProblemStreak() {
    return this.get("/api/problems/streak");
  }

  async getProblemStats() {
    return this.get("/api/problems/stats");
  }

  async getCompanyProblems(companyName) {
    return this.get(`/api/problems/company/${encodeURIComponent(companyName)}`);
  }

  // Random question for quick practice
  async getRandomQuestion(params = {}) {
    const qs = new URLSearchParams();
    if (params.type) qs.set("type", params.type);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.topic) qs.set("topic", params.topic);
    if (params.company) qs.set("company", params.company);
    qs.set("exclude_solved", "true");
    return this.get(`/api/questions/random?${qs.toString()}`);
  }

  // Progressive hints solution
  async getQuestionSolution(questionId, hintLevel = 1) {
    return this.post(`/api/questions/${encodeURIComponent(questionId)}/solution`, {
      hint_level: hintLevel,
    });
  }

  // ==================== Mock Interview ====================

  async startMockInterview(config = {}) {
    return this.post("/api/mock-interview/start", config);
  }

  async submitMockInterviewAnswer(sessionId, questionIndex, code, language) {
    return this.post(`/api/mock-interview/${sessionId}/submit`, {
      question_index: questionIndex,
      code,
      language,
    });
  }

  async getMockInterviewStatus(sessionId) {
    return this.get(`/api/mock-interview/${sessionId}/status`);
  }

  async getMockInterviewHistory() {
    return this.get("/api/mock-interview/history");
  }

  // ==================== Personal Dashboard ====================

  async getPersonalDashboard() {
    return this.get("/api/dashboard/personal");
  }

  async getRecommendations() {
    return this.get("/api/dashboard/recommendations");
  }

  // ==================== Hiring Readiness ====================

  async getCompanyReadiness(companyName) {
    return this.get(`/api/readiness/company/${encodeURIComponent(companyName)}`);
  }

  // ==================== AI Debugger ====================

  async analyzeFailedSubmission(questionId, code, language, failedTestCase = null) {
    return this.post("/api/ai-debugger/analyze", {
      question_id: questionId,
      code,
      language,
      failed_test_case: failedTestCase,
    });
  }

  async getProgressiveHint(questionId, hintLevel = 1, code = null) {
    return this.post("/api/ai-debugger/hint", {
      question_id: questionId,
      hint_level: hintLevel,
      code,
    });
  }

  async explainError(errorMessage, code, language) {
    return this.post("/api/ai-debugger/explain-error", {
      error_message: errorMessage,
      code,
      language,
    });
  }

  // ==================== Concept Cards ====================

  async getConceptCard(topic) {
    return this.get(`/api/concepts/${encodeURIComponent(topic)}`);
  }

  async getAvailableConcepts() {
    return this.get("/api/concepts");
  }

  // ==================== Daily Challenge & Leagues ====================

  async getDailyChallenge() {
    return this.get("/api/daily/challenge");
  }

  async submitDailyChallenge(problemId, code, language) {
    return this.post("/api/daily/challenge/submit", {
      problem_id: problemId,
      code,
      language,
    });
  }

  async getLeagues() {
    return this.get("/api/daily/leagues");
  }

  async getDailyLeaderboard(timeframe = "daily") {
    return this.get(`/api/daily/leaderboard?timeframe=${timeframe}`);
  }

  // ==================== Discussions ====================

  async getDiscussions(questionId, sort = "best", page = 1) {
    return this.get(`/api/discussions/${questionId}?sort=${sort}&page=${page}`);
  }

  async createDiscussion(questionId, content, code = null, language = null, type = "solution") {
    return this.post(`/api/discussions/${questionId}`, {
      content,
      code,
      language,
      discussion_type: type,
    });
  }

  async upvoteDiscussion(discussionId) {
    return this.post(`/api/discussions/${discussionId}/upvote`);
  }

  async replyToDiscussion(discussionId, content) {
    return this.post(`/api/discussions/${discussionId}/reply`, { content });
  }

  async getDiscussionSummary(questionId) {
    return this.get(`/api/discussions/${questionId}/summary`);
  }

  // ==================== Playlists ====================

  async getPlaylists(difficulty = null, company = null) {
    let params = new URLSearchParams();
    if (difficulty) params.append("difficulty", difficulty);
    if (company) params.append("company", company);
    return this.get(`/api/playlists?${params.toString()}`);
  }

  async getPlaylist(playlistId) {
    return this.get(`/api/playlists/${playlistId}`);
  }

  async getNextPlaylistProblem(playlistId) {
    return this.get(`/api/playlists/${playlistId}/next`);
  }

  async createCustomPlaylist(title, description, problemIds) {
    return this.post("/api/playlists/custom", {
      title,
      description,
      problem_ids: problemIds,
    });
  }

  async getMyCustomPlaylists() {
    return this.get("/api/playlists/my/custom");
  }

  // ==================== Company-Specific Mock Portals ====================

  async getCompanyMocks() {
    return this.get("/api/company-mocks/companies");
  }

  async getCompanyMockConfig(companyId) {
    return this.get(`/api/company-mocks/${companyId}/config`);
  }

  async startCompanyMock(companyId, roundName = null) {
    return this.post(`/api/company-mocks/${companyId}/start`, { round_name: roundName });
  }

  async getCompanyMockStatus(sessionId) {
    return this.get(`/api/company-mocks/${sessionId}/status`);
  }

  async getCompanyMockResults(sessionId) {
    return this.get(`/api/company-mocks/${sessionId}/results`);
  }

  // ==================== Indian Placement ====================

  async getIndianCompanies() {
    return this.get("/api/indian-placement/companies");
  }

  async getIndianCompanyDetail(companyId) {
    return this.get(`/api/indian-placement/${companyId}`);
  }

  async getIndianCompanyMockConfig(companyId) {
    return this.get(`/api/indian-placement/${companyId}/mock-config`);
  }

  async getIndianCompanyHRQuestions(companyId) {
    return this.get(`/api/indian-placement/${companyId}/hr-questions`);
  }

  async getIndianCompanyCodingPatterns(companyId) {
    return this.get(`/api/indian-placement/${companyId}/coding-patterns`);
  }

  async startIndianPlacementMock(companyId, sectionName = null) {
    return this.post("/api/indian-placement/start-mock", { company_id: companyId, section_name: sectionName });
  }

  // ==================== DSA Fingerprint ====================

  async getSkillProfile() {
    return this.get("/api/fingerprint/skill-profile");
  }

  async getCompanyPredictions() {
    return this.get("/api/fingerprint/company-predictions");
  }

  async getCompanyFingerprint(companyId) {
    return this.get(`/api/fingerprint/company/${companyId}`);
  }

  // ==================== Placement Tower ====================

  async getTower() {
    return this.get("/api/gamification/tower");
  }

  async getBoss(bossLevel) {
    return this.get(`/api/gamification/tower/boss/${bossLevel}`);
  }

  async defeatBoss(bossLevel, score) {
    return this.post(`/api/gamification/tower/boss/${bossLevel}/defeat?score=${score}`);
  }

  async usePowerUp(powerUpId) {
    return this.post(`/api/gamification/tower/powerup/use?power_up_id=${powerUpId}`);
  }

  async buyPowerUp(powerUpId) {
    return this.post(`/api/gamification/tower/powerup/buy?power_up_id=${powerUpId}`);
  }

  async getPowerUps() {
    return this.get("/api/gamification/tower/powerups");
  }

  async getChallenges() {
    return this.get("/api/gamification/tower/challenges");
  }

  async claimChallenge(challengeType, challengeId) {
    return this.post(`/api/gamification/tower/challenges/claim?challenge_type=${challengeType}&challenge_id=${challengeId}`);
  }

  async getStreakFreezeStatus() {
    return this.get("/api/gamification/tower/streak-freeze");
  }

  async buyStreakFreeze() {
    return this.post("/api/gamification/tower/streak-freeze/buy");
  }

  async getDailyGoal() {
    return this.get("/api/gamification/tower/daily-goal");
  }

  // ==================== Card Collection ====================

  async getCardCollection(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/cards/collection?${query.toString()}`);
  }

  async getDailyDraw() {
    return this.get("/api/cards/daily-draw");
  }

  async fuseCards(cardIds) {
    return this.post("/api/cards/fuse", cardIds);
  }

  async toggleCardFavorite(cardId) {
    return this.post(`/api/cards/favorite/${cardId}`);
  }

  async getCardStats() {
    return this.get("/api/cards/stats");
  }

  async getMissingCards() {
    return this.get("/api/cards/missing");
  }

  // ==================== Code Wizard ====================

  async getWizardProfile() {
    return this.get("/api/wizard/profile");
  }

  async customizeWizard(updates) {
    return this.put("/api/wizard/customize", updates);
  }

  async getWizardDialogue(situation) {
    return this.get(`/api/wizard/dialogue/${situation}`);
  }

  async getWizardLevels() {
    return this.get("/api/wizard/levels");
  }

  // ==================== System Design Tests ====================

  async getSystemDesignCategories() {
    return this.get("/api/system-design-tests/categories");
  }

  async listSystemDesignProblems(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/system-design-tests/problems?${query.toString()}`);
  }

  async getSystemDesignProblem(problemId) {
    return this.get(`/api/system-design-tests/problem/${problemId}`);
  }

  async evaluateSystemDesign(problemId, answer) {
    return this.post(`/api/system-design-tests/evaluate/${problemId}`, { answer });
  }

  async getSystemDesignModelAnswer(problemId) {
    return this.get(`/api/system-design-tests/model-answer/${problemId}`);
  }

  async getSystemDesignRubric() {
    return this.get("/api/system-design-tests/rubric");
  }

  async getSystemDesignTestsHistory(limit = 20) {
    return this.get(`/api/system-design-tests/history?limit=${limit}`);
  }

  async getSystemDesignStats() {
    return this.get("/api/system-design-tests/stats");
  }

  async getSystemDesignLeaderboard() {
    return this.get("/api/system-design-tests/leaderboard");
  }

  async submitCode(questionId, code, language) {
    return this.post(`/api/submissions/${questionId}/submit`, { code, language });
  }

  async getSubmissionHistory(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/submissions/history?${query.toString()}`);
  }

  async getProblemSubmissions(questionId, limit = 10) {
    return this.get(`/api/submissions/problem/${questionId}?limit=${limit}`);
  }

  async getSolvedStatus(questionId) {
    return this.get(`/api/submissions/status/${questionId}`);
  }

  async getSolvedProblems(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/submissions/solved?${query.toString()}`);
  }

  async getSubmissionStats() {
    return this.get("/api/submissions/stats");
  }

  // ==================== Progress Tracking ====================

  async getHeatmap(days = 365) {
    return this.get(`/api/progress/heatmap?days=${days}`);
  }

  async getStreak() {
    return this.get("/api/progress/streak");
  }

  async getTopicProgress() {
    return this.get("/api/progress/topic-progress");
  }

  async getWeeklyGoal() {
    return this.get("/api/progress/weekly-goal");
  }

  async getDailyGoal() {
    return this.get("/api/progress/daily-goal");
  }

  async getProgressOverview() {
    return this.get("/api/progress/overview");
  }

  // ==================== Features ====================

  async getRandomProblem(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/features/random?${query.toString()}`);
  }

  async toggleBookmark(questionId) {
    return this.post(`/api/features/bookmarks/${questionId}`);
  }

  async getBookmarks(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) query.set(k, v); });
    return this.get(`/api/features/bookmarks?${query.toString()}`);
  }

  async saveNote(questionId, content) {
    return this.post(`/api/features/notes/${questionId}`, { content });
  }

  async getNote(questionId) {
    return this.get(`/api/features/notes/${questionId}`);
  }

  async getAllNotes() {
    return this.get("/api/features/notes");
  }

  async getEnhancedProblemDetail(questionId) {
    return this.get(`/api/features/problem/${questionId}/enhanced`);
  }

  async getSimilarProblems(questionId, limit = 5) {
    return this.get(`/api/features/problem/${questionId}/similar?limit=${limit}`);
  }

  async getAcceptanceRate(questionId) {
    return this.get(`/api/features/problem/${questionId}/acceptance`);
  }

  // ==================== 1v1 Battles ====================

  async createBattle(config = "standard", difficulty = null, topic = null) {
    return this.post("/api/battles/create", { config, difficulty, topic });
  }

  async joinBattle(inviteCode) {
    return this.post(`/api/battles/join/${inviteCode}`);
  }

  async quickMatch() {
    return this.post("/api/battles/matchmaking");
  }

  async startBattle(battleId) {
    return this.post(`/api/battles/start/${battleId}`);
  }

  async submitBattleCode(battleId, problemIndex, code, language) {
    return this.post(`/api/battles/submit/${battleId}`, {
      problem_index: problemIndex, code, language,
    });
  }

  async getBattleStatus(battleId) {
    return this.get(`/api/battles/status/${battleId}`);
  }

  async getBattleHistory() {
    return this.get("/api/battles/history");
  }

  async getBattleLeaderboard() {
    return this.get("/api/battles/leaderboard");
  }

  // ==================== Visual Dry Runs ====================

  async generateVisualization(questionId, testCaseInput) {
    return this.post(`/api/visualizations/generate/${questionId}`, {
      test_case_input: testCaseInput,
    });
  }

  async getAlgorithmExplanation(algorithmName) {
    return this.get(`/api/visualizations/algorithm/${algorithmName}`);
  }

  async getVisualizationTemplates() {
    return this.get("/api/visualizations/templates");
  }

  // ==================== Submission Distributions ====================

  async getRuntimeDistribution(questionId, language = null) {
    const params = language ? `?language=${language}` : '';
    return this.get(`/api/distributions/runtime/${questionId}${params}`);
  }

  async getMemoryDistribution(questionId, language = null) {
    const params = language ? `?language=${language}` : '';
    return this.get(`/api/distributions/memory/${questionId}${params}`);
  }

  async getSubmissionComparison(questionId) {
    return this.get(`/api/distributions/comparison/${questionId}`);
  }

  // ==================== Enhanced AI Debugger ====================

  async stepByStepTrace(questionId, code, language, testCaseInput) {
    return this.post("/api/ai-debugger/step-by-step", {
      question_id: questionId, code, language, test_case_input: testCaseInput,
    });
  }

  async suggestFix(questionId, code, language, errorDescription) {
    return this.post("/api/ai-debugger/suggest-fix", {
      question_id: questionId, code, language, error_description: errorDescription,
    });
  }

  async rubberDuckDebug(questionId, code, language, userThoughts) {
    return this.post("/api/ai-debugger/rubber-duck", {
      question_id: questionId, code, language, user_thoughts: userThoughts,
    });
  }

  // ==================== Aptitude Timed Tests ====================

  async getAptitudeTestCategories() {
    return this.get("/api/aptitude-tests/categories");
  }

  async getAptitudeTestConfigurations() {
    return this.get("/api/aptitude-tests/configurations");
  }

  async startAptitudeTimedTest(category = "mixed", config = "standard", difficulty = null) {
    return this.post("/api/aptitude-tests/start", { category, config, difficulty });
  }

  async submitAptitudeTestAnswer(testId, questionIndex, answer, timeTaken = null) {
    return this.post(`/api/aptitude-tests/${testId}/answer`, {
      question_index: questionIndex, answer, time_taken: timeTaken,
    });
  }

  async completeAptitudeTimedTest(testId) {
    return this.post(`/api/aptitude-tests/${testId}/complete`);
  }

  async getAptitudeTestHistory(category = null, limit = 20) {
    const params = new URLSearchParams({ limit });
    if (category) params.append("category", category);
    return this.get(`/api/aptitude-tests/history?${params.toString()}`);
  }

  async getAptitudeTestStats() {
    return this.get("/api/aptitude-tests/stats");
  }

  async getAptitudeLeaderboard(timeframe = "all", category = null, limit = 20) {
    const params = new URLSearchParams({ timeframe, limit });
    if (category) params.append("category", category);
    return this.get(`/api/aptitude-tests/leaderboard?${params.toString()}`);
  }

  async getAptitudeMyRank() {
    return this.get("/api/aptitude-tests/leaderboard/my-rank");
  }

  // Clear memory cache (call after mutations)
  clearCache() {
    memoryCache.clear();
  }
}

const api = new ApiService();
export default api;
