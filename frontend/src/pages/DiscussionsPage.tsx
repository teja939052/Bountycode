import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { MessageCircle, ArrowUp, ArrowDown } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function DiscussionsPage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/v1/questions/browse?limit=20").then((d: any) => {
      setQuestions(d.questions || d || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-sky/10 border border-brand-sky/20 mb-3">
          <MessageCircle size={14} className="text-brand-sky" />
          <span className="text-xs font-mono text-brand-sky">DISCUSSIONS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Discussions</h1>
        <p className="text-sm text-gray-500 mt-1">Discuss problems with the community</p>
      </motion.div>

      <div className="space-y-2">
        {questions.map((q: any, i: number) => (
          <a key={q.id || i} href={`/solve/${q.id}`}
            className="block glass rounded-xl p-4 hover:border-brand-sky/20 transition-all group">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-white border-border shadow-card flex items-center justify-center text-xs font-mono text-gray-500 shrink-0">
                {i + 1}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-mono text-gray-300 truncate group-hover:text-brand-sky transition-colors">{q.title}</h3>
                <div className="flex gap-2 mt-1">
                  {q.difficulty && <span className="text-[10px] font-mono text-gray-600">{q.difficulty}</span>}
                  {q.topic && <span className="text-[10px] font-mono text-gray-600">{q.topic}</span>}
                </div>
              </div>
              <MessageCircle size={14} className="text-gray-600 group-hover:text-brand-sky transition-colors shrink-0" />
            </div>
          </a>
        ))}
        {questions.length === 0 && (
          <div className="glass rounded-xl p-12 text-center">
            <MessageCircle size={32} className="text-gray-600 mx-auto mb-3" />
            <p className="text-sm text-gray-500 font-mono">No discussions yet</p>
          </div>
        )}
      </div>
    </div>
  );
}
