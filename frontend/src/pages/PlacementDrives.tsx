import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import {
  Building2, Lock, ExternalLink, Clock, MapPin, IndianRupee,
  Users, AlertTriangle, CheckCircle, Zap, TrendingUp, GraduationCap
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

const TIER_STYLES = {
  FAANG: "border-red-300 dark:border-red-800 bg-red-50/50 dark:bg-red-900/5",
  Product: "border-purple-300 dark:border-purple-800 bg-purple-50/50 dark:bg-purple-900/5",
  Services: "border-blue-300 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/5",
  Startup: "border-green-300 dark:border-green-800 bg-green-50/50 dark:bg-green-900/5",
};

export default function PlacementDrives() {
  const [drives, setDrives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all"); // all | eligible | likely
  const reduced = useReducedMotion();

  useEffect(() => {
    loadDrives();
  }, []);

  const loadDrives = async () => {
    setLoading(true);
    try {
      const data = await api.getPlacementDrives();
      setDrives(data.drives || []);
    } catch {} finally {
      setLoading(false);
    }
  };

  const visibleDrives = drives.filter((d) => {
    if (filter === "eligible") return d.eligible;
    if (filter === "likely") return d.likely_to_clear;
    return true;
  });

  const eligibleCount = drives.filter((d) => d.eligible).length;
  const likelyCount = drives.filter((d) => d.likely_to_clear).length;

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
              <GraduationCap size={24} className="text-emerald-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold dark:text-white">Placement Drives</h1>
              <p className="text-gray-600 dark:text-gray-400">Companies you're eligible for and likely to clear</p>
            </div>
          </div>
        </motion.div>

        {/* Stats bar */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[
            { label: "Total Drives", value: drives.length, color: "text-gray-600 dark:text-gray-400" },
            { label: "Eligible", value: eligibleCount, color: "text-green-600" },
            { label: "Likely to Clear", value: likelyCount, color: "text-emerald-600" },
          ].map((s, i) => (
            <AnimatedCard key={s.label} delay={i * 0.05} className="card text-center">
              <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
              <p className="text-xs text-gray-500">{s.label}</p>
            </AnimatedCard>
          ))}
        </div>

        {/* Filters */}
        <div className="flex gap-2 mb-6">
          {[
            { key: "all", label: "All Drives" },
            { key: "eligible", label: `Eligible (${eligibleCount})` },
            { key: "likely", label: `Likely to Clear (${likelyCount})` },
          ].map((f) => (
            <button
              key={f.key}
              onClick={() => setFilter(f.key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === f.key
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="space-y-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2" />
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
              </div>
            ))}
          </div>
        ) : visibleDrives.length === 0 ? (
          <div className="card text-center py-12">
            <GraduationCap size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400">No drives match your filter</p>
          </div>
        ) : (
          <div className="space-y-4">
            {visibleDrives.map((drive, i) => (
              <motion.div
                key={drive.id}
                className={`card border-2 ${drive.locked ? "opacity-60" : TIER_STYLES[drive.tier] || ""}`}
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-bold text-lg dark:text-white">{drive.company}</h3>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                        {drive.tier}
                      </span>
                      {drive.likely_to_clear && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
                          <TrendingUp size={12} /> {drive.probability}% match
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{drive.role}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500">Deadline</p>
                    <p className={`text-sm font-bold ${drive.days_left <= 5 ? "text-red-600" : "text-gray-700 dark:text-gray-300"}`}>
                      {drive.days_left} days
                    </p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3 mb-3 text-sm text-gray-600 dark:text-gray-400">
                  <span className="flex items-center gap-1"><MapPin size={14} /> {drive.location}</span>
                  <span className="flex items-center gap-1"><IndianRupee size={14} /> {drive.package_lpa} LPA</span>
                  {drive.eligibility?.min_cgpa && (
                    <span className="flex items-center gap-1"><GraduationCap size={14} /> Min CGPA {drive.eligibility.min_cgpa}</span>
                  )}
                </div>

                {drive.match_reasons?.length > 0 && (
                  <div className="mb-3">
                    {drive.match_reasons.slice(0, 3).map((reason, ri) => (
                      <div key={ri} className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-400 mb-1">
                        {drive.eligible ? (
                          <CheckCircle size={12} className="text-green-500" />
                        ) : (
                          <AlertTriangle size={12} className="text-red-500" />
                        )}
                        {reason}
                      </div>
                    ))}
                  </div>
                )}

                {drive.locked ? (
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Lock size={14} />
                    Upgrade to Pro to unlock this drive alert
                  </div>
                ) : (
                  drive.apply_url && (
                    <a
                      href={drive.apply_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                      Apply Now <ExternalLink size={14} />
                    </a>
                  )
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
