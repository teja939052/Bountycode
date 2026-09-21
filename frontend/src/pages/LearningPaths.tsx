import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import {
  BookOpen, Code2, FlaskConical, Settings, ArrowRight, Star, Trophy,
  Clock, Users, TrendingUp, Sparkles, ChevronRight, Flame, Target,
  Zap, Shield, BarChart3, Briefcase, Building2, Crown, CheckCircle2, Lock,
} from "lucide-react";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";

const DIFFICULTY_COLORS = {
  easy: "text-green-400 bg-green-500/10 border-green-500/20",
  medium: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20",
  hard: "text-red-400 bg-red-500/10 border-red-500/20",
};

export default function LearningPaths() {
  const { user } = useAuthStore();
  const [selectedRole, setSelectedRole] = useState<string | null>(null);

  const { data: rolesData, isLoading } = useQuery({
    queryKey: ["learning-paths", "roles"],
    queryFn: () => api.learningPaths.listRoles(),
  });

  const { data: recsData } = useQuery({
    queryKey: ["learning-paths", "recommendations"],
    queryFn: () => api.learningPaths.getRecommendations(),
  });

  const roles = rolesData?.paths || [];
  const recommendations = recsData?.recommendations || [];

  if (selectedRole) {
    return (
      <div className="min-h-screen py-6 px-3 sm:py-8 sm:px-4 max-w-6xl mx-auto">
        <button
          onClick={() => setSelectedRole(null)}
          className="mb-4 text-sm text-gray-500 hover:text-gray-700 flex items-center gap-1"
        >
          ← Back to all paths
        </button>
        <RoleDetail roleId={selectedRole} onBack={() => setSelectedRole(null)} />
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
            <BookOpen className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Learning Paths</h1>
            <p className="text-sm text-gray-500">Role-based curricula designed to get you hired</p>
          </div>
        </div>
      </motion.div>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-yellow-500" />
            <h2 className="text-lg font-semibold text-gray-900">Recommended for You</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendations.map((rec, i) => (
              <motion.div
                key={rec.path_id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
              >
                <RoleCard roleId={rec.path_id} compact recommended={rec} onClick={() => setSelectedRole(rec.path_id)} />
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* All Roles */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4">All Learning Paths</h2>
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
            {roles.map((role, i) => (
              <motion.div
                key={role.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <RoleCard roleId={role.id} onClick={() => setSelectedRole(role.id)} />
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
}

function RoleCard({ roleId, compact, recommended, onClick }: { roleId: string; compact?: boolean; recommended?: { match_score: number; reason: string }; onClick: () => void }) {
  const { data: roleData } = useQuery({
    queryKey: ["learning-paths", "role", roleId],
    queryFn: () => api.learningPaths.getRole(roleId),
    enabled: !!roleId,
  });

  const role = roleData;
  if (!role) return null;

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      onClick={onClick}
      className={`rounded-2xl border border-white/10 bg-white/[0.03] p-5 cursor-pointer hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all ${compact ? "flex flex-col h-full" : ""}`}
    >
      {recommended && (
        <div className="flex items-center gap-1 mb-2 text-xs text-yellow-400">
          <Sparkles className="w-3 h-3" />
          <span>{recommended.match_score}% match</span>
        </div>
      )}
      <div className="flex items-start gap-3 mb-3">
        <div className="text-3xl">{role.icon}</div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 truncate">{role.short_name}</h3>
          <p className="text-xs text-gray-500 line-clamp-2">{role.description}</p>
        </div>
      </div>
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
          {role.duration_weeks} weeks
        </span>
        <span className={`text-[10px] px-2 py-0.5 rounded-full border ${DIFFICULTY_COLORS[role.difficulty as keyof typeof DIFFICULTY_COLORS] || DIFFICULTY_COLORS.easy}`}>
          {role.difficulty}
        </span>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
          {role.total_modules} modules
        </span>
      </div>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <Trophy className="w-3 h-3" />
          {role.total_xp} Diamonds
        </span>
        <span className="flex items-center gap-1">
          <TrendingUp className="w-3 h-3" />
          {role.avg_package}
        </span>
      </div>
      {role.enrolled && (
        <div className="mt-3">
          <div className="h-1.5 rounded-full bg-gray-800 overflow-hidden">
            <div className="h-full rounded-full bg-primary-500 transition-all" style={{ width: `${role.progress_pct || 0}%` }} />
          </div>
          <p className="text-[10px] text-gray-500 mt-1">{role.progress_pct || 0}% complete</p>
        </div>
      )}
    </motion.div>
  );
}

function RoleDetail({ roleId, onBack }: { roleId: string; onBack: () => void }) {
  const queryClient = useQueryClient();
  const { data: roleData, isLoading } = useQuery({
    queryKey: ["learning-paths", "role", roleId],
    queryFn: () => api.learningPaths.getRole(roleId),
  });

  const enrollMutation = useMutation({
    mutationFn: () => api.learningPaths.enroll(roleId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["learning-paths"] });
    },
  });

  const [completing, setCompleting] = useState<string | null>(null);

  const handleComplete = async (moduleId: string) => {
    setCompleting(moduleId);
    try {
      await api.learningPaths.completeModule(roleId, moduleId, 85);
      queryClient.invalidateQueries({ queryKey: ["learning-paths", "role", roleId] });
    } catch (e) {
      console.error("Failed to complete module:", e);
    } finally {
      setCompleting(null);
    }
  };

  if (isLoading || !roleData) {
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
      {/* Role Header */}
      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <div className="flex items-start gap-4">
          <div className="text-5xl">{roleData.icon}</div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{roleData.name}</h2>
            <p className="text-sm text-gray-500 mt-1">{roleData.description}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-xs px-2 py-1 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
                {roleData.duration_weeks} weeks
              </span>
              <span className={`text-xs px-2 py-1 rounded-full border ${DIFFICULTY_COLORS[roleData.difficulty as keyof typeof DIFFICULTY_COLORS] || ""}`}>
                {roleData.difficulty}
              </span>
              <span className="text-xs px-2 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
                {roleData.total_xp_earned || 0} / {roleData.total_xp} Diamonds
              </span>
            </div>
          </div>
          {!roleData.enrolled && (
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

      {/* Modules */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-primary-600" />
          Modules
        </h3>
        {roleData.modules?.map((mod, i) => (
          <motion.div
            key={mod.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className={`rounded-xl border p-4 ${mod.completed ? "border-green-500/20 bg-green-500/5" : mod.locked ? "border-gray-500/10 bg-gray-500/5 opacity-60" : "border-white/10 bg-white/[0.02]"}`}
          >
            <div className="flex items-start gap-3">
              <div className="text-2xl">{mod.icon}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-medium text-gray-900">{mod.title}</h4>
                  {mod.completed && <CheckCircle2 className="w-4 h-4 text-green-500" />}
                  {mod.locked && <Lock className="w-4 h-4 text-gray-500" />}
                </div>
                <p className="text-xs text-gray-500 mb-2">{mod.description}</p>
                <div className="flex flex-wrap gap-1 mb-2">
                  {mod.topics.slice(0, 4).map(t => (
                    <span key={t} className="text-[10px] px-1.5 py-0.5 rounded bg-gray-500/10 text-gray-400">{t}</span>
                  ))}
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {mod.duration_days} days
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
              {roleData.enrolled && !mod.locked && !mod.completed && (
                <button
                  onClick={() => handleComplete(mod.id)}
                  disabled={completing === mod.id}
                  className="px-3 py-1.5 rounded-lg bg-primary-600 text-white text-xs font-medium hover:bg-primary-700 disabled:opacity-50"
                >
                  {completing === mod.id ? "Completing..." : "Complete"}
                </button>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Final Project */}
      {roleData.final_project && (
        <div className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2 mb-2">
            <Crown className="w-5 h-5 text-yellow-500" />
            Final Project
          </h3>
          <p className="text-sm text-gray-500 mb-2">{roleData.final_project.description}</p>
          <p className="text-xs text-yellow-600">+{roleData.final_project.xp_reward} Diamonds on completion</p>
        </div>
      )}
    </motion.div>
  );
}
