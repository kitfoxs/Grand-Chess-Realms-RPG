import { useState, useEffect } from 'react';

function Journal() {
  const [entries, setEntries] = useState([]);
  const [newEntry, setNewEntry] = useState('');
  const [saving, setSaving] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState(null);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/game/journal');
      const data = await response.json();
      setEntries(data);
    } catch (error) {
      console.error('Error loading journal entries:', error);
    }
  };

  const saveEntry = async () => {
    if (!newEntry.trim()) return;

    setSaving(true);
    try {
      const response = await fetch('http://localhost:3001/api/game/journal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: newEntry,
          metadata: {
            sessionNumber: entries.length + 1,
            tags: []
          }
        })
      });

      if (response.ok) {
        setNewEntry('');
        loadEntries();
      }
    } catch (error) {
      console.error('Error saving entry:', error);
      alert('Failed to save journal entry');
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">📖 Campaign Journal</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Entry List */}
        <div className="lg:col-span-1">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Journal Entries</h3>
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {entries.length === 0 && (
                <p className="text-gray-400 text-sm">No entries yet. Start writing!</p>
              )}
              {entries.map((entry) => (
                <button
                  key={entry.id}
                  onClick={() => setSelectedEntry(entry)}
                  className={`w-full text-left p-3 rounded transition-colors ${
                    selectedEntry?.id === entry.id
                      ? 'bg-gray-700 text-white'
                      : 'bg-gray-750 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <p className="font-semibold mb-1">
                    Session {entry.metadata?.sessionNumber || entry.id}
                  </p>
                  <p className="text-xs text-gray-400">
                    {formatDate(entry.timestamp)}
                  </p>
                  <p className="text-sm text-gray-300 line-clamp-2 mt-1">
                    {entry.content}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Entry Editor/Viewer */}
        <div className="lg:col-span-2">
          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <h3 className="text-xl font-bold text-white mb-4">New Entry</h3>
            <textarea
              value={newEntry}
              onChange={(e) => setNewEntry(e.target.value)}
              className="w-full bg-gray-700 text-white rounded p-4 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none font-mono"
              rows="15"
              placeholder="Write your session notes here...

You can record:
- What happened in your adventure
- NPCs you met and conversations
- Chess matches won or lost
- Discoveries and revelations
- Quest progress
- Character thoughts and feelings"
            />
            <div className="flex justify-end mt-4">
              <button
                onClick={saveEntry}
                disabled={saving || !newEntry.trim()}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? 'Saving...' : '💾 Save Entry'}
              </button>
            </div>
          </div>

          {/* Selected Entry Viewer */}
          {selectedEntry && (
            <div className="bg-gray-800 rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    Session {selectedEntry.metadata?.sessionNumber || selectedEntry.id}
                  </h3>
                  <p className="text-sm text-gray-400">
                    {formatDate(selectedEntry.timestamp)}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedEntry(null)}
                  className="text-gray-400 hover:text-white"
                >
                  ✕
                </button>
              </div>
              <div className="prose prose-invert max-w-none">
                <p className="text-gray-300 whitespace-pre-wrap">
                  {selectedEntry.content}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Journal;
