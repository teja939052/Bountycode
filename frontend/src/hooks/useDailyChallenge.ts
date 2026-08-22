import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

const STATUS_KEY = ["daily-challenge", "status"] as const;
const PROGRESS_KEY = ["daily-challenge", "progress"] as const;
const LEADERBOARD_KEY = ["daily-challenge", "leaderboard"] as const;
const TODAY_KEY = ["daily-challenge", "today"] as const;

export function useDailyChallenge() {
  const queryClient = useQueryClient();

  const status = useQuery({
    queryKey: STATUS_KEY,
    queryFn: () => api.getDailyChallengeStatus().catch(() => ({ enrolled: false })),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const progress = useQuery({
    queryKey: PROGRESS_KEY,
    queryFn: () => api.getDailyChallengeProgress().catch(() => ({ enrolled: false })),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const leaderboard = useQuery({
    queryKey: LEADERBOARD_KEY,
    queryFn: () => api.getDailyChallengeLeaderboard().catch(() => ({ leaderboard: [], user_rank: null })),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const today = useQuery({
    queryKey: TODAY_KEY,
    queryFn: () => api.getDailyChallengeToday(),
    enabled: Boolean(status.data?.enrolled),
    retry: 1,
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });

  const enrollMutation = useMutation({
    mutationFn: (path: string) => api.enrollDailyChallenge(path),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STATUS_KEY });
      queryClient.invalidateQueries({ queryKey: PROGRESS_KEY });
      queryClient.invalidateQueries({ queryKey: TODAY_KEY });
    },
  });

  const completeDayMutation = useMutation({
    mutationFn: (questIds: string[]) => api.completeDailyChallengeDay(questIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROGRESS_KEY });
      queryClient.invalidateQueries({ queryKey: TODAY_KEY });
      queryClient.invalidateQueries({ queryKey: LEADERBOARD_KEY });
    },
  });

  const isLoading = status.isLoading || progress.isLoading;

  const refetch = async () => {
    await Promise.all([
      status.refetch(),
      progress.refetch(),
      leaderboard.refetch(),
      today.refetch(),
    ]);
  };

  return {
    status: status.data ?? null,
    progress: progress.data ?? null,
    leaderboard: leaderboard.data ?? null,
    today: today.data ?? null,
    enrollMutation,
    completeDayMutation,
    isLoading,
    isError: status.isError || progress.isError,
    refetch,
  };
}
