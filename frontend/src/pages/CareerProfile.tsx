import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  User, Briefcase, GraduationCap, FolderGit2, Award,
  Upload, Plus, Trash2, Save, Sparkles, ExternalLink, Link as LinkIcon, Github, Linkedin, Target
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";
import Spinner from "../components/ui/Spinner";

const TABS = [
  { id: "contact", label: "Contact", icon: User },
  { id: "experience", label: "Experience", icon: Briefcase },
  { id: "education", label: "Education", icon: GraduationCap },
  { id: "projects", label: "Projects", icon: FolderGit2 },
  { id: "certifications", label: "Certifications", icon: Award },
  { id: "skills", label: "Skills", icon: Sparkles },
];

export default function CareerProfile() {
  const [profile, setProfile] = useState(null);
  const [activeTab, setActiveTab] = useState("contact");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [practiceCompany, setPracticeCompany] = useState("");
  const [practiceRole, setPracticeRole] = useState("SDE");
  const [practiceResult, setPracticeResult] = useState(null);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const data = await api.getCareerProfile();
      setProfile(data);
    } catch {} finally {
      setLoading(false);
    }
  };

  const handleSave = async (updates) => {
    setSaving(true);
    try {
      const data = await api.updateCareerProfile(updates);
      setProfile(data);
      setMessage("Saved successfully");
      setTimeout(() => setMessage(""), 2000);
    } catch {} finally {
      setSaving(false);
    }
  };

  const handleUploadResume = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const data = await api.uploadResumeToProfile(file);
      setProfile(data);
      setMessage("Profile parsed from resume");
      setTimeout(() => setMessage(""), 3000);
    } catch {} finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const handleAddItem = async (section, item) => {
    const data = await api.addProfileSectionItem(section, { item });
    setProfile(data);
  };

  const handleRemoveItem = async (section, index) => {
    const data = await api.removeProfileSectionItem(section, index);
    setProfile(data);
  };

  const handlePracticeForRole = async (e) => {
    e.preventDefault();
    if (!practiceCompany.trim()) return;
    setPracticeResult(null);
    try {
      const data = await api.createPracticeSession({ company: practiceCompany.trim(), role: practiceRole.trim() || "SDE" });
      setPracticeResult(data);
    } catch {}
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Failed to load profile</p>
      </div>
    );
  }

  const sourceLabel = {
    manual: "Manually created",
    resume_upload: "Imported from resume",
    github: "Imported from GitHub",
    linkedin: "Imported from LinkedIn",
  }[profile.source] || "Career Profile";

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center">
                <User size={24} className="text-indigo-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold dark:text-white">Career Profile</h1>
                <p className="text-gray-600 dark:text-gray-400">
                  {profile.full_name || "Your master profile"} · {sourceLabel}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                <Upload size={16} />
                <span className="text-sm font-medium">Import Resume</span>
                <input type="file" accept=".pdf" className="hidden" onChange={handleUploadResume} disabled={uploading} />
              </label>
              {uploading && <Spinner size="sm" />}
            </div>
          </div>
        </motion.div>

        {message && (
          <motion.div className="mb-6 px-4 py-3 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 text-sm"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {message}
          </motion.div>
        )}

        {/* Practice for This Role */}
        <form onSubmit={handlePracticeForRole} className="card mb-6">
          <div className="flex flex-wrap items-end gap-3">
            <div className="flex-1 min-w-[180px]">
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Target Company</label>
              <input className="input" placeholder="e.g. Amazon" value={practiceCompany} onChange={(e) => setPracticeCompany(e.target.value)} required />
            </div>
            <div className="w-40">
              <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Role</label>
              <input className="input" placeholder="SDE" value={practiceRole} onChange={(e) => setPracticeRole(e.target.value)} />
            </div>
            <button type="submit" className="btn-primary flex items-center gap-2">
              <Target size={16} /> Practice for This Role
            </button>
          </div>
          {practiceResult && (
            <div className="mt-4 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
              <p className="text-sm font-semibold dark:text-white mb-2">Practice session created for {practiceResult.company}</p>
              <div className="flex flex-wrap gap-4 text-xs text-gray-600 dark:text-gray-400">
                <span>Coding: {practiceResult.coding?.length || 0}</span>
                <span>Behavioral: {practiceResult.behavioral?.length || 0}</span>
                <span>System Design: {practiceResult.system_design?.length || 0}</span>
                <span>Probability: {practiceResult.probability_before}% → {practiceResult.probability_after_target}%</span>
              </div>
            </div>
          )}
        </form>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Sidebar tabs */}
          <div className="lg:col-span-1">
            <div className="card p-2">
              {TABS.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                      : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
                  }`}
                >
                  <tab.icon size={18} />
                  {tab.label}
                </button>
              ))}
            </div>

            {profile.resume_id && (
              <div className="mt-4 card p-4">
                <p className="text-xs text-gray-500 mb-2">Source Resume</p>
                <p className="text-sm font-medium dark:text-white">Linked to resume upload</p>
              </div>
            )}
          </div>

          {/* Tab content */}
          <div className="lg:col-span-3">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === "contact" && (
                  <ContactTab profile={profile} onSave={handleSave} saving={saving} />
                )}
                {activeTab === "experience" && (
                  <ListSectionTab
                    title="Experience"
                    items={profile.experience || []}
                    emptyLabel="No experience added yet"
                    onAdd={(item) => handleAddItem("experience", item)}
                    onRemove={(idx) => handleRemoveItem("experience", idx)}
                    renderForm={ExperienceForm}
                    renderItem={ExperienceItem}
                  />
                )}
                {activeTab === "education" && (
                  <ListSectionTab
                    title="Education"
                    items={profile.education || []}
                    emptyLabel="No education added yet"
                    onAdd={(item) => handleAddItem("education", item)}
                    onRemove={(idx) => handleRemoveItem("education", idx)}
                    renderForm={EducationForm}
                    renderItem={EducationItem}
                  />
                )}
                {activeTab === "projects" && (
                  <ListSectionTab
                    title="Projects"
                    items={profile.projects || []}
                    emptyLabel="No projects added yet"
                    onAdd={(item) => handleAddItem("projects", item)}
                    onRemove={(idx) => handleRemoveItem("projects", idx)}
                    renderForm={ProjectForm}
                    renderItem={ProjectItem}
                  />
                )}
                {activeTab === "certifications" && (
                  <ListSectionTab
                    title="Certifications"
                    items={profile.certifications || []}
                    emptyLabel="No certifications added yet"
                    onAdd={(item) => handleAddItem("certifications", item)}
                    onRemove={(idx) => handleRemoveItem("certifications", idx)}
                    renderForm={CertificationForm}
                    renderItem={CertificationItem}
                  />
                )}
                {activeTab === "skills" && (
                  <SkillsTab skills={profile.skills || []} onSave={handleSave} saving={saving} />
                )}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Sub-components ──────────────────────────────────────────────────────── */

function ContactTab({ profile, onSave, saving }) {
  const [form, setForm] = useState({
    full_name: profile.full_name || "",
    email: profile.contact?.email || "",
    phone: profile.contact?.phone || "",
    location: profile.contact?.location || "",
    linkedin: profile.contact?.linkedin || "",
    github: profile.contact?.github || "",
    website: profile.contact?.website || "",
    summary: profile.summary || "",
  });

  useEffect(() => {
    setForm({
      full_name: profile.full_name || "",
      email: profile.contact?.email || "",
      phone: profile.contact?.phone || "",
      location: profile.contact?.location || "",
      linkedin: profile.contact?.linkedin || "",
      github: profile.contact?.github || "",
      website: profile.contact?.website || "",
      summary: profile.summary || "",
    });
  }, [profile]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      full_name: form.full_name,
      contact: {
        email: form.email, phone: form.phone, location: form.location,
        linkedin: form.linkedin, github: form.github, website: form.website,
      },
      summary: form.summary,
    });
  };

  const inputClass = "w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm focus:ring-2 focus:ring-primary-500";

  return (
    <AnimatedCard className="card">
      <h2 className="text-xl font-bold mb-4 dark:text-white">Contact & Summary</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
            <input className={inputClass} value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input className={inputClass} type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Phone</label>
            <input className={inputClass} value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Location</label>
            <input className={inputClass} value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">LinkedIn</label>
            <div className="relative">
              <Linkedin size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input className={`${inputClass} pl-10`} value={form.linkedin} onChange={(e) => setForm({ ...form, linkedin: e.target.value })} />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">GitHub</label>
            <div className="relative">
              <Github size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input className={`${inputClass} pl-10`} value={form.github} onChange={(e) => setForm({ ...form, github: e.target.value })} />
            </div>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Website / Portfolio</label>
          <div className="relative">
            <LinkIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input className={`${inputClass} pl-10`} value={form.website} onChange={(e) => setForm({ ...form, website: e.target.value })} />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Professional Summary</label>
          <textarea
            className={inputClass}
            rows={4}
            value={form.summary}
            onChange={(e) => setForm({ ...form, summary: e.target.value })}
            placeholder="Brief summary of your background and goals..."
          />
        </div>

        <button type="submit" disabled={saving} className="btn-primary flex items-center gap-2">
          {saving ? "Saving..." : <><Save size={18} /> Save Changes</>}
        </button>
      </form>
    </AnimatedCard>
  );
}

function ListSectionTab({ title, items, emptyLabel, onAdd, onRemove, renderForm, renderItem }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd(formData);
    setFormData({});
    setShowForm(false);
  };

  return (
    <AnimatedCard className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold dark:text-white">{title}</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary text-sm py-2 flex items-center gap-2">
          <Plus size={16} /> Add {title.slice(0, -1)}
        </button>
      </div>

      {showForm && (
        <motion.form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 dark:bg-gray-700/30 rounded-lg space-y-3"
          initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}>
          {renderForm(formData, setFormData)}
          <div className="flex gap-2">
            <button type="submit" className="btn-primary text-sm py-2">Save</button>
            <button type="button" onClick={() => { setShowForm(false); setFormData({}); }} className="btn-secondary text-sm py-2">Cancel</button>
          </div>
        </motion.form>
      )}

      {items.length === 0 ? (
        <p className="text-gray-400 dark:text-gray-500 text-sm">{emptyLabel}</p>
      ) : (
        <div className="space-y-4">
          {items.map((item, idx) => (
            <div key={idx} className="flex items-start justify-between p-4 bg-gray-50 dark:bg-gray-700/30 rounded-lg">
              <div className="flex-1 min-w-0">
                {renderItem(item, idx)}
              </div>
              <button onClick={() => onRemove(idx)} className="ml-3 p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg">
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </AnimatedCard>
  );
}

function ExperienceForm(data, set) {
  return (
    <>
      <div className="grid md:grid-cols-2 gap-3">
        <input className="input" placeholder="Job Title" value={data.title || ""} onChange={(e) => set({ ...data, title: e.target.value })} required />
        <input className="input" placeholder="Company" value={data.company || ""} onChange={(e) => set({ ...data, company: e.target.value })} required />
        <input className="input" placeholder="Location" value={data.location || ""} onChange={(e) => set({ ...data, location: e.target.value })} />
        <input className="input" placeholder="Start Date (YYYY or YYYY-MM)" value={data.start_date || ""} onChange={(e) => set({ ...data, start_date: e.target.value })} />
        <input className="input" placeholder="End Date (or 'Present')" value={data.end_date || ""} onChange={(e) => set({ ...data, end_date: e.target.value })} />
        <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
          <input type="checkbox" checked={data.current || false} onChange={(e) => set({ ...data, current: e.target.checked })} />
          Current role
        </label>
      </div>
      <textarea className="input" rows={3} placeholder="Bullets (one per line)" value={(data.bullets || []).join("\n")} onChange={(e) => set({ ...data, bullets: e.target.value.split("\n").filter(Boolean) })} />
    </>
  );
}

function ExperienceItem(item) {
  return (
    <>
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-semibold text-sm dark:text-white">{item.title}</h3>
        <span className="text-gray-400">at</span>
        <span className="text-sm text-gray-600 dark:text-gray-400">{item.company}</span>
        {item.current && <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700">Current</span>}
      </div>
      <p className="text-xs text-gray-500 mb-2">{item.location} · {item.start_date} — {item.end_date || "Present"}</p>
      {item.bullets?.length > 0 && (
        <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400 space-y-1">
          {item.bullets.slice(0, 3).map((b, i) => <li key={i}>{b}</li>)}
        </ul>
      )}
    </>
  );
}

function EducationForm(data, set) {
  return (
    <div className="grid md:grid-cols-2 gap-3">
      <input className="input" placeholder="School / University" value={data.school || ""} onChange={(e) => set({ ...data, school: e.target.value })} required />
      <input className="input" placeholder="Degree" value={data.degree || ""} onChange={(e) => set({ ...data, degree: e.target.value })} required />
      <input className="input" placeholder="Field of Study" value={data.field || ""} onChange={(e) => set({ ...data, field: e.target.value })} />
      <input className="input" placeholder="Start Year" value={data.start_year || ""} onChange={(e) => set({ ...data, start_year: e.target.value })} />
      <input className="input" placeholder="End Year" value={data.end_year || ""} onChange={(e) => set({ ...data, end_year: e.target.value })} />
      <input className="input" placeholder="GPA" value={data.gpa || ""} onChange={(e) => set({ ...data, gpa: e.target.value })} />
    </div>
  );
}

function EducationItem(item) {
  return (
    <>
      <h3 className="font-semibold text-sm dark:text-white">{item.school}</h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">{item.degree} in {item.field}</p>
      <p className="text-xs text-gray-500">{item.start_year} — {item.end_year} {item.gpa ? `· GPA: ${item.gpa}` : ""}</p>
    </>
  );
}

function ProjectForm(data, set) {
  return (
    <div className="space-y-3">
      <input className="input" placeholder="Project Name" value={data.name || ""} onChange={(e) => set({ ...data, name: e.target.value })} required />
      <textarea className="input" rows={2} placeholder="Description" value={data.description || ""} onChange={(e) => set({ ...data, description: e.target.value })} />
      <input className="input" placeholder="Tech Stack (comma-separated)" value={(data.tech_stack || []).join(", ")} onChange={(e) => set({ ...data, tech_stack: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })} />
      <input className="input" placeholder="Link (optional)" value={data.link || ""} onChange={(e) => set({ ...data, link: e.target.value })} />
      <textarea className="input" rows={2} placeholder="Highlights (one per line)" value={(data.highlights || []).join("\n")} onChange={(e) => set({ ...data, highlights: e.target.value.split("\n").filter(Boolean) })} />
    </div>
  );
}

function ProjectItem(item) {
  return (
    <>
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-semibold text-sm dark:text-white">{item.name}</h3>
        {item.link && (
          <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-primary-600">
            <ExternalLink size={14} />
          </a>
        )}
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{item.description}</p>
      <div className="flex flex-wrap gap-1 mb-1">
        {item.tech_stack?.map((t, i) => (
          <span key={i} className="text-xs px-2 py-0.5 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400">{t}</span>
        ))}
      </div>
      {item.highlights?.length > 0 && (
        <ul className="list-disc list-inside text-xs text-gray-500 space-y-0.5">
          {item.highlights.slice(0, 2).map((h, i) => <li key={i}>{h}</li>)}
        </ul>
      )}
    </>
  );
}

function CertificationForm(data, set) {
  return (
    <div className="grid md:grid-cols-2 gap-3">
      <input className="input" placeholder="Certification Name" value={data.name || ""} onChange={(e) => set({ ...data, name: e.target.value })} required />
      <input className="input" placeholder="Issuer" value={data.issuer || ""} onChange={(e) => set({ ...data, issuer: e.target.value })} required />
      <input className="input" placeholder="Date (YYYY-MM)" value={data.date || ""} onChange={(e) => set({ ...data, date: e.target.value })} />
      <input className="input" placeholder="Expiry (YYYY-MM, optional)" value={data.expiry || ""} onChange={(e) => set({ ...data, expiry: e.target.value })} />
      <input className="input md:col-span-2" placeholder="Credential ID (optional)" value={data.credential_id || ""} onChange={(e) => set({ ...data, credential_id: e.target.value })} />
    </div>
  );
}

function CertificationItem(item) {
  return (
    <>
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-semibold text-sm dark:text-white">{item.name}</h3>
        <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400">
          {item.issuer}
        </span>
      </div>
      <p className="text-xs text-gray-500">
        {item.date} {item.expiry ? `· Expires ${item.expiry}` : ""}
        {item.credential_id ? `· ID: ${item.credential_id}` : ""}
      </p>
    </>
  );
}

function SkillsTab({ skills, onSave, saving }) {
  const [input, setInput] = useState("");
  const [local, setLocal] = useState(skills);

  useEffect(() => {
    setLocal(skills);
  }, [skills]);

  const addSkill = () => {
    const val = input.trim();
    if (!val) return;
    const next = [...local, val];
    setLocal(next);
    setInput("");
    onSave({ skills: next });
  };

  const removeSkill = (idx) => {
    const next = local.filter((_, i) => i !== idx);
    setLocal(next);
    onSave({ skills: next });
  };

  return (
    <AnimatedCard className="card">
      <h2 className="text-xl font-bold mb-4 dark:text-white">Skills</h2>
      <div className="flex gap-2 mb-4">
        <input
          className="input flex-1"
          placeholder="Add a skill..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
        />
        <button onClick={addSkill} className="btn-primary flex items-center gap-2">
          <Plus size={16} /> Add
        </button>
      </div>
      {local.length === 0 ? (
        <p className="text-gray-400 dark:text-gray-500 text-sm">No skills added yet</p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {local.map((skill, idx) => (
            <span key={idx} className="inline-flex items-center gap-1 px-3 py-1.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-full text-sm">
              {skill}
              <button onClick={() => removeSkill(idx)} className="hover:text-red-500">
                <Trash2 size={14} />
              </button>
            </span>
          ))}
        </div>
      )}
    </AnimatedCard>
  );
}
