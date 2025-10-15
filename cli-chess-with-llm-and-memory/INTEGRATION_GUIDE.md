# Integration Instructions for LM Studio Chat

## Quick Start Guide

### 1. Prerequisites
```bash
# Install required packages
pip install openai requests
```

### 2. Set Up LM Studio
1. Download LM Studio from https://lmstudio.ai/
2. Install and open LM Studio
3. Download a model (recommended):
   - **Mistral 7B Instruct** (good balance)
   - **Phi-3 Mini** (fast, 4GB RAM)
   - **Llama 3 8B** (high quality)
4. Load the model (click on model in UI)
5. Go to "Developer" tab and click "Start Server"
6. Server should start on http://localhost:1234

### 3. Test Connection
```bash
# Test if LM Studio is running
curl http://localhost:1234/v1/models

# Should return JSON with model info
```

### 4. Add Files to cli-chess

Copy these files to your cli-chess installation:

```
src/cli_chess/
├── modules/
│   └── llm_chat/
│       ├── __init__.py
│       ├── llm_chat_client.py  (from llm_chat_client.py)
│       └── chat_view.py  (new file for UI)
└── core/
    └── game/
        └── offline_game/
            └── ai_chat_game_presenter.py  (from ai_chat_game_presenter.py)
```

### 5. Configuration

Create or edit `~/.config/cli-chess/config.json`:

```json
{
  "lm_studio": {
    "enabled": true,
    "api_url": "http://localhost:1234/v1",
    "model": "local-model",
    "personality": "friendly",
    "commentary_frequency": "medium",
    "max_tokens": 150,
    "temperature": 0.7
  }
}
```

### 6. Menu Integration

Add to the offline games menu (src/cli_chess/menus/offline_games_menu/):

```python
def _create_menu_options(self) -> list:
    return [
        ("Play vs Computer", self._start_vs_computer),
        ("Play vs AI Chat Opponent", self._start_vs_ai_chat),  # NEW
        ("Analysis Board", self._start_analysis),
        ("Back", self._back)
    ]

def _start_vs_ai_chat(self):
    """Start game with AI chat opponent"""
    from cli_chess.core.game.offline_game.ai_chat_game_presenter import start_ai_chat_game
    
    # Load LM Studio config
    config = load_config()  # Your config loading function
    lm_studio_config = config.get('lm_studio', {})
    
    # Use existing game parameters
    game_params = self.model.get_game_parameters()
    
    start_ai_chat_game(game_params, lm_studio_config)
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│          User Interface (View)              │
│  ┌─────────────┐      ┌─────────────────┐  │
│  │   Board     │      │   Chat Window   │  │
│  │   Display   │      │   - AI msgs     │  │
│  │             │      │   - User input  │  │
│  └─────────────┘      └─────────────────┘  │
└─────────────────────────────────────────────┘
              │                  │
              ▼                  ▼
┌─────────────────────────────────────────────┐
│      AIChatGamePresenter                    │
│  ┌──────────────────┐  ┌─────────────────┐ │
│  │  Chess Logic     │  │  Chat Logic     │ │
│  │  - Make moves    │  │  - Send msgs    │ │
│  │  - Get engine mv │  │  - Get replies  │ │
│  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────┘
         │                       │
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│ Fairy Stockfish  │    │  LMStudioClient  │
│ (Chess Engine)   │    │  (LLM Chat)      │
└──────────────────┘    └──────────────────┘
         │                       │
         ▼                       ▼
   Best moves            HTTP API (localhost:1234)
                                │
                                ▼
                         LM Studio Server
                         (Running locally)
```

## Code Flow Example

### Starting a Game:
```python
1. User selects "Play vs AI Chat Opponent"
2. AIChatGamePresenter initializes:
   - Creates OfflineGameModel (chess logic)
   - Creates LMStudioChatClient (chat logic)
   - Tests LM Studio connection
3. Chat client sends system prompt to LM Studio
4. AI responds with greeting: "Hey! Ready for a game?"
5. Game begins
```

### Making a Move:
```python
1. User plays move: "e4"
2. AIChatGamePresenter.make_move("e4"):
   - Updates board
   - Sends to chat client: "Opponent played e4"
3. Chat client (async):
   - Adds to conversation history
   - Calls LM Studio API
   - Gets response: "Strong opening! I'll meet you in the center."
   - Displays in chat window
4. Meanwhile, engine calculates response:
   - EnginePresenter.get_best_move()
   - Returns "e5"
5. AIChatGamePresenter.make_engine_move():
   - Makes move on board
   - Sends to chat: "You played e5"
   - Gets commentary: "Classic response. This should be an interesting game!"
6. User sees:
   - Board updated with e5
   - Chat shows: "Classic response. This should be an interesting game!"
```

### Chat Interaction:
```python
1. User types: "What's your plan here?"
2. AIChatGamePresenter.handle_chat_input()
3. Adds to conversation history
4. Sends to LM Studio with context:
   - Current FEN position
   - Recent moves
   - Material count
5. LM Studio responds with strategically aware answer
6. Displays in chat window
```

