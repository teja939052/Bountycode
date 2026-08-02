import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '../services/api';
import { ChevronLeft, ChevronRight, Lock, Star, Clock, Code, Trophy, Flame, BookOpen, Zap, Target } from 'lucide-react';

const LANGUAGES = [
  { id: 'python', name: 'Python', icon: '🐍', primary_use: 'Web, Data Science, AI/ML, Automation', color: 'from-blue-500 to-cyan-400' },
  { id: 'javascript', name: 'JavaScript', icon: '🟨', primary_use: 'Web Frontend, Backend (Node.js), Mobile', color: 'from-yellow-400 to-orange-400' },
  { id: 'java', name: 'Java', icon: '☕', primary_use: 'Enterprise, Android, Web Backend', color: 'from-red-500 to-orange-500' },
  { id: 'cpp', name: 'C++', icon: '⚡', primary_use: 'Systems, Game Dev, High Performance', color: 'from-purple-500 to-indigo-500' },
  { id: 'c', name: 'C', icon: '🔷', primary_use: 'Systems Programming, Embedded, OS', color: 'from-blue-600 to-purple-600' },
  { id: 'go', name: 'Go', icon: '🟢', primary_use: 'Cloud, Backend, DevOps, Microservices', color: 'from-green-400 to-teal-400' },
  { id: 'rust', name: 'Rust', icon: '🦀', primary_use: 'Systems, WebAssembly, Performance-Critical', color: 'from-orange-600 to-yellow-600' },
];

const TIERS = [
  { name: 'First Principles', levels: '1-10', color: 'text-green-400', icon: '🌱' },
  { name: 'Core Programming', levels: '11-20', color: 'text-blue-400', icon: '⚙️' },
  { name: 'Data Structures I', levels: '21-30', color: 'text-indigo-400', icon: '📊' },
  { name: 'Data Structures II', levels: '31-40', color: 'text-purple-400', icon: '🌳' },
  { name: 'Algorithms I', levels: '41-50', color: 'text-pink-400', icon: '🧠' },
  { name: 'Object-Oriented Programming', levels: '51-60', color: 'text-red-400', icon: '🏗️' },
  { name: 'Advanced Data Structures', levels: '61-70', color: 'text-orange-400', icon: '💎' },
  { name: 'Algorithms II', levels: '71-80', color: 'text-yellow-400', icon: '⚡' },
  { name: 'System Design', levels: '81-90', color: 'text-cyan-400', icon: '🏗️' },
  { name: 'Capstone & Mastery', levels: '91-100', color: 'text-white', icon: '👑' },
];

