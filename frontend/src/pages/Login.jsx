import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";
import { Zap } from "lucide-react";
import LoginReveal from "../components/LoginReveal";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showReveal, setShowReveal] = useState(false);
  const [loginData, setLoginData] = useState(null);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await api.login(email, password);
      setAuth(data.user);
      setLoginData(data.user);
      setShowReveal(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRevealComplete = () => {
    setShowReveal(false);
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-cyber-blue to-cyber-purple rounded-xl flex items-center justify-center mx-auto mb-4 shadow-cyber-blue">
            <Zap size={24} className="text-white" />
          </div>
          <h1 className="text-3xl font-display font-black text-white">Access Command Deck</h1>
          <p className="text-gray-500 font-mono text-sm mt-2">Sign in to continue your mission</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg text-sm font-mono">
                {error}
              </div>
            )}

            <Input
              label="Email"
              type="email"
              placeholder="cadet@placementpro.app"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <Input
              label="Password"
              type="password"
              placeholder="Access code"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <div className="text-right">
              <Link to="/forgot-password" className="text-xs text-cyber-blue hover:underline font-mono">
                Forgot access code?
              </Link>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Authenticating..." : "Engage"}
            </Button>
          </form>

          <p className="text-center mt-6 text-sm text-gray-500 font-mono">
            No clearance?{" "}
            <Link to="/register" className="text-cyber-blue font-semibold hover:underline">
              Register cadet
            </Link>
          </p>
        </div>
      </div>

      {showReveal && loginData && (
        <LoginReveal
          user={loginData}
          streak={loginData.streak || 0}
          level={loginData.level || 1}
          onComplete={handleRevealComplete}
        />
      )}
    </div>
  );
}
