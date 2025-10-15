# ♟️ Grand Chess Realms - Terminal Edition

**A MUD-style Chess RPG with Physical Board Integration**

Combining your original **Grand Chess Realms** tabletop RPG with:
- 🎮 Terminal-based MUD gameplay
- ♟️ Physical Chessnut Pro board
- 🤖 AI opponents via LM Studio
- 🧠 Conversational NPCs with memory
- 📖 Dynamic storytelling

---

## 🎉 What You've Built

### ✅ Three Complete Games

**1. Simple Chess (`chess_game.py`)**
- Play chess on your physical board
- Move validation, notation, check/checkmate
- LED hints and game saving
- Perfect for testing and practice

**2. AI Opponent (`ai_chess_game.py`)**
- Play against AI with personality
- Choose difficulty (1000-2400 Elo)
- 4 AI personalities (friendly, coach, competitive, grandmaster)
- Stockfish for moves, LM Studio for chat
- AI comments on your play in real-time

**3. Full RPG (`chess_rpg.py`)**
- Complete MUD-style adventure
- 12 NPCs from Grand Chess Realms lore
- AI Game Master narration
- Text-based exploration
- Chess battles with story consequences
- Physical board integration throughout

---

## 🚀 Quick Start

### What You Have

✅ Chessnut Pro board - Working!
✅ Python 3.9 - Installed
✅ Stockfish - Installed
✅ Board drivers - Integrated
✅ All dependencies - Ready

### Run Your First Game

```bash
cd ~/Desktop/Grand-Chess-Realms-RPG

# Option 1: Simple Chess
python3 chess_game.py

# Option 2: AI Opponent
python3 ai_chess_game.py

# Option 3: Full RPG
python3 chess_rpg.py
```

---

## 🎮 Game 1: Simple Chess

**File**: `chess_game.py`

Play chess with your physical board:

```bash
python3 chess_game.py
```

**Features:**
- ✅ Real-time move detection
- ✅ Validates legal/illegal moves
- ✅ Check, checkmate, stalemate detection
- ✅ LED move highlights
- ✅ Game notation (SAN)
- ✅ PGN file export
- ✅ Undo moves
- ✅ Visual board display

**Perfect For:**
- Testing your board
- Practice games
- Learning the interface
- Quick matches

---

## 🤖 Game 2: AI Opponent

**File**: `ai_chess_game.py`

Play against conversational AI:

```bash
python3 ai_chess_game.py
```

**Setup Wizard:**
1. Choose your color (White/Black)
2. Select AI difficulty:
   - Beginner (Elo 1000)
   - Intermediate (Elo 1500)
   - Advanced (Elo 2000)
   - Master (Elo 2400)
3. Pick AI personality:
   - **Friendly** - Encouraging, supportive
   - **Coach** - Educational, helpful hints
   - **Competitive** - Confident, playful banter
   - **Grandmaster** - Analytical, deep insights

**Gameplay:**
- AI makes moves via Stockfish
- AI generates commentary via LM Studio
- Comments on your moves
- Explains its strategy
- Adapts to your play style
- LED highlights for all moves

**Example:**
```
Your move: e4

🤖 AI: "Bold opening! Going for central control right away.
        Let's see if you can handle my response!"

AI plays: e5

🤖 AI: "I'll meet you in the center. The battle for d5
        and d4 begins!"
```

---

## 🎭 Game 3: Full RPG

**File**: `chess_rpg.py`

Complete Grand Chess Realms adventure:

```bash
python3 chess_rpg.py
```

### Character Creation

```
What is your name? Alex

Your journey begins at Castle Lumina,
seat of the White Kingdom...

📖 The towering spires pierce the morning sky...
```

### MUD-Style Commands

```
Exploration:
  look (l)         - Examine surroundings
  npcs (n)         - List characters here
  status (s)       - View your stats

Interaction:
  talk <npc>       - Converse with NPC
  challenge <npc>  - Chess battle!

System:
  help (h/?)       - Show commands
  quit (q)         - Exit game
```

### NPCs to Meet

