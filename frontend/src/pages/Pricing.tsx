import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { Zap, Shield, Check, CreditCard, Smartphone, Rocket, GraduationCap } from "lucide-react";
import { motion } from "framer-motion";

function detectCountry() {
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (tz && (tz.startsWith("Asia/Kolkata") || tz.startsWith("Asia/Calcutta"))) return "IN";
    const lang = navigator.language || "";
    if (lang.includes("en-IN") || lang.includes("hi")) return "IN";
  } catch {}
  return "US";
}

function getPlans(isIndia, prices) {
  const usdAmt = (id, fb) => (prices && prices[id] && prices[id].usd != null ? prices[id].usd : fb);
  const inrAmt = (id, fb) => (prices && prices[id] && prices[id].inr != null ? prices[id].inr : fb);
  const usd = (id, fb) => `$${usdAmt(id, fb)}`;
  const inr = (id, fb) => `₹${inrAmt(id, fb)}`;
  return [
    {
      id: "free",
      name: "Cadet",
      price: "$0",
      priceINR: "₹0",
      period: "Forever free",
      desc: "Resets monthly. No credit card needed.",
      features: [
        "3 AI interviews / month",
        "3 resume reviews / month",
        "5 aptitude tests / month",
        "ATS score check",
        "Basic AI feedback",
      ],
      cta: "Enlist",
      className: "card",
    },
    {
      id: "pro",
      name: "Commander",
      price: isIndia ? inr("pro", 99) : usd("pro", 19),
      priceINR: isIndia ? `${inr("pro", 99)}/mo` : `${usd("pro", 19)}/mo`,
      priceUsd: `${usd("pro", 19)}/mo`,
      priceInr: `${inr("pro", 99)}/mo`,
      period: "/month",
      desc: "Cancel anytime. Instant access.",
      features: [
        "Unlimited AI interviews",
        "Unlimited resume reviews",
        "Unlimited aptitude tests",
        "ATS optimization engine",
        "Resume export (PDF & DOCX)",
        "Detailed AI feedback + scores",
        "System design practice",
        "Coding challenges",
        "Company-specific mock tests (53 companies)",
        "Priority support",
      ],
      cta: "Upgrade to Pro",
      className: "card-glow border-2 border-cyber-blue/40 relative",
      badge: "Commander",
    },
      {
        id: "yearly",
        name: "Strategist",
        price: isIndia ? inr("yearly", 899) : usd("yearly", 99),
        priceINR: isIndia ? `${inr("yearly", 899)}/yr` : `${usd("yearly", 99)}/yr`,
        priceUsd: `${usd("yearly", 99)}/yr`,
        priceInr: `${inr("yearly", 899)}/yr`,
        period: "/year",
        desc: isIndia ? "Save ₹289/yr vs monthly!" : "Save $129/yr vs monthly!",
        features: [
          "Everything in Pro",
          isIndia ? "Just ₹75/month (save 24%)" : "$8.25/month (save 57%)",
          "Unlimited all features",
          "Company-specific placement prep",
          "53 companies with real patterns",
          "576+ curated DSA/aptitude questions",
          "All future updates included",
          "Priority support",
        ],
        cta: "Get Yearly — Best Deal",
        className: "card-pro relative",
        badge: "Best Value",
      },
      {
        id: "lifetime",
        name: "Admiral",
        price: isIndia ? inr("lifetime", 1499) : usd("lifetime", 149),
        priceINR: isIndia ? `${inr("lifetime", 1499)} one-time` : `${usd("lifetime", 149)} one-time`,
        priceUsd: `${usd("lifetime", 149)} one-time`,
        priceInr: `${inr("lifetime", 1499)} one-time`,
        period: "one-time",
        desc: "Pay once. Use forever.",
        features: [
          "Everything in Pro",
          "One-time payment — never billed again",
          "Lifetime access to all current features",
          "All future updates included",
          "Priority support",
        ],
        cta: "Get Lifetime",
        className: "card-pro",
        badge: "Forever",
      },
    ];
  }

