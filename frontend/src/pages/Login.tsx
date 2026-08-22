import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { validateForm } from "../utils/validation";
import { Button, Input, Card } from "../design-system/components";
import { Leaf } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});
    const validationErrors = validateForm([
      { name: "email", value: email, rules: [{ type: "required", message: "Email is required" }, { type: "email" }] },
      { name: "password", value: password, rules: [{ type: "required", message: "Password is required" }] },
    ]);
    if (validationErrors) {
      setFieldErrors(validationErrors);
      return;
    }
    setLoading(true);
    try {
      const data = await api.login(email, password);
      setAuth(data.user);
      await api.gamification.getStartupState().catch(() => null);
      navigate("/hub");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-background-primary relative overflow-hidden">
      {/* Subtle ambient nature */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-8 w-32 h-32 rounded-full bg-brand-mint/30 blur-3xl" />
        <div className="absolute bottom-20 right-8 w-24 h-24 rounded-full bg-brand-mint/20 blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 rounded-full bg-brand-mint/10 blur-3xl" />
      </div>

      <div className="w-full max-w-md relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="rounded-2xl border border-border-primary bg-background-surface shadow-soft-lg overflow-hidden"
        >
          <div className="text-center px-6 py-8 border-b border-border-primary">
            <div className="relative mx-auto mb-4 w-14 h-14">
              <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-brand-primary/30 to-brand-tertiary/30 blur-md opacity-70" />
              <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-primary via-brand-deep to-brand-tertiary shadow-soft-lg">
                <Leaf size={26} className="text-white" />
              </div>
            </div>
            <h1 className="text-3xl font-display font-black text-text-primary">Welcome back</h1>
            <p className="text-text-secondary font-mono text-sm mt-2">Sign in to continue your prep</p>
          </div>

          <Card padding="lg" className="bg-transparent border-none shadow-none">
            <form onSubmit={handleSubmit} className="space-y-5">
              {error && (
                <div className="bg-error/10 border border-error/20 text-error px-4 py-3 rounded-xl text-sm font-mono">
                  {error}
                </div>
              )}

              <Input
                label="Email"
                type="email"
                placeholder="you@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                error={fieldErrors.email}
                required
              />

              <Input
                label="Password"
                type="password"
                placeholder="Your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={fieldErrors.password}
                required
              />

              <div className="text-right">
                <Link to="/forgot-password" className="text-xs text-brand-primary hover:underline font-mono">
                  Forgot password?
                </Link>
              </div>

              <Button type="submit" className="w-full" size="lg" loading={loading}>
                {loading ? "Signing in..." : "Sign In"}
              </Button>
            </form>

            <p className="text-center mt-6 text-sm text-text-secondary font-mono">
              New here?{" "}
              <Link to="/register" className="text-brand-primary font-semibold hover:underline">
                Create an account
              </Link>
            </p>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}