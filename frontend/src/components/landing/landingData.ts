import {
  Home,
  Trees,
  Mountain,
  Building2,
  Rocket,
  Crown,
  Code2,
  MessageSquare,
  FileText,
  Target,
  TrendingUp,
  Users,
} from "lucide-react";

export const world = [
  { icon: Home, label: "Village", blurb: "Aptitude & fundamentals" },
  { icon: Trees, label: "Forest", blurb: "Core DSA patterns" },
  { icon: Mountain, label: "Mountain", blurb: "Advanced algorithms" },
  { icon: Building2, label: "Cyber City", blurb: "System design & LLD" },
  { icon: Rocket, label: "Silicon Valley", blurb: "Product & behavioral" },
  { icon: Crown, label: "FAANG Castle", blurb: "Company-specific rounds" },
];

export const howItWorks = [
  { word: "Learn.", line: "Bite-size lessons across 7 languages. No walls of text." },
  { word: "Practice.", line: "Daily quests, streaks, and code that actually runs." },
  { word: "Level up.", line: "XP, calm boss battles, and a skill radar that guides you." },
  { word: "Get placed.", line: "Company mocks, ATS-ready resume, and salary coaching." },
];

export const coreFeatures = [
  { icon: Code2, title: "DSA Practice", desc: "Curated problems with hidden tests, progressive hints, and company filters." },
  { icon: MessageSquare, title: "AI Mock Interviews", desc: "Company-specific questions with calm, instant AI feedback after each round." },
  { icon: FileText, title: "Resume & ATS", desc: "Upload, get an honest ATS score, and rewrite bullets that actually pass." },
  { icon: Target, title: "Aptitude Drills", desc: "Quant, logical, verbal, and technical questions for campus tests." },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Streaks, XP, and weak-area detection — you always know what's next." },
  { icon: Users, title: "Company Prep", desc: "53+ company guides with patterns, behavioral questions, and experiences." },
];

export const testimonials = [
  { name: "Priya S.", role: "SDE at Amazon", text: "The aptitude drills and mock interviews felt exactly like the real thing. I cleared 5 company tests in one month.", tone: "bg-nature-blossom/20 text-nature-blossom" },
  { name: "Rahul V.", role: "TCS NQT Ranker", text: "I used the question bank and ATS scanner daily. The progress heatmap kept me accountable.", tone: "bg-nature-blossom/20 text-nature-blossom" },
  { name: "Ananya M.", role: "PM at Google", text: "The resume optimizer and salary coach helped me negotiate a 40% higher offer.", tone: "bg-nature-blossom/20 text-nature-blossom" },
];

export const plans = [
  {
    title: "Free",
    price: "$0",
    cadence: "Monthly reset",
    note: "Everything you need to build the habit.",
    features: ["3 interviews / month", "3 resume reviews / month", "5 aptitude tests / month", "3 cover letters / month"],
    cta: "Start free",
    featured: false,
  },
  {
    title: "Pro",
    price: "$9",
    cadence: "Per month",
    note: "For the final sprint before drives.",
    features: ["Unlimited interviews", "Unlimited resume & ATS", "ATS optimization", "Priority support"],
    cta: "Upgrade",
    featured: true,
  },
  {
    title: "Lifetime",
    price: "$39",
    cadence: "One-time",
    note: "Pay once, keep every future update.",
    features: ["Everything in Pro", "All future features", "Lifetime access", "Best value"],
    cta: "Go lifetime",
    featured: false,
  },
];

export const CROWS = [
  { x: 770, y: 68, flip: 1 },
  { x: 720, y: 86, flip: -1 },
];

export const TREES = [
  { x: 60, y: 325, s: 1.1 },
  { x: 880, y: 330, s: 0.9 },
  { x: 460, y: 318, s: 0.8 },
  { x: 1020, y: 332, s: 0.75 },
];

export const BUSHES = [
  { x: 160, y: 340, s: 1.0, c: ["#2E6B35", "#3F7A47", "#356B3A"] },
  { x: 640, y: 360, s: 0.8, c: ["#356B3A", "#4F8F57", "#3F7A47"] },
  { x: 920, y: 348, s: 0.9, c: ["#4F8F57", "#356B3A", "#3F7A47"] },
  { x: 1080, y: 358, s: 0.7, c: ["#2E6B35", "#356B3A", "#3F7A47"] },
];

export const GRASS = [60, 180, 300, 420, 540, 680, 790, 920, 1040, 1140];

export const PEACOCKS = [{ x: 820, y: 200, s: 0.75 }, { x: 520, y: 335, s: 0.6 }];

export const BUTTERFLIES = [
  { x: 150, y: 200, s: 0.7, c: "#0EA5E9" },
  { x: 480, y: 190, s: 0.6, c: "#F97316" },
  { x: 960, y: 230, s: 0.7, c: "#EF4444" },
  { x: 700, y: 120, s: 0.55, c: "#FACC15" },
];

export const LOTUS = [
  { x: 860, y: 222, s: 1 },
  { x: 780, y: 230, s: 0.85 },
  { x: 940, y: 250, s: 0.9 },
];

export const FIREFLIES = [120, 250, 520, 680, 820, 960, 1080];

export const FLOCK = [730, 750, 772, 790];
