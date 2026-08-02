import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import useAuthStore from "../store/authStore";
import Spinner from "./ui/Spinner";

export default function ProtectedRoute({ children }: { children?: ReactNode }) {
  const { user, loading } = useAuthStore();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