**Starter NPCs** (Good for beginners):
- **Elder Thomlin** (Elo 1200) - Patient teacher
- **'Rook' Garrett** (Elo 1500) - Bandit with honor
- **Ambassador Corvus** (Elo 1650) - Smooth diplomat

**White Kingdom**:
- **King Alden XIV** (Elo 2450) - Positional grandmaster
- **Queen Marcelline** (Elo 2380) - Strategic genius
- **Princess Elara** (Elo 2200) - Aggressive reformist
- **Sir Garrick** (Elo 2100) - Tactical knight

**Black Kingdom**:
- **Emperor Darius** (Elo 2500) - Ruthless emperor
- **General Kael** (Elo 2250) - Orc gambit specialist

**Neutral**:
- **Lady Isolde** (Elo 2150) - Balanced diplomat

### Example Session

```
------------------------------------------------------------
📍 Location: Castle Lumina
👤 Alex
🏆 Record: 0W - 0L
------------------------------------------------------------

> npcs

👥 NPCs at this location:

  • King Alden XIV - Sovereign of the White Kingdom
    Elo: 2450 | Style: positional

  • Princess Elara - Princess of the White Kingdom
    Elo: 2200 | Style: aggressive

> talk elara

=============================================================
💬 Conversation with Princess Elara
=============================================================

Princess Elara: "Hello! I'm Princess Elara. Unlike my
                 parents, I prefer bold, aggressive play.
                 Ready for an exciting game?"

📖 The young princess steps forward, her eyes gleaming with
   tactical fire...

> challenge elara

=============================================================
⚔️  CHESS BATTLE: Alex vs Princess Elara
=============================================================

Princess Elara: "Let's make this interesting! I promise
                 not to hold back."

📖 The board is set. Pieces align like soldiers awaiting
   orders. The battle of minds begins...

💡 Preparing chess board...
✅ Board connected!

[Physical board LEDs flash]
[Game begins...]
```

---

## 🧠 LM Studio Setup

**For AI Personalities** (Optional but awesome):