const LanguageLearning = () => {
  const [selectedLang, setSelectedLang] = useState('python');
  const [modules, setModules] = useState([]);
  const [levels, setLevels] = useState([]);
  const [progress, setProgress] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('path');
  const [completedModules, setCompletedModules] = useState(new Set());

  useEffect(() => {
    loadLanguageData();
  }, [selectedLang]);

  const loadLanguageData = async () => {
    setLoading(true);
    try {
      const [modulesRes, levelsRes, progressRes, recRes] = await Promise.all([
        api.get(`/api/languages/${selectedLang}`),
        api.get(`/api/languages/${selectedLang}/levels`),
        api.get(`/api/languages/${selectedLang}/progress`),
        api.get(`/api/languages/${selectedLang}/recommendations`),
      ]);
      setModules(modulesRes.data || []);
      setLevels(levelsRes.data || []);
      setProgress(progressRes.data || null);
      setRecommendations(recRes.data || []);
      
      if (progressRes.data?.completed_modules) {
        setCompletedModules(new Set(progressRes.data.completed_modules));
      }
    } catch (err) {
      console.error('Error loading language data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteModule = async (moduleIndex) => {
    try {
      const res = await api.post(`/api/languages/${selectedLang}/modules/${moduleIndex}/complete`, {});
      const module = modules.find(m => m.module_index === moduleIndex);
      if (module) {
        setCompletedModules(prev => new Set([...prev, module.id]));
      }
      if (progress) {
        setProgress({
          ...progress,
          xp: (progress.xp || 0) + (res.data.xp_gained || 0),
          level: res.data.level || progress.level,
        });
      }
    } catch (err) {
      console.error('Error completing module:', err);
    }
  };

  const langInfo = LANGUAGES.find(l => l.id === selectedLang);
  const currentLevel = progress?.level || 1;
  const currentXp = progress?.xp || 0;
  const xpForNextLevel = currentLevel * 100;
  const xpProgress = ((currentXp % 100) / 100) * 100;

  const getTierForModule = (moduleIndex) => {
    return Math.min(Math.ceil(moduleIndex / 8), 10);
  };

  const getTierColor = (tier) => {
    const colors = ['text-green-400', 'text-blue-400', 'text-indigo-400', 'text-purple-400', 
                    'text-pink-400', 'text-red-400', 'text-orange-400', 'text-yellow-400', 
                    'text-cyan-400', 'text-white'];
    return colors[tier - 1] || 'text-gray-400';
  };

  const getTierIcon = (tier) => {
    const icons = ['🌱', '⚙️', '📊', '🌳', '🧠', '🏗️', '💎', '⚡', '🏗️', '👑'];
    return icons[tier - 1] || '📦';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 pb-20 md:pb-0">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Language Selector */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Language Learning Paths</h1>
          <p className="text-gray-400 mb-4">Master programming from first principles to building complex systems</p>
          
          <div className="flex flex-wrap gap-3">
            {LANGUAGES.map((lang) => (
              <motion.button
                key={lang.id}
                onClick={() => setSelectedLang(lang.id)}
                className={`px-4 py-3 rounded-xl font-medium transition-all flex items-center gap-2 ${
                  selectedLang === lang.id
                    ? `bg-gradient-to-r ${lang.color} text-white shadow-lg shadow-gray-900/50`
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                <span className="text-xl">{lang.icon}</span>
                {lang.name}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Language Header */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-gray-700">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-4xl">{langInfo?.icon}</span>
            <div>
              <h2 className="text-2xl font-bold text-white">{langInfo?.name} Learning Path</h2>
              <p className="text-gray-400">{langInfo?.primary_use}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-gray-900/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{modules.length}</div>
              <div className="text-sm text-gray-400">Modules</div>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{levels.length}</div>
              <div className="text-sm text-gray-400">Levels</div>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{currentLevel}</div>
              <div className="text-sm text-gray-400">Current Level</div>
            </div>
            <div className="bg-gray-900/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{currentXp}</div>
              <div className="text-sm text-gray-400">Total XP</div>
            </div>
          </div>

          {/* Level Progress Bar */}
          <div className="mt-6">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-400">Level {currentLevel} Progress</span>
              <span className="text-gray-400">{currentXp % 100}/100 XP</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3">
              <div 
                className="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full transition-all duration-500"
                style={{ width: `${xpProgress}%` }}
              />
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6 border-b border-gray-700">
          <button
            onClick={() => setActiveTab('path')}
            className={`pb-3 px-4 font-medium transition-colors ${
              activeTab === 'path' ? 'text-white border-b-2 border-purple-500' : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            Learning Path
          </button>
          <button
            onClick={() => setActiveTab('modules')}
            className={`pb-3 px-4 font-medium transition-colors ${
              activeTab === 'modules' ? 'text-white border-b-2 border-purple-500' : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            All Modules
          </button>
          <button
            onClick={() => setActiveTab('recommendations')}
            className={`pb-3 px-4 font-medium transition-colors ${
              activeTab === 'recommendations' ? 'text-white border-b-2 border-purple-500' : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            Recommended
          </button>
        </div>

        {/* Learning Path View */}
        {activeTab === 'path' && (
          <div className="space-y-6">
            {TIERS.map((tier, tierIdx) => {
              const tierNum = tierIdx + 1;
              const tierModules = modules.filter(m => getTierForModule(m.module_index) === tierNum);
              const isUnlocked = tierNum <= Math.ceil(currentLevel / 10) || tierNum === 1;
              
              return (
                <motion.div
                  key={tier.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: tierIdx * 0.1 }}
                  className={`bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border ${
                    isUnlocked ? 'border-gray-700' : 'border-gray-800 opacity-60'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{tier.icon}</span>
                      <div>
                        <h3 className={`text-xl font-bold ${getTierColor(tierNum)}`}>{tier.name}</h3>
                        <p className="text-sm text-gray-500">{tier.levels}</p>
                      </div>
                    </div>
                    {!isUnlocked && <Lock className="w-5 h-5 text-gray-600" />}
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {tierModules.map((module) => {
                      const isCompleted = completedModules.has(module.id);
                      const isModuleUnlocked = isUnlocked && (
                        module.module_index <= currentLevel + 5 || isCompleted
                      );
                      
                      return (
                        <motion.div
                          key={module.id}
                          className={`bg-gray-900/50 rounded-lg p-4 border transition-all ${
                            isCompleted
                              ? 'border-green-500/50 bg-green-500/10'
                              : isModuleUnlocked
                              ? 'border-gray-700 hover:border-purple-500'
                              : 'border-gray-800 opacity-50'
                          }`}
                          whileHover={isModuleUnlocked ? { scale: 1.02 } : {}}
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <span className={`text-sm font-bold ${getTierColor(getTierForModule(module.module_index))}`}>
                                  M{module.module_index}
                                </span>
                                {module.difficulty === 'beginner' && <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded">BEGINNER</span>}
                                {module.difficulty === 'intermediate' && <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded">INTERMEDIATE</span>}
                                {module.difficulty === 'advanced' && <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded">ADVANCED</span>}
                                {module.difficulty === 'expert' && <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded">EXPERT</span>}
                              </div>
                              <h4 className="font-medium text-white mt-1">{module.name}</h4>
                              <p className="text-xs text-gray-500 mt-1 line-clamp-2">{module.description}</p>
                            </div>
                            {isCompleted && <Trophy className="w-4 h-4 text-yellow-400 flex-shrink-0" />}
                          </div>
                          
                          <div className="flex items-center justify-between mt-3">
                            <div className="flex items-center gap-2 text-xs text-gray-500">
                              <Clock className="w-3 h-3" />
                              <span>{module.estimated_time}</span>
                              <span>•</span>
                              <span>{module.xp_reward} XP</span>
                            </div>
                            
                            {isModuleUnlocked && !isCompleted && (
                              <button
                                onClick={() => handleCompleteModule(module.module_index)}
                                className="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium transition-colors"
                              >
                                Start
                              </button>
                            )}
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* All Modules View */}
        {activeTab === 'modules' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {modules.map((module) => {
              const isCompleted = completedModules.has(module.id);
              const tierNum = getTierForModule(module.module_index);
              const isUnlocked = module.module_index <= currentLevel + 5 || isCompleted;
              
              return (
                <motion.div
                  key={module.id}
                  className={`bg-gray-800/50 backdrop-blur-sm rounded-xl p-5 border ${
                    isCompleted
                      ? 'border-green-500/50 bg-green-500/10'
                      : isUnlocked
                      ? 'border-gray-700 hover:border-purple-500'
                      : 'border-gray-800 opacity-50'
                  }`}
                  whileHover={isUnlocked ? { scale: 1.02 } : {}}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-bold ${getTierColor(tierNum)}`}>
                        {getTierIcon(tierNum)} M{module.module_index}
                      </span>
                      {module.type === 'project' && <span className="text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded">PROJECT</span>}
                      {module.type === 'tutorial' && <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded">TUTORIAL</span>}
                    </div>
                    {isCompleted && <Trophy className="w-5 h-5 text-yellow-400" />}
                  </div>
                  
                  <h3 className="font-bold text-white mb-2">{module.name}</h3>
                  <p className="text-sm text-gray-400 mb-3 line-clamp-2">{module.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span className={getTierColor(tierNum)}>Tier {tierNum}</span>
                      <span>•</span>
                      <span>{module.xp_reward} XP</span>
                    </div>
                    
                    {isUnlocked && !isCompleted && (
                      <button
                        onClick={() => handleCompleteModule(module.module_index)}
                        className="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium transition-colors"
                      >
                        Start
                      </button>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Recommendations View */}
        {activeTab === 'recommendations' && (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Recommended for You</h3>
            {recommendations.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {recommendations.map((module) => {
                  const isCompleted = completedModules.has(module.id);
                  const tierNum = getTierForModule(module.module_index);
                  
                  return (
                    <motion.div
                      key={module.id}
                      className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-5 border border-purple-500/30"
                      whileHover={{ scale: 1.02 }}
                    >
                      <div className="flex items-center gap-2 mb-3">
                        <Zap className="w-5 h-5 text-purple-400" />
                        <span className={`text-sm font-bold ${getTierColor(tierNum)}`}>
                          {getTierIcon(tierNum)} M{module.module_index}
                        </span>
                      </div>
                      
                      <h3 className="font-bold text-white mb-2">{module.name}</h3>
                      <p className="text-sm text-gray-400 mb-3">{module.description}</p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 text-xs text-gray-500">
                          <span className={getTierColor(tierNum)}>Tier {tierNum}</span>
                          <span>•</span>
                          <span>{module.xp_reward} XP</span>
                        </div>
                        
                        {!isCompleted && (
                          <button
                            onClick={() => handleCompleteModule(module.module_index)}
                            className="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium transition-colors"
                          >
                            Start
                          </button>
                        )}
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            ) : (
              <p className="text-gray-500">No recommendations available. Complete more modules to get personalized recommendations!</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LanguageLearning;