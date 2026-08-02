import { useState, useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import api from '../services/api';
import { Card } from '../components/ui/Card';

const SECTION_ICONS = {
  'Aptitude': '📊', 'Programming Logic': '💻', 'Coding': '⌨️', 'English': '📝',
  'Aptitude & Logic': '🧠', 'Programming (MCQ)': '💻', 'SQL': '🗄️',
  'Quantitative Aptitude': '📊', 'Logical Reasoning': '🧩', 'Verbal Ability': '📝',
  'Verbal': '📝', 'Numerical Ability': '📊', 'Essay Writing': '✍️',
  'Aptitude Section': '📊', 'Coding Section': '⌨️', 'English Section': '📝',
  'Quantitative': '📊', 'Data Interpretation': '📈',
};

const TABS = [
  { id: 'overview', label: 'Overview', icon: '📋' },
  { id: 'exam', label: 'Exam Pattern', icon: '📝' },
  { id: 'coding', label: 'Coding', icon: '💻' },
  { id: 'hr', label: 'HR Round', icon: '🗣️' },
  { id: 'mock', label: 'Take Mock', icon: '🎯' },
];

export default function IndianPlacement() {
  const [companies, setCompanies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [mockConfig, setMockConfig] = useState(null);
  const [hrData, setHrData] = useState(null);
  const [codingData, setCodingData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [mockStarted, setMockStarted] = useState(false);
  const [mockSections, setMockSections] = useState(null);
  const [mockLoading, setMockLoading] = useState(false);

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    setLoading(true);
    try {
      const data = await api.getIndianCompanies?.().catch(() => null);
      if (data?.companies) {
        setCompanies(data.companies);
      } else {
        // Fallback - fetch directly
        const res = await fetch('/api/v1/indian-placement/companies');
        const json = await res.json();
        setCompanies(json.companies || []);
      }
    } catch { setCompanies([]); }
    setLoading(false);
  };

  const selectCompany = async (companyId) => {
    setDetailLoading(true);
    setSelected(companyId);
    setActiveTab('overview');
    setMockStarted(false);
    setMockSections(null);
    try {
      const [detailRes, hrRes, codingRes] = await Promise.all([
        fetch(`/api/v1/indian-placement/${companyId}`).then(r => r.ok ? r.json() : null).catch(() => null),
        fetch(`/api/v1/indian-placement/${companyId}/hr-questions`).then(r => r.ok ? r.json() : null).catch(() => null),
        fetch(`/api/v1/indian-placement/${companyId}/coding-patterns`).then(r => r.ok ? r.json() : null).catch(() => null),
      ]);
      setDetail(detailRes);
      setHrData(hrRes);
      setCodingData(codingRes);
    } catch {}
    setDetailLoading(false);
  };

  const startMock = async () => {
    setMockLoading(true);
    try {
      const res = await fetch('/api/v1/indian-placement/start-mock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ company_id: selected }),
      });
      const data = await res.json();
      setMockSections(data);
      setMockStarted(true);
    } catch {}
    setMockLoading(false);
  };

  const company = companies.find(c => c.id === selected);

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-6 sm:mb-8">
          <span className="section-subheader mb-2 block">Campus Placement Prep</span>
          <h1 className="section-header text-2xl sm:text-3xl mb-2">
            Indian Company <span className="text-cyber-blue">Mock Tests</span>
          </h1>
          <p className="text-gray-500 text-xs sm:text-sm font-mono">Real placement patterns from TCS, Infosys, Wipro & more</p>
        </motion.div>

        {!selected ? (
          /* Company Grid */
          <>
            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4">
                {Array.from({ length: 8 }).map((_, i) => (
                  <div key={i} className="h-40 rounded-xl border border-gray-700/20 p-5 animate-pulse bg-gray-900/20" />
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4">
                {companies.map((c, i) => (
                  <motion.div
                    key={c.id}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                  >
                    <Card
                      rarity={i < 2 ? 'rare' : i < 4 ? 'uncommon' : 'common'}
                      hoverEffect
                      onClick={() => selectCompany(c.id)}
                    >
                      <div className="text-center">
                        <div className="text-3xl mb-2">{c.icon}</div>
                        <h3 className="font-display font-bold text-sm text-white mb-1">{c.name}</h3>
                        <p className="text-[10px] font-mono text-cyber-green mb-2">{c.package}</p>
                        <p className="text-[9px] font-mono text-gray-500 mb-2">{c.exam_pattern}</p>
                        <div className="flex flex-wrap gap-1 justify-center">
                          {(c.focus_areas || []).slice(0, 3).map((area, j) => (
                            <span key={j} className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-gray-800 text-gray-400 border border-gray-700/30">
                              {area}
                            </span>
                          ))}
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>
            )}
          </>
        ) : detailLoading ? (
          <div className="text-center py-16"><div className="spinner-cyber mx-auto" /></div>
        ) : (
          /* Company Detail */
          <div>
            <button
              onClick={() => { setSelected(null); setDetail(null); setHrData(null); setCodingData(null); setMockStarted(false); setMockSections(null); }}
              className="mb-4 text-sm font-mono text-cyber-blue hover:text-cyber-blue/80 transition-colors"
            >
              ← Back to Companies
            </button>

            {/* Company Header */}
            <div className="flex items-center gap-4 mb-5 flex-wrap">
              <span className="text-3xl">{company?.icon || '🏢'}</span>
              <div>
                <h2 className="text-xl font-display font-bold text-text-primary">{detail?.name || company?.name}</h2>
                <p className="text-xs font-mono text-gray-400">{detail?.full_name} · {detail?.package}</p>
              </div>
            </div>

            {/* Eligibility Banner */}
            <div className="mb-4 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20 text-xs font-mono text-yellow-400">
              📋 Eligibility: {detail?.eligibility} · Pattern: {detail?.exam_pattern}
            </div>

            {/* Tabs */}
            <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
              {TABS.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-lg text-xs font-mono font-medium uppercase tracking-wider transition-all border whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40'
                      : 'border-transparent text-gray-500 hover:text-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Tab Content */}
            {activeTab === 'overview' && detail && (
              <div className="space-y-4">
                {/* Interview Rounds */}
                <Card rarity="rare" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Interview Rounds</h3>
                  <div className="flex flex-wrap gap-3">
                    {(detail.interview_rounds || []).map((round, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <span className="w-7 h-7 rounded-lg bg-cyber-blue/15 text-cyber-blue flex items-center justify-center text-xs font-bold font-mono">{i + 1}</span>
                        <span className="text-sm text-gray-300">{round}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Focus Areas */}
                <Card rarity="uncommon" hoverEffect={false}>
                  <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Focus Areas</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {(detail.focus_areas || []).map((area, i) => (
                      <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">{area}</span>
                    ))}
                  </div>
                </Card>

                {/* Tips */}
                {detail.tips?.length > 0 && (
                  <Card rarity="epic" hoverEffect={false}>
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">🎯 Pro Tips</h3>
                    <ul className="space-y-2">
                      {detail.tips.map((tip, i) => (
                        <li key={i} className="text-xs text-gray-300 font-mono flex items-start gap-2">
                          <span className="text-cyber-blue mt-0.5">→</span>
                          <span>{tip}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>
                )}
              </div>
            )}

            {activeTab === 'exam' && detail && (
              <ExamPatternTab detail={detail} />
            )}

            {activeTab === 'coding' && codingData && (
              <CodingPatternsTab data={codingData} />
            )}

            {activeTab === 'hr' && hrData && (
              <HRTab data={hrData} />
            )}

            {activeTab === 'mock' && (
              <div>
                {!mockStarted ? (
                  <Card rarity="legendary" hoverEffect={false}>
                    <div className="text-center py-6">
                      <div className="text-4xl mb-3">🎯</div>
                      <h3 className="text-lg font-display font-bold text-white mb-2">Start Mock Test</h3>
                      <p className="text-xs text-gray-400 mb-4 max-w-md mx-auto">
                        Simulate the actual {company?.name || selected} placement test with real patterns,
                        timed sections, and scoring.
                      </p>
                      <button
                        onClick={startMock}
                        disabled={mockLoading}
                        className="btn-primary text-sm inline-flex items-center gap-2"
                      >
                        {mockLoading ? 'Loading...' : '🚀 Start Full Mock Test'}
                      </button>
                    </div>
                  </Card>
                ) : mockSections ? (
                  <MockTestView data={mockSections} />
                ) : null}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function ExamPatternTab({ detail }) {
  // Find the pattern based on company
  const patternKey = ['nqt_pattern', 'infytq_pattern', 'nlth_pattern', 'genc_pattern', 'hcl_pattern', 'amcat_pattern', 'indrive_pattern', 'smart_pattern'];
  let pattern = null;
  for (const key of patternKey) {
    if (detail[key]) { pattern = detail[key]; break; }
  }

  if (!pattern) return (
    <Card rarity="common" hoverEffect={false}>
      <p className="text-sm text-gray-400 text-center py-4">No exam pattern data available yet.</p>
    </Card>
  );

  return (
    <div className="space-y-4">
      <Card rarity="rare" hoverEffect={false}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400">Exam Structure</h3>
          <span className="text-xs font-mono text-cyber-blue">⏱ {pattern.total_time_minutes} min total</span>
        </div>

        <div className="space-y-3">
          {(pattern.sections || []).map((section, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="p-4 rounded-xl bg-gray-800/40 border border-gray-700/30"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{SECTION_ICONS[section.name] || '📋'}</span>
                  <span className="font-display font-bold text-sm text-white">{section.name}</span>
                </div>
                <div className="flex items-center gap-3 text-[10px] font-mono text-gray-500">
                  <span>{section.questions} Q</span>
                  <span>{section.time_minutes} min</span>
                  <span className={`px-1.5 py-0.5 rounded ${
                    section.difficulty === 'easy' ? 'bg-green-500/15 text-green-400' :
                    section.difficulty === 'medium' ? 'bg-yellow-500/15 text-yellow-400' :
                    'bg-red-500/15 text-red-400'
                  }`}>
                    {section.difficulty}
                  </span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1">
                {(section.topics || []).map((topic, j) => (
                  <span key={j} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-gray-700/30 text-gray-400">
                    {topic}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </Card>
    </div>
  );
}

function CodingPatternsTab({ data }) {
  return (
    <div className="space-y-4">
      <Card rarity="rare" hoverEffect={false}>
        <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Frequently Asked Coding Problems</h3>
        <p className="text-[10px] text-gray-500 mb-4">Practice these patterns — they commonly appear in {data.company} placements</p>

        <div className="space-y-2">
          {(data.coding_patterns || []).map((pattern, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center gap-3 p-3 rounded-lg bg-gray-800/30 border border-gray-700/20 hover:border-cyber-blue/20 transition-all"
            >
              <span className="w-6 h-6 rounded-md bg-cyber-blue/15 text-cyber-blue flex items-center justify-center text-[10px] font-bold font-mono shrink-0">
                {i + 1}
              </span>
              <span className="text-xs text-gray-300 font-mono">{pattern}</span>
            </motion.div>
          ))}
        </div>
      </Card>

      {data.focus_areas?.length > 0 && (
        <Card rarity="uncommon" hoverEffect={false}>
          <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Key Topics to Master</h3>
          <div className="flex flex-wrap gap-1.5">
            {data.focus_areas.map((area, i) => (
              <span key={i} className="px-2.5 py-1 rounded-lg text-[10px] font-mono bg-purple-500/10 text-purple-400 border border-purple-500/20">{area}</span>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

function HRTab({ data }) {
  return (
    <div className="space-y-4">
      <Card rarity="epic" hoverEffect={false}>
        <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">Common HR Questions at {data.company}</h3>
        <div className="space-y-2">
          {(data.hr_questions || []).map((q, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-start gap-3 p-3 rounded-lg bg-gray-800/30 border border-gray-700/20"
            >
              <span className="w-6 h-6 rounded-md bg-purple-500/15 text-purple-400 flex items-center justify-center text-[10px] font-bold font-mono shrink-0 mt-0.5">
                {i + 1}
              </span>
              <div>
                <p className="text-xs text-gray-300 font-mono">{q}</p>
                <p className="text-[9px] text-gray-500 mt-1">💡 Think of a specific example from your experience</p>
              </div>
            </motion.div>
          ))}
        </div>
      </Card>

      {data.tips?.length > 0 && (
        <Card rarity="rare" hoverEffect={false}>
          <h3 className="font-display font-bold text-xs uppercase tracking-widest text-gray-400 mb-3">🎯 HR Round Tips</h3>
          <ul className="space-y-2">
            {data.tips.map((tip, i) => (
              <li key={i} className="text-xs text-gray-300 font-mono flex items-start gap-2">
                <span className="text-cyber-green mt-0.5">✓</span>
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}

function MockTestView({ data }) {
  const [currentSection, setCurrentSection] = useState(0);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [sectionTimeLeft, setSectionTimeLeft] = useState(0);
  const timerRef = useRef(null);

  const section = data.sections?.[currentSection];
  const question = section?.questions?.[currentQ];
  const totalQ = data.total_questions || 0;
  const totalTime = data.total_time_minutes || 0;

  // Initialize section timer
  useEffect(() => {
    if (section && !submitted) {
      setSectionTimeLeft(section.time_minutes * 60);
    }
  }, [currentSection, submitted]);

  // Countdown timer
  useEffect(() => {
    if (submitted) return;
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          setSubmitted(true);
          return 0;
        }
        return prev - 1;
      });
      setSectionTimeLeft(prev => {
        if (prev <= 1) {
          // Auto-advance to next section
          if (currentSection < data.sections.length - 1) {
            setCurrentSection(s => s + 1);
            setCurrentQ(0);
            setShowExplanation(false);
          } else {
            setSubmitted(true);
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, [submitted, currentSection]);

  // Initialize total time
  useEffect(() => {
    if (!submitted) setTimeLeft(totalTime * 60);
  }, []);

  useEffect(() => {
    if (!submitted && section) setSectionTimeLeft(section.time_minutes * 60);
  }, [currentSection]);

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const handleAnswer = useCallback((optionIdx) => {
    const key = `${currentSection}-${currentQ}`;
    const isCorrect = question.correct_answer === question.options?.[optionIdx];
    setAnswers(prev => ({ ...prev, [key]: { answer: optionIdx, correct: isCorrect, selected: question.options?.[optionIdx] } }));
    setShowExplanation(true);

    // Auto-advance after 1.5s (show explanation briefly)
    setTimeout(() => {
      setShowExplanation(false);
      if (currentQ < section.questions.length - 1) {
        setCurrentQ(currentQ + 1);
      } else if (currentSection < data.sections.length - 1) {
        setCurrentSection(currentSection + 1);
        setCurrentQ(0);
      } else {
        setSubmitted(true);
        clearInterval(timerRef.current);
      }
    }, 1500);
  }, [currentSection, currentQ, question, section]);

  if (submitted) {
    const correct = Object.values(answers).filter((a: any) => a.correct).length;
    const attempted = Object.keys(answers).length;
    const accuracy = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;
    const score = Math.round((correct / totalQ) * 100);
    const timeUsed = totalTime * 60 - timeLeft;

    return (
      <Card rarity="legendary" hoverEffect={false}>
        <div className="text-center py-8">
          <div className="text-5xl mb-4">🎉</div>
          <h3 className="text-xl font-display font-bold text-white mb-2">Mock Test Complete!</h3>
          <p className="text-sm text-gray-400 mb-4">{data.company} Placement Mock</p>

          {/* Score Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6 max-w-lg mx-auto">
            <div className="p-3 rounded-xl bg-gray-800/40 border border-gray-700/30">
              <div className="text-2xl font-display font-bold text-cyber-blue">{score}%</div>
              <div className="text-[10px] text-gray-500 uppercase">Score</div>
            </div>
            <div className="p-3 rounded-xl bg-gray-800/40 border border-gray-700/30">
              <div className="text-2xl font-display font-bold text-green-400">{correct}</div>
              <div className="text-[10px] text-gray-500 uppercase">Correct</div>
            </div>
            <div className="p-3 rounded-xl bg-gray-800/40 border border-gray-700/30">
              <div className="text-2xl font-display font-bold text-yellow-400">{accuracy}%</div>
              <div className="text-[10px] text-gray-500 uppercase">Accuracy</div>
            </div>
            <div className="p-3 rounded-xl bg-gray-800/40 border border-gray-700/30">
              <div className="text-2xl font-display font-bold text-purple-400">{formatTime(timeUsed)}</div>
              <div className="text-[10px] text-gray-500 uppercase">Time Used</div>
            </div>
          </div>

          {/* Section Breakdown */}
          <div className="text-left max-w-md mx-auto mb-6">
            <h4 className="text-xs font-mono text-gray-400 uppercase mb-2">Section Breakdown</h4>
            {data.sections.map((s, i) => {
              const sectionCorrect = s.questions.filter((_, qi) => answers[`${i}-${qi}`]?.correct).length;
              const sectionAttempted = s.questions.filter((_, qi) => answers[`${i}-${qi}`] !== undefined).length;
              return (
                <div key={i} className="flex items-center gap-3 py-1.5 text-xs font-mono">
                  <span className="text-gray-400 w-32 truncate">{s.section_name}</span>
                  <span className="text-green-400">{sectionCorrect}/{s.questions.length}</span>
                  <div className="flex-1 h-1.5 rounded bg-gray-700/30 overflow-hidden">
                    <div className="h-full rounded bg-cyber-blue" style={{ width: `${(sectionCorrect / s.questions.length) * 100}%` }} />
                  </div>
                </div>
              );
            })}
          </div>

          <button onClick={() => { setSubmitted(false); setCurrentSection(0); setCurrentQ(0); setAnswers({}); setTimeLeft(0); setShowExplanation(false); }} className="btn-primary text-sm">
            Retake Mock
          </button>
        </div>
      </Card>
    );
  }

  if (!section || !question) {
    return (
      <Card rarity="rare" hoverEffect={false}>
        <p className="text-sm text-gray-400 text-center py-4">No questions loaded. Try starting the mock again.</p>
      </Card>
    );
  }

  const isCoding = section.section_type === 'Problem Solving' || section.section_type?.includes('Coding');
  const globalProgress = ((currentSection * section.questions.length + currentQ) / totalQ) * 100;

  return (
    <div className="space-y-4">
      {/* Timer & Progress */}
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <div className="flex items-center gap-2 text-xs font-mono text-gray-500">
          <span className="text-cyber-blue font-bold">{section.section_name}</span>
          <span>·</span>
          <span>Q{currentQ + 1}/{section.questions.length}</span>
        </div>
        <div className="flex items-center gap-3">
          <div className={`px-3 py-1 rounded-lg text-xs font-mono font-bold ${
            timeLeft < 60 ? 'bg-red-500/20 text-red-400 animate-pulse' :
            timeLeft < 300 ? 'bg-yellow-500/20 text-yellow-400' :
            'bg-gray-800/40 text-gray-300'
          }`}>
            ⏱ {formatTime(timeLeft)}
          </div>
          <div className={`px-2 py-1 rounded-lg text-[10px] font-mono ${
            sectionTimeLeft < 30 ? 'bg-red-500/15 text-red-400' : 'bg-gray-800/30 text-gray-500'
          }`}>
            Section: {formatTime(sectionTimeLeft)}
          </div>
        </div>
      </div>

      {/* Global Progress Bar */}
      <div className="h-1 rounded-full bg-gray-700/30 overflow-hidden">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-cyber-blue to-cyber-green"
          animate={{ width: `${globalProgress}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      {/* Section Tabs */}
      <div className="flex gap-1 overflow-x-auto pb-1">
        {data.sections.map((s, i) => {
          const secCorrect = s.questions.filter((_, qi) => answers[`${i}-${qi}`]?.correct).length;
          const secDone = s.questions.filter((_, qi) => answers[`${i}-${qi}`] !== undefined).length;
          return (
            <button
              key={i}
              onClick={() => { setCurrentSection(i); setCurrentQ(0); setShowExplanation(false); }}
              className={`px-3 py-1.5 rounded-lg text-[10px] font-mono whitespace-nowrap transition-all border ${
                i === currentSection
                  ? 'bg-cyber-blue/15 text-cyber-blue border-cyber-blue/40'
                  : secDone > 0
                    ? 'border-green-500/20 text-green-400/70'
                    : 'border-gray-700/20 text-gray-500'
              }`}
            >
              {SECTION_ICONS[s.section_name] || '📋'} {s.section_name}
              {secDone > 0 && <span className="ml-1 text-green-400">{secCorrect}/{s.questions.length}</span>}
            </button>
          );
        })}
      </div>

      {/* Question Card */}
      <Card rarity="rare" hoverEffect={false}>
        {isCoding ? (
          <div>
            <h3 className="text-sm font-display font-bold text-white mb-2">{question.question_title || question.statement || 'Coding Problem'}</h3>
            <p className="text-xs text-gray-400 font-mono mb-4">{question.statement || 'Implement the solution.'}</p>
            {question.examples?.map((ex, i) => (
              <div key={i} className="p-2 rounded-lg bg-gray-800/50 border border-gray-700/20 mb-2 text-[10px] font-mono text-gray-400">
                <p>Input: {ex.input || ex}</p>
                <p>Output: {ex.output || 'N/A'}</p>
              </div>
            ))}
            <button
              onClick={() => {
                const key = `${currentSection}-${currentQ}`;
                setAnswers(prev => ({ ...prev, [key]: { answer: -1, correct: false, skipped: true } }));
                setShowExplanation(true);
                setTimeout(() => {
                  setShowExplanation(false);
                  if (currentQ < section.questions.length - 1) setCurrentQ(currentQ + 1);
                  else if (currentSection < data.sections.length - 1) { setCurrentSection(currentSection + 1); setCurrentQ(0); }
                  else setSubmitted(true);
                }, 1000);
              }}
              className="btn-primary text-xs mt-4"
            >
              Next →
            </button>
          </div>
        ) : (
          <div>
            {/* Question */}
            <div className="flex items-start gap-2 mb-4">
              <span className="w-6 h-6 rounded-md bg-cyber-blue/15 text-cyber-blue flex items-center justify-center text-[10px] font-bold font-mono shrink-0 mt-0.5">
                {currentQ + 1}
              </span>
              <p className="text-sm font-mono text-gray-300">{question.question}</p>
            </div>

            {/* Company Tag */}
            {question.companies?.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-3">
                {question.companies.slice(0, 3).map((c, i) => (
                  <span key={i} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
                    🏢 {c}
                  </span>
                ))}
              </div>
            )}

            {/* Options */}
            <div className="space-y-2">
              {question.options?.map((opt, i) => {
                const key = `${currentSection}-${currentQ}`;
                const selected = answers[key]?.answer === i;
                const isCorrectOption = question.correct_answer === opt;
                const showResult = showExplanation;

                let optStyle = 'bg-gray-800/30 border-gray-700/20 text-gray-300 hover:border-gray-600/30 hover:bg-gray-800/50';
                if (showResult && isCorrectOption) {
                  optStyle = 'bg-green-500/15 border-green-500/40 text-green-400';
                } else if (showResult && selected && !isCorrectOption) {
                  optStyle = 'bg-red-500/15 border-red-500/40 text-red-400';
                } else if (selected) {
                  optStyle = 'bg-cyber-blue/15 border-cyber-blue/40 text-cyber-blue';
                }

                return (
                  <button
                    key={i}
                    onClick={() => !showExplanation && handleAnswer(i)}
                    disabled={showExplanation}
                    className={`w-full text-left p-3 rounded-lg border text-xs font-mono transition-all ${optStyle}`}
                  >
                    <span className="font-bold text-gray-500 mr-2">{String.fromCharCode(65 + i)}.</span>
                    {opt}
                    {showResult && isCorrectOption && <span className="ml-2 text-green-400">✓</span>}
                    {showResult && selected && !isCorrectOption && <span className="ml-2 text-red-400">✗</span>}
                  </button>
                );
              })}
            </div>

            {/* Explanation */}
            {showExplanation && question.explanation && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-3 rounded-lg bg-cyber-blue/5 border border-cyber-blue/20"
              >
                <p className="text-[10px] font-mono text-cyber-blue uppercase mb-1">💡 Explanation</p>
                <p className="text-xs font-mono text-gray-300">{question.explanation}</p>
                {question.correct_answer && (
                  <p className="text-xs font-mono text-green-400 mt-1">Answer: {question.correct_answer}</p>
                )}
              </motion.div>
            )}
          </div>
        )}
      </Card>

      {/* Progress Dots */}
      <div className="flex flex-wrap gap-1">
        {section.questions.map((_, i) => {
          const key = `${currentSection}-${i}`;
          const answered = answers[key] !== undefined;
          const isCorrect = answers[key]?.correct;
          return (
            <div
              key={i}
              className={`w-3 h-3 rounded-full transition-all ${
                i === currentQ ? 'ring-2 ring-cyber-blue ring-offset-1 ring-offset-space-void' :
                answered ? (isCorrect ? 'bg-green-500' : 'bg-red-500') :
                'bg-gray-700'
              }`}
            />
          );
        })}
      </div>
    </div>
  );
}
