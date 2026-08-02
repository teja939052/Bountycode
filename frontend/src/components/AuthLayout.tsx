import { Outlet } from "react-router-dom";
import ProfileSidebar from "./ProfileSidebar";

export default function AuthLayout() {
  return (
    <div className="flex min-h-[calc(100vh-64px)]">
      <ProfileSidebar />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
