import { useState, useEffect } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import api from "../services/api";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const urlToken = searchParams.get("token") || "";
  const urlEmail = searchParams.get("email") || "";
  const navigate = useNavigate();
  const [email, setEmail] = useState(urlEmail);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (urlToken) {
      document.getElementById("token")?.focus();
    }
  }, [urlToken]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters");
      setLoading(false);
      return;
    }

    try {
      await api.resetPassword(email, urlToken, newPassword);
      setMessage("Password reset successful. You can now log in.");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError(err.message || "Reset failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-base py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-text-primary">
            Set new password
          </h2>
          <p className="mt-2 text-center text-sm text-brand-secondary">
            Choose a strong password for your account.
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">Email address</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-brand-primary/20 placeholder-brand-dim text-text-primary rounded-t-md focus:outline-none focus:ring-brand-primary focus:border-brand-primary focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="token" className="sr-only">Reset token</label>
              <input
                id="token"
                name="token"
                type="text"
                required
                readOnly
                value={urlToken}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-brand-primary/20 placeholder-brand-dim text-brand-dim bg-surface-card focus:outline-none focus:ring-brand-primary focus:border-brand-primary focus:z-10 sm:text-sm"
                placeholder="Reset token auto-filled"
              />
              <p className="text-[10px] text-brand-dim mt-1">Token auto-filled from email link</p>
            </div>
            <div>
              <label htmlFor="new-password" className="sr-only">New password</label>
              <input
                id="new-password"
                name="new_password"
                type="password"
                required
                minLength={8}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-brand-primary/20 placeholder-brand-dim text-text-primary focus:outline-none focus:ring-brand-primary focus:border-brand-primary focus:z-10 sm:text-sm"
                placeholder="New password (min 8 characters)"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="confirm-password" className="sr-only">Confirm password</label>
              <input
                id="confirm-password"
                name="confirm_password"
                type="password"
                required
                minLength={8}
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-brand-primary/20 placeholder-brand-dim text-text-primary rounded-b-md focus:outline-none focus:ring-brand-primary focus:border-brand-primary focus:z-10 sm:text-sm"
                placeholder="Confirm new password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <div className="text-brand-accent text-sm text-center">{error}</div>
          )}
          {message && (
            <div className="text-brand-emerald text-sm text-center">{message}</div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-text-primary bg-brand-primary hover:bg-brand-primary/80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary disabled:opacity-50"
            >
              {loading ? "Resetting..." : "Reset password"}
            </button>
          </div>

          <div className="text-sm text-center">
            <Link to="/login" className="font-medium text-brand-secondary hover:text-brand-primary">
              Back to login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}