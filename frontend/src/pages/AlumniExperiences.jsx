import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import {
  Building2, Lock, ChevronDown, Star, AlertTriangle,
  CheckCircle, XCircle, Users, Calendar, MapPin, Tag
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

const OUTCOME_COLORS = {
  selected: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  rejected: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
  pending: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
};

export default function AlumniExperiences() {
  const [experiences, setExperiences] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedRole, setSelectedRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [lockedCount, setLockedCount] = useState(0);
  const [proUnlocksAll, setProUnlocksAll] = useState(false);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadExperiences();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [selectedCompany, selectedRole, experiences]);

  const loadExperiences = async () => {
    setLoading(true);
    try {
      const data = await api.getAlumniExperiences();
      setExperiences(data.experiences || []);
      setLockedCount(data.locked_count || 0);
      setProUnlocksAll(data.pro_unlocks_all || false);

      const uniqueCompanies = [...new Set((data.experiences || []).map((e) => e.company))];
      setCompanies(uniqueCompanies.sort());
    } catch {} finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let result = experiences;
    if (selectedCompany) {
      result = result.filter((e) => e.company === selectedCompany);
    }
    if (selectedRole) {
      result = result.filter((e) => e.role?.toLowerCase().includes(selectedRole.toLowerCase()));
    }
    setFiltered(result);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center">
              <Users size={24} className="text-purple-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold dark:text-white">Alumni Experiences</h1>
              <p className="text-gray-600 dark:text-gray-400">Real interview stories from people who've been in the room</p>
            </div>
          </div>
        </motion.div>

        {lockedCount > 0 && proUnlocksAll && (
          <AnimatedCard className="card mb-6 border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-900/10">
            <div className="flex items-center gap-3">
              <Lock size={20} className="text-yellow-600" />
              <p className="text-sm text-yellow-800 dark:text-yellow-300">
                {lockedCount} experience{lockedCount > 1 ? "s" : ""} locked. Upgrade to Pro to unlock all alumni stories.
              </p>
            </div>
          </AnimatedCard>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3 mb-6">
          <div className="relative">
            <Building2 size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <select
              value={selectedCompany}
              onChange={(e) => setSelectedCompany(e.target.value)}
              className="pl-10 pr-8 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm appearance-none"
            >
              <option value="">All Companies</option>
              {companies.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
          <div className="relative flex-1 min-w-[200px]">
            <input
              type="text"
              placeholder="Filter by role..."
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm"
            />
          </div>
        </div>

        {loading ? (
          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-3" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full mb-2" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3" />
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="card text-center py-12">
            <Users size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No experiences found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map((exp, i) => (
              <motion.div
                key={exp.id}
                className={`card ${exp.locked ? "opacity-75" : ""}`}
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-bold text-lg dark:text-white">{exp.role}</h3>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${OUTCOME_COLORS[exp.outcome] || OUTCOME_COLORS.pending}`}>
                        {exp.outcome}
                      </span>
                    </div>
                    <div className="flex flex-wrap items-center gap-3 text-sm text-gray-500">
                      <span className="flex items-center gap-1"><Building2 size={14} /> {exp.company}</span>
                      <span className="flex items-center gap-1"><Calendar size={14} /> {exp.year}</span>
                      <span className="flex items-center gap-1"><MapPin size={14} /> {exp.campus}</span>
                      <span className="flex items-center gap-1"><Star size={14} /> {exp.difficulty}/10</span>
                    </div>
                  </div>
                  {exp.locked && <Lock size={18} className="text-gray-400" />}
                </div>

                {exp.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-3">
                    {exp.tags.map((tag, ti) => (
                      <span key={ti} className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 flex items-center gap-1">
                        <Tag size={10} /> {tag}
                      </span>
                    ))}
                  </div>
                )}

                {!exp.locked && exp.rounds?.length > 0 && (
                  <div className="space-y-3 mb-4">
                    {exp.rounds.map((round, ri) => (
                      <div key={ri} className="bg-gray-50 dark:bg-gray-700/30 rounded-lg p-4 border-l-4 border-primary-400">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-sm dark:text-white">{round.name}</span>
                          <span className="text-xs text-gray-500">{round.duration}</span>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{round.what_happened}</p>
                      </div>
                    ))}
                  </div>
                )}

                {exp.locked && exp.rounds_teaser?.length > 0 && (
                  <div className="mb-4">
                    {exp.rounds_teaser.map((r, ri) => (
                      <div key={ri} className="flex items-center gap-2 text-sm text-gray-500 mb-1">
                        <span className="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xs font-bold text-gray-600 dark:text-gray-400">
                          {ri + 1}
                        </span>
                        <span>{r.name}</span>
                        <span className="text-xs text-gray-400">({r.duration})</span>
                        <Lock size={12} className="text-gray-400 ml-auto" />
                      </div>
                    ))}
                    <p className="text-xs text-gray-400 mt-2">Unlock full round details with Pro</p>
                  </div>
                )}

                {!exp.locked && exp.tips?.length > 0 && (
                  <div className="bg-yellow-50 dark:bg-yellow-900/10 rounded-lg p-4">
                    <h4 className="font-semibold text-sm text-yellow-800 dark:text-yellow-300 mb-2 flex items-center gap-2">
                      <Star size={14} /> Tips from the candidate
                    </h4>
                    <ul className="space-y-1">
                      {exp.tips.map((tip, ti) => (
                        <li key={ti} className="text-sm text-gray-600 dark:text-gray-400 flex items-start gap-2">
                          <span className="text-yellow-500 mt-0.5">•</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
