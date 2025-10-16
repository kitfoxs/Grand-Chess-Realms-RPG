import { useState, useEffect } from 'react';

function CharacterSheet({ character, onSave }) {
  const [formData, setFormData] = useState({
    name: '',
    concept: '',
    faction: 'Neutral',
    race: 'Human',
    playerElo: 1500,
    openingRepertoire: '',
    backstory: '',
    currentLocation: 'Knightfall City',
    relationshipNotes: {},
    questLog: []
  });

  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (character) {
      setFormData(character);
    }
  }, [character]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const response = await fetch('http://localhost:3001/api/game/character', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        onSave(formData);
        alert('Character saved successfully!');
      }
    } catch (error) {
      console.error('Error saving character:', error);
      alert('Failed to save character');
    } finally {
      setSaving(false);
    }
  };

  const factions = ['White Kingdom', 'Black Kingdom', 'Neutral'];
  const races = ['Human', 'Elf', 'Dwarf', 'Orc', 'Beastfolk', 'Undead', 'Mystical Being'];

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">Character Sheet</h2>

      <div className="bg-gray-800 rounded-lg p-6 space-y-6">
        {/* Basic Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Character Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your character's name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Concept
            </label>
            <input
              type="text"
              name="concept"
              value={formData.concept}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Noble Strategist, Wandering Philosopher"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Faction
            </label>
            <select
              name="faction"
              value={formData.faction}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {factions.map(f => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Race
            </label>
            <select
              name="race"
              value={formData.race}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {races.map(r => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Chess Elo Rating
            </label>
            <input
              type="number"
              name="playerElo"
              value={formData.playerElo}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="800"
              max="2800"
            />
            <p className="text-xs text-gray-500 mt-1">
              Your honest chess rating (800-2800)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Current Location
            </label>
            <input
              type="text"
              name="currentLocation"
              value={formData.currentLocation}
              onChange={handleChange}
              className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Opening Repertoire */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Opening Repertoire
          </label>
          <textarea
            name="openingRepertoire"
            value={formData.openingRepertoire}
            onChange={handleChange}
            className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows="3"
            placeholder="Describe your preferred chess openings and playing style..."
          />
        </div>

        {/* Backstory */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Backstory
          </label>
          <textarea
            name="backstory"
            value={formData.backstory}
            onChange={handleChange}
            className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows="6"
            placeholder="Tell your character's story..."
          />
        </div>

        {/* Character Stats Display */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-6 border-t border-gray-700">
          <div className="text-center">
            <p className="text-gray-400 text-sm">Faction</p>
            <p className="text-white text-lg font-semibold">
              {formData.faction === 'White Kingdom' && '⚪'}
              {formData.faction === 'Black Kingdom' && '⚫'}
              {formData.faction === 'Neutral' && '🔘'}
            </p>
          </div>
          <div className="text-center">
            <p className="text-gray-400 text-sm">Race</p>
            <p className="text-white text-lg font-semibold">{formData.race}</p>
          </div>
          <div className="text-center">
            <p className="text-gray-400 text-sm">Elo Rating</p>
            <p className="text-white text-lg font-semibold">{formData.playerElo}</p>
          </div>
          <div className="text-center">
            <p className="text-gray-400 text-sm">Location</p>
            <p className="text-white text-lg font-semibold truncate" title={formData.currentLocation}>
              {formData.currentLocation}
            </p>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end pt-6 border-t border-gray-700">
          <button
            onClick={handleSave}
            disabled={saving || !formData.name}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Saving...' : 'Save Character'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default CharacterSheet;
