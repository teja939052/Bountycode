// @ts-nocheck
import { useEffect, lazy, Suspense } from "react";
import { Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

const Landing = lazy(() => import("../pages/Landing"));

export default function HomeRedirect() {
  const { user, loadUser } = useAuthStore();
  const loaded = typeof user !== "undefined";

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  if (!loaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f] text-[#e9e9e9]">
        <div className="inline-block w-8 h-8 border-2 border-[#ffa116] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return (
      <Suspense
        fallback={
          <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f] text-[#e9e9e9]">
            <div className="inline-block w-8 h-8 border-2 border-[#ffa116] border-t-transparent rounded-full animate-spin" />
          </div>
        }
      >
        <Landing />
      </Suspense>
    );
  }

  // Signed-in users land on the campaign regardless of whether they have set a
  // target company. This used to gate on `target_company` and otherwise bounce
  // to /company-select, which was never implemented — the redirect fell through
  // to the catch-all 404 on every entry. The target is editable in /profile.
  return <Navigate to="/placement" replace />;
}
