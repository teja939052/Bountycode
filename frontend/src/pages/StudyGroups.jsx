import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../services/api';
import useAuthStore from '../store/authStore';
import { Card, CardGrid } from '../components/ui/Card';

export default function StudyGroups() {
  const { user } = useAuthStore();
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [creating, setCreating] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => { loadGroups(); }, []);

  const loadGroups = async () => {
    setLoading(true);
    try {
      const data = await api.getStudyGroups();
      setGroups(data.groups || data || []);
    } catch { setGroups([]); }
    finally { setLoading(false); }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await api.createStudyGroup(newName, newDesc);
      setShowCreate(false);
      setNewName(''); setNewDesc('');
      loadGroups();
    } catch {} finally { setCreating(false); }
  };

  const handleJoin = async (groupId) => {
    try { await api.joinStudyGroup(groupId); loadGroups(); } catch {}
  };

  const filtered = groups.filter(g => g.name?.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <motion.div initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }}>
            <span className="section-subheader mb-1 block">Prep Squads</span>
            <h1 className="section-header text-3xl">
              Study <span className="text-cyber-blue">Groups</span>
            </h1>
            <p className="text-gray-500 text-sm font-mono mt-1">Prepare together, succeed together</p>
          </motion.div>
          <motion.button
            onClick={() => setShowCreate(!showCreate)}
            className="btn-primary text-sm flex items-center gap-2"
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
          >
            {showCreate ? '✕ Cancel' : '+ Create Group'}
          </motion.button>
        </div>

        {/* Create form */}
        <AnimatePresence>
          {showCreate && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-6 overflow-hidden"
            >
              <Card rarity="rare" hoverEffect={false}>
                <h3 className="font-display font-bold text-sm uppercase tracking-wider text-white mb-4">
                  Create a Study Group
                </h3>
                <form onSubmit={handleCreate} className="space-y-3">
                  <input
                    type="text"
                    placeholder="Group name (e.g., FAANG Prep Squad)"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    className="input"
                    required
                  />
                  <input
                    type="text"
                    placeholder="Description (optional)"
                    value={newDesc}
                    onChange={(e) => setNewDesc(e.target.value)}
                    className="input"
                  />
                  <div className="flex gap-3">
                    <button type="submit" disabled={creating} className="btn-primary text-sm">
                      {creating ? 'Creating...' : 'Create'}
                    </button>
                    <button type="button" onClick={() => setShowCreate(false)} className="btn-ghost text-sm">
                      Cancel
                    </button>
                  </div>
                </form>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Search */}
        <div className="relative mb-6">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm">🔍</span>
          <input
            type="text"
            placeholder="Search groups..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-10"
          />
        </div>

        {/* Groups grid */}
        {loading ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="rounded-xl border border-gray-700/20 p-5 animate-pulse bg-gray-900/20">
                <div className="h-4 bg-gray-700/40 rounded w-1/2 mb-3" />
                <div className="h-3 bg-gray-700/30 rounded w-2/3 mb-2" />
                <div className="h-3 bg-gray-700/20 rounded w-1/3" />
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <Card rarity="common" hoverEffect={false} className="text-center py-12">
            <div className="text-4xl mb-3">👥</div>
            <p className="text-gray-400 text-sm">{searchQuery ? 'No groups found' : 'No study groups yet'}</p>
            <p className="text-xs text-gray-600 mt-1 font-mono">Create one and invite your friends!</p>
          </Card>
        ) : (
          <CardGrid>
            {filtered.map((group, i) => (
              <Card
                key={group._id || group.group_id || i}
                rarity={i < 3 ? 'uncommon' : 'common'}
                hoverEffect
                onClick={() => {}}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-cyber-blue/15 flex items-center justify-center text-lg">
                      {group.is_private ? '🔒' : '🌐'}
                    </div>
                    <div className="min-w-0">
                      <h3 className="font-semibold text-sm text-white truncate">{group.name}</h3>
                      <p className="text-[10px] font-mono text-gray-500">
                        {group.members?.length || 0} members
                      </p>
                    </div>
                  </div>
                </div>

                {group.description && (
                  <p className="text-xs text-gray-400 mb-3 line-clamp-2">{group.description}</p>
                )}

                <div className="flex items-center justify-between">
                  {/* Avatars */}
                  <div className="flex -space-x-2">
                    {(group.members || []).slice(0, 4).map((m, j) => (
                      <div
                        key={j}
                        className="w-7 h-7 rounded-full bg-gray-700 border-2 border-gray-900 flex items-center justify-center text-[9px] font-bold text-gray-300"
                      >
                        {m.name?.[0] || '?'}
                      </div>
                    ))}
                    {(group.members?.length || 0) > 4 && (
                      <div className="w-7 h-7 rounded-full bg-gray-800 border-2 border-gray-900 flex items-center justify-center text-[9px] text-gray-500">
                        +{group.members.length - 4}
                      </div>
                    )}
                  </div>

                  <button
                    onClick={(e) => { e.stopPropagation(); handleJoin(group._id || group.group_id); }}
                    className="text-[11px] font-mono font-bold text-cyber-blue hover:text-cyber-blue/80 transition-colors"
                  >
                    + Join
                  </button>
                </div>
              </Card>
            ))}
          </CardGrid>
        )}
      </div>
    </div>
  );
}