export default function Pricing() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [trialLoading, setTrialLoading] = useState(false);
  const [trialMessage, setTrialMessage] = useState("");
  const [studentEmail, setStudentEmail] = useState("");
  const [studentLoading, setStudentLoading] = useState(false);
  const [studentMessage, setStudentMessage] = useState("");
  const [studentVerified, setStudentVerified] = useState(false);
  const [country] = useState(() => detectCountry());
  const [couponCode, setCouponCode] = useState("");
  const [couponApplied, setCouponApplied] = useState(false);
  const [couponDiscount, setCouponDiscount] = useState(0);
  const [couponError, setCouponError] = useState("");
  const [serverPrices, setServerPrices] = useState<any>(null);

  const isIndia = country === "IN";

  // Prices are the single source of truth from the backend (billing.py PRICING).
  // If the fetch fails we fall back to the hardcoded values below.
  useEffect(() => {
    let active = true;
    api.getPlans().then((res) => {
      if (!active || !res) return;
      const map: Record<string, any> = {};
      res.forEach((p) => { map[p.id] = p; });
      setServerPrices(map);
    }).catch(() => {});
    return () => { active = false; };
  }, []);

  const plans = getPlans(isIndia, serverPrices);

  const handleCheckout = async (planId, seats = 1) => {
    if (!user) {
      navigate("/register");
      return;
    }
    setLoading(true);
    setError("");
    try {
      let data;
      if (planId === "lifetime") {
        data = await api.createLifetimeCheckout(country, couponCode);
      } else if (planId === "yearly") {
        data = await api.createYearlyCheckout(country, couponCode);
      } else {
        data = await api.createCheckout(country, couponCode, seats);
      }
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else if (data.stripe_checkout_url) {
        window.location.href = data.stripe_checkout_url;
      }
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleValidateCoupon = async (planId, amount) => {
    if (!couponCode.trim()) {
      setCouponApplied(false);
      setCouponDiscount(0);
      return;
    }
    try {
      const data = await api.validateCoupon(couponCode);
      if (data.valid) {
        setCouponApplied(true);
        if (data.discount_type === "percent") {
          setCouponDiscount(Math.round(amount * (data.discount_value / 100) * 100) / 100);
        } else {
          setCouponDiscount(Math.min(data.discount_value, amount));
        }
        setCouponError("");
      } else {
        setCouponApplied(false);
        setCouponDiscount(0);
        setCouponError(data.error || "Invalid coupon");
      }
    } catch (err) {
      setCouponError("Failed to validate coupon");
    }
  };

  const handleStartTrial = async () => {
    if (!user) {
      navigate("/register");
      return;
    }
    setTrialLoading(true);
    setTrialMessage("");
    try {
      await api.startTrial({});
      setTrialMessage("7-day Pro trial activated! No card required.");
      window.location.reload();
    } catch (err) {
      setTrialMessage(err.message || "Failed to start trial");
    }
    setTrialLoading(false);
  };

  const handleStudentVerify = async (e) => {
    e.preventDefault();
    if (!studentEmail.trim()) return;
    setStudentLoading(true);
    setStudentMessage("");
    try {
      const data = await (api as any).verifyStudentDiscount(studentEmail.trim());
      if (data.eligible) {
        setStudentVerified(true);
        setStudentMessage(data.message);
      } else {
        setStudentMessage(data.reason || "Not eligible for student discount");
      }
    } catch (err) {
      setStudentMessage(err.message || "Verification failed");
    }
    setStudentLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50/70 via-white to-slate-50 py-14 px-4 text-slate-800">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-10 mx-auto max-w-3xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <span className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700">Simple, transparent plans</span>
          <h1 className="mt-4 mb-4 text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">Choose the plan that helps you <span className="text-emerald-600">move forward</span></h1>
          <p className="mx-auto max-w-2xl text-base leading-7 text-slate-600">Build skills, practise for interviews, and prepare for placements at your own pace. Start free and upgrade only when you need more.</p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3 text-sm text-slate-600">
            <span className="flex items-center gap-1"><CreditCard size={12} /> Cards accepted</span>
            {isIndia && <span className="flex items-center gap-1"><Smartphone size={12} /> UPI for India</span>}
            <span className="flex items-center gap-2 rounded-full bg-white px-3 py-2 shadow-sm ring-1 ring-slate-200"><Shield size={15} className="text-emerald-600" /> Secure checkout</span>
          </div>
          {isIndia && (
            <div className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyber-green/10 border border-cyber-green/20">
              <span className="text-lg">🇮🇳</span>
              <span className="text-xs font-mono text-cyber-green">India pricing detected — special rates for Indian students</span>
            </div>
          )}
        </motion.div>

        {error && (
          <div className="mx-auto mb-6 max-w-md rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-center text-sm text-rose-700">
            {error}
          </div>
        )}

        <div className="text-center mt-4 mb-8">
          {user?.plan === "free" && (
            <button
              onClick={handleStartTrial}
              disabled={trialLoading}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-emerald-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
            >
              {trialLoading ? "Starting..." : <><Zap size={18} /> Start 7-Day Free Trial</>}
            </button>
          )}
          {trialMessage && (
            <p className={`text-sm mt-2 ${trialMessage.includes("activated") ? "text-green-600" : "text-red-600"}`}>
              {trialMessage}
            </p>
          )}
        </div>

        {!isIndia && (
          <div className="text-center mb-8">
            <form onSubmit={handleStudentVerify} className="flex flex-col sm:inline-flex sm:items-center gap-2 max-w-xs sm:max-w-none mx-auto">
              <GraduationCap size={16} className="text-gray-500" />
              <input
                type="email"
                placeholder="College email for 50% off Lifetime"
                value={studentEmail}
                onChange={(e) => setStudentEmail(e.target.value)}
                className="px-4 py-2 bg-space-panel border border-space-border rounded-lg text-sm text-gray-700 focus:border-cyber-blue focus:outline-none"
                disabled={studentVerified}
              />
              <button
                type="submit"
                disabled={studentLoading || studentVerified}
                className="px-4 py-2 bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30 rounded-lg text-sm font-medium hover:bg-cyber-blue/20 transition-colors disabled:opacity-50"
              >
                {studentLoading ? "Checking..." : studentVerified ? "Verified" : "Verify"}
              </button>
            </form>
            {studentMessage && (
              <p className={`text-xs mt-1 ${studentVerified ? "text-green-600" : "text-orange-600"}`}>
                {studentMessage}
              </p>
            )}
            <p className="text-[10px] text-gray-500 mt-1">50% off Lifetime plan for .edu / .ac.in emails</p>
          </div>
        )}

        {/* V3 §7 — ONE tier ₹99/mo. Student code STUDENT50 → ₹49/mo with .edu.in/.ac.in email. Coupon box below applies it. */}
        <div className="text-center mb-4 text-xs font-mono text-text-muted">
          Job Seeker — ₹99/mo · Students: enter <span className="font-bold text-primary">STUDENT50</span> below with your college email → ₹49/mo
        </div>
        {/* Coupon code input */}
        <div className="mx-auto mb-8 flex w-full max-w-md justify-center">
          <div className="flex w-full items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
            <input
              type="text"
              placeholder="Promo code"
              value={couponCode}
              onChange={(e) => setCouponCode(e.target.value)}
              className="min-w-0 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-emerald-500 focus:bg-white focus:ring-2 focus:ring-emerald-100"
            />
            <button
              onClick={() => {
                const plan = plans.find((p) => p.id === "pro");
                const price = isIndia ? 99 : 19;
                handleValidateCoupon("pro", price);
              }}
              className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2"
            >
              Apply
            </button>
          </div>
        </div>
        {couponError && (
          <div className="text-center mb-4 text-red-600 text-xs font-mono">{couponError}</div>
        )}
        {couponApplied && (
          <div className="text-center mb-4 text-green-600 text-xs font-mono">✓ Coupon applied — discount active</div>
        )}

        <div className="grid items-stretch gap-6 md:grid-cols-2 xl:grid-cols-4">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className={`relative flex h-full flex-col rounded-3xl border bg-white p-6 shadow-[0_12px_40px_-24px_rgba(15,23,42,0.28)] transition duration-200 hover:-translate-y-1 hover:shadow-[0_20px_50px_-24px_rgba(15,23,42,0.35)] ${plan.id === "pro" ? "border-emerald-400 ring-2 ring-emerald-100" : "border-slate-200"}`}
            >
              {plan.badge && (
                <div className={`absolute -top-3 left-1/2 -translate-x-1/2 text-space-void px-3 py-1 rounded-full text-[10px] font-display font-bold uppercase tracking-wider flex items-center gap-1 ${
                  plan.badge === "Best Value" ? "bg-cyber-green" : plan.badge === "Commander" ? "bg-cyber-blue" : plan.badge === "Forever" ? "bg-purple-500" : "bg-cyber-blue"
                }`}>
                  {plan.badge === "Commander" && <Zap size={10} />}
                  {plan.badge === "Best Value" && <Rocket size={10} />}
                  {plan.badge}
                </div>
              )}
              {plan.icon && (
                <div className="flex justify-center mb-2">
                  <plan.icon size={24} className="text-cyber-blue" />
                </div>
              )}
              <h3 className="mb-2 text-lg font-bold text-slate-900">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-1">
                <span className="text-4xl font-extrabold tracking-tight text-slate-900">
                  {plan.price}
                </span>
                {plan.period.startsWith("/") && (
                  <span className="text-sm text-slate-500">{plan.period}</span>
                )}
              </div>
              {isIndia && plan.priceInr && (
                <p className="mb-1 text-sm font-semibold text-emerald-700">🇮🇳 {plan.priceInr}</p>
              )}
              {!isIndia && plan.priceUsd && (
                <p className="text-xs text-cyber-green font-mono mb-1">{plan.priceUsd}</p>
              )}
              <p className="mb-5 min-h-10 text-sm leading-6 text-slate-600">{plan.desc}</p>
              <ul className="mb-7 flex-1 space-y-3">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm leading-5 text-slate-600">
                    <Check size={16} className="mt-0.5 shrink-0 text-emerald-600" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              <button
                onClick={() => {
                  if (plan.id === "free") {
                     navigate(user ? "/journey" : "/register");
                  } else {
                    handleCheckout(plan.id, 1);
                  }
                }}
                disabled={loading}
                className={`mt-auto w-full rounded-xl py-3 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 ${
                  plan.id === "pro" ? "btn-primary" : plan.id === "lifetime" ? "btn-pro" : plan.id === "yearly" ? "btn-pro" : "btn-secondary"
                }`}
              >
                {loading ? "Processing..." : user?.plan === plan.id ? "Current Tier" : plan.cta}
              </button>
            </motion.div>
          ))}
        </div>

        {isIndia && (
          <div className="mx-auto mt-6 max-w-md rounded-2xl border border-emerald-100 bg-emerald-50 p-5 text-center">
            <p className="text-xs font-mono text-cyber-blue mb-1">🇮🇳 India Student Special</p>
            <p className="text-xs font-mono text-gray-500">
              Lifetime plan at just <span className="text-text-primary font-bold">₹1,499 one-time</span> — less than 2 months of coffee!
            </p>
          </div>
        )}

        <div className="mt-10 flex items-center justify-center gap-2 text-center text-sm text-slate-500">
          <Shield size={14} />
          <span>Secure payments via PayPal & Stripe. Financial data never stored on servers.</span>
        </div>

        {/* FAQ */}
        <div className="mx-auto mt-14 max-w-3xl rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <h3 className="mb-6 text-center text-2xl font-bold text-slate-900">Frequently asked questions</h3>
          <div className="divide-y divide-slate-100">
            {[
              { q: "Can I cancel my subscription?", a: "Yes, cancel anytime. You keep access until the end of your billing period." },
              { q: isIndia ? "Do you accept UPI?" : "What payment methods are accepted?", a: isIndia ? "Yes! UPI, credit/debit cards, and net banking via PayPal." : "Credit/debit cards via PayPal & Stripe. Secure and encrypted." },
              { q: "What happens if I downgrade?", a: "Your data is always safe. You keep past interviews, resumes, and test results." },
              { q: isIndia ? "Is ₹99/mo really worth it?" : "Is $19/mo worth it?", a: isIndia ? "For ₹99/mo you get unlimited access to 53 companies' placement patterns, mock tests, resume optimization, and AI interviews. That's less than a movie ticket!" : "You get unlimited AI interviews, resume optimization, 53 company-specific prep guides, and more." },
              { q: "Do you offer promo codes?", a: "Yes — enter a promo code on the pricing page to apply discounts to your next purchase." },
              { q: "How many companies are covered?", a: "53 companies including TCS, Infosys, Wipro, Google, Amazon, Microsoft, Flipkart, Zomato, and more — all with real exam patterns." },
            ].map((faq) => (
              <div key={faq.q} className="py-4 first:pt-0 last:pb-0">
                <p className="font-semibold text-slate-900">{faq.q}</p>
                <p className="mt-2 text-sm leading-6 text-slate-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
