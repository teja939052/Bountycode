import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "../public/curriculum");
const languagesDir = path.join(root, "languages");

const TRACK_META = {
  html: { title: "HTML", icon: "Code2", color: "#F97316", difficulty: "beginner", tagline: "Structure the web — from your first tag to full pages." },
  css: { title: "CSS", icon: "Palette", color: "#3B82F6", difficulty: "beginner", tagline: "Bring pages to life — colors, layout, and responsive design." },
  javascript: { title: "JavaScript", icon: "Braces", color: "#EAB308", difficulty: "beginner", tagline: "Make pages interactive — variables to events." },
  python: { title: "Python", icon: "Terminal", color: "#3776AB", difficulty: "beginner", tagline: "The friendliest language — perfect for your first program." },
  java: { title: "Java", icon: "Coffee", color: "#F59E0B", difficulty: "beginner", tagline: "The classic OOP language behind Android and enterprise apps." },
  cpp: { title: "C++", icon: "Cpu", color: "#8B5CF6", difficulty: "beginner", tagline: "Speed and control — the language of systems and games." },
  sql: { title: "SQL", icon: "Database", color: "#06B6D4", difficulty: "beginner", tagline: "Query data like a pro — the language of databases." },
};

const tracks = [];

const byTrack = {};

for (const dir of fs.readdirSync(languagesDir)) {
  const lessonFiles = fs
    .readdirSync(path.join(languagesDir, dir))
    .filter((f) => f.endsWith(".json"));

  for (const f of lessonFiles) {
    const raw = JSON.parse(fs.readFileSync(path.join(languagesDir, dir, f), "utf8"));
    const trackId = raw.track;
    if (!TRACK_META[trackId]) continue;
    if (!byTrack[trackId]) byTrack[trackId] = [];
    byTrack[trackId].push({
      id: raw.id,
      title: raw.title,
      type: raw.type || "lesson",
      duration: raw.duration,
      xp: raw.xp,
      section: raw.section,
      order: raw.order,
    });
  }
}

for (const [trackId, lessons] of Object.entries(byTrack)) {
  lessons.sort((a, b) => (a.order || 0) - (b.order || 0));

  const sections = [];
  for (const lesson of lessons) {
    const sectionName = lesson.section || "Lessons";
    let section = sections.find((s) => s.title === sectionName);
    if (!section) {
      section = { id: sectionName.toLowerCase().replace(/[^a-z0-9]+/g, "-"), title: sectionName, lessons: [] };
      sections.push(section);
    }
    const { section: _s, order: _o, ...lessonMeta } = lesson;
    section.lessons.push(lessonMeta);
  }

  tracks.push({ id: trackId, ...TRACK_META[trackId], sections });
}

const index = { version: 1, tracks };
fs.writeFileSync(path.join(root, "index.json"), JSON.stringify(index, null, 2) + "\n", "utf8");
console.log(`index.json written: ${tracks.length} tracks, ${tracks.reduce((n, t) => n + t.sections.reduce((m, s) => m + s.lessons.length, 0), 0)} lessons`);
