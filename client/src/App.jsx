import { useState, useEffect } from 'react';
import ChessBoard from './components/ChessBoard';
import CharacterSheet from './components/CharacterSheet';
import NPCConversation from './components/NPCConversation';
import DiceRoller from './components/DiceRoller';
import Journal from './components/Journal';
import Oracle from './components/Oracle';
import NPCDatabase from './components/NPCDatabase';
import WorldReference from './components/WorldReference';

function App() {
  const [activeTab, setActiveTab] = useState('npc-database');
  const [lmStudioConnected, setLmStudioConnected] = useState(false);
  const [selectedNPC, setSelectedNPC] = useState(null);
  const [character, setCharacter] = useState(null);

  useEffect(() => {
    checkLMStudio();
    loadCharacter();
  }, []);

  const checkLMStudio = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/lm-studio/check');
      const data = await response.json();
      setLmStudioConnected(data.connected);
    } catch (error) {
      console.error('Error checking LM Studio:', error);
      setLmStudioConnected(false);
    }
  };

  const loadCharacter = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/game/character');
      const data = await response.json();
      setCharacter(data);
    } catch (error) {
      console.error('Error loading character:', error);
    }
  };

  const handleNPCSelect = (npc) => {
    setSelectedNPC(npc);
    setActiveTab('conversation');
  };

  const handleStartChessMatch = (npc) => {
    setSelectedNPC(npc);
    setActiveTab('chess');
  };

  const tabs = [
    { id: 'npc-database', label: 'NPCs', icon: '👥' },
    { id: 'conversation', label: 'Talk', icon: '💬' },
    { id: 'chess', label: 'Chess', icon: '♟️' },
    { id: 'character', label: 'Character', icon: '📋' },
    { id: 'journal', label: 'Journal', icon: '📖' },
    { id: 'tools', label: 'Tools', icon: '🎲' },
    { id: 'world', label: 'World', icon: '🗺️' },
  ];

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white-kingdom-gold">
            ♔ Grand Chess Realms ♚
          </h1>
          <div className="flex items-center gap-4">
            {!lmStudioConnected && (
              <div className="text-sm text-yellow-400 flex items-center gap-2">
                <span className="inline-block w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                LM Studio not connected
              </div>
            )}
            {lmStudioConnected && (
              <div className="text-sm text-green-400 flex items-center gap-2">
                <span className="inline-block w-2 h-2 bg-green-400 rounded-full"></span>
                LM Studio connected
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="flex overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? 'bg-gray-700 text-white border-b-2 border-white-kingdom-gold'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-750'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-auto p-6">
        {activeTab === 'npc-database' && (
          <NPCDatabase 
            onSelectNPC={handleNPCSelect}
            onStartChessMatch={handleStartChessMatch}
          />
        )}
        {activeTab === 'conversation' && (
          <NPCConversation 
            npc={selectedNPC}
            lmStudioConnected={lmStudioConnected}
          />
        )}
        {activeTab === 'chess' && (
          <ChessBoard npc={selectedNPC} character={character} />
        )}
        {activeTab === 'character' && (
          <CharacterSheet 
            character={character} 
            onSave={setCharacter}
          />
        )}
        {activeTab === 'journal' && <Journal />}
        {activeTab === 'tools' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <DiceRoller />
            <Oracle />
          </div>
        )}
        {activeTab === 'world' && <WorldReference />}
      </main>
    </div>
  );
}

export default App;
