import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { Zap, Shield, Check, CreditCard, Smartphone, Rocket, GraduationCap, Users, Building2, Crown } from "lucide-react";
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

function getPlans(isIndia) {
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
        "3 cover letters / month",
        "ATS score check",
        "Basic AI feedback",
      ],
      cta: "Enlist",
      className: "card",
    },
    {
      id: "pro",
      name: "Commander",
      price: isIndia ? "₹99" : "$19",
      priceINR: isIndia ? "₹99/mo" : "$19/mo",
      priceUsd: "$19/mo",
      priceInr: "₹99/mo",
      period: "/month",
      desc: "Cancel anytime. Instant access.",
      features: [
        "Unlimited AI interviews",
        "Unlimited resume reviews",
        "Unlimited aptitude tests",
        "Unlimited cover letters",
        "ATS optimization engine",
        "Resume export (PDF & DOCX)",
        "Detailed AI feedback + scores",
        "System design practice",
        "Coding challenges",
        "Salary negotiation coach",
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
      price: isIndia ? "₹499" : "$49",
      priceINR: isIndia ? "₹499/yr" : "$49/yr",
      priceUsd: "$49/yr",
      priceInr: "₹499/yr",
      period: "/year",
      desc: isIndia ? "Save ₹689/yr vs monthly!" : "Save $179/yr vs monthly!",
      features: [
        "Everything in Pro",
        isIndia ? "Just ₹41/month (save 59%)" : "$4.08/month (save 78%)",
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
      price: isIndia ? "₹499" : "$49",
      priceINR: isIndia ? "₹499 one-time" : "$49 one-time",
      priceUsd: "$49 one-time",
      priceInr: "₹499 one-time",
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
    {
      id: "team",
      name: "Command Squad",
      price: isIndia ? "₹2,499" : "$29",
      priceINR: isIndia ? "₹2,499/mo" : "$29/mo",
      priceUsd: "$29/mo",
      priceInr: "₹2,499/mo",
      period: "/month per seat",
      desc: "5–50 seats. Perfect for teams.",
      icon: Users,
      features: [
        "Everything in Pro",
        "5–50 team members",
        "Team dashboard & analytics",
        "Bulk invitations",
        "Custom roles & permissions",
        "Usage analytics per member",
        "All future updates included",
        "Priority support",
      ],
      cta: "Get Team Plan",
      className: "card-pro relative",
      badge: "Teams",
    },
    {
      id: "enterprise",
      name: "Executive Suite",
      price: isIndia ? "₹8,299" : "$99",
      priceINR: isIndia ? "₹8,299/mo" : "$99/mo",
      priceUsd: "$99/mo",
      priceInr: "₹8,299/mo",
      period: "/month per seat",
      desc: "Unlimited seats. White-label. API access.",
      icon: Building2,
      features: [
        "Everything in Team",
        "Unlimited seats (10+)",
        "White-label platform",
        "API access for integrations",
        "Custom branding & SSO",
        "Dedicated account manager",
        "24/7 priority support",
        "SLA guarantee",
        "Custom training for team",
      ],
      cta: "Contact Sales",
      className: "card-pro relative",
      badge: "Enterprise",
      isEnterprise: true,
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

  const isIndia = country === "IN";
  const plans = getPlans(isIndia);

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
      } else if (planId === "team") {
        data = await api.createTeamCheckout(country, seats, couponCode);
      } else if (planId === "enterprise") {
        data = await api.createEnterpriseCheckout(country, seats, couponCode);
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
      const data = await api.verifyStudentDiscount(studentEmail.trim());
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
    <div className="min-h-screen py-16 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <span className="section-subheader mb-3 block">Mission Tiers</span>
          <h1 className="section-header text-4xl mb-4">Command <span className="text-cyber-blue">Clearance</span></h1>
          <p className="text-gray-400 font-mono text-sm">
            Start free. Upgrade when ready. Cancel anytime.
          </p>
          <div className="flex items-center justify-center gap-4 mt-4 text-xs font-mono text-gray-500 flex-wrap">
            <span className="flex items-center gap-1"><CreditCard size={12} /> Cards accepted</span>
            {isIndia && <span className="flex items-center gap-1"><Smartphone size={12} /> UPI for India</span>}
            <span className="flex items-center gap-1"><Shield size={12} /> 2M ARR goal — enterprise-grade</span>
          </div>
          {isIndia && (
            <div className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyber-green/10 border border-cyber-green/20">
              <span className="text-lg">🇮🇳</span>
              <span className="text-xs font-mono text-cyber-green">India pricing detected — special rates for Indian students</span>
            </div>
          )}
        </motion.div>

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center max-w-md mx-auto font-mono text-sm">
            {error}
          </div>
        )}

        <div className="text-center mt-4 mb-8">
          {user?.plan === "free" && (
            <button
              onClick={handleStartTrial}
              disabled={trialLoading}
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-text-primary rounded-xl font-semibold hover:shadow-lg transition-all"
            >
              {trialLoading ? "Starting..." : <><Zap size={18} /> Start 7-Day Free Trial</>}
            </button>
          )}
          {trialMessage && (
            <p className={`text-sm mt-2 ${trialMessage.includes("activated") ? "text-green-400" : "text-red-400"}`}>
              {trialMessage}
            </p>
          )}
        </div>

        {!isIndia && (
          <div className="text-center mb-8">
            <form onSubmit={handleStudentVerify} className="flex flex-col sm:inline-flex sm:items-center gap-2 max-w-xs sm:max-w-none mx-auto">
              <GraduationCap size={16} className="text-gray-400" />
              <input
                type="email"
                placeholder="College email for 50% off Lifetime"
                value={studentEmail}
                onChange={(e) => setStudentEmail(e.target.value)}
                className="px-4 py-2 bg-space-panel border border-space-border rounded-lg text-sm text-gray-200 focus:border-cyber-blue focus:outline-none"
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
              <p className={`text-xs mt-1 ${studentVerified ? "text-green-400" : "text-orange-400"}`}>
                {studentMessage}
              </p>
            )}
            <p className="text-[10px] text-gray-500 mt-1">50% off Lifetime plan for .edu / .ac.in emails</p>
          </div>
        )}

        {/* Coupon code input */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center gap-2 max-w-sm w-full">
            <input
              type="text"
              placeholder="Promo code"
              value={couponCode}
              onChange={(e) => setCouponCode(e.target.value)}
              className="flex-1 px-4 py-2 bg-space-panel border border-space-border rounded-lg text-sm text-gray-200 focus:border-cyber-blue focus:outline-none font-mono"
            />
            <button
              onClick={() => {
                const plan = plans.find((p) => p.id === "pro");
                const price = isIndia ? 99 : 19;
                handleValidateCoupon("pro", price);
              }}
              className="px-4 py-2 bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30 rounded-lg text-sm font-medium hover:bg-cyber-blue/20 transition-colors"
            >
              Apply
            </button>
          </div>
        </div>
        {couponError && (
          <div className="text-center mb-4 text-red-400 text-xs font-mono">{couponError}</div>
        )}
        {couponApplied && (
          <div className="text-center mb-4 text-green-400 text-xs font-mono">✓ Coupon applied — discount active</div>
        )}

        <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-4">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className={`${plan.className} flex flex-col`}
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
              <h3 className="font-display font-bold text-text-primary text-sm mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-1">
                <span className="text-2xl font-display font-black text-text-primary">
                  {plan.price}
                </span>
                {plan.period.startsWith("/") && (
                  <span className="text-xs font-mono text-gray-500">{plan.period}</span>
                )}
              </div>
              {isIndia && plan.priceInr && (
                <p className="text-xs text-cyber-green font-mono mb-1">🇮🇳 {plan.priceInr}</p>
              )}
              {!isIndia && plan.priceUsd && (
                <p className="text-xs text-cyber-green font-mono mb-1">{plan.priceUsd}</p>
              )}
              <p className="text-gray-500 text-xs font-mono mb-4">{plan.desc}</p>
              <ul className="space-y-2 mb-6 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-gray-400 text-xs">
                    <Check size={12} className="text-cyber-green mt-0.5 shrink-0" />
                    <span className="font-mono">{f}</span>
                  </li>
                ))}
              </ul>
              <button
                onClick={() => {
                  if (plan.id === "free") {
                    navigate(user ? "/dashboard" : "/register");
                  } else if (plan.id === "enterprise") {
                    navigate("/enterprise-contact");
                  } else {
                    const seats = plan.id === "team" ? 5 : 1;
                    handleCheckout(plan.id, seats);
                  }
                }}
                disabled={loading}
                className={`w-full ${
                  plan.id === "pro" ? "btn-primary" : plan.id === "lifetime" ? "btn-pro" : plan.id === "yearly" ? "btn-pro" : plan.isEnterprise ? "btn-enterprise" : plan.id === "team" ? "btn-team" : "btn-secondary"
                }`}
              >
                {loading ? "Processing..." : user?.plan === plan.id ? "Current Tier" : plan.cta}
              </button>
            </motion.div>
          ))}
        </div>

        {isIndia && (
          <div className="text-center mt-6 bg-space-panel/80 border border-space-border rounded-xl p-4 max-w-md mx-auto">
            <p className="text-xs font-mono text-cyber-blue mb-1">🇮🇳 India Student Special</p>
            <p className="text-xs font-mono text-gray-400">
              Lifetime plan at just <span className="text-text-primary font-bold">₹499 one-time</span> — less than 2 months of coffee!
            </p>
          </div>
        )}

        <div className="text-center mt-10 text-gray-500 flex items-center justify-center gap-2 text-xs font-mono">
          <Shield size={14} />
          <span>Secure payments via PayPal & Stripe. Financial data never stored on servers.</span>
        </div>

        {/* FAQ */}
        <div className="mt-12 bg-space-panel/80 border border-space-border rounded-2xl p-8 max-w-3xl mx-auto">
          <h3 className="font-display font-bold text-text-primary text-lg mb-4 text-center">Mission Briefing</h3>
          <div className="space-y-4">
            {[
              { q: "Can I cancel my subscription?", a: "Yes, cancel anytime. You keep access until the end of your billing period." },
              { q: isIndia ? "Do you accept UPI?" : "What payment methods are accepted?", a: isIndia ? "Yes! UPI, credit/debit cards, and net banking via PayPal." : "Credit/debit cards via PayPal & Stripe. Secure and encrypted." },
              { q: "What happens if I downgrade?", a: "Your data is always safe. You keep past interviews, resumes, and test results." },
              { q: isIndia ? "Is ₹99/mo really worth it?" : "Is $19/mo worth it?", a: isIndia ? "For ₹99/mo you get unlimited access to 53 companies' placement patterns, mock tests, resume optimization, and AI interviews. That's less than a movie ticket!" : "You get unlimited AI interviews, resume optimization, 53 company-specific prep guides, and more." },
              { q: "Do you have team and enterprise plans?", a: "Yes — Team plans start at $29/seat/month (min 5 seats). Enterprise plans start at $99/seat/month with white-label, API access, and dedicated support." },
              { q: "Do you offer promo codes?", a: "Yes — enter a promo code on the pricing page to apply discounts to your next purchase." },
              { q: "How many companies are covered?", a: "53 companies including TCS, Infosys, Wipro, Google, Amazon, Microsoft, Flipkart, Zomato, and more — all with real exam patterns." },
            ].map((faq) => (
              <div key={faq.q}>
                <p className="font-display font-bold text-text-primary text-sm">{faq.q}</p>
                <p className="text-gray-500 font-mono text-xs mt-1">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
