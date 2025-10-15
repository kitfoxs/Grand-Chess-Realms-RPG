# LM Studio Integration Guide for cli-chess

## Overview
This guide explains how to integrate LM Studio's local LLMs into cli-chess to create an AI opponent that can chat naturally while playing chess using Fairy Stockfish for move generation.

## Architecture

```
User Input
    ↓
┌─────────────────────────────────────┐
│  Chat-Enabled Offline Game          │
│  ├─ User makes move                 │
│  ├─ LLM comments on move (optional) │
│  ├─ Fairy Stockfish calculates move │
│  └─ LLM presents move with context  │
└─────────────────────────────────────┘
```

## Key Components

### 1. LM Studio Chat Client
- Connects to LM Studio's OpenAI-compatible API (default: http://localhost:1234)
- Maintains conversation history
- Provides game context to the LLM

### 2. Enhanced Offline Game Mode
- Extends existing `OfflineGamePresenter`
- Adds chat interface alongside board
- Coordinates between LLM chat and Stockfish moves

### 3. Game Context Provider
- Formats current game state for the LLM
- Includes: board position (FEN), last moves, material count, position evaluation
- Gives LLM personality and chess knowledge

## Implementation Steps

### Step 1: Install Dependencies
```bash
pip install openai  # For LM Studio API client
pip install requests  # For HTTP requests
```