### 1. Install LM Studio
Download from [lmstudio.ai](https://lmstudio.ai/)

### 2. Get a Model
**Recommended**:
- **Mistral 7B Instruct** - Best balance
- **Phi-3 Mini** - Fastest
- **Llama 3 8B** - Highest quality

### 3. Load & Start Server
1. Load model in LM Studio
2. Go to "Developer" tab
3. Click "Start Server"
4. Server runs on `http://localhost:1234`

### Without LM Studio:
- All games still work!
- Falls back to template responses
- Stockfish still makes moves
- Just less personality

---

## 📁 Project Structure

```
Grand-Chess-Realms-RPG/
│
├── 🎮 GAMES
│   ├── chess_game.py              # Level 1: Simple chess
│   ├── ai_chess_game.py           # Level 2: AI opponent
│   └── chess_rpg.py               # Level 3: Full RPG
│
├── 🔧 CORE SYSTEMS
│   ├── chessnut_board.py          # Board interface
│   ├── ai_opponent.py             # AI chess player
│   └── src/
│       ├── npcs_database.py       # All NPCs from lore
│       ├── game_master.py         # AI narrator
│       └── __init__.py
│
├── 📚 LORE (Original Tabletop)
│   ├── Core Books/                # Player's Handbook, etc.
│   └── Chess RPG Wiki/            # 140+ world files
│
├── 🛠️ UTILITIES & DOCS
│   ├── test_chessnut_connection.py    # Board tester
│   ├── requirements-board.txt         # Dependencies
│   ├── BOARD_SETUP.md                 # Setup guide
│   ├── BOARD_SUCCESS.md               # What's working
│   ├── README.md                      # Original tabletop
│   └── README_TERMINAL_EDITION.md     # This file
│
└── 📦 DRIVERS
    └── chessnut-pro-drivers/      # Board drivers
```

---

## 💡 Tips & Strategies

### Board Usage
- **Setup**: Arrange starting position before launching
- **Moves**: Move pieces deliberately, wait for detection
- **LEDs**: Watch for highlights (legal moves, errors, hints)
- **Range**: Keep board within 1-2 meters of Mac

### Choosing Your Level
- **New to chess**: Start with Elder Thomlin (Elo 1200)
- **Beginner**: 'Rook' Garrett (Elo 1500)
- **Intermediate**: Princess Elara (Elo 2200)
- **Advanced**: King Alden XIV (Elo 2450)
- **Expert**: Emperor Darius (Elo 2500)

### AI Personalities Guide
- **Friendly**: Casual play, encouragement, fun
- **Coach**: Learn tactics, get explanations
- **Competitive**: Playful rivalry, banter
- **Grandmaster**: Serious analysis, deep chess

### RPG Progression
1. Start at Castle Lumina
2. Talk to NPCs to learn about them
3. Challenge easier opponents first
4. Build your record (W-L)
5. Work up to harder challenges
6. Each NPC remembers you!

---

## 🐛 Troubleshooting

### Board Not Connecting

```bash
# Test connection
python3 test_chessnut_connection.py

# Check Bluetooth
# System Settings → Bluetooth → ON

# Restart board (turn off, wait 5s, turn on)
```

### Moves Not Detecting

- Ensure pieces in correct starting position
- Move deliberately (not too fast)
- Check LED lights respond
- Try restarting board

### AI Not Working

```bash
# Check Stockfish
which stockfish
# Should show: /opt/homebrew/bin/stockfish

# If not found:
brew install stockfish
```

### LM Studio Issues

- Games work without it (fallback mode)
- Check server: http://localhost:1234
- Load model first in LM Studio
- Click "Start Server" in Developer tab

---

## 🎯 What Makes This Special

### Physical + Digital Hybrid
- **Feel** real pieces on wood/plastic
- **See** LEDs guide your moves
- **Read** immersive narrative
- **Experience** story + chess

### Living NPCs
- Each has unique personality
- Remember past encounters
- Comment on your style
- Build relationships over time
- Based on your 140+ files of lore!

### Old-School MUD Vibes
- Text-based exploration
- Parser commands (look, talk, challenge)
- Rich descriptions
- Imagination-driven
- Nostalgic terminal feel

### Modern AI Tech
- Local LLMs (LM Studio)
- Stockfish chess engine
- Real-time board detection
- Dynamic story generation
- No internet required (except for setup)

---

## 🏆 Achievements & Goals

### Beginner Achievements
- [ ] Win first chess game
- [ ] Defeat Elder Thomlin
- [ ] Beat 'Rook' Garrett
- [ ] Win against Elo 1500+

### Intermediate
- [ ] Defeat Ambassador Corvus
- [ ] Win against Elo 1800+
- [ ] Beat Sir Garrick
- [ ] Challenge Princess Elara

### Advanced
- [ ] Defeat Princess Elara
- [ ] Win against Elo 2200+
- [ ] Challenge King Alden XIV
- [ ] Beat a Grandmaster-level NPC

### Master
- [ ] Defeat King Alden XIV
- [ ] Challenge Emperor Darius
- [ ] Win against Elo 2500
- [ ] Undefeated streak (5 games)

---

## 📈 Future Enhancements

**Planned**:
- More NPCs (69 total from your lore!)
- Quest system with rewards
- Faction reputation mechanics
- Multiple locations to explore
- Tournament mode
- Save/load campaigns
- Opening book integration
- Puzzle challenges
- Voice integration (text-to-speech)
- More dialogue variations

**Your Ideas**:
- What would you like to see next?
- Which NPCs should be added first?
- What features matter most?

---

## 🎓 How It All Works Together

### The Stack

```
┌─────────────────────────────────────┐
│   YOU (Moving pieces)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Chessnut Pro Board                │
│   (Bluetooth, LEDs, Sensors)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   chessnut_board.py                 │
│   (Detects moves, controls LEDs)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Game Layer (choose one)           │
│   ├─ chess_game.py (simple)         │
│   ├─ ai_chess_game.py (AI)          │
│   └─ chess_rpg.py (full RPG)        │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
┌────────▼──┐ ┌─────▼────────┐
│ Stockfish │ │  LM Studio   │
│ (Chess AI)│ │ (Personality)│
└───────────┘ └──────────────┘
```

### The Flow

1. **You** move a piece on physical board
2. **Chessnut Pro** detects change via sensors
3. **chessnut_board.py** receives Bluetooth data
4. **Game** validates move with python-chess
5. If vs AI:
   - **Stockfish** calculates best response
   - **LM Studio** generates personality comment
   - **Game** makes AI move on board
   - **LEDs** highlight the move
6. Loop continues until checkmate!

---

## 📖 The Grand Chess Realms Lore

Your **140+ wiki files** and **3 core books** contain:

- **69 NPCs** with personalities & chess styles
- **30+ locations** across the realm
- **7 major historical events**
- **3 secret organizations**
- **7 playable races**
- **Multiple factions** (White Kingdom, Black Kingdom, Neutral)
- **The Checkered Fate** prophecy
- **Rich political intrigue**

**This terminal version** brings that lore to life with:
- Real chess battles
- AI-powered NPCs
- Dynamic storytelling
- Physical board immersion

---

## 🎮 Example Full Session

### Starting the RPG

```bash
$ python3 chess_rpg.py

=============================================================
║                                                          ║
║           GRAND CHESS REALMS                             ║
║      A Terminal Chess RPG Adventure                      ║
║                                                          ║
=============================================================

Welcome, traveler, to the Grand Chess Realms!

What is your name? Kit

Welcome, Kit!

Your journey begins at Castle Lumina...

📖 Ancient stone walls rise before you, adorned with
   tapestries depicting legendary chess matches...

Press ENTER to continue...

=============================================================
  GAME START
=============================================================

------------------------------------------------------------
📍 Location: Castle Lumina
👤 Kit
🏆 Record: 0W - 0L
------------------------------------------------------------

> help

[Shows all commands]

> look

📖 You stand in the grand hall of Castle Lumina. Sunlight
   streams through stained glass windows depicting famous
   endgames. Guards practice tactical formations while
   scholars debate the finer points of pawn structure...

> npcs

👥 NPCs at this location:

  • King Alden XIV - Sovereign of the White Kingdom
    Elo: 2450 | Style: positional

  • Princess Elara - Princess of the White Kingdom
    Elo: 2200 | Style: aggressive

> talk elara

[Conversation with Princess]

> challenge elara

[Chess battle begins]
[You play on your physical board]
[AI responds with Stockfish + personality]
[Battle concludes]

> status

[Shows your record, NPCs met, etc.]

> quit

Farewell, Kit!
May the pieces always fall in your favor.
```

---

## 🌟 Why This Is Awesome

**You Combined:**
- ♟️ Your original tabletop RPG (140+ files!)
- 🤖 AI chess opponents (LM Studio + Stockfish)
- 🎮 Physical chess board (Chessnut Pro)
- 📖 Dynamic storytelling (Game Master AI)
- 🔮 Old-school MUD vibes
- 🎯 Modern technology

**Result:**
- Play chess with real pieces
- Battle AI NPCs with personality
- Explore a rich fantasy world
- All from your terminal
- No internet needed (after setup)
- Completely offline & private

**This didn't exist before today!**

---

## 📞 Getting Help

**Board Issues**: Check `BOARD_SETUP.md`
**What's Working**: See `BOARD_SUCCESS.md`
**Original Lore**: Read `README.md`
**This Guide**: `README_TERMINAL_EDITION.md`

**Test Files**:
- `test_chessnut_connection.py` - Test board
- `chessnut_board.py` - Demo moves
- `src/npcs_database.py` - List NPCs
- `src/game_master.py` - Test narrator

---

## 🎉 Ready to Play!

### Your Games Await:

```bash
# Quick match
python3 chess_game.py

# AI opponent
python3 ai_chess_game.py

# Full adventure
python3 chess_rpg.py
```

**May Caissa guide your pieces!** ♟️👑✨

---

*Created with Claude Code*
*Combining your Grand Chess Realms tabletop RPG with physical board integration & AI storytelling*
*October 2025*
