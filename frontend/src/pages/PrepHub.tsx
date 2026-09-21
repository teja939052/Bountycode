import { useState } from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import {
  Search, BookOpen, Building2, Code2, Trophy, TrendingUp,
  Sparkles, ArrowRight, Flame, Target, Zap, Star, Crown,
  BarChart3, Briefcase, Users, Clock,
} from "lucide-react";

type Tab = "roles" | "companies" | "recommended";

export default function PrepHub() {
  const [tab, setTab] = useState<Tab>("recommended");
  const [search, setSearch] = useState("");

  const { data: rolesData } = useQuery({
    queryKey: ["learning-paths", "roles"],
    queryFn: () => api.learningPaths.listRoles(),
  });

  const { data: tracksData } = useQuery({
    queryKey: ["company-tracks", "list"],
    queryFn: () => api.companyTracks.listCompanies(),
  });

  const { data: recsData } = useQuery({
    queryKey: ["learning-paths", "recommendations"],
    queryFn: () => api.learningPaths.getRecommendations(),
  });

  const roles = rolesData?.paths || [];
  const tracks = tracksData?.tracks || [];
  const recommendations = recsData?.recommendations || [];

  const filteredRoles = roles.filter(r =>
    r.name.toLowerCase().includes(search.toLowerCase()) ||
    r.short_name.toLowerCase().includes(search.toLowerCase()) ||
    r.description.toLowerCase().includes(search.toLowerCase())
  );

  const filteredTracks = tracks.filter(t =>
    t.name.toLowerCase().includes(search.toLowerCase()) ||
    t.full_name.toLowerCase().includes(search.toLowerCase()) ||
    t.role.toLowerCase().includes(search.toLowerCase())
  );

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
            <Target className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Prep Hub</h1>
            <p className="text-sm text-gray-500">Your unified command center for placement preparation</p>
          </div>
        </div>
      </motion.div>

      {/* Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search roles, companies, skills..."
            className="w-full pl-10 pr-4 py-3 rounded-xl border border-white/10 bg-white/[0.03] text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500/50"
          />
        </div>
      </motion.div>

      {/* Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 flex gap-2"
      >
        {[
          { id: "recommended" as Tab, label: "For You", icon: Sparkles },
          { id: "roles" as Tab, label: "Learning Paths", icon: BookOpen },
          { id: "companies" as Tab, label: "Company Tracks", icon: Building2 },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              tab === t.id
                ? "bg-primary-600 text-white shadow-lg shadow-primary-500/20"
                : "bg-white/[0.03] text-gray-500 hover:text-gray-700 border border-white/10"
            }`}
          >
            <t.icon className="w-4 h-4" />
            {t.label}
          </button>
        ))}
      </motion.div>

      {/* Content */}
      {tab === "recommended" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          {/* Recommended Roles */}
          {recommendations.length > 0 && (
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-yellow-500" />
                Recommended Learning Paths
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {recommendations.map((rec, i) => (
                  <motion.div
                    key={rec.path_id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.1 }}
                  >
                    <Link to={`/learning-paths?role=${rec.path_id}`} className="block">
                      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all">
                        <div className="flex items-center gap-2 mb-2 text-xs text-yellow-400">
                          <Sparkles className="w-3 h-3" />
                          <span>{rec.match_score}% match</span>
                        </div>
                        <h3 className="font-semibold text-gray-900">{rec.name}</h3>
                        <p className="text-xs text-gray-500 mt-1 line-clamp-2">{rec.reason}</p>
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Top Companies */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Building2 className="w-5 h-5 text-primary-600" />
              Top Company Tracks
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {tracks.slice(0, 6).map((track, i) => (
                <motion.div
                  key={track.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Link to={`/company-tracks?track=${track.id}`} className="block">
                    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all">
                      <div className="flex items-start gap-3">
                        <div className="text-2xl">{track.icon}</div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-gray-900 truncate">{track.name}</h3>
                          <p className="text-xs text-gray-500 line-clamp-2">{track.description}</p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-gray-500/10 text-gray-400">
                              {track.package_range}
                            </span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-green-500/10 text-green-400">
                              {track.difficulty}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {tab === "roles" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          {filteredRoles.map((role, i) => (
            <motion.div
              key={role.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link to={`/learning-paths?role=${role.id}`} className="block">
                <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all h-full">
                  <div className="flex items-start gap-3 mb-3">
                    <div className="text-3xl">{role.icon}</div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900">{role.short_name}</h3>
                      <p className="text-xs text-gray-500 line-clamp-2">{role.description}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
                      {role.duration_weeks} weeks
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
                      {role.total_modules} modules
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
                      {role.avg_package}
                    </span>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      )}

      {tab === "companies" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          {filteredTracks.map((track, i) => (
            <motion.div
              key={track.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link to={`/company-tracks?track=${track.id}`} className="block">
                <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 hover:border-primary-500/30 hover:shadow-lg hover:shadow-primary-500/5 transition-all h-full">
                  <div className="flex items-start gap-3 mb-3">
                    <div className="text-3xl">{track.icon}</div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-gray-900 truncate">{track.name}</h3>
                      <p className="text-xs text-gray-500 line-clamp-2">{track.description}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 border border-gray-500/20">
                      {track.duration_minutes} min
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
                      {track.total_modules} modules
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">
                      {track.package_range}
                    </span>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
