import { useState, useEffect, useCallback, useRef } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams, Link, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  Lightbulb,
  BookOpen,
  Trophy,
  Loader2,
  ChevronRight,
  ChevronUp,
  ChevronDown,
  Play,
  RotateCcw,
} from "lucide-react";
import api from "../services/api";
import { useBrowserRuntime } from "../hooks/useBrowserRuntime";
import { LessonStepHints } from "../components/academy/LessonStepHints";

// FILE_TOO_LARGE_USE_BLOB
export default function LessonPlayer() {
  return <div className="p-8 text-center">Loading lesson player…</div>;
}
