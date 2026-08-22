import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useEffect, ReactNode } from "react";
import { queryClient } from "../services/queryClient";
import useAuthStore from "../store/authStore";

export function QueryProvider({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.user);

  // Clear cache on logout so user data doesn't leak between accounts
  useEffect(() => {
    if (!user) {
      queryClient.clear();
    }
  }, [user]);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}