import { useState } from 'react';

function WorldReference() {
  const [selectedTab, setSelectedTab] = useState('locations');

  const locations = [
    {
      name: 'Castle Lumina',
      faction: 'White Kingdom',
      description: 'The gleaming capital of the White Kingdom, home to King Alden XIV.',
      npcs: ['King Alden XIV', 'Princess Elara', 'Knight Roland'],
      plotHooks: ['Royal court intrigue', 'Tournament preparations', 'Reform movement']
    },
    {
      name: 'Obsidian Throne',
      faction: 'Black Kingdom',
      description: 'The dark fortress of the Black Kingdom, seat of Emperor Darius.',
      npcs: ['Emperor Darius', 'Empress Selene'],
      plotHooks: ['Political maneuvering', 'Meritocratic challenges', 'Expansion plans']
    },
    {
      name: 'Knightfall City',
      faction: 'Neutral',
      description: 'A major neutral hub where both kingdoms meet for trade and diplomacy.',
      npcs: ['Grandmaster Altan'],
      plotHooks: ['Spy networks', 'Chess academy', 'Neutral ground meetings']
    },
    {
      name: 'Greyhaven',
      faction: 'Neutral',
      description: 'A strategic port city controlling vital sea routes.',
      npcs: ['Grandmaster Rionn'],
      plotHooks: ['Naval power', 'Trade disputes', 'Smuggling operations']
    },
    {
      name: 'FourSquares',
      faction: 'Neutral',
      description: 'The great trading city where all factions conduct business.',
      npcs: ['Ambassador Corvus'],
      plotHooks: ['Trade agreements', 'Market manipulation', 'Information brokers']
    }
  ];

  const campaigns = [
    {
      name: 'Pieces in Play',
      type: 'Starter Adventure',
      sessions: '1-2',
      description: 'Introduction to Grand Chess Realms. Meet Knight Roland, learn the basics of chess-based conflict resolution, and get drawn into a simple mystery.',
      objectives: ['Learn game mechanics', 'Meet first NPCs', 'Complete first chess match']
    },
    {
      name: 'The Grand Tournament',
      type: 'Major Campaign',
      sessions: '6-10',
      description: 'Compete in a realm-wide chess tournament. Political intrigue and secret societies threaten the competition\'s integrity.',
      objectives: ['Win tournament matches', 'Uncover conspiracy', 'Choose allegiances']
    },
    {
      name: 'War of Two Kings',
      type: 'Major Campaign',
      sessions: '10-15',
      description: 'A border incident escalates into full-scale war. Strategic chess battles determine territorial control.',
      objectives: ['Lead military campaigns', 'Negotiate peace', 'Shape the realm\'s future']
    },
    {
      name: 'The Lost Tome of Caissa',
      type: 'Major Campaign',
      sessions: '8-12',
      description: 'Race to find an ancient magical text containing pre-Bisection knowledge. Solve chess puzzles and explore dangerous ruins.',
      objectives: ['Solve ancient puzzles', 'Navigate faction politics', 'Decide fate of knowledge']
    }
  ];

  const factions = [
    {
      name: 'White Kingdom',
      symbol: '⚪',
      values: 'Tradition • Honor • Defense',
      description: 'The White Kingdom values structured hierarchy, ancient traditions, and defensive chess principles.',
      leader: 'King Alden XIV',
      capital: 'Castle Lumina'
    },
    {
      name: 'Black Kingdom',
      symbol: '⚫',
      values: 'Ambition • Innovation • Aggression',
      description: 'The Black Kingdom embraces meritocracy where anyone can rise through skill and cunning.',
      leader: 'Emperor Darius Blackbourne',
      capital: 'Obsidian Throne'
    },
    {
      name: 'Neutral Territories',
      symbol: '🔘',
      values: 'Independence • Pragmatism • Balance',
      description: 'Independent cities maintaining precarious freedom through diplomacy and economic leverage.',
      leader: 'Various city councils',
      capital: 'Knightfall City, Greyhaven, FourSquares'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">🗺️ World Reference</h2>

      {/* Tab Navigation */}
      <div className="mb-6 flex gap-2">
        <button
          onClick={() => setSelectedTab('locations')}
          className={`px-4 py-2 rounded ${
            selectedTab === 'locations'
              ? 'bg-gray-700 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          📍 Locations
        </button>
        <button
          onClick={() => setSelectedTab('campaigns')}
          className={`px-4 py-2 rounded ${
            selectedTab === 'campaigns'
              ? 'bg-gray-700 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          ⚔️ Campaigns
        </button>
        <button
          onClick={() => setSelectedTab('factions')}
          className={`px-4 py-2 rounded ${
            selectedTab === 'factions'
              ? 'bg-gray-700 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-750'
          }`}
        >
          🏰 Factions
        </button>
      </div>

      {/* Locations Tab */}
      {selectedTab === 'locations' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {locations.map((location, index) => (
            <div key={index} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-white">{location.name}</h3>
                <span className={`text-sm px-2 py-1 rounded ${
                  location.faction === 'White Kingdom' ? 'bg-white-kingdom-gold text-black' :
                  location.faction === 'Black Kingdom' ? 'bg-black-kingdom-purple text-white' :
                  'bg-neutral-gray text-white'
                }`}>
                  {location.faction}
                </span>
              </div>
              
              <p className="text-gray-300 mb-4">{location.description}</p>
              
              <div className="mb-3">
                <p className="text-sm font-semibold text-gray-400 mb-1">Notable NPCs:</p>
                <div className="flex flex-wrap gap-2">
                  {location.npcs.map((npc, i) => (
                    <span key={i} className="text-xs bg-gray-700 px-2 py-1 rounded text-gray-300">
                      {npc}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <p className="text-sm font-semibold text-gray-400 mb-1">Plot Hooks:</p>
                <ul className="text-sm text-gray-300 list-disc list-inside">
                  {location.plotHooks.map((hook, i) => (
                    <li key={i}>{hook}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Campaigns Tab */}
      {selectedTab === 'campaigns' && (
        <div className="space-y-6">
          {campaigns.map((campaign, index) => (
            <div key={index} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-2xl font-bold text-white mb-2">{campaign.name}</h3>
                  <div className="flex gap-4 text-sm text-gray-400">
                    <span>📚 {campaign.type}</span>
                    <span>🕐 {campaign.sessions} sessions</span>
                  </div>
                </div>
              </div>
              
              <p className="text-gray-300 mb-4">{campaign.description}</p>
              
              <div>
                <p className="text-sm font-semibold text-gray-400 mb-2">Campaign Objectives:</p>
                <ul className="text-sm text-gray-300 list-disc list-inside space-y-1">
                  {campaign.objectives.map((obj, i) => (
                    <li key={i}>{obj}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Factions Tab */}
      {selectedTab === 'factions' && (
        <div className="space-y-6">
          {factions.map((faction, index) => (
            <div key={index} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex items-start gap-4 mb-4">
                <span className="text-4xl">{faction.symbol}</span>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-white mb-2">{faction.name}</h3>
                  <p className="text-gray-400 italic mb-4">{faction.values}</p>
                </div>
              </div>
              
              <p className="text-gray-300 mb-4">{faction.description}</p>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-400 font-semibold mb-1">Leader:</p>
                  <p className="text-white">{faction.leader}</p>
                </div>
                <div>
                  <p className="text-gray-400 font-semibold mb-1">Capital:</p>
                  <p className="text-white">{faction.capital}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default WorldReference;
