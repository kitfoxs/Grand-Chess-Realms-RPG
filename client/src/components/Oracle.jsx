import { useState } from 'react';

function Oracle() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [oracleHistory, setOracleHistory] = useState([]);

  const askOracle = () => {
    const roll = Math.floor(Math.random() * 20) + 1;
    let answer, description;

    if (roll <= 3) {
      answer = 'No, and...';
      description = 'Things go worse than expected';
    } else if (roll <= 10) {
      answer = 'No';
      description = 'The answer is negative';
    } else if (roll === 11) {
      answer = 'No, but...';
      description = 'No, but there\'s a silver lining';
    } else if (roll <= 14) {
      answer = 'Yes, but...';
      description = 'Yes, but with a complication';
    } else if (roll <= 19) {
      answer = 'Yes';
      description = 'The answer is positive';
    } else {
      answer = 'Yes, and...';
      description = 'Things go better than expected!';
    }

    const oracleResult = {
      question: question || 'Unknown question',
      roll,
      answer,
      description,
      timestamp: new Date().toISOString()
    };

    setResult(oracleResult);
    setOracleHistory(prev => [oracleResult, ...prev.slice(0, 9)]);
    setQuestion('');
  };

  const generateRandomEvent = () => {
    const events = [
      'A mysterious stranger arrives',
      'An unexpected chess challenge',
      'A secret message is delivered',
      'Weather changes dramatically',
      'A rumor spreads through the city',
      'An old friend reappears',
      'A valuable item is discovered',
      'A faction makes a move',
      'A prophecy is revealed',
      'A tournament is announced'
    ];

    const event = events[Math.floor(Math.random() * events.length)];
    setResult({
      question: 'Random Event',
      answer: event,
      description: 'A twist in your story...',
      timestamp: new Date().toISOString()
    });
  };

  const generatePlotTwist = () => {
    const twists = [
      'Someone you trust is not who they seem',
      'A hidden alliance is revealed',
      'The true objective was something else entirely',
      'An NPC has been playing both sides',
      'A chess match was more than it appeared',
      'Ancient prophecy begins to unfold',
      'A long-lost heir emerges',
      'The kingdoms face a common threat'
    ];

    const twist = twists[Math.floor(Math.random() * twists.length)];
    setResult({
      question: 'Plot Twist',
      answer: twist,
      description: 'Your story takes an unexpected turn...',
      timestamp: new Date().toISOString()
    });
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-2xl font-bold text-white mb-6">🔮 Oracle</h3>

      {/* Yes/No Oracle */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3">Yes/No Oracle</h4>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full bg-gray-700 text-white rounded p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none mb-3"
          rows="3"
          placeholder="Ask a yes/no question..."
        />
        <button
          onClick={askOracle}
          className="w-full px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors"
        >
          🎱 Consult the Oracle
        </button>
      </div>

      {/* Result Display */}
      {result && (
        <div className="bg-gray-700 rounded-lg p-6 mb-6">
          <p className="text-gray-400 text-sm mb-2">{result.question}</p>
          <p className="text-3xl font-bold text-white mb-2">{result.answer}</p>
          <p className="text-gray-300 text-sm">{result.description}</p>
          {result.roll && (
            <p className="text-gray-500 text-xs mt-2">Roll: {result.roll}/20</p>
          )}
        </div>
      )}

      {/* Oracle Interpretation Guide */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3">Interpretation Guide</h4>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">1-3:</span>
            <span className="text-red-400">No, and... (complication)</span>
          </div>
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">4-10:</span>
            <span className="text-orange-400">No</span>
          </div>
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">11:</span>
            <span className="text-yellow-400">No, but... (silver lining)</span>
          </div>
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">12-14:</span>
            <span className="text-blue-400">Yes, but... (complication)</span>
          </div>
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">15-19:</span>
            <span className="text-green-400">Yes</span>
          </div>
          <div className="flex justify-between bg-gray-700 rounded p-2">
            <span className="text-gray-300">20:</span>
            <span className="text-purple-400">Yes, and... (bonus!)</span>
          </div>
        </div>
      </div>

      {/* Additional Generators */}
      <div className="mb-6 space-y-2">
        <button
          onClick={generateRandomEvent}
          className="w-full px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
        >
          🎲 Random Event
        </button>
        <button
          onClick={generatePlotTwist}
          className="w-full px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
        >
          🌀 Plot Twist
        </button>
      </div>

      {/* Oracle History */}
      <div>
        <h4 className="text-lg font-semibold text-white mb-3">Recent Consultations</h4>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {oracleHistory.length === 0 && (
            <p className="text-gray-400 text-sm">No consultations yet</p>
          )}
          {oracleHistory.map((consultation, index) => (
            <div key={index} className="bg-gray-700 rounded p-3 text-sm">
              <p className="text-gray-400 mb-1">{consultation.question}</p>
              <p className="text-white font-semibold">{consultation.answer}</p>
              <span className="text-gray-500 text-xs">
                {new Date(consultation.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Oracle;
