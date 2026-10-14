// @ts-nocheck
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { BountyCodeLoader } from "../components/brand/BountyCodeBrandMotion";
import { requestWithRetry } from "../services/api/request.ts";

export default function OnboardingGuard({ children }) {
  const [status, setStatus] = useState({ loading: true, completed: false });

  useEffect(() => {
    const check = async () => {
      try {
        const data = await requestWithRetry("/api/v1/auth/onboarding-status");
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
        <BountyCodeLoader size={48} />
      </div>
    );
  }

  if (!status.completed) {
    return <Navigate to="/onboarding" replace />;
  }

  return children;
}
