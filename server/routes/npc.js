const express = require('express');
const fetch = require('node-fetch');
const { getDatabase } = require('../db/database');
const { buildSystemPrompt } = require('../prompts/npcPrompts');

const router = express.Router();

// Get NPC data
router.get('/:npcId', async (req, res) => {
  try {
    const { npcId } = req.params;
    // Load NPC data from JSON files or database
    const npcsData = require('../data/npcs.json');
    const npc = npcsData[npcId];
    
    if (!npc) {
      return res.status(404).json({ error: 'NPC not found' });
    }

    res.json(npc);
  } catch (error) {
    console.error('Error fetching NPC:', error);
    res.status(500).json({ error: 'Failed to fetch NPC data' });
  }
});

// Send message to NPC
router.post('/:npcId/message', async (req, res) => {
  try {
    const { npcId } = req.params;
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Get NPC data
    const npcsData = require('../data/npcs.json');
    const npc = npcsData[npcId];

    if (!npc) {
      return res.status(404).json({ error: 'NPC not found' });
    }

    // Get NPC memory and relationship
    const db = await getDatabase();
    const memory = await getNPCMemory(db, npcId);
    const relationship = await getNPCRelationship(db, npcId);

    // Build system prompt
    const systemPrompt = buildSystemPrompt(npc, { 
      chessMatches: memory.chessMatches,
      recentMemories: memory.recentMemories,
      relationship 
    }, { currentScene: 'Conversation' });

    // Save user message
    await saveConversation(db, npcId, 'user', message);

    // Get recent conversation history
    const conversationHistory = await getRecentConversation(db, npcId, 10);

    // Call LM Studio
    try {
      const response = await fetch('http://127.0.0.1:1234/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'local-model',
          messages: [
            { role: 'system', content: systemPrompt },
            ...conversationHistory,
            { role: 'user', content: message }
          ],
          temperature: 0.8,
          max_tokens: 400
        }),
        timeout: 30000
      });

      if (!response.ok) {
        throw new Error('LM Studio request failed');
      }

      const data = await response.json();
      const npcResponse = data.choices[0].message.content;

      // Save NPC response
      await saveConversation(db, npcId, 'assistant', npcResponse);

      res.json({ response: npcResponse });
    } catch (lmError) {
      console.error('LM Studio error:', lmError);
      
      // Fallback response
      const fallbackResponse = `[LM Studio not available] ${npc.name}: I appreciate your message, but I'm currently unable to respond properly. Please ensure LM Studio is running.`;
      
      res.json({ 
        response: fallbackResponse,
        error: 'LM Studio not available' 
      });
    }
  } catch (error) {
    console.error('Error sending message to NPC:', error);
    res.status(500).json({ error: 'Failed to send message' });
  }
});

// Helper functions
async function getNPCMemory(db, npcId) {
  return new Promise((resolve, reject) => {
    const memory = { chessMatches: [], recentMemories: [] };

    // Get recent chess matches
    db.all(
      'SELECT * FROM chess_matches WHERE npc_id = ? ORDER BY timestamp DESC LIMIT 5',
      [npcId],
      (err, matches) => {
        if (err) {
          reject(err);
          return;
        }
        memory.chessMatches = matches || [];

        // Get recent memories
        db.all(
          'SELECT * FROM npc_memories WHERE npc_id = ? ORDER BY importance DESC, timestamp DESC LIMIT 10',
          [npcId],
          (err, memories) => {
            if (err) {
              reject(err);
              return;
            }
            memory.recentMemories = memories || [];
            resolve(memory);
          }
        );
      }
    );
  });
}

async function getNPCRelationship(db, npcId) {
  return new Promise((resolve, reject) => {
    db.get(
      'SELECT * FROM npc_relationships WHERE npc_id = ?',
      [npcId],
      (err, row) => {
        if (err) {
          reject(err);
          return;
        }
        resolve(row || { trust: 50, respect: 50, friendship: 50 });
      }
    );
  });
}

async function saveConversation(db, npcId, role, content) {
  return new Promise((resolve, reject) => {
    db.run(
      'INSERT INTO npc_conversations (npc_id, role, content) VALUES (?, ?, ?)',
      [npcId, role, content],
      (err) => {
        if (err) {
          reject(err);
          return;
        }
        resolve();
      }
    );
  });
}

async function getRecentConversation(db, npcId, limit) {
  return new Promise((resolve, reject) => {
    db.all(
      'SELECT role, content FROM npc_conversations WHERE npc_id = ? ORDER BY timestamp DESC LIMIT ?',
      [npcId, limit],
      (err, rows) => {
        if (err) {
          reject(err);
          return;
        }
        // Reverse to get chronological order
        const messages = (rows || []).reverse().map(row => ({
          role: row.role,
          content: row.content
        }));
        resolve(messages);
      }
    );
  });
}

module.exports = router;
