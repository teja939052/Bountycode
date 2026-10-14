// @ts-nocheck
import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { MailCheck, MailWarning, Loader2, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import api from "../services/api";

export default function VerifyEmail() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const token = params.get("token") || "";
  const [status, setStatus] = useState(token ? "verifying" : "idle");
  const [email, setEmail] = useState("");
  const [resent, setResent] = useState(false);

  useEffect(() => {
    if (!token) return;
    api.auth
      .verifyEmail(token)
      .then(() => setStatus("done"))
      .catch(() => setStatus("error"));
  }, [token]);

  const handleResend = async (e) => {
    e.preventDefault();
    if (!email.trim()) return;
    try {
      await api.auth.resendVerification(email.trim());
      setResent(true);
    } catch {
      setResent(true); // endpoint is enumeration-safe; same message either way
    }
  };

  return (
    <div className="min-h-screen bg-surface-base flex items-center justify-center p-4">
      <motion.div
        className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-8 md:p-10 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        {status === "verifying" && (
          <>
            <Loader2 className="w-12 h-12 mx-auto text-green-600 animate-spin" />
            <h2 className="text-2xl font-bold text-gray-900 mt-4">Verifying your email…</h2>
          </>
        )}
        {status === "done" && (
          <>
            <MailCheck className="w-12 h-12 mx-auto text-green-600" />
            <h2 className="text-2xl font-bold text-gray-900 mt-4">Email verified</h2>
            <p className="text-sm text-gray-500 mt-2">
              Pro checkout is now unlocked on your account.
            </p>
            <button
              onClick={() => navigate("/pricing")}
              className="mt-6 inline-flex items-center gap-2 px-6 py-3 bg-green-600 text-white font-medium rounded-xl hover:bg-green-700 transition-all"
            >
              Continue to pricing <ArrowRight className="w-4 h-4" />
            </button>
          </>
        )}
        {(status === "error" || status === "idle") && (
          <>
            <MailWarning className="w-12 h-12 mx-auto text-amber-500" />
            <h2 className="text-2xl font-bold text-gray-900 mt-4">
              {status === "error" ? "Link expired or invalid" : "Verify your email"}
            </h2>
            <p className="text-sm text-gray-500 mt-2">
              Enter your account email and we'll send a fresh verification link.
            </p>
            {resent ? (
              <p className="text-sm text-green-600 mt-4">
                If the email exists, a verification link has been sent.
              </p>
            ) : (
              <form className="mt-4 space-y-3" onSubmit={handleResend}>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full px-4 py-3 border-2 border-gray-100 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-gray-900 text-base"
                />
                <button
                  type="submit"
                  className="w-full py-3 bg-green-600 text-white font-medium rounded-xl hover:bg-green-700 transition-all"
                >
                  Resend verification link
                </button>
              </form>
            )}
            <Link to="/login" className="inline-block mt-4 text-sm text-gray-500 hover:text-gray-700">
              Back to login
            </Link>
          </>
        )}
      </motion.div>
    </div>
  );
}
