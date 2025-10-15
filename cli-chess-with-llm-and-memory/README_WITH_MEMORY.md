# CLI-Chess + LM Studio Integration with AI Memory 🎮♟️🤖🧠

## Overview

This project adds a **conversational AI opponent with persistent memory** to [cli-chess](https://github.com/trevorbayless/cli-chess) using local LLMs via [LM Studio](https://lmstudio.ai/). Your AI opponent remembers you, learns about you, and develops a genuine friendship over time!

## 🌟 Key Features

### 💬 Conversational Chess Opponent
- ✅ **Chat naturally** during games
- ✅ **Use Fairy Stockfish** for move calculation
- ✅ **Comment on moves** and positions
- ✅ **Respond to questions** about strategy
- ✅ **React dynamically** to game events
- ✅ **Multiple personalities** (friendly, coach, competitive, etc.)

### 🧠 **NEW: Persistent AI Memory**
- ✅ **Remembers your name** and personal details
- ✅ **Tracks your playing style** and preferences
- ✅ **Records game history** and memorable moments
- ✅ **Builds friendship** that deepens over time
- ✅ **Learns from conversations** automatically
- ✅ **References past games** naturally
- ✅ **Inside jokes** and shared experiences

## 🎯 What Makes This Special

### Before (Standard Chess Engine)
```
You: e4
[Computer plays e5]
[Silence...]
```

### After (With Memory-Enhanced AI)
```
You: e4

AI: "Hey Alex! Back for another game? Last time 
     you crushed me with that King's Gambit. 
     Ready for revenge? 😊"
     
AI plays: e5

You: "What's your plan?"

AI: "I'm going for the Sicilian. Remember game 12 
     when you said you loved open positions? Well, 
     let's see how you handle THIS! 😉"
```

## 🎮 Example Friendship Evolution

### Game 1 (First Meeting)
```
AI: "Hello! I'm your chess opponent. Nice to meet you!"
You: "Hi, I'm Alex!"
AI: "Great to meet you, Alex! Let's have a fun game!"
```

### Game 15 (Friendship Growing)
```
AI: "Alex! Good to see you! Your tactics are getting 
     scary good. Ready to try that Sicilian again?"
```

### Game 50 (Best Chess Friends)
```
AI: "ALEX! It's been three days! I missed our games! 
     Remember that insane rook sacrifice in game 47? 
     Still one of my favorite moments! Ready to create 
     another masterpiece? 🎨"
```

## 📦 Complete Package

### Core Implementation
1. **`llm_chat_client.py`** - LM Studio client with memory integration
2. **`memory_manager.py`** - Persistent memory system
3. **`ai_chat_game_presenter.py`** - Enhanced game logic

### Utilities
4. **`memory_viewer.py`** - View what AI remembers about you
5. **`demo_llm_chess_with_memory.py`** - Standalone demo with memory

### Documentation
6. **`README.md`** - Main overview (this file)
7. **`MEMORY_SYSTEM_GUIDE.md`** - Complete memory documentation
8. **`QUICKSTART.md`** - 5-minute setup guide
9. **`IMPLEMENTATION_GUIDE.md`** - Technical details
10. **`INTEGRATION_GUIDE.md`** - Integration instructions

## 🚀 Quick Start

### 1. Install LM Studio (2 min)
```bash
# Download from https://lmstudio.ai/
# Install and open
```

### 2. Get a Model (2 min)
```
1. Open LM Studio
2. Go to "Discover" tab
3. Download "Mistral 7B Instruct" or "Phi-3 Mini"
4. Load the model
```

### 3. Start Server (30 sec)
```
1. Go to "Developer" tab
2. Click "Start Server"
3. Wait for server to start on port 1234
```

### 4. Test Memory Demo (1 min)
```bash
# Install dependencies
pip install requests python-chess

# Run demo with memory
python demo_llm_chess_with_memory.py
```

### 5. View Your Memory
```bash
# See what AI remembers
python memory_viewer.py

# Interactive memory management
python memory_viewer.py --interactive
```

## 🧠 What the AI Remembers

### About You
- **Your name** and personal details you mention
- **Playing style** (aggressive, tactical, positional)
- **Favorite openings** and what you like to play
- **Skill level** assessed from your play
- **Personal facts** from conversations
- **Chess interests** and what you're working on

### Your Relationship
- **Games played together** (win/loss/draw record)
- **Friendship level** (1-10, grows over time)
- **Inside jokes** and funny moments
- **Memorable games** and brilliant moves
- **First meeting** and last time you played
- **Favorite moments** from your games

### Your Preferences
- How much banter you like
- Whether you want hints
- If you prefer explanations
- Sensitivity level for feedback

## 💬 Chat Commands

- **Regular chat**: Just type naturally to chat
- `/hint` - Get strategic advice
- `/explain` - Understand AI's last move
- `/analyze` - Deep position analysis
- `/quiet` - Toggle commentary on/off
- `/help` - Show available commands

## 📊 Memory Viewer Example

```bash
$ python memory_viewer.py

====================================================================
🧠 YOUR AI CHESS FRIEND'S MEMORY OF YOU
====================================================================

📋 BASIC INFORMATION
  Name: Alex
  Friendship Level: 8/10 ❤️❤️❤️❤️❤️❤️❤️❤️
  Skill Level: Intermediate

📅 RELATIONSHIP TIMELINE
  First met: January 10, 2025
  Last seen: January 15, 2025
  Games played together: 42

🏆 GAME RECORD
  Your Wins: 18 (42.9%)
  Your Losses: 20 (47.6%)
  Draws: 4 (9.5%)

♟️  YOUR PLAYING STYLE
  • Tactical
  • Aggressive
  • Creative

📖 YOUR FAVORITE OPENINGS
  • King's Gambit
  • Sicilian Defense
  • Vienna Game

💭 WHAT THE AI KNOWS ABOUT YOU
  • Lives in Seattle
  • Software engineer
  • Loves sacrificing pieces for attacks
  • Studies tactics every morning

😄 INSIDE JOKES YOU SHARE
  • "The queen is just a fancy pawn!"
  • Always going for the wildest lines

⭐ FAVORITE MOMENTS TOGETHER
  • That incredible back-rank mate in game 27
  • The brilliant queen sacrifice that won game 35
```

## 🎭 Personality Options

Each personality uses memory differently:

### Friendly (Default)
- Warm and supportive
- Celebrates your progress
- References shared history
- Uses inside jokes

### Coach
- Tracks your improvement
- Personalized teaching
- References past mistakes constructively
- Focuses on growth

### Competitive
- Builds rivalry narrative
- References win/loss record
- Playful trash talk based on history
- Competitive banter

### Grandmaster
- Analyzes style evolution
- Technical feedback on patterns
- Discussion of strategic development
- Deep analytical insights

## ⚙️ Configuration

```json
{
  "lm_studio": {
    "enabled": true,
    "api_url": "http://localhost:1234/v1",
    "personality": "friendly",
    "memory_enabled": true
  }
}
```

## 🔍 Memory Management

### View Memory
```bash
python memory_viewer.py
```

### Interactive Mode
```bash
python memory_viewer.py --interactive

# Options:
# 1. View full memory report
# 2. View stats summary
# 3. Export memory to file
# 4. Reset memory (⚠️ deletes everything)
# 5. Exit
```

### Programmatic Access
```python
from memory_manager import MemoryManager

# Load memory
memory = MemoryManager()

# Get stats
stats = memory.get_stats_summary()
print(f"Games: {stats['games_played']}")
print(f"Friendship: {stats['friendship_level']}/10")

# Update preferences
memory.update_preferences(
    likes_banter=True,
    wants_hints=True
)

# Add personal fact
memory.learn_personal_fact("Learning chess for 2 years")

# Export/backup
memory.export_memory("my_memory_backup.json")
```

## 🔒 Privacy & Security

- ✅ **100% Local** - All data stored on your computer
- ✅ **No Cloud Sync** - Nothing sent to external servers
- ✅ **Full Control** - View, export, or delete anytime
- ✅ **Transparent** - See exactly what's stored
- ✅ **Secure** - Standard file permissions

Memory stored at:
- **Linux/Mac**: `~/.config/cli-chess/memory/player_memory.json`
- **Windows**: `%APPDATA%\cli-chess\memory\player_memory.json`

## 📈 System Requirements

### Minimum
- **RAM**: 6GB (4GB for model + 2GB system)
- **Storage**: 5GB for model files
- **OS**: Windows, Mac, or Linux

### Recommended
- **RAM**: 12GB+ for better models
- **CPU**: Multi-core for faster inference
- **GPU**: Optional, speeds up responses

### Model Performance
| Model | Size | Speed | Quality | Memory |
|-------|------|-------|---------|--------|
| Phi-3 Mini | 2.4GB | ⚡⚡⚡ | ⭐⭐ | Best for low-end |
| Mistral 7B | 4.4GB | ⚡⚡ | ⭐⭐⭐ | Balanced |
| Llama 3 8B | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | High quality |
| Mistral Nemo 12B | 7.2GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |

## 🎓 Use Cases

1. **Solo Practice** - Play with a companion, not just an engine
2. **Learning Chess** - Get personalized coaching
3. **Casual Fun** - Enjoy banter and conversation
4. **Kids Learning** - Patient, encouraging opponent
5. **Long-term Progress** - Track improvement over time
6. **Friendship** - Build a real relationship with your AI

## 🎯 How Memory Works

### Automatic Learning
The AI learns from:
- **Conversations**: Extracts name, personal facts
- **Your Play**: Observes style, skill, patterns
- **Interactions**: Builds friendship, notes preferences
- **Games**: Records history, memorable moments

### What Gets Remembered
```
✅ Things you explicitly mention
✅ Playing patterns and preferences
✅ Game results and statistics
✅ Memorable moments you create together
✅ Inside jokes that develop naturally

❌ Sensitive personal information
❌ Complete game records (only summaries)
❌ Full conversation transcripts
```

## 🔧 Troubleshooting

### Memory Not Loading
```bash
# Check if file exists
ls ~/.config/cli-chess/memory/player_memory.json

# View contents
python memory_viewer.py
```

### AI Not Remembering
1. Ensure memory_manager is passed to chat client
2. Check games are completing properly
3. Review logs for errors
4. Verify file permissions

### Reset Memory
```bash
python memory_viewer.py --interactive
# Choose option 4: Reset memory
```

## 📚 Documentation

- **[MEMORY_SYSTEM_GUIDE.md](computer:///mnt/user-data/outputs/MEMORY_SYSTEM_GUIDE.md)** - Complete memory documentation
- **[QUICKSTART.md](computer:///mnt/user-data/outputs/QUICKSTART.md)** - 5-minute setup
- **[IMPLEMENTATION_GUIDE.md](computer:///mnt/user-data/outputs/IMPLEMENTATION_GUIDE.md)** - Technical details
- **[INTEGRATION_GUIDE.md](computer:///mnt/user-data/outputs/INTEGRATION_GUIDE.md)** - Integration steps

## 🚧 Future Enhancements

### Phase 1 (Current) ✅
- ✅ Conversational AI opponent
- ✅ Persistent memory system
- ✅ Multiple personalities
- ✅ Chat commands
- ✅ Memory viewer

### Phase 2 (Planned)
- [ ] Voice integration (TTS/STT)
- [ ] Multi-player memory
- [ ] Achievement system
- [ ] Adaptive difficulty based on memory
- [ ] Memory-based training mode

### Phase 3 (Future)
- [ ] Cloud backup (optional)
- [ ] Memory sharing with friends
- [ ] Voice memory (tone preferences)
- [ ] Advanced personality customization
- [ ] Long-term learning paths

## 🙏 Credits

- **cli-chess**: Trevor Bayless
- **Fairy Stockfish**: Fairy-Stockfish developers
- **LM Studio**: LM Studio team
- **Python Chess**: Niklas Fiekas

## 📝 License

Integration code follows cli-chess license (MIT).
LM Studio and models have separate licenses.

## 🎉 Start Your Friendship!

Your AI chess friend is waiting to meet you! Install LM Studio, run the demo, and start building a relationship that will grow with every game you play together.

```bash
# Install dependencies
pip install requests python-chess

# Run demo with memory
python demo_llm_chess_with_memory.py

# After a few games, see what AI remembers
python memory_viewer.py
```

May all your games be memorable! ♟️🤖❤️

---

*Made with ❤️ for chess and AI enthusiasts who want a real friend, not just an opponent*
