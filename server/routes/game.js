const express = require('express');
const { getDatabase } = require('../db/database');

const router = express.Router();

// Save chess match
router.post('/chess-match', async (req, res) => {
  try {
    const { npcId, playerColor, result, moves, pgn, notableMoments } = req.body;

    const db = await getDatabase();
    
    db.run(
      'INSERT INTO chess_matches (npc_id, player_color, result, moves, pgn, notable_moments) VALUES (?, ?, ?, ?, ?, ?)',
      [npcId, playerColor, result, moves, pgn, notableMoments],
      function(err) {
        if (err) {
          console.error('Error saving chess match:', err);
          return res.status(500).json({ error: 'Failed to save chess match' });
        }

        // Update relationship based on result
        updateRelationship(db, npcId, result);

        res.json({ 
          id: this.lastID,
          message: 'Chess match saved successfully' 
        });
      }
    );
  } catch (error) {
    console.error('Error saving chess match:', error);
    res.status(500).json({ error: 'Failed to save chess match' });
  }
});

// Get character data
router.get('/character', async (req, res) => {
  try {
    const db = await getDatabase();
    
    db.get('SELECT data FROM character_data WHERE id = 1', (err, row) => {
      if (err) {
        console.error('Error fetching character:', err);
        return res.status(500).json({ error: 'Failed to fetch character data' });
      }

      if (!row) {
        return res.json(null);
      }

      res.json(JSON.parse(row.data));
    });
  } catch (error) {
    console.error('Error fetching character:', error);
    res.status(500).json({ error: 'Failed to fetch character data' });
  }
});

// Save character data
router.post('/character', async (req, res) => {
  try {
    const characterData = req.body;
    const db = await getDatabase();
    
    db.run(
      'INSERT OR REPLACE INTO character_data (id, data, updated_at) VALUES (1, ?, CURRENT_TIMESTAMP)',
      [JSON.stringify(characterData)],
      (err) => {
        if (err) {
          console.error('Error saving character:', err);
          return res.status(500).json({ error: 'Failed to save character data' });
        }

        res.json({ message: 'Character saved successfully' });
      }
    );
  } catch (error) {
    console.error('Error saving character:', error);
    res.status(500).json({ error: 'Failed to save character data' });
  }
});

// Save journal entry
router.post('/journal', async (req, res) => {
  try {
    const { content, metadata } = req.body;
    const db = await getDatabase();
    
    db.run(
      'INSERT INTO journal_entries (content, metadata) VALUES (?, ?)',
      [content, JSON.stringify(metadata || {})],
      function(err) {
        if (err) {
          console.error('Error saving journal entry:', err);
          return res.status(500).json({ error: 'Failed to save journal entry' });
        }

        res.json({ 
          id: this.lastID,
          message: 'Journal entry saved successfully' 
        });
      }
    );
  } catch (error) {
    console.error('Error saving journal entry:', error);
    res.status(500).json({ error: 'Failed to save journal entry' });
  }
});

// Get journal entries
router.get('/journal', async (req, res) => {
  try {
    const db = await getDatabase();
    
    db.all(
      'SELECT * FROM journal_entries ORDER BY timestamp DESC',
      (err, rows) => {
        if (err) {
          console.error('Error fetching journal entries:', err);
          return res.status(500).json({ error: 'Failed to fetch journal entries' });
        }

        const entries = rows.map(row => ({
          id: row.id,
          content: row.content,
          metadata: JSON.parse(row.metadata || '{}'),
          timestamp: row.timestamp
        }));

        res.json(entries);
      }
    );
  } catch (error) {
    console.error('Error fetching journal entries:', error);
    res.status(500).json({ error: 'Failed to fetch journal entries' });
  }
});

// Helper function to update relationship
function updateRelationship(db, npcId, result) {
  db.get(
    'SELECT * FROM npc_relationships WHERE npc_id = ?',
    [npcId],
    (err, row) => {
      if (err) {
        console.error('Error fetching relationship:', err);
        return;
      }

      let trust = row ? row.trust_level : 50;
      let respect = row ? row.respect_level : 50;
      let friendship = row ? row.friendship_level : 50;

      // Adjust based on result
      if (result === 'player_won') {
        respect += 5;
        friendship += 2;
      } else if (result === 'npc_won') {
        respect -= 2;
        friendship += 1;
      } else if (result === 'draw') {
        respect += 2;
        friendship += 3;
      }

      // Clamp values
      trust = Math.max(0, Math.min(100, trust));
      respect = Math.max(0, Math.min(100, respect));
      friendship = Math.max(0, Math.min(100, friendship));

      db.run(
        'INSERT OR REPLACE INTO npc_relationships (npc_id, trust_level, respect_level, friendship_level, last_interaction) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)',
        [npcId, trust, respect, friendship],
        (err) => {
          if (err) {
            console.error('Error updating relationship:', err);
          }
        }
      );
    }
  );
}

module.exports = router;
