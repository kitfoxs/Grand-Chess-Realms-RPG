import { useState, useEffect, useRef } from 'react';

function NPCConversation({ npc, lmStudioConnected }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [relationship, setRelationship] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (npc) {
      loadConversationHistory();
      loadRelationship();
    }
  }, [npc]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversationHistory = async () => {
    try {
      const response = await fetch(`http://localhost:3001/api/memory/conversation/${npc.id}?limit=20`);
      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const loadRelationship = async () => {
    try {
      const response = await fetch(`http://localhost:3001/api/memory/relationship/${npc.id}`);
      const data = await response.json();
      setRelationship(data);
    } catch (error) {
      console.error('Error loading relationship:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setLoading(true);

    // Add user message to UI immediately
    const newUserMessage = { role: 'user', content: userMessage, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await fetch(`http://localhost:3001/api/npc/${npc.id}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();

      // Add NPC response
      const npcMessage = { role: 'assistant', content: data.response, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, npcMessage]);

      // Reload relationship after conversation
      loadRelationship();
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'I apologize, but I cannot respond right now. Please ensure the server is running.',
        timestamp: new Date().toISOString() 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!npc) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-gray-400">
          <p className="text-xl mb-2">No NPC selected</p>
          <p>Please select an NPC from the NPC Database to start a conversation</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col">
      {/* NPC Header */}
      <div className="bg-gray-800 rounded-lg p-6 mb-4">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-white mb-2">{npc.name}</h2>
            <p className="text-gray-400 mb-2">{npc.title}</p>
            <p className="text-sm text-gray-500">📍 {npc.location} | ♟️ Elo {npc.elo}</p>
          </div>
          {relationship && (
            <div className="text-sm">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-gray-400">Trust:</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${relationship.trust_level}%` }}
                  ></div>
                </div>
                <span className="text-white">{relationship.trust_level}</span>
              </div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-gray-400">Respect:</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${relationship.respect_level}%` }}
                  ></div>
                </div>
                <span className="text-white">{relationship.respect_level}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-400">Friendship:</span>
                <div className="w-24 bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-purple-500 h-2 rounded-full"
                    style={{ width: `${relationship.friendship_level}%` }}
                  ></div>
                </div>
                <span className="text-white">{relationship.friendship_level}</span>
              </div>
            </div>
          )}
        </div>

        {!lmStudioConnected && (
          <div className="mt-4 p-3 bg-yellow-900 border border-yellow-700 rounded text-yellow-200 text-sm">
            ⚠️ LM Studio is not connected. Responses may be limited. Please start LM Studio to enable full AI conversations.
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 bg-gray-800 rounded-lg p-4 overflow-y-auto mb-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 py-12">
            <p>Start a conversation with {npc.name}</p>
            <p className="text-sm mt-2">They are known for: {npc.personality}</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
              <p className="text-xs mt-1 opacity-70">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-700 rounded-lg p-3">
              <p className="text-gray-400">Typing...</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-gray-800 rounded-lg p-4">
        <div className="flex gap-2">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Talk to ${npc.name}...`}
            className="flex-1 bg-gray-700 text-white rounded p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !inputMessage.trim()}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default NPCConversation;
