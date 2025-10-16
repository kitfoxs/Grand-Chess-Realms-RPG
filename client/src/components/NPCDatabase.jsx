import { useState, useEffect } from 'react';

function NPCDatabase({ onSelectNPC, onStartChessMatch }) {
  const [npcs, setNpcs] = useState([]);
  const [selectedFaction, setSelectedFaction] = useState('all');

  useEffect(() => {
    loadNPCs();
  }, []);

  const loadNPCs = async () => {
    try {
      const response = await fetch('/server/data/npcs.json');
      const data = await response.json();
      setNpcs(Object.values(data));
    } catch (error) {
      console.error('Error loading NPCs:', error);
    }
  };

  const filteredNPCs = selectedFaction === 'all'
    ? npcs
    : npcs.filter(npc => npc.faction === selectedFaction);

  const getFactionColor = (faction) => {
    if (faction === 'White Kingdom') return 'text-white-kingdom-gold';
    if (faction === 'Black Kingdom') return 'text-black-kingdom-purple';
    return 'text-neutral-gray-light';
  };

  const getEloColor = (elo) => {
    if (elo >= 2400) return 'text-red-400';
    if (elo >= 2200) return 'text-orange-400';
    if (elo >= 2000) return 'text-yellow-400';
    if (elo >= 1800) return 'text-green-400';
    return 'text-blue-400';
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">NPC Database</h2>

      {/* Faction Filter */}
      <div className="mb-6 flex gap-2">
        <button
          onClick={() => setSelectedFaction('all')}
          className={`px-4 py-2 rounded ${
            selectedFaction === 'all'
              ? 'bg-gray-700 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setSelectedFaction('White Kingdom')}
          className={`px-4 py-2 rounded ${
            selectedFaction === 'White Kingdom'
              ? 'bg-gray-700 text-white-kingdom-gold'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          ⚪ White Kingdom
        </button>
        <button
          onClick={() => setSelectedFaction('Black Kingdom')}
          className={`px-4 py-2 rounded ${
            selectedFaction === 'Black Kingdom'
              ? 'bg-gray-700 text-black-kingdom-purple'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          ⚫ Black Kingdom
        </button>
        <button
          onClick={() => setSelectedFaction('Neutral')}
          className={`px-4 py-2 rounded ${
            selectedFaction === 'Neutral'
              ? 'bg-gray-700 text-neutral-gray-light'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          🔘 Neutral
        </button>
      </div>

      {/* NPC Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredNPCs.map((npc) => (
          <div
            key={npc.id}
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-gray-600 transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold text-white mb-1">{npc.name}</h3>
                <p className="text-sm text-gray-400">{npc.title}</p>
              </div>
              <div className={`text-2xl font-bold ${getEloColor(npc.elo)}`}>
                {npc.elo}
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <p className={`text-sm ${getFactionColor(npc.faction)}`}>
                📍 {npc.location}
              </p>
              <p className="text-sm text-gray-400">
                ♟️ {npc.chessStyle}
              </p>
              <p className="text-sm text-gray-300 italic">{npc.personality}</p>
            </div>

            <p className="text-sm text-gray-400 mb-4 line-clamp-3">
              {npc.backstory}
            </p>

            <div className="flex gap-2">
              <button
                onClick={() => onSelectNPC(npc)}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
              >
                💬 Talk
              </button>
              <button
                onClick={() => onStartChessMatch(npc)}
                className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded transition-colors"
              >
                ♟️ Challenge
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredNPCs.length === 0 && (
        <div className="text-center text-gray-400 py-12">
          No NPCs found for this faction.
        </div>
      )}
    </div>
  );
}

export default NPCDatabase;