### Step 2: Set Up LM Studio
1. Download and install LM Studio
2. Load a conversational model (recommended: Mistral 7B, Llama 3, or Phi-3)
3. Start the local server (Settings → Local Server → Start Server)
4. Note the server URL (usually http://localhost:1234)

### Step 3: Add Configuration
Add to cli-chess config file (`~/.config/cli-chess/config.json`):
```json
{
  "lm_studio": {
    "enabled": true,
    "api_url": "http://localhost:1234/v1",
    "model": "local-model",
    "personality": "friendly",
    "verbosity": "medium"
  }
}
```

### Step 4: Create New Modules

#### Files to Create:
1. `src/cli_chess/modules/llm_chat/llm_chat_client.py` - LM Studio client
2. `src/cli_chess/modules/llm_chat/chat_view.py` - Chat UI component
3. `src/cli_chess/core/game/offline_game/ai_chat_game_presenter.py` - Enhanced presenter
4. `src/cli_chess/utils/game_context.py` - Game state formatter

## Features

### Chat Commands
- Regular messages: Just type naturally to chat
- `/hint` - Ask the AI for strategic advice
- `/explain` - Ask AI to explain its last move
- `/analyze` - Get current position analysis
- `/trash` - Engage in friendly banter
- `/quiet` - Toggle commentary on/off

### LLM Personality Options
- **Friendly**: Encouraging, supportive chess buddy
- **Coach**: Educational, explains concepts
- **Trash-talker**: Playful, competitive banter
- **Grandmaster**: Serious, technical analysis
- **Beginner**: Learning alongside you

### Context Awareness
The LLM receives:
- Current FEN position
- Last 5 moves with notation
- Material count
- Stockfish evaluation (centipawns)
- Game phase (opening/middlegame/endgame)
- Time spent thinking
- Move annotations (blunder, good, brilliant, etc.)

## Technical Details

### API Integration
LM Studio provides OpenAI-compatible endpoints:
```python
POST http://localhost:1234/v1/chat/completions
{
  "model": "local-model",
  "messages": [...],
  "temperature": 0.7,
  "max_tokens": 150
}
```

### System Prompt Template
```
You are a friendly chess opponent playing against a human. You're playing as {color}.
You use Stockfish to calculate moves, but you present them naturally.
Current position: {fen}
Last moves: {moves}
Material: {material}
Evaluation: {eval}

Be conversational, react to moves, and make chess fun!
```

### Move Generation Flow
1. User makes move
2. (Optional) LLM comments on user's move
3. Stockfish calculates best move (2 seconds)
4. LLM receives move and generates natural commentary
5. Move is displayed with LLM's message
6. Wait for user's response

## Performance Considerations

### Latency Management
- LLM responses run async (don't block game)
- Stockfish calculation and LLM commentary happen in parallel
- Cache common responses (opening moves)
- Set reasonable token limits (100-200 tokens)

### Model Recommendations
- **Fast**: Phi-3 Mini (3.8B) - ~1-2 sec response
- **Balanced**: Mistral 7B - ~2-4 sec response  
- **Quality**: Llama 3 8B - ~3-5 sec response
- **Best**: Mistral Nemo 12B - ~5-8 sec response

### Resource Usage
- Model loaded once at game start
- ~4-8GB RAM depending on model
- CPU-only is fine for chat (quantized models)
- GPU optional but faster

## UI Layout

```
┌─────────────────────────────────────────────────────┐
│  CLI Chess - Playing vs AI Chat Opponent            │
├─────────────────────┬───────────────────────────────┤
│                     │  AI: "Nice opening! I'll     │
│    8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜│  respond with the Sicilian   │
│    7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟│  Defense. Let's see how this │
│    6 . . . . . . . .│  plays out! 1...c5"          │
│    5 . . . . . . . .│                              │
│    4 . . . . ♙ . . .│  You: "Good move! What's     │
│    3 . . . . . . . .│  your plan here?"            │
│    2 ♙ ♙ ♙ ♙ . ♙ ♙ ♙│                              │
│    1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖│  AI: "I'm aiming to control  │
│      a b c d e f g h│  the center and develop      │
│                     │  quickly. Watch for d5!"     │
│                     │                              │
│  Your move:         │  [Type message or move]      │
│  > e2e4            │  >                           │
└─────────────────────┴───────────────────────────────┘
```

## Testing Checklist

- [ ] LM Studio server running
- [ ] Model loaded in LM Studio
- [ ] API connection successful
- [ ] Chat messages send/receive
- [ ] Moves execute correctly
- [ ] LLM commentary appears
- [ ] No blocking of game UI
- [ ] Conversation history maintained
- [ ] Config file loads properly
- [ ] Error handling works

## Troubleshooting

### LM Studio won't connect
- Ensure server is running (check LM Studio status)
- Verify URL (try `curl http://localhost:1234/v1/models`)
- Check firewall settings

### Slow responses
- Use smaller/quantized model
- Reduce max_tokens
- Disable commentary on every move
- Use GPU if available

### Out of memory
- Close other applications
- Use smaller model (4B or less)
- Restart LM Studio

### LLM seems confused
- Improve system prompt
- Provide more game context
- Reduce conversation history
- Try different model

## Future Enhancements

1. **Opening book integration**: LLM can discuss opening theory
2. **Post-game analysis**: Review and discuss the game
3. **Adaptive difficulty**: LLM adjusts Stockfish depth based on skill
4. **Multiple personalities**: Save/load different AI opponents
5. **Voice integration**: Text-to-speech for AI comments
6. **Learning mode**: LLM provides hints and lessons
7. **Puzzle mode**: LLM presents and discusses tactical puzzles

## Example Session

```
Game Start:
AI: "Hey! Ready for a game? I'm playing Black today. Good luck! 👋"

After 1.e4:
AI: "Classic! King's pawn opening. I'll meet you in the center with 1...e5"

After tactical shot:
AI: "Whoa! Didn't see that knight fork coming. Nice tactic! 😅 
Let me regroup with Kg8."

After blunder:
You: "Was that a mistake?"
AI: "Yeah, I probably should have castled first. You're up a pawn now. 
I'll have to fight for compensation!"

Game end:
AI: "Good game! That endgame was tough. Want to analyze what happened 
around move 15? I think that's where I started losing control."
```

## License & Credits

This implementation builds on cli-chess by Trevor Bayless.
Uses Fairy Stockfish for move generation.
LLM integration via LM Studio API.
