import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";
import { Zap } from "lucide-react";
import { validateForm } from "../utils/validation";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const { setAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setFieldErrors({});
    const validationErrors = validateForm([
      { name: "name", value: name, rules: [{ type: "required", message: "Name is required" }] },
      { name: "email", value: email, rules: [{ type: "required", message: "Email is required" }, { type: "email" }] },
      { name: "password", value: password, rules: [{ type: "required", message: "Password is required" }, { type: "minLength", value: 6 }, { type: "password" }] },
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
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-cyber-blue to-cyber-purple rounded-xl flex items-center justify-center mx-auto mb-4 shadow-cyber-blue">
            <Zap size={24} className="text-white" />
          </div>
          <h1 className="text-3xl font-display font-black text-text-primary">Initialize Cadet Profile</h1>
          <p className="text-gray-500 font-mono text-sm mt-2">Begin your career navigation</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg text-sm font-mono">
                {error}
              </div>
            )}

            <Input
              label="Cadet Name"
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
              placeholder="cadet@placementpro.app"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={fieldErrors.email}
              required
            />

            <Input
              label="Access Code"
              type="password"
              placeholder="Min 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={fieldErrors.password}
              minLength={6}
              required
            />

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Initializing..." : "Launch Mission"}
            </Button>
          </form>

          <p className="text-center mt-6 text-sm text-gray-500 font-mono">
            Already have clearance?{" "}
            <Link to="/login" className="text-cyber-blue font-semibold hover:underline">
              Access deck
            </Link>
          </p>
        </div>

        <p className="text-center mt-4 text-xs text-gray-600 font-mono">
          Free cadet tier: 3 interviews + 3 resume reviews. No credit required.
        </p>
      </div>
    </div>
  );
}
