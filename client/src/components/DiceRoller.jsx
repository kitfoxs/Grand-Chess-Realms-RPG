import { useState } from 'react';

function DiceRoller() {
  const [selectedDice, setSelectedDice] = useState('d20');
  const [modifier, setModifier] = useState(0);
  const [result, setResult] = useState(null);
  const [rollHistory, setRollHistory] = useState([]);

  const diceTypes = [
    { value: 'd20', label: 'd20', sides: 20 },
    { value: 'd12', label: 'd12', sides: 12 },
    { value: 'd10', label: 'd10', sides: 10 },
    { value: 'd8', label: 'd8', sides: 8 },
    { value: 'd6', label: 'd6', sides: 6 },
    { value: 'd4', label: 'd4', sides: 4 },
  ];

  const quickActions = [
    { label: 'Persuasion', dc: 15 },
    { label: 'Insight', dc: 15 },
    { label: 'Investigation', dc: 15 },
    { label: 'Stealth', dc: 15 },
  ];

  const difficulties = [
    { label: 'Easy', dc: 10 },
    { label: 'Medium', dc: 15 },
    { label: 'Hard', dc: 20 },
    { label: 'Very Hard', dc: 25 },
  ];

  const roll = (actionName = null) => {
    const dice = diceTypes.find(d => d.value === selectedDice);
    const baseRoll = Math.floor(Math.random() * dice.sides) + 1;
    const total = baseRoll + modifier;

    const rollResult = {
      dice: selectedDice,
      baseRoll,
      modifier,
      total,
      action: actionName,
      timestamp: new Date().toISOString()
    };

    setResult(rollResult);
    setRollHistory(prev => [rollResult, ...prev.slice(0, 9)]);
  };

  const quickRoll = (action) => {
    roll(action.label);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-2xl font-bold text-white mb-6">🎲 Dice Roller</h3>

      {/* Dice Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Select Dice
        </label>
        <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
          {diceTypes.map(dice => (
            <button
              key={dice.value}
              onClick={() => setSelectedDice(dice.value)}
              className={`p-3 rounded transition-colors ${
                selectedDice === dice.value
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {dice.label}
            </button>
          ))}
        </div>
      </div>

      {/* Modifier */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Modifier
        </label>
        <input
          type="number"
          value={modifier}
          onChange={(e) => setModifier(parseInt(e.target.value) || 0)}
          className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="0"
        />
      </div>

      {/* Roll Button */}
      <button
        onClick={() => roll()}
        className="w-full px-6 py-4 bg-green-600 hover:bg-green-700 text-white rounded text-lg font-semibold transition-colors mb-6"
      >
        Roll {selectedDice}
        {modifier !== 0 && ` ${modifier >= 0 ? '+' : ''}${modifier}`}
      </button>

      {/* Result Display */}
      {result && (
        <div className="bg-gray-700 rounded-lg p-6 mb-6 text-center">
          <p className="text-gray-400 text-sm mb-2">
            {result.action || 'Roll'} - {result.dice}
            {result.modifier !== 0 && ` ${result.modifier >= 0 ? '+' : ''}${result.modifier}`}
          </p>
          <p className="text-5xl font-bold text-white mb-2">{result.total}</p>
          {result.modifier !== 0 && (
            <p className="text-gray-400 text-sm">
              ({result.baseRoll} {result.modifier >= 0 ? '+' : ''}{result.modifier})
            </p>
          )}
        </div>
      )}

      {/* Quick Actions */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3">Quick Actions (d20)</h4>
        <div className="grid grid-cols-2 gap-2">
          {quickActions.map(action => (
            <button
              key={action.label}
              onClick={() => {
                setSelectedDice('d20');
                quickRoll(action);
              }}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors text-sm"
            >
              {action.label}
            </button>
          ))}
        </div>
      </div>

      {/* DC Reference */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3">Difficulty Reference</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {difficulties.map(diff => (
            <div key={diff.label} className="flex justify-between bg-gray-700 rounded p-2">
              <span className="text-gray-300">{diff.label}:</span>
              <span className="text-white font-semibold">DC {diff.dc}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Roll History */}
      <div>
        <h4 className="text-lg font-semibold text-white mb-3">Recent Rolls</h4>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {rollHistory.length === 0 && (
            <p className="text-gray-400 text-sm">No rolls yet</p>
          )}
          {rollHistory.map((roll, index) => (
            <div key={index} className="bg-gray-700 rounded p-3 text-sm">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">
                  {roll.action || 'Roll'} - {roll.dice}
                  {roll.modifier !== 0 && ` ${roll.modifier >= 0 ? '+' : ''}${roll.modifier}`}
                </span>
                <span className="text-white font-bold">{roll.total}</span>
              </div>
              <span className="text-gray-500 text-xs">
                {new Date(roll.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DiceRoller;
