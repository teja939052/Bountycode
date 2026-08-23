import { useState } from "react";
import { Link } from "react-router-dom";
import { Mail, ArrowLeft, Send } from "lucide-react";
import { motion } from "framer-motion";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    setTimeout(() => {
      setMessage(
        "If an account exists with this email, a reset token has been generated."
      );
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-surface-base flex items-center justify-center p-4">
      <div className="w-full max-w-5xl bg-white rounded-3xl shadow-2xl overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
          {/* Left Side - Form */}
          <div className="flex flex-col justify-center p-8 md:p-12">
            <Link
              to="/login"
              className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 mb-6 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to login
            </Link>

            <div className="mb-8 text-center lg:text-left">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Reset your password
              </h2>
              <p className="text-sm text-gray-500">
                Enter your email and we'll send you a reset link.
              </p>
            </div>

            <form className="space-y-5" onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700 mb-1.5"
                >
                  Email address
                </label>
                <div className="relative group">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-300 group-focus-within:text-green-500 transition-colors" />
                  <motion.input
                    id="email"
                    type="email"
                    required
                    className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 placeholder-gray-400 text-base"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                  />
                </div>
              </div>

              {error && (
                <div className="text-red-600 text-sm text-center">{error}</div>
              )}
              {message && (
                <div className="text-green-600 text-sm text-center">
                  {message}
                </div>
              )}

              <motion.button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 bg-green-600 text-white font-medium rounded-xl hover:bg-green-700 transition-all shadow-lg shadow-green-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-base"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                {loading ? (
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
                {loading ? "Sending..." : "Send reset link"}
              </motion.button>
            </form>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-400">or</span>
              </div>
            </div>

            <motion.button
              type="button"
              className="w-full flex items-center justify-center gap-3 border-2 border-gray-100 rounded-xl py-3 text-gray-700 hover:bg-gray-50 transition-all"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              whileHover={{ scale: 1.02 }}
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
              </svg>
              Continue with Google
            </motion.button>
          </div>

          {/* Right Side - Animated Character */}
          <div className="relative hidden lg:flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
            <div className="relative w-64 h-64">
              <motion.div
                className="absolute inset-0 flex items-center justify-center"
                animate={{
                  scale: email.length > 0 ? 1.1 : 1,
                }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <motion.span
                  className="text-9xl"
                  animate={{
                    rotate: email.length > 0 ? [0, -8, 8, -8, 0] : [0, 2, -2, 2, 0],
                    y: [0, -8, 0],
                    scale: email.length > 0 ? 1.1 : 1,
                  }}
                  transition={{
                    duration: 6,
                    repeat: Infinity,
                    repeatType: "mirror",
                    ease: "easeInOut",
                  }}
                >
                  🌱
                </motion.span>
              </motion.div>

              {message && (
                <motion.div
                  className="absolute -bottom-16 left-1/2 -translate-x-1/2 text-sm text-green-600 bg-white/90 px-4 py-2 rounded-full shadow"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  Check your inbox 📧
                </motion.div>
              )}

              <motion.div
                className="absolute -bottom-8 left-0 right-0 flex justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <p className="text-sm text-gray-600">
                  We'll help you get back in
                </p>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
