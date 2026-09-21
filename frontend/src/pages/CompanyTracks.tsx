import { useState } from "react";
import { motion } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import {
  Building2, Briefcase, Clock, Trophy, TrendingUp, Sparkles, ArrowRight,
  BookOpen, Target, Zap, Crown, CheckCircle2, Lock, Star,
} from "lucide-react";

const DIFFICULTY_COLORS = {
  easy: "text-green-400 bg-green-500/10 border-green-500/20",
  medium: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20",
  hard: "text-red-400 bg-red-500/10 border-red-500/20",
};

export default function CompanyTracks() {
  const { user } = useAuthStore();
  const [selectedTrack, setSelectedTrack] = useState<string | null>(null);

  const { data: tracksData, isLoading } = useQuery({
    queryKey: ["company-tracks", "list"],
    queryFn: () => api.companyTracks.listCompanies(),
  });

  const tracks = tracksData?.tracks || [];

  if (selectedTrack) {
    return (
      <div className="min-h-screen py-6 px-3 sm:py-8 sm:px-4 max-w-6xl mx-auto">
        <button
          onClick={() => setSelectedTrack(null)}
          className="mb-4 text-sm text-gray-500 hover:text-gray-700 flex items-center gap-1"
        >
          ← Back to all tracks
        </button>
        <TrackDetail trackId={selectedTrack} onBack={() => setSelectedTrack(null)} />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 px-3 sm:py-8 sm:px-4 max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-xl bg-primary-500/10 border border-primary-500/20">
            <Building2 className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Company Tracks</h1>
            <p className="text-sm text-gray-500">TCS, Accenture, Infosys, Wipro — targeted prep for India's top recruiters</p>
          </div>
        </div>
      </motion.div>

      {/* Tracks Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 animate-pulse">
              <div className="h-6 bg-gray-700 rounded w-1/2 mb-3" />
              <div className="h-4 bg-gray-700 rounded w-full mb-2" />
              <div className="h-4 bg-gray-700 rounded w-2/3" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {tracks.map((track, i) => (
            <motion.div
              key={track.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <TrackCard track={track} onClick={() => setSelectedTrack(track.id)} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}

function TrackCard({ track, onClick }: { track: any; onClick: () => void }) {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      onClick={onClick}
      className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 cursor-pointer hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all"
    >
      <div className="flex items-start gap-3 mb-3">
        <div className="text-3xl">{track.icon}</div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 truncate">{track.name}</h3>
          <p className="text-xs text-gray-500 line-clamp-2">{track.description}</p>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
          {track.duration_minutes} min
        </span>
        <span className={`text-[10px] px-2 py-0.5 rounded-full border ${DIFFICULTY_COLORS[track.difficulty as keyof typeof DIFFICULTY_COLORS] || DIFFICULTY_COLORS.easy}`}>
          {track.difficulty}
        </span>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
          {track.total_modules} modules
        </span>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
          {track.package_range}
        </span>
      </div>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <Trophy className="w-3 h-3" />
          {track.total_xp} Diamonds
        </span>
        <span className="flex items-center gap-1">
          <BookOpen className="w-3 h-3" />
          {track.total_sections} sections
        </span>
      </div>
      {track.enrolled && (
        <div className="mt-3">
          <div className="h-1.5 rounded-full bg-gray-800 overflow-hidden">
            <div className="h-full rounded-full bg-primary-500 transition-all" style={{ width: `${track.progress_pct || 0}%` }} />
          </div>
          <p className="text-[10px] text-gray-500 mt-1">{track.progress_pct || 0}% complete</p>
        </div>
      )}
    </motion.div>
  );
}

function TrackDetail({ trackId, onBack }: { trackId: string; onBack: () => void }) {
  const queryClient = useQueryClient();
  const { data: trackData, isLoading } = useQuery({
    queryKey: ["company-tracks", "detail", trackId],
    queryFn: () => api.companyTracks.getTrack(trackId),
  });

  const enrollMutation = useMutation({
    mutationFn: () => api.companyTracks.enroll(trackId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["company-tracks"] });
    },
  });

  const [completing, setCompleting] = useState<string | null>(null);

  const handleComplete = async (moduleId: string) => {
    setCompleting(moduleId);
    try {
      await api.companyTracks.completeModule(trackId, moduleId, 85);
      queryClient.invalidateQueries({ queryKey: ["company-tracks", "detail", trackId] });
    } catch (e) {
      console.error("Failed to complete module:", e);
    } finally {
      setCompleting(null);
    }
  };

  if (isLoading || !trackData) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Track Header */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <div className="flex items-start gap-4">
          <div className="text-5xl">{trackData.icon}</div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{trackData.full_name}</h2>
            <p className="text-sm text-gray-500 mt-1">{trackData.description}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-xs px-2 py-1 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
                {trackData.duration_minutes} minutes
              </span>
              <span className={`text-xs px-2 py-1 rounded-full border ${DIFFICULTY_COLORS[trackData.difficulty as keyof typeof DIFFICULTY_COLORS] || ""}`}>
                {trackData.difficulty}
              </span>
              <span className="text-xs px-2 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
                {trackData.role}
              </span>
              <span className="text-xs px-2 py-1 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
                {trackData.package_range}
              </span>
            </div>
          </div>
          {!trackData.enrolled && (
            <button
              onClick={() => enrollMutation.mutate()}
              disabled={enrollMutation.isPending}
              className="px-4 py-2 rounded-xl bg-primary-600 text-white text-sm font-medium hover:bg-primary-700 disabled:opacity-50"
            >
              {enrollMutation.isPending ? "Enrolling..." : "Enroll Now"}
            </button>
          )}
        </div>
      </div>

      {/* Sections */}
      {trackData.sections?.map((section: any, sIdx: number) => (
        <motion.div
          key={section.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: sIdx * 0.1 }}
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{section.title}</h3>
              <p className="text-xs text-gray-500">{section.description}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-2 py-1 rounded-full bg-gray-500/10 text-gray-400">
                {section.duration_minutes} min
              </span>
              <span className="text-xs px-2 py-1 rounded-full bg-gray-500/10 text-gray-400">
                {section.questions_count} questions
              </span>
            </div>
          </div>

          {/* Topics */}
          <div className="mb-4">
            <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Topics</h4>
            <div className="flex flex-wrap gap-2">
              {section.topics?.map((topic: any) => (
                <div key={topic.name} className="text-xs px-3 py-1.5 rounded-lg bg-gray-500/5 border border-gray-500/10">
                  <span className="font-medium text-gray-300">{topic.name}</span>
                  <span className="text-gray-500 ml-1">({topic.weight}%)</span>
                </div>
              ))}
            </div>
          </div>

          {/* Modules */}
          <div className="space-y-3">
            {section.modules?.map((mod: any, mIdx: number) => (
              <div
                key={mod.id}
                className={`rounded-xl border p-4 ${mod.completed ? "border-green-500/20 bg-green-500/5" : "border-white/10 bg-white/[0.02]"}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-medium text-gray-900">{mod.title}</h4>
                      {mod.completed && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                    </div>
                    <p className="text-xs text-gray-500 mb-2">{mod.description}</p>
                    <div className="flex flex-wrap gap-1 mb-2">
                      {mod.topics.slice(0, 5).map((t: string) => (
                        <span key={t} className="text-[10px] px-1.5 py-0.5 rounded bg-gray-500/10 text-gray-400">{t}</span>
                      ))}
                    </div>
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {mod.duration_minutes} min
                      </span>
                      <span className="flex items-center gap-1">
                        <BookOpen className="w-3 h-3" />
                        {mod.questions_count} questions
                      </span>
                      <span className="flex items-center gap-1">
                        <Zap className="w-3 h-3 text-yellow-500" />
                        {mod.xp_reward} Diamonds
                      </span>
                      {mod.score && (
                        <span className="flex items-center gap-1">
                          <Target className="w-3 h-3 text-primary-500" />
                          {mod.score}%
                        </span>
                      )}
                    </div>
                  </div>
                  {trackData.enrolled && !mod.completed && (
                    <button
                      onClick={() => handleComplete(mod.id)}
                      disabled={completing === mod.id}
                      className="ml-3 px-3 py-1.5 rounded-lg bg-primary-600 text-white text-xs font-medium hover:bg-primary-700 disabled:opacity-50"
                    >
                      {completing === mod.id ? "..." : "Complete"}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      ))}

      {/* Coding Patterns */}
      {trackData.coding_patterns && trackData.coding_patterns.length > 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
            <Code2 className="w-5 h-5 text-primary-600" />
            Practice Coding Patterns
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {trackData.coding_patterns.map((pattern: string, i: number) => (
              <div key={i} className="text-sm px-3 py-2 rounded-lg bg-gray-500/5 border border-gray-500/10 text-gray-400">
                {pattern}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* HR Questions */}
      {trackData.hr_questions && trackData.hr_questions.length > 0 && (
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
            <Briefcase className="w-5 h-5 text-primary-600" />
            Common HR Questions
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {trackData.hr_questions.map((q: string, i: number) => (
              <div key={i} className="text-sm px-3 py-2 rounded-lg bg-gray-500/5 border border-gray-500/10 text-gray-400">
                {q}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      {trackData.tips && trackData.tips.length > 0 && (
        <div className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-yellow-500" />
            Pro Tips
          </h3>
          <ul className="space-y-2">
            {trackData.tips.map((tip: string, i: number) => (
              <li key={i} className="text-sm text-gray-400 flex items-start gap-2">
                <Star className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}
