# 🚀 Getting Started - Quick Guide

## What You Have

✅ **Grand Chess Realms** - Your original tabletop RPG (140+ lore files)
✅ **Chessnut Pro Board** - Connected and working via Bluetooth
✅ **3 Complete Games** - Simple chess, AI opponent, Full RPG
✅ **All Dependencies** - Python, Stockfish, board drivers installed

---

## 5-Minute Quick Start

### Step 1: Test Your Board (30 seconds)

```bash
cd ~/Desktop/Grand-Chess-Realms-RPG
python3 chessnut_board.py
```

- Board should connect
- LEDs will flash (welcome animation)
- Move a piece to test
- Press Ctrl+C to exit

✅ If this works, you're ready!

---

### Step 2: Play Your First Game (5 minutes)

**Simple Chess** - Best for first time:

```bash
python3 chess_game.py
```

1. Board connects with LED animation
2. Make moves on your physical board
3. Terminal shows validation and notation
4. Play until checkmate!

---

### Step 3: Try AI Opponent (10 minutes)

```bash
python3 ai_chess_game.py
```

**Choose:**
- Your color (White or Black)
- AI difficulty (1500 Elo recommended for first try)
- AI personality (Friendly is good to start)

**Then:**
- AI will greet you
- You play on physical board
- AI responds automatically
- AI comments on moves (if LM Studio running)

---

### Step 4: Full RPG Adventure (As long as you want!)

```bash
python3 chess_rpg.py
```

1. Enter your name
2. Start at Castle Lumina
3. Type `help` to see commands
4. Type `npcs` to see who's here
5. Try `talk elara` to meet Princess Elara
6. Challenge NPCs when ready: `challenge elara`

---

## Commands Quick Reference

### Simple Chess Game
- Just move pieces on board
- System validates automatically
- Game saves when done

### AI Chess Game
- You move on board
- AI responds automatically
- Watch for AI comments in terminal

### RPG Game
```
look          - Examine location
npcs          - List characters
talk <npc>    - Talk to someone
challenge <npc> - Start chess battle
status        - Your record
help          - All commands
quit          - Exit
```

---

## What Each Game Does

### 🎮 chess_game.py
**Purpose**: Simple, clean chess
**Perfect For**:
- Testing board
- Practice
- Quick games
- Learning interface

**Features**:
- Move validation
- Check/checkmate detection
- LED hints
- Game saving

---

### 🤖 ai_chess_game.py
**Purpose**: Play vs AI with personality
**Perfect For**:
- Solo practice
- Improving skills
- Fun conversations
- Adaptive difficulty

**Features**:
- Stockfish for moves
- LM Studio for personality
- 4 difficulty levels
- 4 personalities
- AI comments on your play

**Requires**:
- ✅ Stockfish (installed)
- ⚠️ LM Studio (optional, for personality)

---

### 🎭 chess_rpg.py
**Purpose**: Full MUD-style adventure
**Perfect For**:
- Story-driven play
- Meeting characters
- Exploring your world
- Building a campaign

**Features**:
- 12 NPCs from your lore
- AI narrator (Game Master)
- Text-based exploration
- Chess battles with consequences
- Character progression

**Requires**:
- ✅ Stockfish (installed)
- ⚠️ LM Studio (optional, for narration)

---

## LM Studio Setup (Optional)

**Don't have it?** Games still work with fallback dialogue!

**Want it?** Takes 5 minutes:

1. **Download**: [lmstudio.ai](https://lmstudio.ai/)
2. **Install** and open
3. **Download model**:
   - Click "Discover" tab
   - Search "Mistral 7B Instruct"
   - Click download
4. **Load model**:
   - Click on model to load
   - Wait for it to load
5. **Start server**:
   - Go to "Developer" tab
   - Click "Start Server"
   - Wait for "Server running..."

Done! Now your AI has personality.

---

## Common Issues & Fixes

### "Board not found"
```bash
# Check if board is on
# Check Bluetooth enabled (System Settings)
# Restart board
# Run test: python3 test_chessnut_connection.py
```

### "Stockfish not found"
```bash
# Check installation
which stockfish

# Should show: /opt/homebrew/bin/stockfish
# ✅ You have this!
```

### "LM Studio not responding"
```bash
# Is LM Studio open?
# Is server running? (Developer tab → Start Server)
# Is model loaded?

# Don't have it? Games work anyway!
```

### "Moves not detecting"
```bash
# Set up starting position correctly
# Move pieces deliberately (not too fast)
# Wait for LED confirmation
# Try restarting board
```

---

## Recommended Play Order

### First Time:
1. **Test board**: `python3 chessnut_board.py`
2. **Simple game**: `python3 chess_game.py`
3. **AI opponent**: `python3 ai_chess_game.py`
4. **Full RPG**: `python3 chess_rpg.py`

### Regular Play:
- **Quick match**: `chess_game.py`
- **Practice**: `ai_chess_game.py` (with difficulty)
- **Story mode**: `chess_rpg.py` (ongoing campaign)

---

## Tips for Success

### Board Setup
- Arrange pieces in starting position
- Keep board within 1-2 meters of Mac
- Wait for LEDs after each move
- Don't move too fast

### First RPG Session
- Start at Castle Lumina
- Talk to NPCs before challenging
- Try Elder Thomlin first (Elo 1200)
- Work your way up in difficulty
- Use `status` to track progress

### Improving at Chess
- Play AI at your level (not too hard)
- Use Coach personality for hints
- Study your games afterward
- Try different openings
- Practice tactics between sessions

---

## File Reference

| File | What It Does | When To Use |
|------|--------------|-------------|
| `chess_game.py` | Simple chess | Testing, practice |
| `ai_chess_game.py` | AI opponent | Solo play, learning |
| `chess_rpg.py` | Full RPG | Story mode |
| `chessnut_board.py` | Board demo | Testing hardware |
| `test_chessnut_connection.py` | Connection test | Troubleshooting |

---

## Documentation Files

| File | Contains |
|------|----------|
| `README_TERMINAL_EDITION.md` | Complete guide (this is the main one!) |
| `GETTING_STARTED.md` | This quick start guide |
| `BOARD_SETUP.md` | Board connection help |
| `BOARD_SUCCESS.md` | What's working |
| `README.md` | Original tabletop RPG |

---

## Next Steps

### After Your First Game:

1. **Explore the RPG**:
   - Meet all 12 NPCs
   - Try different personalities
   - Build your record
   - Create a story

2. **Add LM Studio**:
   - Download and install
   - Get a model
   - Restart games
   - Enjoy AI personality!

3. **Customize**:
   - Add more NPCs (your 140+ files!)
   - Create new quests
   - Adjust AI difficulty
   - Build your campaign

---

## Having Fun?

**Share your experience:**
- Which NPCs did you battle?
- What's your record?
- Favorite AI personality?
- Coolest game moment?

**Future ideas:**
- More NPCs from your lore
- Quest system
- Tournament mode
- Campaign save/load
- Voice integration

---

## Ready? Let's Play!

```bash
# Start here:
python3 chess_game.py

# Or jump right into the RPG:
python3 chess_rpg.py
```

**Enjoy your Grand Chess Realms adventure!** ♟️

*Questions? Check README_TERMINAL_EDITION.md for the full guide*
