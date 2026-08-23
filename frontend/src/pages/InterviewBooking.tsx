import { useState, useEffect, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import {
  Calendar, Clock, Plus, X, ChevronLeft, ChevronRight,
  CheckCircle2, XCircle, AlertCircle, Zap, Trophy, Star,
  Target, ArrowRight, RotateCcw, Trash2, Bell, ChevronDown,
  Filter, Search, CalendarClock, Award, Flame as Fire, TrendingUp,
} from "lucide-react";

const INTERVIEW_TYPES = [
  { id: "technical", label: "Technical", color: "bg-cyber-green/10 text-cyber-green border-cyber-green/30", icon: "⚡" },
  { id: "behavioral", label: "Behavioral", color: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30", icon: "💬" },
  { id: "system_design", label: "System Design", color: "bg-cyber-purple/10 text-cyber-purple border-cyber-purple/30", icon: "🏗️" },
  { id: "hr", label: "HR", color: "bg-cyber-yellow/10 text-cyber-yellow border-cyber-yellow/30", icon: "🎯" },
  { id: "full_round", label: "Full Round", color: "bg-cyber-red/10 text-cyber-red border-cyber-red/30", icon: "🔥" },
];

const DURATIONS = [
  { id: 15, label: "15 min" },
  { id: 30, label: "30 min" },
  { id: 45, label: "45 min" },
  { id: 60, label: "60 min" },
];

const COMPANIES = [
  "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Tesla", "Nvidia",
  "Twitter/X", "LinkedIn", "Stripe", "Uber", "Airbnb", "Spotify", "Pinterest",
  "Snapchat", "TikTok", "Discord", "Slack", "Notion", "Atlassian", "Salesforce",
  "Oracle", "SAP", "IBM", "Intel", "AMD", "Qualcomm", "Broadcom", "Palantir",
  "SpaceX", "Goldman Sachs", "JPMorgan", "Morgan Stanley", "Citadel", "Two Sigma",
  "Jane Street", "Bloomberg", "TCS", "Infosys", "Wipro", "Cognizant", "HCL Tech",
  "Tech Mahindra", "L&T Infotech", "Mphasis", "Hexaware", "Accenture", "Capgemini",
  "Deloitte", "Ernst & Young", "KPMG", "PwC", "Zomato", "Razorpay", "Flipkart",
  "Swiggy", "PhonePe", "Paytm", "Adobe", "Shopify", "Twilio", "Databricks",
  "Snowflake", "Datadog", "Cloudflare", "Vercel", "Supabase",
];

const ROLES = [
  "Software Engineer", "Senior Software Engineer", "Staff Engineer", "Principal Engineer",
  "Product Manager", "Senior Product Manager", "Engineering Manager", "Tech Lead",
  "Data Scientist", "Senior Data Scientist", "ML Engineer", "Data Engineer",
  "UX Designer", "Senior UX Designer", "Product Designer", "Design Lead",
  "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
  "Business Analyst", "Consultant", "Solution Architect", "Security Engineer",
  "Mobile Engineer", "iOS Engineer", "Android Engineer", "Frontend Engineer",
  "Backend Engineer", "Full Stack Engineer", "QA Engineer", "Tech Writer",
];

const STATUS_COLORS = {
  scheduled: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30",
  in_progress: "bg-cyber-orange/10 text-cyber-orange border-cyber-orange/30",
  completed: "bg-cyber-green/10 text-cyber-green border-cyber-green/30",
  cancelled: "bg-surface-card/30 text-brand-muted border-brand-primary/10",
  no_show: "bg-cyber-red/10 text-cyber-red border-cyber-red/30",
};

const STATUS_ICONS = {
  scheduled: Bell,
  in_progress: Zap,
  completed: CheckCircle2,
  cancelled: XCircle,
  no_show: AlertCircle,
};

function ScoreBadge({ score }) {
  if (score === null || score === undefined) return null;
  const colors = score >= 8 ? "text-cyber-green" : score >= 5 ? "text-cyber-yellow" : "text-cyber-red";
  const bgColors = score >= 8 ? "bg-cyber-green/10" : score >= 5 ? "bg-cyber-yellow/10" : "bg-cyber-red/10";
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold ${colors} ${bgColors} border`}>
      <Star size={10} />
      {score}/10
    </span>
  );
}

export default function InterviewBooking() {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState("book");
  const [historyTab, setHistoryTab] = useState("completed");

  const [bookings, setBookings] = useState([]);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [slotsLoading, setSlotsLoading] = useState(false);

  const [showBookingForm, setShowBookingForm] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [bookingError, setBookingError] = useState(null);

  const [formData, setFormData] = useState({
    type: "technical",
    date: "",
    time: "",
    duration_minutes: 30,
    company_target: "",
    role_target: "",
    notes: "",
  });

  const loadData = useCallback(async () => {
    try {
      const [upcomingRes, historyRes, statsRes] = await Promise.all([
        api.booking.getUpcomingBookings(),
        api.booking.getBookingHistory(1, 20),
        api.booking.getBookingStats(),
      ]);
      setBookings(upcomingRes.bookings || []);
      setHistory(historyRes.bookings || []);
      setStats(statsRes);
    } catch (err) {
      console.error("Failed to load booking data:", err);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const fetchSlots = useCallback(async (date, type) => {
    if (!date) return;
    setSlotsLoading(true);
    try {
      const res = await api.booking.getAvailableSlots(date, type || formData.type);
      setAvailableSlots(res.available_slots || []);
    } catch (err) {
      console.error("Failed to fetch slots:", err);
    } finally {
      setSlotsLoading(false);
    }
  }, [formData.type]);

  useEffect(() => {
    if (formData.date) {
      fetchSlots(formData.date, formData.type);
    } else {
      setAvailableSlots([]);
    }
  }, [formData.date, formData.type]);

  const handleBook = async () => {
    if (!formData.date || !formData.time || submitting) {
      return;
    }

    const scheduledAt = new Date(`${formData.date}T${formData.time}:00`);
    const payload = {
      type: formData.type,
      scheduled_at: scheduledAt.toISOString(),
      duration_minutes: formData.duration_minutes,
      company_target: formData.company_target || null,
      role_target: formData.role_target || null,
      notes: formData.notes,
    };

    setSubmitting(true);
    setBookingError(null);
    try {
      const res = await api.booking.bookInterview(payload);
      setShowConfirmModal(false);
      setFormData({
        type: "technical",
        date: "",
        time: "",
        duration_minutes: 30,
        company_target: "",
        role_target: "",
        notes: "",
      });
      setSelectedSlot(null);
      await loadData();
    } catch (err) {
      console.error("Booking failed:", err);
      const detail = err?.message || "Failed to book the interview. Please try again.";
      setBookingError(detail);
      if (err?.status === 429 || detail === "Duplicate request") {
        await loadData();
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleStart = async (bookingId) => {
    try {
      await api.booking.startBooking(bookingId);
      await loadData();
    } catch (err) {
      console.error("Failed to start booking:", err);
    }
  };

  const handleCancel = async (bookingId) => {
    try {
      await api.booking.cancelBooking(bookingId);
      await loadData();
    } catch (err) {
      console.error("Failed to cancel booking:", err);
    }
  };

  const handleSubmitAnswers = async (bookingId, answers) => {
    try {
      const res = await api.booking.submitBookingAnswers(bookingId, answers);
      await loadData();
      return res;
    } catch (err) {
      console.error("Failed to submit answers:", err);
      throw err;
    }
  };

  const formattedDate = useMemo(() => {
    if (!formData.date) return "";
    const d = new Date(formData.date + "T00:00:00");
    return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
  }, [formData.date]);

  const selectedSlotInfo = useMemo(() => {
    if (!selectedSlot) return null;
    const slot = availableSlots.find(
      (s) => s.time === (formData.date ? `${formData.time}` : null) || s.time === selectedSlot.time
    );
    return slot;
  }, [selectedSlot, availableSlots, formData.date, formData.time]);

  const canCancel = (booking) => {
    if (booking.status !== "scheduled") return false;
    const scheduledAt = new Date(booking.scheduled_at);
    const now = new Date();
    const diff = scheduledAt.getTime() - now.getTime();
    return diff > 3600000;
  };

  const canJoin = (booking) => {
    if (booking.status !== "in_progress") return false;
    const scheduledAt = new Date(booking.scheduled_at);
    const now = new Date();
    const diff = Math.abs(now.getTime() - scheduledAt.getTime());
    return diff < 3600000 * 2;
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-display font-extrabold text-text-primary">
                Mock Interview <span className="text-brand-sky">Booking</span>
              </h1>
              <p className="text-brand-secondary mt-1">Schedule, attend, and review AI-powered mock interviews</p>
            </div>
            <button
              onClick={() => setShowBookingForm(!showBookingForm)}
              className="btn-primary px-5 py-2.5 text-sm flex items-center gap-2"
            >
              <Plus size={16} />
              Book New
            </button>
          </div>

          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-xl bg-cyber-blue/10 flex items-center justify-center">
                    <Target size={18} className="text-cyber-blue" />
                  </div>
                  <span className="text-[11px] font-mono uppercase tracking-[0.15em] text-text-light">Total Booked</span>
                </div>
                <div className="text-2xl font-display font-bold text-text-primary">{stats.total_booked}</div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-xl bg-cyber-green/10 flex items-center justify-center">
                    <CheckCircle2 size={18} className="text-cyber-green" />
                  </div>
                  <span className="text-[11px] font-mono uppercase tracking-[0.15em] text-text-light">Completed</span>
                </div>
                <div className="text-2xl font-display font-bold text-text-primary">{stats.completed}</div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-xl bg-cyber-yellow/10 flex items-center justify-center">
                    <Star size={18} className="text-cyber-yellow" />
                  </div>
                  <span className="text-[11px] font-mono uppercase tracking-[0.15em] text-text-light">Avg Score</span>
                </div>
                <div className="text-2xl font-display font-bold text-text-primary">{stats.avg_score.toFixed(1)}</div>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-10 h-10 rounded-xl bg-cyber-orange/10 flex items-center justify-center">
                    <Fire size={18} className="text-cyber-orange" />
                  </div>
                  <span className="text-[11px] font-mono uppercase tracking-[0.15em] text-text-light">Streak</span>
                </div>
                <div className="text-2xl font-display font-bold text-text-primary">{stats.streak_days}d</div>
              </motion.div>
            </div>
          )}

          <AnimatePresence mode="wait">
            {showBookingForm && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-6 mb-8 overflow-hidden"
              >
                <h3 className="text-lg font-display font-bold text-text-primary mb-6">Schedule a Mock Interview</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Interview Type</label>
                    <select
                      value={formData.type}
                      onChange={(e) => setFormData((prev) => ({ ...prev, type: e.target.value }))}
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                    >
                      {INTERVIEW_TYPES.map((t) => (
                        <option key={t.id} value={t.id}>{t.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Duration</label>
                    <div className="flex gap-2">
                      {DURATIONS.map((d) => (
                        <button
                          key={d.id}
                          onClick={() => setFormData((prev) => ({ ...prev, duration_minutes: d.id }))}
                          className={`flex-1 py-2.5 rounded-xl text-sm font-medium border transition-all ${
                            formData.duration_minutes === d.id
                              ? "border-brand-sky bg-brand-sky/10 text-brand-sky"
                              : "border-brand-primary/10 bg-surface-card/30 text-brand-secondary hover:border-brand-sky/30"
                          }`}
                        >
                          {d.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Date</label>
                    <input
                      type="date"
                      value={formData.date}
                      onChange={(e) => setFormData((prev) => ({ ...prev, date: e.target.value, time: "" }))}
                      min={new Date().toISOString().split("T")[0]}
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Time</label>
                    {slotsLoading ? (
                      <div className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-light">Loading slots...</div>
                    ) : availableSlots.length > 0 ? (
                      <select
                        value={formData.time}
                        onChange={(e) => setFormData((prev) => ({ ...prev, time: e.target.value }))}
                        className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                      >
                        <option value="">Select a time slot</option>
                        {availableSlots
                          .filter((s) => s.duration === formData.duration_minutes)
                          .map((s) => (
                            <option key={s.time} value={s.time}>{s.time} ({s.duration} min)</option>
                          ))}
                      </select>
                    ) : (
                      <select
                        value={formData.time}
                        onChange={(e) => setFormData((prev) => ({ ...prev, time: e.target.value }))}
                        className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                      >
                        <option value="">Select a time</option>
                        {Array.from({ length: 11 }, (_, i) => {
                          const h = 9 + i;
                          const time = `${h.toString().padStart(2, "0")}:00`;
                          return <option key={time} value={time}>{time}</option>;
                        })}
                      </select>
                    )}
                  </div>

                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Target Company (optional)</label>
                    <select
                      value={formData.company_target}
                      onChange={(e) => setFormData((prev) => ({ ...prev, company_target: e.target.value }))}
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                    >
                      <option value="">None</option>
                      {COMPANIES.map((c) => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Target Role (optional)</label>
                    <select
                      value={formData.role_target}
                      onChange={(e) => setFormData((prev) => ({ ...prev, role_target: e.target.value }))}
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all"
                    >
                      <option value="">None</option>
                      {ROLES.map((r) => (
                        <option key={r} value={r}>{r}</option>
                      ))}
                    </select>
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-[11px] font-mono uppercase tracking-[0.15em] text-text-light mb-2">Notes</label>
                    <textarea
                      value={formData.notes}
                      onChange={(e) => setFormData((prev) => ({ ...prev, notes: e.target.value }))}
                      rows={3}
                      placeholder="Add any notes or focus areas for this interview..."
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-3 text-sm text-text-primary focus:outline-none focus:border-brand-sky/50 focus:ring-1 focus:ring-brand-sky/20 transition-all resize-none"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-brand-primary/5">
                  <button
                    onClick={() => {
                      setShowBookingForm(false);
                      setFormData({
                        type: "technical",
                        date: "",
                        time: "",
                        duration_minutes: 30,
                        company_target: "",
                        role_target: "",
                        notes: "",
                      });
                      setSelectedSlot(null);
                    }}
                    className="px-5 py-2.5 rounded-xl border border-brand-primary/10 bg-surface-card/30 text-sm font-medium text-brand-secondary hover:text-white transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => {
                      if (!formData.date || !formData.time) {
                        return;
                      }
                      setShowConfirmModal(true);
                    }}
                    className="btn-primary px-5 py-2.5 text-sm flex items-center gap-2"
                  >
                    <Calendar size={14} />
                    Review Booking
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {showConfirmModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm"
              onClick={() => setShowConfirmModal(false)}
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.95, opacity: 0 }}
                className="rounded-2xl border border-brand-primary/10 bg-surface-card p-6 max-w-md w-full mx-4 shadow-soft-xl"
                onClick={(e) => e.stopPropagation()}
              >
                <h3 className="text-lg font-display font-bold text-text-primary mb-4">Confirm Booking</h3>

                <div className="space-y-3 mb-6">
                  <div className="flex justify-between text-sm">
                    <span className="text-text-light">Type</span>
                    <span className="text-text-primary font-medium">{formData.type.replace("_", " ")}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-light">Date & Time</span>
                    <span className="text-text-primary font-medium">{formattedDate} at {formData.time}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-text-light">Duration</span>
                    <span className="text-text-primary font-medium">{formData.duration_minutes} minutes</span>
                  </div>
                  {formData.company_target && (
                    <div className="flex justify-between text-sm">
                      <span className="text-text-light">Company</span>
                      <span className="text-text-primary font-medium">{formData.company_target}</span>
                    </div>
                  )}
                  {formData.role_target && (
                    <div className="flex justify-between text-sm">
                      <span className="text-text-light">Role</span>
                      <span className="text-text-primary font-medium">{formData.role_target}</span>
                    </div>
                  )}
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => setShowConfirmModal(false)}
                    disabled={submitting}
                    className="flex-1 px-4 py-2.5 rounded-xl border border-brand-primary/10 bg-surface-card/30 text-sm font-medium text-brand-secondary hover:text-white transition-colors disabled:opacity-50"
                  >
                    Back
                  </button>
                  <button
                    onClick={handleBook}
                    disabled={submitting}
                    className="flex-1 btn-primary px-4 py-2.5 text-sm flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
                  >
                    <CheckCircle2 size={14} />
                    {submitting ? "Booking..." : "Confirm Booking"}
                  </button>
                </div>
                {bookingError && (
                  <div className="mt-3 rounded-lg border border-cyber-red/30 bg-cyber-red/10 px-3 py-2 text-xs text-cyber-red">
                    {bookingError}
                  </div>
                )}
              </motion.div>
            </motion.div>
          )}

          <div className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 overflow-hidden">
            <div className="flex border-b border-brand-primary/5">
              <button
                onClick={() => setActiveTab("book")}
                className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                  activeTab === "book"
                    ? "text-brand-sky border-b-2 border-brand-sky bg-brand-sky/5"
                    : "text-text-light hover:text-white"
                }`}
              >
                Upcoming ({bookings.length})
              </button>
              <button
                onClick={() => setActiveTab("history")}
                className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
                  activeTab === "history"
                    ? "text-brand-sky border-b-2 border-brand-sky bg-brand-sky/5"
                    : "text-text-light hover:text-white"
                }`}
              >
                History
              </button>
            </div>

            {activeTab === "book" ? (
              <div className="p-6">
                {bookings.length === 0 ? (
                  <div className="text-center py-12">
                    <CalendarClock size={48} className="mx-auto text-text-light/30 mb-4" />
                    <p className="text-brand-secondary text-sm">No upcoming interviews</p>
                    <button
                      onClick={() => {
                        setShowBookingForm(true);
                        setActiveTab("book");
                      }}
                      className="mt-4 btn-primary px-5 py-2.5 text-sm"
                    >
                      Book Your First Interview
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {bookings.map((booking) => {
                      const StatusIcon = STATUS_ICONS[booking.status] || Bell;
                      return (
                        <motion.div
                          key={booking.id || booking.booking_id}
                          whileHover={{ scale: 1.005 }}
                          className="rounded-xl border border-white/8 bg-white border-border/3 p-5 flex flex-col sm:flex-row sm:items-center gap-4"
                        >
                          <div className="flex items-center gap-4 flex-1 min-w-0">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center border ${STATUS_COLORS[booking.status] || STATUS_COLORS.scheduled}`}>
                              <StatusIcon size={18} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase tracking-wider border ${STATUS_COLORS[booking.status] || STATUS_COLORS.scheduled}`}>
                                  {booking.status}
                                </span>
                                <span className="text-sm font-medium text-text-primary">{booking.type?.replace("_", " ")}</span>
                              </div>
                              <div className="flex items-center gap-4 mt-1 text-xs text-text-light">
                                <span className="flex items-center gap-1"><Calendar size={12} />{booking.scheduled_at ? new Date(booking.scheduled_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : ""}</span>
                                <span className="flex items-center gap-1"><Clock size={12} />{booking.duration_minutes || 30} min</span>
                                {booking.company_target && <span className="flex items-center gap-1"><Target size={12} />{booking.company_target}</span>}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {canJoin(booking) && (
                              <button
                                onClick={() => handleStart(booking.id || booking.booking_id)}
                                className="px-4 py-2 rounded-xl bg-cyber-green/10 text-cyber-green text-sm font-medium border border-cyber-green/20 hover:bg-cyber-green/20 transition-colors"
                              >
                                Join
                              </button>
                            )}
                            {canCancel(booking) && (
                              <button
                                onClick={() => handleCancel(booking.id || booking.booking_id)}
                                className="px-4 py-2 rounded-xl border border-cyber-red/20 bg-cyber-red/5 text-cyber-red text-sm font-medium hover:bg-cyber-red/10 transition-colors"
                              >
                                Cancel
                              </button>
                            )}
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </div>
            ) : (
              <div className="p-6">
                <div className="flex items-center gap-2 mb-4 border-b border-brand-primary/5 pb-4">
                  {["completed", "cancelled", "no_show", "all"].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setHistoryTab(tab)}
                      className={`px-4 py-2 rounded-lg text-xs font-mono uppercase tracking-wider transition-colors ${
                        historyTab === tab
                          ? "bg-brand-sky/10 text-brand-sky border border-brand-sky/20"
                          : "text-text-light hover:text-white"
                      }`}
                    >
                      {tab === "all" ? "All" : tab.replace("_", " ")}
                    </button>
                  ))}
                </div>

                {history.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-brand-secondary text-sm">No history found</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {history.map((booking) => (
                      <motion.div
                        key={booking.id || booking.booking_id}
                        whileHover={{ scale: 1.005 }}
                        className="rounded-xl border border-white/8 bg-white border-border/3 p-4 flex flex-col sm:flex-row sm:items-center gap-4"
                      >
                        <div className="flex items-center gap-4 flex-1 min-w-0">
                            <div className="w-10 h-10 rounded-xl bg-surface-card/30 flex items-center justify-center border border-brand-primary/10">
                              {(() => {
                                const IconComp = STATUS_ICONS[booking.status];
                                return IconComp ? <IconComp size={16} /> : <Bell size={16} />;
                              })()}
                            </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-sm font-medium text-text-primary">{booking.type?.replace("_", " ")}</span>
                              <ScoreBadge score={booking.overall_score} />
                            </div>
                            <div className="flex items-center gap-3 mt-1 text-xs text-text-light">
                              <span>{booking.scheduled_at ? new Date(booking.scheduled_at).toLocaleDateString() : ""}</span>
                              {booking.duration_minutes && <span>{booking.duration_minutes} min</span>}
                              {booking.company_target && <span>{booking.company_target}</span>}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {booking.status === "completed" && (
                            <>
                              <button
                                onClick={() => {
                                  if (booking.id || booking.booking_id) {
                                    api.booking.getBookingDetail(booking.id || booking.booking_id);
                                  }
                                }}
                                className="px-3 py-1.5 rounded-lg border border-brand-primary/10 bg-surface-card/30 text-xs font-medium text-brand-secondary hover:text-white transition-colors"
                              >
                                Review
                              </button>
                              <button
                                onClick={() => {
                                  if (booking.id || booking.booking_id) {
                                    handleStart(booking.id || booking.booking_id);
                                  }
                                }}
                                className="px-3 py-1.5 rounded-lg bg-cyber-green/10 text-cyber-green text-xs font-medium border border-cyber-green/20 hover:bg-cyber-green/20 transition-colors flex items-center gap-1"
                              >
                                <RotateCcw size={10} />
                                Retry
                              </button>
                            </>
                          )}
                          <button
                            onClick={() => {
                              if (booking.id || booking.booking_id) {
                                api.booking.getBookingDetail(booking.id || booking.booking_id);
                              }
                            }}
                            className="px-3 py-1.5 rounded-lg border border-brand-primary/10 bg-surface-card/30 text-xs font-medium text-brand-secondary hover:text-white transition-colors"
                          >
                            View
                          </button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}