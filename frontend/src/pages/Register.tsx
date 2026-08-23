import { useState } from "react";
import { Link } from "react-router-dom";
import { User, Mail, Lock, Eye, EyeOff, CheckCircle, XCircle, UserPlus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const UPPERCASE_REGEX = new RegExp("[A-Z]");
const NUMBER_REGEX = new RegExp("[0-9]");

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);

  const passwordRules = [
    { check: password.length >= 8, label: "8+ characters" },
    { check: UPPERCASE_REGEX.test(password), label: "One uppercase" },
    { check: NUMBER_REGEX.test(password), label: "One number" },
  ];

  const isPasswordValid = passwordRules.every((r) => r.check);
  const passwordsMatch = password === confirmPassword;
  const isFormValid = isPasswordValid && passwordsMatch && name && email && password;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormValid) return;
    setLoading(true);
    setTimeout(() => setLoading(false), 1000);
  };

  return (
    <div className="min-h-screen bg-surface-base flex items-center justify-center p-4">
      <div className="w-full max-w-5xl bg-white rounded-3xl shadow-2xl overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
          {/* Left Side - Form */}
          <div className="flex flex-col justify-center p-8 md:p-12">
            <div className="mb-8 text-center lg:text-left">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">PlacementPro</h1>
              <p className="text-sm text-gray-500">Start your journey</p>
            </div>

            <div className="mb-6 text-center lg:text-left">
              <p className="text-xs text-gray-400 mb-2">Trusted by:</p>
              <div className="flex flex-wrap justify-center lg:justify-start gap-4 text-xs text-gray-400">
                <span>50,000+ Students</span>
                <span>4.8 Rating</span>
                <span>3,000+ Offers</span>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Full Name
                </label>
                <div className="relative group">
                  <User
                    className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors ${
                      focusedField === "name"
                        ? "text-green-500"
                        : "text-gray-300"
                    }`}
                  />
                  <motion.input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    onFocus={() => setFocusedField("name")}
                    onBlur={() => setFocusedField(null)}
                    placeholder="Enter your full name"
                    className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 placeholder-gray-400 text-base"
                    required
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Email Address
                </label>
                <div className="relative group">
                  <Mail
                    className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors ${
                      focusedField === "email"
                        ? "text-green-500"
                        : "text-gray-300"
                    }`}
                  />
                  <motion.input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onFocus={() => setFocusedField("email")}
                    onBlur={() => setFocusedField(null)}
                    placeholder="Enter your email"
                    className="w-full pl-12 pr-4 py-3.5 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 placeholder-gray-400 text-base"
                    required
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Password
                </label>
                <div className="relative group">
                  <Lock
                    className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors ${
                      focusedField === "password"
                        ? "text-green-500"
                        : "text-gray-300"
                    }`}
                  />
                  <motion.input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onFocus={() => setFocusedField("password")}
                    onBlur={() => setFocusedField(null)}
                    placeholder="Create a password"
                    className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 placeholder-gray-400 text-base"
                    required
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 }}
                  />
                  <motion.button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer transition-colors"
                    whileTap={{ scale: 0.9 }}
                  >
                    {showPassword ? (
                      <EyeOff className="w-5 h-5" />
                    ) : (
                      <Eye className="w-5 h-5" />
                    )}
                  </motion.button>
                </div>

                <div className="mt-2 space-y-1.5">
                  {passwordRules.map((rule) => (
                    <div key={rule.label} className="flex items-center gap-2 text-xs">
                      {rule.check ? (
                        <CheckCircle className="w-3.5 h-3.5 text-green-500" />
                      ) : (
                        <XCircle className="w-3.5 h-3.5 text-gray-300" />
                      )}
                      <span className={rule.check ? "text-green-600" : "text-gray-400"}>
                        {rule.label}
                      </span>
                    </div>
                  ))}
                </div>

                <div className="mt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1.5">
                    Confirm Password
                  </label>
                  <div className="relative group">
                    <Lock
                      className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 transition-colors ${
                        focusedField === "confirmPassword"
                          ? "text-green-500"
                          : "text-gray-300"
                      }`}
                    />
                    <motion.input
                      type={showPassword ? "text" : "password"}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      onFocus={() => setFocusedField("confirmPassword")}
                      onBlur={() => setFocusedField(null)}
                      placeholder="Confirm password"
                      className="w-full pl-12 pr-12 py-3.5 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 placeholder-gray-400 text-base"
                      required
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 }}
                    />
                    <motion.button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 cursor-pointer transition-colors"
                      whileTap={{ scale: 0.9 }}
                    >
                      {showPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </motion.button>
                  </div>

                  {password && isPasswordValid && passwordsMatch ? (
                    <motion.div
                      className="mt-2 flex items-center gap-2 text-sm text-green-600"
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Passwords match</span>
                    </motion.div>
                  ) : password ? (
                    <motion.div
                      className="mt-2 flex items-center gap-2 text-sm text-red-500"
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Passwords do not match or are too weak</span>
                    </motion.div>
                  ) : null}
                </div>
              </div>

              <motion.button
                type="submit"
                disabled={loading || !isFormValid}
                className="w-full py-3.5 bg-green-600 text-white font-medium rounded-xl hover:bg-green-700 transition-all shadow-lg shadow-green-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-base"
                whileHover={{ scale: isFormValid ? 1.02 : 1 }}
                whileTap={{ scale: 0.98 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                {loading ? (
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <UserPlus className="w-5 h-5" />
                )}
                {loading ? "Creating account..." : "Start Your Journey"}
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
              transition={{ delay: 0.6 }}
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

            <p className="text-center text-sm text-gray-500 mt-6">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-green-600 font-medium hover:text-green-700 transition-colors"
              >
                Login
              </Link>
            </p>
          </div>

          {/* Right Side - Animated Character */}
          <div className="relative hidden lg:flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
            <div className="relative w-64 h-64">
              <motion.div
                className="absolute inset-0 flex items-center justify-center"
                animate={{
                  scale: focusedField ? 1.1 : 1,
                }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <motion.span
                  className="text-9xl"
                  animate={{
                    rotate: focusedField ? [0, -8, 8, -8, 0] : [0, 2, -2, 2, 0],
                    y: focusedField ? [0, -8, 0] : [0, -5, 0],
                    scale: focusedField ? 1.1 : 1,
                  }}
                  transition={{
                    duration: focusedField ? 0.5 : 8,
                    repeat: Infinity,
                    repeatType: "mirror",
                    ease: "easeInOut",
                  }}
                >
                  🌱
                </motion.span>
              </motion.div>

              <AnimatePresence>
                {focusedField === "name" && (
                  <motion.div
                    className="absolute -top-16 left-1/2 -translate-x-1/2 text-sm text-gray-600 bg-white/80 px-3 py-1 rounded-full shadow"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                  >
                    Tell us your name!
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {focusedField === "email" && (
                  <motion.div
                    className="absolute -top-16 left-1/2 -translate-x-1/2 text-sm text-gray-600 bg-white/80 px-3 py-1 rounded-full shadow"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                  >
                    {email.length > 0
                      ? `Great, ${email.split("@")[0]}!`
                      : "Where should we send updates?"}
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {focusedField === "password" && (
                  <motion.div
                    className="absolute -bottom-16 left-1/2 -translate-x-1/2 text-sm text-gray-600 bg-white/80 px-3 py-1 rounded-full shadow"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                  >
                    {isPasswordValid
                      ? "Strong password! 💪"
                      : "Must include uppercase + number"}
                  </motion.div>
                )}
              </AnimatePresence>

              {passwordsMatch && (
                <motion.div
                  className="absolute -bottom-20 left-1/2 -translate-x-1/2 text-sm text-green-600 bg-white/90 px-3 py-1 rounded-full shadow"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <CheckCircle className="w-4 h-4 inline mr-1" />
                  Passwords match!
                </motion.div>
              )}

              <motion.div
                className="absolute -bottom-8 left-0 right-0 flex justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <p className="text-sm text-gray-600">
                  Join thousands learning with PlacementPro
                </p>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
