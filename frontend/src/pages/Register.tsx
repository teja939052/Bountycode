import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { User, Mail, Lock, Eye, EyeOff, UserPlus, Zap } from "lucide-react";
import { motion } from "framer-motion";
import NeuralNetworkBackground from "../components/NeuralNetworkBackground";
import useAuthStore from "../store/authStore";
import { authApi } from "../services/api/auth";
import { validateForm } from "../utils/validation";

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
      navigate("/onboarding");
    } catch (err: any) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0f0d] flex items-center justify-center p-4 relative overflow-hidden">
      <NeuralNetworkBackground reducedMotion={reducedMotion} />

      <div className="w-full max-w-md relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-[#111a15]/80 backdrop-blur-xl border border-green-500/20 rounded-2xl shadow-2xl shadow-green-500/5 overflow-hidden"
        >
          <div className="text-center px-6 pt-8 pb-6">
            <div className="relative mx-auto mb-4 w-14 h-14">
              <div className="absolute -inset-1 rounded-2xl bg-green-500/20 blur-lg" />
              <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 shadow-lg shadow-green-500/25">
                <Zap size={26} className="text-white" />
              </div>
            </div>
            <h1 className="text-2xl font-bold text-white">Initialize Cadet Profile</h1>
            <p className="text-gray-400 text-sm mt-1 font-mono">Begin your career navigation</p>
          </div>

          <div className="px-6 pb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-xl text-sm font-mono">
                  {error}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Cadet Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Jane Doe"
                    className="w-full pl-12 pr-4 py-3 bg-[#0d1510] border border-green-500/20 rounded-xl text-white placeholder-gray-500 focus:border-green-500/50 focus:ring-1 focus:ring-green-500/30 transition-all outline-none font-mono text-sm"
                    required
                  />
                </div>
                {fieldErrors.name && <p className="text-red-400 text-xs mt-1">{fieldErrors.name}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="cadet@placementpro.app"
                    className="w-full pl-12 pr-4 py-3 bg-[#0d1510] border border-green-500/20 rounded-xl text-white placeholder-gray-500 focus:border-green-500/50 focus:ring-1 focus:ring-green-500/30 transition-all outline-none font-mono text-sm"
                    required
                  />
                </div>
                {fieldErrors.email && <p className="text-red-400 text-xs mt-1">{fieldErrors.email}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Access Code</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Min 8 characters"
                    className="w-full pl-12 pr-12 py-3 bg-[#0d1510] border border-green-500/20 rounded-xl text-white placeholder-gray-500 focus:border-green-500/50 focus:ring-1 focus:ring-green-500/30 transition-all outline-none font-mono text-sm"
                    minLength={8}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {fieldErrors.password && <p className="text-red-400 text-xs mt-1">{fieldErrors.password}</p>}
              </div>

              <motion.button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-semibold rounded-xl transition-all shadow-lg shadow-green-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {loading ? (
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <UserPlus className="w-5 h-5" />
                )}
                {loading ? "Initializing..." : "Launch Mission"}
              </motion.button>
            </form>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-green-500/10" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-[#111a15]/80 text-gray-500 font-mono text-xs">or</span>
              </div>
            </div>

            <a
              href="/api/auth/google"
              className="w-full flex items-center justify-center gap-3 border border-green-500/20 rounded-xl py-3 text-gray-300 hover:bg-green-500/5 transition-all font-mono text-sm"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.30-4.53 6.16-4.53z" fill="#EA4335" />
              </svg>
              Continue with Google
            </a>

            <p className="text-center mt-6 text-sm text-gray-500 font-mono">
              Already have clearance?{" "}
              <Link to="/login" className="text-green-400 font-semibold hover:text-green-300 transition-colors">
                Access deck
              </Link>
            </p>

            <p className="text-center mt-4 text-xs text-gray-600 font-mono">
              Free cadet tier: 3 interviews + 3 resume reviews. No credit required.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
