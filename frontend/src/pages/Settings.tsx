import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { User, Mail, Lock, Save, Shield, CreditCard, Crown } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";

export default function Settings() {
  const { user } = useAuthStore();
  const [name, setName] = useState(user?.name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [activeTab, setActiveTab] = useState("profile");
  const reduced = useReducedMotion();

  const isPremium = user?.plan === "pro" || user?.plan === "lifetime";

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      await api.updateProfile(name, email);
      setMessage("Profile updated successfully!");
    } catch (err) {
      setMessage(err.message || "Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      await api.changePassword(currentPassword, newPassword);
      setMessage("Password changed successfully!");
      setCurrentPassword("");
      setNewPassword("");
    } catch (err) {
      setMessage(err.message || "Failed to change password");
    } finally {
      setSaving(false);
    }
  };

  const tabs = [
    { id: "profile", label: "Profile", icon: User },
    { id: "security", label: "Security", icon: Shield },
    { id: "billing", label: "Billing", icon: CreditCard },
  ];

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <motion.h1
          className="text-3xl font-display font-black text-text-primary mb-8"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Command Center
        </motion.h1>

        {message && (
          <motion.div
            className={`p-4 rounded-lg mb-6 border ${message.includes("success") ? "bg-cyber-green/10 border-cyber-green/20 text-cyber-green" : "bg-cyber-red/10 border-cyber-red/20 text-cyber-red"}`}
            initial={reduced ? {} : { opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {message}
          </motion.div>
        )}

        <div className="flex gap-2 mb-8 border-b border-space-border">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 font-medium border-b-2 transition-colors ${
                activeTab === tab.id
                  ? "border-cyber-blue text-cyber-blue"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              <tab.icon size={18} />
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "profile" && (
          <motion.form
            onSubmit={handleSaveProfile}
            className="card space-y-6"
            initial={reduced ? {} : { opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-display font-bold text-text-primary">Profile Information</h2>
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Full Name</label>
              <div className="relative">
                <User size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="input w-full pl-10"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Email</label>
              <div className="relative">
                <Mail size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input w-full pl-10"
                  required
                />
              </div>
            </div>
            <motion.button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 btn-primary px-6 py-3"
              whileHover={reduced ? {} : { scale: 1.02 }}
              whileTap={reduced ? {} : { scale: 0.98 }}
            >
              <Save size={18} />
              {saving ? "Saving..." : "Save Changes"}
            </motion.button>
          </motion.form>
        )}

        {activeTab === "security" && (
          <motion.form
            onSubmit={handleChangePassword}
            className="card space-y-6"
            initial={reduced ? {} : { opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-display font-bold text-text-primary">Change Password</h2>
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">Current Password</label>
              <div className="relative">
                <Lock size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="input w-full pl-10"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-mono uppercase tracking-wider text-gray-400 mb-1.5">New Password</label>
              <div className="relative">
                <Lock size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="input w-full pl-10"
                  minLength={6}
                  required
                />
              </div>
            </div>
            <motion.button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 btn-primary px-6 py-3"
              whileHover={reduced ? {} : { scale: 1.02 }}
              whileTap={reduced ? {} : { scale: 0.98 }}
            >
              <Lock size={18} />
              {saving ? "Changing..." : "Change Password"}
            </motion.button>
          </motion.form>
        )}

        {activeTab === "billing" && (
          <motion.div
            className="card"
            initial={reduced ? {} : { opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h2 className="text-xl font-display font-bold text-text-primary mb-6">Billing & Plan</h2>
            <div className={`p-4 rounded-lg mb-6 ${isPremium ? "bg-cyber-green/5 border border-cyber-green/20" : "bg-space-panel border border-space-border"}`}>
              <div className="flex items-center gap-3">
                <Crown size={24} className={isPremium ? "text-cyber-blue" : "text-gray-500"} />
                <div>
                  <p className="font-bold text-lg capitalize text-text-primary">{user?.plan || "Free"} Plan</p>
                  <p className="text-sm text-gray-400">
                    {isPremium
                      ? "You have unlimited access to all features"
                      : "Upgrade for unlimited access to all features"}
                  </p>
                </div>
              </div>
            </div>
            {!isPremium && (
              <Link
                to="/pricing"
                className="block w-full btn-primary text-center py-3 font-bold"
              >
                Upgrade to Pro — $19/month
              </Link>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
