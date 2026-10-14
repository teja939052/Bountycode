// @ts-nocheck
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { User, Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";
import useAuthStore from "../store/authStore";
import { authApi } from "../services/api/auth";
import { validateForm } from "../utils/validation";
import { getStartBrief, briefToOnboardingPayload } from "../utils/startBrief";
import { authApi as authApiDirect } from "../services/api/auth";
import { PageShell } from "../design-system/PageShell";
import { Button } from "../design-system/Button";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const handler = () => setReducedMotion(mq.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});
    const errs = validateForm([
      { name: "name", value: name, rules: [{ type: "required", message: "Name is required" }] },
      { name: "email", value: email, rules: [{ type: "required", message: "Email is required" }, { type: "email" }] },
      { name: "password", value: password, rules: [{ type: "required", message: "Password is required" }, { type: "minLength", value: 8 }, { type: "password" }] },
    ]);
    if (errs) { setFieldErrors(errs); return; }
    setLoading(true);
    try {
      const data = await authApi.register(email, password, name);
      setAuth(data.user);
      const brief = getStartBrief();
      if (brief) {
        try {
          await authApiDirect.onboardingComplete(briefToOnboardingPayload(brief) as never);
        } catch {
          /* onboarding still reachable via /onboarding */
        }
        if (brief.intent === "diagnostic") {
          navigate("/placement");
        } else if (brief.track === "learn" || brief.track === "explore") {
          navigate("/placement");
        } else {
          navigate("/placement");
        }
        return;
      }
      navigate("/placement");
    } catch (err: any) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageShell theme="spring">
      <div className="flex min-h-screen items-center justify-center p-4">
        <motion.div
          initial={reducedMotion ? {} : { opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          <div className="rounded-2xl border border-border bg-surface p-6 shadow-soft-lg">
            <div className="text-center mb-8">
              <h1 className="font-display text-2xl font-extrabold text-text">
                Create your account
              </h1>
              <p className="mt-2 text-sm text-text-muted">
                Start learning. We will guide the rest.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="rounded-xl border border-error/20 bg-error/5 px-4 py-3 text-sm text-error">
                  {error}
                </div>
              )}

              <div>
                <label htmlFor="register-name" className="block text-sm font-medium text-text mb-1.5">
                  Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-dim" />
                  <input
                    id="register-name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Your name"
                    className="w-full pl-12 pr-4 py-3 rounded-xl border border-border bg-surface text-text placeholder-text-dim focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all outline-none text-sm"
                    required
                  />
                </div>
                {fieldErrors.name && <p className="text-error text-xs mt-1">{fieldErrors.name}</p>}
              </div>

              <div>
                <label htmlFor="register-email" className="block text-sm font-medium text-text mb-1.5">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-dim" />
                  <input
                    id="register-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full pl-12 pr-4 py-3 rounded-xl border border-border bg-surface text-text placeholder-text-dim focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all outline-none text-sm"
                    required
                  />
                </div>
                {fieldErrors.email && <p className="text-error text-xs mt-1">{fieldErrors.email}</p>}
              </div>

              <div>
                <label htmlFor="register-password" className="block text-sm font-medium text-text mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-dim" />
                  <input
                    id="register-password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Min 8 characters"
                    className="w-full pl-12 pr-12 py-3 rounded-xl border border-border bg-surface text-text placeholder-text-dim focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all outline-none text-sm"
                    minLength={8}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-text-dim hover:text-text transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {fieldErrors.password && <p className="text-error text-xs mt-1">{fieldErrors.password}</p>}
              </div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                fullWidth
                loading={loading}
                rightIcon={<ArrowRight size={16} />}
              >
                Create account
              </Button>
            </form>

            <p className="mt-6 text-center text-sm text-text-muted">
              Already have an account?{" "}
              <Link to="/login" className="text-primary font-semibold hover:underline">
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </PageShell>
  );
}
