-- NPCs and Memory
CREATE TABLE IF NOT EXISTS npc_conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  npc_id TEXT NOT NULL,
  role TEXT NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS npc_relationships (
  npc_id TEXT PRIMARY KEY,
  trust_level INTEGER DEFAULT 50,
  respect_level INTEGER DEFAULT 50,
  friendship_level INTEGER DEFAULT 50,
  last_interaction DATETIME
);

CREATE TABLE IF NOT EXISTS chess_matches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  npc_id TEXT,
  player_color TEXT, -- 'white' or 'black'
  result TEXT, -- 'player_won', 'npc_won', 'draw'
  moves INTEGER,
  pgn TEXT,
  notable_moments TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS npc_memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  npc_id TEXT NOT NULL,
  memory_text TEXT NOT NULL,
  importance INTEGER DEFAULT 5, -- 1-10 scale
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Game State
CREATE TABLE IF NOT EXISTS character_data (
  id INTEGER PRIMARY KEY,
  data JSON NOT NULL,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS journal_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  metadata JSON,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
