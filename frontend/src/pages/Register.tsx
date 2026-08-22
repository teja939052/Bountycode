import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { validateForm } from "../utils/validation";
import { Button, Input, Card } from "../design-system/components";
import { Leaf, TreeDeciduous } from "lucide-react";

export default function Register() {
  const [name, setName] = useState("");
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
      { name: "name", value: name, rules: [{ type: "required", message: "Name is required" }] },
      { name: "email", value: email, rules: [{ type: "required", message: "Email is required" }, { type: "email" }] },
      { name: "password", value: password, rules: [{ type: "required", message: "Password is required" }, { type: "minLength", value: 8 }, { type: "password" }] },
    ]);
    if (validationErrors) {
      setFieldErrors(validationErrors);
      return;
    }
    setLoading(true);
    try {
      const data = await api.register(email, password, name);
      setAuth(data.user);
      navigate("/onboarding");
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
            <h1 className="text-3xl font-display font-black text-text-primary">Create your account</h1>
            <p className="text-text-secondary font-mono text-sm mt-2">Start your placement prep journey</p>
          </div>

          <Card padding="lg" className="bg-transparent border-none shadow-none">
            <form onSubmit={handleSubmit} className="space-y-5">
              {error && (
                <div className="bg-error/10 border border-error/20 text-error px-4 py-3 rounded-xl text-sm font-mono">
                  {error}
                </div>
              )}

              <Input
                label="Full Name"
                type="text"
                placeholder="Jane Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                error={fieldErrors.name}
                required
              />

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
                placeholder="Min 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                error={fieldErrors.password}
                minLength={8}
                required
              />

              <Button type="submit" className="w-full" size="lg" loading={loading}>
                {loading ? "Creating account..." : "Create Account"}
              </Button>
            </form>

            <p className="text-center mt-6 text-sm text-text-secondary font-mono">
              Already have an account?{" "}
              <Link to="/login" className="text-brand-primary font-semibold hover:underline">
                Sign in
              </Link>
            </p>

            <p className="text-center mt-4 text-xs text-text-secondary font-mono">
              Free plan: 3 interviews + 3 resume reviews. No credit card required.
            </p>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}