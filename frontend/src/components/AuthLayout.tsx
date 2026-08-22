import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="flex min-h-[calc(100vh-64px)] bg-[color:var(--bg-base,#f6f3ea)]">
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto w-full max-w-7xl px-4 py-4 sm:px-6 sm:py-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
