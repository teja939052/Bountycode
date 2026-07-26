import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../services/api';
import { Card } from '../components/ui/Card';

const DIFFICULTIES = [
  { id: 'easy', name: 'Easy', desc: 'URL Shortener, Key-Value Store', emoji: '🟢', color: '#22C55E' },
  { id: 'medium', name: 'Medium', desc: 'Chat System, News Feed, Rate Limiter', emoji: '🟡', color: '#EAB308' },
  { id: 'hard', name: 'Hard', desc: 'Google-scale distributed systems', emoji: '🔴', color: '#EF4444' },
];

const TOPICS = [
  'URL Shortener', 'Chat System', 'News Feed', 'Rate Limiter',
  'Search Autocomplete', 'Web Crawler', 'Notification System',
  'Payment System', 'Social Network', 'Video Streaming',
  'E-Commerce Platform', 'Ride Sharing', 'WhatsApp', 'YouTube',
];

export default function SystemDesign() {
  const [step, setStep] = useState('select');
  const [difficulty, setDifficulty] = useState('medium');
  const [topic, setTopic] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState('');
  const [diagram, setDiagram] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const startSession = async () => {
    setLoading(true); setError('');
    try {
      const data = await api.startSystemDesign(difficulty, topic);
      setSessionId(data.session_id); setQuestion(data); setStep('design');
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!answer.trim()) return;
    setLoading(true); setError('');
    try {
      const data = await api.submitSystemDesignAnswer(sessionId, question.question, answer, diagram);
      setFeedback(data.feedback);
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  const finishSession = async () => {
    setLoading(true);
    try {
      const data = await api.getSystemDesignResult(sessionId);
      setResult(data); setStep('results');
    } catch (err) { setError(err.message); }
    setLoading(false);
  };

  if (step === 'select') {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
            <span className="section-subheader mb-2 block">Architecture Practice</span>
            <h1 className="section-header text-3xl mb-2">
              System <span className="text-cyber-purple">Design</span>
            </h1>
            <p className="text-gray-500 text-sm font-mono">Master system design interviews with AI feedback</p>
          </motion.div>

          {error && <div className="bg-red-950/30 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg mb-6 text-center text-sm font-mono">{error}</div>}

          <Card rarity="epic" hoverEffect={false} className="mb-5">
            <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-4">Select Difficulty</h3>
            <div className="grid sm:grid-cols-3 gap-3">
              {DIFFICULTIES.map((d) => (
                <button key={d.id} onClick={() => setDifficulty(d.id)}
                  className={`p-4 rounded-xl text-left transition-all border ${difficulty === d.id ? 'shadow-lg' : 'border-gray-700/30 hover:border-gray-600/40'}`}
                  style={difficulty === d.id ? { borderColor: d.color, boxShadow: `0 0 15px ${d.color}15`, background: `${d.color}08` } : {}}>
                  <span className="text-xl mb-1 block">{d.emoji}</span>
                  <p className="font-semibold text-sm text-white">{d.name}</p>
                  <p className="text-[10px] text-gray-500 font-mono mt-0.5">{d.desc}</p>
                </button>
              ))}
            </div>
          </Card>

          <Card rarity="rare" hoverEffect={false} className="mb-6">
            <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-4">Select Topic (Optional)</h3>
            <div className="flex flex-wrap gap-2">
              {TOPICS.map((t) => (
                <button key={t} onClick={() => setTopic(topic === t ? '' : t)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${topic === t ? 'bg-cyber-purple/15 text-cyber-purple border-cyber-purple/40' : 'border-gray-700/30 text-gray-400 hover:text-gray-300 hover:border-gray-600/40'}`}>
                  {t}
                </button>
              ))}
            </div>
          </Card>

          <button onClick={startSession} disabled={loading} className="btn-primary w-full text-sm">
            {loading ? <span className="spinner-cyber w-5 h-5 inline-block mr-2" /> : null}Start Session →
          </button>
        </div>
      </div>
    );
  }

  if (step === 'design' && question) {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <Card rarity="epic" hoverEffect={false} className="mb-5">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded"
                style={{ backgroundColor: `${DIFFICULTIES.find(d => d.id === question.difficulty)?.color || '#EAB308'}18`, color: DIFFICULTIES.find(d => d.id === question.difficulty)?.color || '#EAB308' }}>
                {question.difficulty}
              </span>
              <span className="text-[10px] font-mono text-gray-500">{question.topic}</span>
            </div>
            <h2 className="text-lg font-display font-bold text-white mb-4">{question.question}</h2>
            {question.hints?.length > 0 && (
              <div className="bg-yellow-950/20 border border-yellow-500/20 rounded-lg p-3 mb-3">
                <p className="text-[10px] font-mono font-bold text-yellow-400 uppercase tracking-wider mb-2">Hints</p>
                <ul className="space-y-1">{question.hints.map((h, i) => <li key={i} className="text-xs text-yellow-300/70 font-mono">• {h}</li>)}</ul>
              </div>
            )}
            {question.expected_components?.length > 0 && (
              <div className="bg-blue-950/20 border border-blue-500/20 rounded-lg p-3">
                <p className="text-[10px] font-mono font-bold text-blue-400 uppercase tracking-wider mb-2">Expected Components</p>
                <div className="flex flex-wrap gap-1.5">
                  {question.expected_components.map((c, i) => (
                    <span key={i} className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">{c}</span>
                  ))}
                </div>
              </div>
            )}
          </Card>

          {feedback && (
            <Card rarity="uncommon" hoverEffect={false} className="mb-5">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg">✓</span>
                <span className="font-display font-bold text-green-400">Score: {feedback.score}/10</span>
              </div>
              {feedback.strengths?.length > 0 && <div className="mb-2"><p className="text-[10px] font-mono font-bold text-green-400 uppercase tracking-wider mb-1">Strengths</p><ul className="text-xs text-green-300/70 space-y-0.5">{feedback.strengths.map((s, i) => <li key={i}>• {s}</li>)}</ul></div>}
              {feedback.improvements?.length > 0 && <div className="mb-2"><p className="text-[10px] font-mono font-bold text-amber-400 uppercase tracking-wider mb-1">Improve</p><ul className="text-xs text-amber-300/70 space-y-0.5">{feedback.improvements.map((s, i) => <li key={i}>• {s}</li>)}</ul></div>}
              {feedback.missing_concepts?.length > 0 && <div><p className="text-[10px] font-mono font-bold text-red-400 uppercase tracking-wider mb-1">Missing</p><ul className="text-xs text-red-300/70 space-y-0.5">{feedback.missing_concepts.map((s, i) => <li key={i}>• {s}</li>)}</ul></div>}
            </Card>
          )}

          <Card rarity="common" hoverEffect={false} className="mb-5">
            <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-2">Your Design Answer</label>
            <textarea className="input min-h-[180px] resize-y" placeholder="High-level architecture, components, data flow, scaling, trade-offs..." value={answer} onChange={(e) => setAnswer(e.target.value)} />
          </Card>

          <Card rarity="common" hoverEffect={false} className="mb-5">
            <label className="block text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider mb-2">Diagram Description (Optional)</label>
            <textarea className="input min-h-[80px] resize-y" placeholder="User → Load Balancer → API Gateway → Service → DB" value={diagram} onChange={(e) => setDiagram(e.target.value)} />
          </Card>

          <div className="flex gap-3">
            <button onClick={submitAnswer} disabled={!answer.trim() || loading} className="btn-primary flex-1 text-sm">
              {loading ? <span className="spinner-cyber w-5 h-5 inline-block mr-2" /> : null}Submit for Feedback
            </button>
            <button onClick={finishSession} className="btn-secondary text-sm">Finish Session</button>
          </div>
        </div>
      </div>
    );
  }

  if (step === 'results' && result) {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <Card rarity="legendary" hoverEffect={false} className="text-center py-10">
            <div className="text-4xl mb-3">🏗️</div>
            <h1 className="text-2xl font-display font-bold text-white mb-4">Session Complete!</h1>
            <div className="w-24 h-24 rounded-full flex items-center justify-center text-3xl font-display font-black mx-auto mb-4"
              style={{ color: result.overall_score >= 7 ? '#22C55E' : result.overall_score >= 5 ? '#EAB308' : '#EF4444', background: result.overall_score >= 7 ? 'rgba(34,197,94,0.1)' : result.overall_score >= 5 ? 'rgba(234,179,8,0.1)' : 'rgba(239,68,68,0.1)', border: `2px solid ${result.overall_score >= 7 ? 'rgba(34,197,94,0.3)' : result.overall_score >= 5 ? 'rgba(234,179,8,0.3)' : 'rgba(239,68,68,0.3)'}` }}>
              {result.overall_score}
            </div>
            <p className="text-gray-400 text-sm font-mono">Overall Score (out of 10) · {result.topic}</p>
            <div className="flex gap-3 mt-6 justify-center">
              <Link to="/system-design" className="btn-primary text-sm">Practice Again</Link>
              <Link to="/dashboard" className="btn-secondary text-sm">Dashboard</Link>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return <div className="min-h-screen flex items-center justify-center"><div className="spinner-cyber" /></div>;
}
