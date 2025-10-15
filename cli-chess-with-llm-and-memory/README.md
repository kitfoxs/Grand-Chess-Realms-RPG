# CLI-Chess + LM Studio Integration 🎮♟️🤖

## Overview

This project adds **conversational AI opponent** capabilities to [cli-chess](https://github.com/trevorbayless/cli-chess) using local LLMs via [LM Studio](https://lmstudio.ai/). The AI opponent can:

- ✅ **Chat naturally** during games
- ✅ **Use Fairy Stockfish** for move calculation
- ✅ **Comment on moves** and positions
- ✅ **Respond to questions** about strategy
- ✅ **React dynamically** to game events
- ✅ **Multiple personalities** (friendly, coach, competitive, etc.)

## 🎯 Key Features

### Conversational Chess Opponent
The AI acts as your chess buddy, not just a silent engine. It:
- Greets you at game start
- Comments on interesting moves (yours and its own)
- Responds to chat messages during the game
- Explains strategy when asked
- Reacts to game endings

### Chat Commands
- **Regular chat**: Just type naturally
- `/hint` - Get strategic advice
- `/explain` - Understand AI's last move
- `/analyze` - Deep position analysis
- `/quiet` - Toggle move commentary
- `/help` - Show available commands

### Smart Integration
- **Non-blocking**: Chat doesn't freeze the game
- **Context-aware**: AI knows board state, move history
- **Efficient**: Uses local LLM (privacy + speed)
- **Fallback**: Works without LLM if unavailable

## 📦 What's Included

### Core Files
1. **`llm_chat_client.py`** - LM Studio API client
   - Handles all LLM communication
   - Manages conversation history
   - Provides different personalities
   - Error handling and fallbacks

2. **`ai_chat_game_presenter.py`** - Enhanced game logic
   - Extends standard offline game
   - Coordinates chess + chat
   - Implements chat commands
   - Async commentary system

### Documentation
3. **`IMPLEMENTATION_GUIDE.md`** - Full technical guide
   - Architecture overview
   - Step-by-step integration
   - Configuration options
   - Troubleshooting

4. **`INTEGRATION_GUIDE.md`** - Practical integration
   - Quick start
   - Code flow examples
   - Testing checklist
   - Performance tuning

5. **`demo_llm_chess.py`** - Standalone demo
   - Test without full cli-chess
   - Simple game loop
   - Shows core concepts
   - Verify setup

## 🚀 Quick Start

### 1. Install LM Studio
```bash
# Download from https://lmstudio.ai/
# Install and open LM Studio
```

### 2. Set Up Model
```
1. In LM Studio, go to "Discover" tab
2. Download a model (recommended):
   - Mistral 7B Instruct
   - Phi-3 Mini (faster)
   - Llama 3 8B (better)
3. Load the model (click on it)
4. Go to "Developer" tab
5. Click "Start Server"
6. Server starts on http://localhost:1234
```

### 3. Test Setup
```bash
# Install dependencies
pip install requests openai python-chess

# Test connection
curl http://localhost:1234/v1/models

# Run standalone demo
python demo_llm_chess.py
```

### 4. Integrate with CLI-Chess

```bash
# Copy files to cli-chess installation
cp llm_chat_client.py /path/to/cli-chess/src/cli_chess/modules/llm_chat/
cp ai_chat_game_presenter.py /path/to/cli-chess/src/cli_chess/core/game/offline_game/

# Add configuration
cat >> ~/.config/cli-chess/config.json << EOF
{
  "lm_studio": {
    "enabled": true,
    "api_url": "http://localhost:1234/v1",
    "personality": "friendly"
  }
}
EOF

# Update menu to add new option (see INTEGRATION_GUIDE.md)
```

## 💡 How It Works

```
┌──────────────────────────────────────────────┐
│                   USER                       │
│  Makes moves + Chats with AI                 │
└──────────────────┬───────────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
    ▼                             ▼
┌─────────────────┐    ┌──────────────────────┐
│ Chess Engine    │    │  LLM (via LM Studio) │
│ (Fairy Stockfish│    │  - Conversation      │
│  calculates     │    │  - Commentary        │
│  best moves)    │    │  - Analysis          │
└─────────────────┘    └──────────────────────┘
    │                             │
    └──────────────┬──────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         AI Chat Game Presenter               │
│  - Coordinates both systems                  │
│  - Manages game flow                         │
│  - Provides context to LLM                   │
└──────────────────────────────────────────────┘
```

### Example Game Flow

```python
# Game starts
AI: "Hey! Ready for a game? I'm playing Black. Good luck! 👋"

# User plays
You: e4

AI: "Strong opening! I'll meet you in the center."
AI plays: e5

# User chats
You: "What's your plan?"

AI: "I'm aiming for quick development and center control. 
Watch out for my knight coming to f6!"

# Later in game
You: Nxe5 (tactical shot)

AI: "Ouch! Didn't see that coming. Nice tactic! 😅
I'll have to recapture with my pawn."

# User asks for help
You: /hint

AI: "Look at your bishop on c4. It's pointing at f7, and your 
knight on e5 can support. There might be a tactical blow there!"

# Game ends
Result: 1-0 (You win by checkmate)

AI: "Great game! That kingside attack was really strong. 
I should have castled earlier. Want a rematch?"
```

## ⚙️ Configuration

### Basic Config (`~/.config/cli-chess/config.json`)
```json
{
  "lm_studio": {
    "enabled": true,
    "api_url": "http://localhost:1234/v1",
    "model": "local-model",
    "personality": "friendly",
    "max_tokens": 150,
    "temperature": 0.7
  }
}
```

### Personality Options
- **friendly**: Casual, encouraging chess buddy
- **coach**: Educational, explains concepts
- **competitive**: Playful trash talk
- **grandmaster**: Serious, technical analysis
- **beginner**: Learning together

### Performance Tuning

**Fast Setup (Low-end hardware)**
```json
{
  "lm_studio": {
    "model": "phi-3-mini-4k-Q4",  // ~2GB model
    "max_tokens": 100,
    "commentary_frequency": "low"
  }
}
```

**Quality Setup (Good hardware)**
```json
{
  "lm_studio": {
    "model": "mistral-nemo-12b-Q4",  // ~7GB model
    "max_tokens": 200,
    "temperature": 0.8
  }
}
```

## 🎓 Example Sessions

### Learning Session (Coach Personality)
```
AI: "Hello! I'm here to help you improve. Let's have a good game!"

You: e4
AI: "Classic king's pawn opening! This controls the center and opens 
lines for your pieces. I'll respond with e5."

You: Bc4
AI: "The Italian Game! This targets f7, which is Black's weak square. 
I'll defend with Nc6."

You: /explain
AI: "I played Nc6 to develop my knight and defend the e5 pawn. It also 
prepares to challenge your center with d7-d5 later."
```

### Competitive Session (Competitive Personality)
```
AI: "Let's see what you got! I'm ready to crush... I mean, play! 😎"

You: e4
AI: "Oh, the king's pawn? Classic. Don't worry, I've seen it before. e5!"

You: Nf3
AI: "Developing knights before bishops, nice. I'll do the same. Nc6!"

[Later, after a blunder]
You: Qxd4
AI: "WHAT?! Okay, I walked into that one. Fine, you got me there. 
But this game isn't over! 😤"

[After winning]
AI: "Alright alright, nice game. That tactic on move 15 was sneaky. 
Rematch? I'll get you next time!"
```

## 🔧 Troubleshooting

### LM Studio Won't Connect
```bash
# Check if server is running
curl http://localhost:1234/v1/models

# If fails:
1. Open LM Studio
2. Go to Developer tab
3. Click "Start Server"
4. Wait for "Server started" message
```

### Slow Responses
```
Solutions:
- Use smaller model (Phi-3 Mini)
- Reduce max_tokens to 100
- Use /quiet to disable commentary
- Close other applications
- Try GPU acceleration in LM Studio
```

### AI Seems Confused
```
Fixes:
- Ensure latest LM Studio version
- Try different model
- Check system prompt in code
- Verify context is being sent
- Look at logs: ~/.config/cli-chess/logs/
```

## 📊 System Requirements

### Minimum
- **RAM**: 6GB (4GB for 4B model + 2GB for system)
- **CPU**: Any modern CPU
- **Storage**: 5GB (for model)
- **OS**: Windows, Mac, Linux

### Recommended
- **RAM**: 12GB+ (8GB for better models)
- **CPU**: Multi-core for faster inference
- **GPU**: Optional, speeds up responses
- **Storage**: 10GB+ for multiple models

### Model Performance
| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| Phi-3 Mini 4K | 2.4GB | 4GB | ⚡⚡⚡ | ⭐⭐ |
| Mistral 7B | 4.4GB | 6GB | ⚡⚡ | ⭐⭐⭐ |
| Llama 3 8B | 4.7GB | 7GB | ⚡⚡ | ⭐⭐⭐⭐ |
| Mistral Nemo 12B | 7.2GB | 10GB | ⚡ | ⭐⭐⭐⭐⭐ |

## 🎯 Use Cases

### 1. **Solo Practice**
Play against an opponent who makes the game more engaging and less lonely.

### 2. **Learning Chess**
Get real-time explanations and strategic guidance from a patient coach.

### 3. **Casual Fun**
Enjoy friendly banter and commentary that makes chess more entertaining.

### 4. **Strategy Discussion**
Talk through positions and ideas with an AI that understands the game.

### 5. **Kids Learning**
A patient, encouraging opponent that explains moves in simple terms.

## 🚧 Known Limitations

1. **Local Only**: Requires LM Studio running locally
2. **Response Time**: 1-5 seconds per response (depends on model)
3. **Context Length**: Limited conversation history (~20 messages)
4. **Chess Strength**: Determined by Stockfish, not LLM
5. **Language**: Currently English only

## 🔮 Future Enhancements

### Planned Features
- [ ] Voice integration (TTS/STT)
- [ ] Multi-language support
- [ ] Post-game analysis mode
- [ ] Opening book commentary
- [ ] Adaptive difficulty based on conversation
- [ ] Save/load different AI personalities
- [ ] Tournament mode with commentary
- [ ] Puzzle mode with hints

### Possible Extensions
- Integration with other chess engines
- Cloud LLM support (GPT-4, Claude)
- Training custom chess personalities
- Spectator mode with AI commentary
- Chess lesson generation
- Game annotation export

## 📚 Resources

- **CLI-Chess**: https://github.com/trevorbayless/cli-chess
- **LM Studio**: https://lmstudio.ai/
- **Python Chess**: https://python-chess.readthedocs.io/
- **Stockfish**: https://stockfishchess.org/

## 🤝 Contributing

Ideas for contribution:
1. New AI personalities
2. Better system prompts
3. UI improvements
4. Additional chat commands
5. Performance optimizations
6. Documentation improvements

## 📝 License

This integration follows the cli-chess license (MIT).
LM Studio and models have separate licenses - check their documentation.

## 🙏 Credits

- **cli-chess**: Trevor Bayless
- **Fairy Stockfish**: Fairy-Stockfish developers
- **LM Studio**: LM Studio team
- **Python Chess**: Niklas Fiekas

## 💬 Support

Having issues?
1. Check the troubleshooting section
2. Review logs in `~/.config/cli-chess/logs/`
3. Test with the standalone demo
4. Verify LM Studio is working with curl
5. Try different model/settings

## 🎉 Enjoy!

Have fun playing chess with your new AI companion! May all your moves be brilliant! ♟️🤖

---

*Made with ❤️ for chess and AI enthusiasts*
