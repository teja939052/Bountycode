import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import Spinner from "./ui/Spinner";
import api from "../services/api";

export default function OnboardingGuard({ children }) {
  const [status, setStatus] = useState({ loading: true, completed: false });

  useEffect(() => {
    const check = async () => {
      try {
        const data = await api.get("/api/v1/auth/onboarding-status");
        setStatus({ loading: false, completed: data.completed });
      } catch {
        setStatus({ loading: false, completed: true });
      }
    };
    check();
  }, []);

  if (status.loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!status.completed) {
    return <Navigate to="/onboarding" replace />;
  }

  return children;
}
