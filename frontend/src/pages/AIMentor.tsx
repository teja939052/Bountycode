import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  Bot, Send, Loader2, Bug, Lightbulb, BookOpen,
  Sparkles, ChevronRight, Code2, Zap, MessageSquare,
  RefreshCw, Trash2, Copy, Check, Terminal,
} from "lucide-react";

const QUICK_ACTIONS = [
  { label: "Explain code", icon: BookOpen, prompt: "Can you explain how this code works step by step?" },
  { label: "Find bug", icon: Bug, prompt: "Find any bugs or issues in this code:" },
  { label: "Optimize", icon: Zap, prompt: "How can I optimize this code for better performance?" },
  { label: "Debug error", icon: Terminal, prompt: "Help me debug this error:" },
];

const WELCOME_MESSAGE = {
  role: "assistant",
  content: `Hey there! I'm your **AI Mentor** 👋

I can help you with:
- **Debugging** — Find and fix bugs in your code
- **Code Reviews** — Get feedback on your solutions
- **Concept Explanations** — Learn DSA, system design, and more
- **Step-by-Step Guidance** — Work through problems interactively

Drop a question below or paste your code!`,
};

export default function AIMentor() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [codeBlock, setCodeBlock] = useState("");
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [language, setLanguage] = useState("python");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (content) => {
    if (!content.trim() || loading) return;
    const fullContent = codeBlock ? `${content}\n\n\`\`\`${language}\n${codeBlock}\n\`\`\`` : content;
    const userMsg = { role: "user", content: fullContent };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setCodeBlock("");
    setShowCodeInput(false);
    setLoading(true);

    try {
      // Use AI debugger analyze endpoint for general chat
      const data = await api.analyzeCode({ code: fullContent, language, context: "chat" });
      const response = data?.analysis || data?.explanation || data?.feedback || "I processed your request. Can you provide more details?";
      setMessages((prev) => [...prev, { role: "assistant", content: response }]);
    } catch {
      const fallback = "I'm having trouble right now. Please try again or rephrase your question.";
      setMessages((prev) => [...prev, { role: "assistant", content: fallback }]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (prompt) => {
    const fullPrompt = codeBlock ? `${prompt}\n\n\`\`\`${language}\n${codeBlock}\n\`\`\`` : prompt;
    sendMessage(fullPrompt);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-surface-base text-text-primary flex flex-col">
      <div className="max-w-5xl mx-auto w-full px-4 py-6 flex-1 flex flex-col">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-gradient-to-br from-[#D9EFCF] to-[#EDF5E6] rounded-2xl border border-nature-leaf/30">
              <Bot className="w-7 h-7 text-nature-blossom" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-[#1F2937] via-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent">
                AI Mentor
              </h1>
              <p className="text-text-muted text-sm">Your personal coding companion — debug, learn, and build better</p>
            </div>
          </div>
        </motion.div>

        <div className="flex-1 flex flex-col lg:flex-row gap-4 min-h-0">
          {/* Chat area */}
          <div className="flex-1 flex flex-col bg-white border border-nature-leaf/20 rounded-2xl overflow-hidden">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}
                >
                  {msg.role === "assistant" && (
                    <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#D9EFCF] to-[#EDF5E6] border border-nature-leaf/30 flex items-center justify-center shrink-0 mt-1">
                      <Bot className="w-4 h-4 text-nature-blossom" />
                    </div>
                  )}
                  <div className={`max-w-[85%] ${msg.role === "user" ? "order-first" : ""}`}>
                    <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      msg.role === "user"
                        ? "bg-surface-card border border-nature-leaf/30 text-text-primary"
                        : "bg-surface-card border border-nature-leaf/20 text-text-secondary"
                    }`}>
                      <div className="prose prose-sm max-w-none">
                        {msg.content}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 mt-1 px-1">
                      <span className="text-[10px] text-text-muted font-mono">
                        {msg.role === "assistant" ? "AI Mentor" : "You"}
                      </span>
                      {msg.role === "assistant" && (
                        <button
                          onClick={() => copyToClipboard(msg.content)}
                          className="text-text-muted hover:text-text-muted transition-colors"
                        >
                          <Copy className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
              {loading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#D9EFCF] to-[#EDF5E6] border border-nature-leaf/30 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-nature-blossom" />
                  </div>
                  <div className="bg-surface-card border border-nature-leaf/20 rounded-2xl px-4 py-3">
                    <div className="flex items-center gap-2 text-sm text-text-muted">
                      <Loader2 className="w-4 h-4 animate-spin text-nature-blossom" />
                      Thinking...
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Code input panel */}
            <AnimatePresence>
              {showCodeInput && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="border-t border-[#EDEAE0] bg-surface-base"
                >
                  <div className="p-3 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-text-muted flex items-center gap-2">
                        <Code2 className="w-3.5 h-3.5 text-nature-blossom" /> Code Context
                      </span>
                      <div className="flex items-center gap-2">
                        <select
                          value={language}
                          onChange={(e) => setLanguage(e.target.value)}
                          className="bg-surface-base border border-nature-leaf/20 rounded-lg px-2 py-1 text-xs text-text-secondary"
                        >
                          <option value="python">Python</option>
                          <option value="javascript">JavaScript</option>
                          <option value="java">Java</option>
                          <option value="cpp">C++</option>
                          <option value="c">C</option>
                          <option value="go">Go</option>
                          <option value="rust">Rust</option>
                        </select>
                        <button
                          onClick={() => { setShowCodeInput(false); setCodeBlock(""); }}
                          className="text-xs text-text-muted hover:text-text-secondary transition-colors"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                    <textarea
                      value={codeBlock}
                      onChange={(e) => setCodeBlock(e.target.value)}
                      placeholder="Paste your code here for context..."
                      rows={4}
                      className="w-full bg-surface-base border border-nature-leaf/20 rounded-lg p-3 text-xs font-mono text-text-primary placeholder-text-muted focus:outline-none focus:border-nature-leaf resize-none"
                    />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Input */}
            <div className="border-t border-[#EDEAE0] p-3">
              <div className="flex items-end gap-2">
                <button
                  onClick={() => setShowCodeInput(!showCodeInput)}
                  className={`p-2.5 rounded-xl border transition-all shrink-0 ${
                    showCodeInput
                      ? "bg-nature-bark border-nature-leaf/30 text-nature-blossom"
                      : "bg-surface-card border-nature-leaf/20 text-text-muted hover:text-text-primary"
                  }`}
                >
                  <Code2 className="w-4 h-4" />
                </button>
                <div className="flex-1 relative">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(input); } }}
                    placeholder="Ask me anything about code..."
                    className="w-full bg-surface-base border border-nature-leaf/20 rounded-xl py-3 px-4 pr-12 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-nature-leaf transition-colors"
                    disabled={loading}
                  />
                </div>
                <button
                  onClick={() => sendMessage(input)}
                  disabled={!input.trim() || loading}
                  className="p-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white transition-all shrink-0 shadow-lg shadow-[#4F8F57]/20"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:w-64 shrink-0 space-y-3">
            <div className="bg-white border border-nature-leaf/20 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
                <Zap className="w-3.5 h-3.5 text-nature-blossom" /> Quick Actions
              </h3>
              <div className="space-y-2">
                {QUICK_ACTIONS.map((action) => (
                  <button
                    key={action.label}
                    onClick={() => handleQuickAction(action.prompt)}
                    className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-surface-base hover:bg-surface-card border border-nature-leaf/20 hover:border-nature-leaf/30 text-left text-xs text-text-secondary hover:text-text-primary transition-all group"
                  >
                    <div className="p-1.5 rounded-lg bg-surface-card group-hover:bg-nature-bark text-text-muted group-hover:text-nature-blossom transition-colors">
                      <action.icon className="w-3.5 h-3.5" />
                    </div>
                    <span>{action.label}</span>
                    <ChevronRight className="w-3 h-3 ml-auto text-text-muted group-hover:text-text-muted transition-colors" />
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-white border border-nature-leaf/20 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-3 flex items-center gap-2">
                <Lightbulb className="w-3.5 h-3.5 text-amber-400" /> Tips
              </h3>
              <ul className="space-y-2 text-xs text-text-muted">
                <li className="flex items-start gap-2">
                  <span className="text-nature-blossom mt-0.5">•</span>
                  Paste code first, then ask questions
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-nature-blossom mt-0.5">•</span>
                  Ask "Explain this code" for walkthroughs
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-nature-blossom mt-0.5">•</span>
                  Use "Find bug" to spot issues
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-nature-blossom mt-0.5">•</span>
                  Try "Optimize this" for improvements
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-[#F3F0E8] to-[#EDF5E6] border border-nature-leaf/20 rounded-xl p-4">
              <div className="flex items-center gap-2 text-xs text-text-muted">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span><span className="text-amber-400 font-semibold">Pro tip:</span> Include error messages for better debugging!</span>
              </div>
            </div>

            <button
              onClick={() => { setMessages([WELCOME_MESSAGE]); setCodeBlock(""); setShowCodeInput(false); }}
              className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-surface-base border border-nature-leaf/20 text-xs text-text-muted hover:text-text-primary hover:bg-surface-card transition-all"
            >
              <RefreshCw className="w-3.5 h-3.5" /> New Conversation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
