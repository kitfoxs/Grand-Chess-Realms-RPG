const express = require('express');
const { getDatabase } = require('../db/database');

const router = express.Router();

// Get NPC relationship
router.get('/relationship/:npcId', async (req, res) => {
  try {
    const { npcId } = req.params;
    const db = await getDatabase();
    
    db.get(
      'SELECT * FROM npc_relationships WHERE npc_id = ?',
      [npcId],
      (err, row) => {
        if (err) {
          console.error('Error fetching relationship:', err);
          return res.status(500).json({ error: 'Failed to fetch relationship' });
        }

        res.json(row || {
          npc_id: npcId,
          trust_level: 50,
          respect_level: 50,
          friendship_level: 50
        });
      }
    );
  } catch (error) {
    console.error('Error fetching relationship:', error);
    res.status(500).json({ error: 'Failed to fetch relationship' });
  }
});

// Get conversation history
router.get('/conversation/:npcId', async (req, res) => {
  try {
    const { npcId } = req.params;
    const limit = parseInt(req.query.limit) || 20;
    const db = await getDatabase();
    
    db.all(
      'SELECT * FROM npc_conversations WHERE npc_id = ? ORDER BY timestamp DESC LIMIT ?',
      [npcId, limit],
      (err, rows) => {
        if (err) {
          console.error('Error fetching conversations:', err);
          return res.status(500).json({ error: 'Failed to fetch conversations' });
        }

        res.json(rows.reverse());
      }
    );
  } catch (error) {
    console.error('Error fetching conversations:', error);
    res.status(500).json({ error: 'Failed to fetch conversations' });
  }
});

// Get chess match history
router.get('/matches/:npcId', async (req, res) => {
  try {
    const { npcId } = req.params;
    const db = await getDatabase();
    
    db.all(
      'SELECT * FROM chess_matches WHERE npc_id = ? ORDER BY timestamp DESC',
      [npcId],
      (err, rows) => {
        if (err) {
          console.error('Error fetching matches:', err);
          return res.status(500).json({ error: 'Failed to fetch matches' });
        }

        res.json(rows);
      }
    );
  } catch (error) {
    console.error('Error fetching matches:', error);
    res.status(500).json({ error: 'Failed to fetch matches' });
  }
});

// Add memory
router.post('/memory', async (req, res) => {
  try {
    const { npcId, memoryText, importance } = req.body;

    if (!npcId || !memoryText) {
      return res.status(400).json({ error: 'npcId and memoryText are required' });
    }

    const db = await getDatabase();
    
    db.run(
      'INSERT INTO npc_memories (npc_id, memory_text, importance) VALUES (?, ?, ?)',
      [npcId, memoryText, importance || 5],
      function(err) {
        if (err) {
          console.error('Error saving memory:', err);
          return res.status(500).json({ error: 'Failed to save memory' });
        }

        res.json({ 
          id: this.lastID,
          message: 'Memory saved successfully' 
        });
      }
    );
  } catch (error) {
    console.error('Error saving memory:', error);
    res.status(500).json({ error: 'Failed to save memory' });
  }
});

// Get memories
router.get('/memory/:npcId', async (req, res) => {
  try {
    const { npcId } = req.params;
    const db = await getDatabase();
    
    db.all(
      'SELECT * FROM npc_memories WHERE npc_id = ? ORDER BY importance DESC, timestamp DESC',
      [npcId],
      (err, rows) => {
        if (err) {
          console.error('Error fetching memories:', err);
          return res.status(500).json({ error: 'Failed to fetch memories' });
        }

        res.json(rows);
      }
    );
  } catch (error) {
    console.error('Error fetching memories:', error);
    res.status(500).json({ error: 'Failed to fetch memories' });
  }
});

module.exports = router;