## Key Design Decisions

### 1. Async Chat
- Chat requests don't block game UI
- Uses @threaded decorator
- User can continue playing while AI "thinks"

### 2. Separation of Concerns
- **Engine**: Pure move calculation (Stockfish)
- **Chat**: Conversational layer (LLM)
- **Presenter**: Coordinates both

### 3. Context Awareness
- LLM receives game state with each message
- Maintains conversation history
- Can reference previous moves and positions

### 4. Personality System
- Different system prompts for different styles
- Configurable via settings
- Easy to add new personalities

## Testing Checklist

### Basic Functionality
- [ ] LM Studio server starts
- [ ] Model loads successfully
- [ ] API connection works
- [ ] Game starts with greeting
- [ ] Moves execute correctly
- [ ] Chat messages send/receive
- [ ] AI commentary appears

### Chat Features
- [ ] Regular chat works
- [ ] /hint command works
- [ ] /explain command works
- [ ] /analyze command works
- [ ] /quiet toggles commentary
- [ ] Conversation context maintained

### Edge Cases
- [ ] LM Studio not running (graceful degradation)
- [ ] Network timeout handling
- [ ] Long message handling
- [ ] Special characters in messages
- [ ] Game over scenarios
- [ ] Takeback during AI thinking

### Performance
- [ ] No UI blocking
- [ ] Acceptable response time
- [ ] Memory usage reasonable
- [ ] No lag in move execution

## Troubleshooting

### "Cannot connect to LM Studio"
**Solutions:**
1. Check LM Studio is running
2. Verify server started (Developer tab)
3. Test with: `curl http://localhost:1234/v1/models`
4. Check firewall settings
5. Try restarting LM Studio

### "Responses are too slow"
**Solutions:**
1. Use smaller model (Phi-3 Mini)
2. Reduce max_tokens (try 100)
3. Disable commentary (use /quiet)
4. Check CPU/GPU usage
5. Close other applications

### "AI responses don't make sense"
**Solutions:**
1. Check system prompt
2. Verify game context is being sent
3. Try different model
4. Adjust temperature (try 0.5-0.8)
5. Check conversation history length

### "Out of memory"
**Solutions:**
1. Use smaller model
2. Reduce context window
3. Clear conversation history more often
4. Use quantized model (Q4_K_M or lower)
5. Close other applications

## Advanced Configuration

### Custom Personalities

Edit the personality in `llm_chat_client.py`:

```python
personalities = {
    "custom_name": """Your custom personality prompt here.
    Be specific about:
    - Tone and style
    - Level of analysis
    - Reaction to moves
    - Teaching vs competing focus
    """,
}
```

### Adjust Response Length

In config.json:
```json
{
  "lm_studio": {
    "max_tokens": 100,  // Shorter responses
    "temperature": 0.6   // More focused
  }
}
```

### Commentary Frequency

Options: "high", "medium", "low", "off"

- **high**: Comments on every move
- **medium**: Comments on interesting moves
- **low**: Only major events
- **off**: Only responds to chat

### Custom API Endpoints

If using different LLM API:
```json
{
  "lm_studio": {
    "api_url": "http://your-server:port/v1",
    "api_key": "your-key-if-needed"
  }
}
```

## Performance Optimization

### Model Selection
- **Fastest**: Phi-3 Mini 4K Q4_K_M (~2GB, 1-2s)
- **Balanced**: Mistral 7B Instruct Q4_K_M (~4GB, 2-4s)
- **Best**: Mistral Nemo 12B Q4_K_M (~7GB, 4-8s)

### Context Management
```python
# Reduce history length
max_history = 10  # Keep last 10 messages only

# Clear history periodically
if len(conversation_history) > 20:
    chat_client.clear_history()
```

### Caching Common Responses
```python
# Cache opening moves
opening_cache = {
    "e4": "Strong king's pawn opening!",
    "d4": "Solid queen's pawn opening.",
}
```

## Future Enhancements

### Phase 1 (Current)
- ✅ Basic chat integration
- ✅ Move commentary
- ✅ Chat commands
- ✅ Multiple personalities

### Phase 2 (Planned)
- [ ] Voice output (TTS)
- [ ] Opening book integration
- [ ] Adaptive difficulty
- [ ] Learning mode
- [ ] Custom training

### Phase 3 (Future)
- [ ] Multi-language support
- [ ] Tournament mode
- [ ] Analysis tools
- [ ] Puzzle generation
- [ ] Teaching curriculum

## Resources

- **LM Studio**: https://lmstudio.ai/
- **cli-chess**: https://github.com/trevorbayless/cli-chess
- **python-chess**: https://python-chess.readthedocs.io/
- **OpenAI API Docs**: https://platform.openai.com/docs/api-reference

## Support

Issues? Questions?
1. Check LM Studio is running
2. Review logs in `~/.config/cli-chess/logs/`
3. Test with curl commands
4. Try different model
5. Report issues on GitHub

## License

Integration code follows cli-chess license (MIT).
LM Studio and models have separate licenses.
