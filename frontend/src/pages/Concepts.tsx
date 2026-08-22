import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Lightbulb, BookOpen, ChevronRight } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function Concepts() {
  const [concepts, setConcepts] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/v1/concepts").then((d: any) => {
      setConcepts(d.concepts || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const loadConcept = async (topic: string) => {
    try {
      const d = await api.get(`/api/v1/concepts/${topic}`);
      setSelected(d);
    } catch { }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3">
          <Lightbulb size={14} className="text-amber-400" />
          <span className="text-xs font-mono text-amber-400">CONCEPTS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Coding Concepts</h1>
        <p className="text-sm text-gray-500 mt-1">Learn fundamental coding concepts at your own pace</p>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-4">
        {concepts.map((c: any, i: number) => (
          <motion.div key={c.topic || i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.03 }}
            onClick={() => loadConcept(c.topic || c.name)}
            className="glass rounded-xl p-5 cursor-pointer hover:border-amber-500/20 transition-all group">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center">
                <BookOpen size={18} className="text-amber-400" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-display font-bold text-text-primary">{c.name || c.topic}</h3>
                <p className="text-[10px] font-mono text-gray-500 capitalize">{c.difficulty || "beginner"}</p>
              </div>
              <ChevronRight size={14} className="text-gray-600 group-hover:text-amber-400 transition-colors" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={() => setSelected(null)}>
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            onClick={e => e.stopPropagation()}
            className="glass rounded-2xl p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto">
            <h2 className="text-xl font-display font-black text-text-primary mb-4">{selected.name || selected.topic}</h2>
            {selected.content && <div className="text-sm text-gray-400 whitespace-pre-wrap mb-4">{selected.content}</div>}
            {selected.explanation && <p className="text-sm text-gray-400 mb-4">{selected.explanation}</p>}
            {selected.code_example && (
              <pre className="bg-black/30 rounded-lg p-4 text-xs font-mono text-emerald-400 overflow-x-auto mb-4">{selected.code_example}</pre>
            )}
            <button onClick={() => setSelected(null)}
              className="w-full py-2.5 rounded-xl bg-white/5 border border-white/10 text-sm font-mono text-gray-400 hover:text-text-primary transition-colors">
              Close
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
}
