import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Building2, ArrowRight, CheckCircle2, Clock, Target } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

type CompanyTrack = {
  id: string;
  company_id: string;
  name: string;
  full_name: string;
  icon: string;
  description: string;
  package_range: string;
  duration_minutes: number;
  difficulty: string;
  total_sections: number;
  total_modules: number;
  enrolled?: boolean;
  progress_pct?: number;
};

export default function Target() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data, isLoading, isError } = useQuery({
    queryKey: ["company-tracks", "list"],
    queryFn: () => api.companyTracks.listCompanies(),
  });

  const tracks = useMemo(() => data?.tracks ?? [], [data]);

  const enrollMutation = useMutation({
    mutationFn: (trackId: string) => api.companyTracks.enroll(trackId),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["company-tracks"] }),
        queryClient.invalidateQueries({ queryKey: ["journey", "state"] }),
        queryClient.invalidateQueries({ queryKey: ["study", "today"] }),
      ]);
      navigate("/journey");
    },
  });

  const startOrContinue = (track: CompanyTrack) => {
    if (track.enrolled) {
      navigate(`/company-tracks?track=${encodeURIComponent(track.id)}`);
      return;
    }
    enrollMutation.mutate(track.id);
  };

  return (
    <div className="min-h-screen px-4 py-6 pb-24 md:py-8">
      <div className="mx-auto max-w-5xl space-y-6">
        <header className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <p className="mb-1 flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-primary">
            <Building2 size={13} /> Placement target
          </p>
          <h1 className="font-display text-2xl font-black text-text-primary">
            Choose the role you are preparing for
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-text-muted">
            Pick one company assessment track. Bountycode will use it to prioritize your daily learning,
            verified practice, mock assessments, and readiness evidence in one Journey.
          </p>
        </header>

        {enrollMutation.isError && (
          <div role="alert" className="rounded-xl border border-red-300 bg-red-50 p-3 text-sm text-red-700">
            We could not save this target. Please retry.
          </div>
        )}

        {isLoading ? (
          <div className="flex justify-center py-16"><Spinner /></div>
        ) : isError ? (
          <div role="alert" className="rounded-xl border border-border bg-white p-5 text-sm text-text-secondary">
            Company tracks could not be loaded. Refresh and try again.
          </div>
        ) : tracks.length === 0 ? (
          <div className="rounded-xl border border-border bg-white p-5 text-sm text-text-secondary">
            No company tracks are available yet.
          </div>
        ) : (
          <section aria-label="Available placement tracks" className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {tracks.map((track: CompanyTrack) => (
              <article key={track.id} className="flex flex-col rounded-2xl border border-border bg-white p-5 shadow-card">
                <div className="flex items-start gap-3">
                  <span aria-hidden className="text-3xl">{track.icon || "🏢"}</span>
                  <div className="min-w-0 flex-1">
                    <h2 className="font-display font-bold text-text-primary">{track.name}</h2>
                    <p className="mt-1 text-xs text-text-muted">{track.full_name}</p>
                  </div>
                  {track.enrolled && <CheckCircle2 aria-label="Enrolled" className="shrink-0 text-emerald-600" size={18} />}
                </div>
                <p className="mt-3 flex-1 text-sm text-text-secondary">{track.description}</p>
                <div className="mt-4 flex flex-wrap gap-2 text-[11px] text-text-muted">
                  <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-1">
                    <Clock size={12} /> {track.duration_minutes} min
                  </span>
                  <span className="rounded-full bg-gray-100 px-2 py-1">{track.total_sections} sections</span>
                  <span className="rounded-full bg-gray-100 px-2 py-1">{track.total_modules} modules</span>
                  {track.package_range && <span className="rounded-full bg-gray-100 px-2 py-1">{track.package_range}</span>}
                </div>
                {track.enrolled && (
                  <div className="mt-3">
                    <div className="h-1.5 overflow-hidden rounded-full bg-gray-100">
                      <div className="h-full rounded-full bg-primary" style={{ width: `${Math.min(100, Math.max(0, track.progress_pct ?? 0))}%` }} />
                    </div>
                    <p className="mt-1 text-[11px] text-text-muted">{track.progress_pct ?? 0}% completed</p>
                  </div>
                )}
                <button
                  type="button"
                  onClick={() => startOrContinue(track)}
                  disabled={enrollMutation.isPending}
                  className="mt-4 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {enrollMutation.isPending && enrollMutation.variables === track.id
                    ? <Spinner size={14} />
                    : <><Target size={15} /> {track.enrolled ? "Continue track" : "Choose this target"} <ArrowRight size={14} /></>}
                </button>
              </article>
            ))}
          </section>
        )}
        <p className="text-xs text-text-muted">
          You can change your target later. Your completed lessons and practice history remain in your account.
        </p>
      </div>
    </div>
  );
}
