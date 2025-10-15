# 🚀 QUICK START GUIDE

## 5-Minute Setup

### Step 1: Download LM Studio (2 min)
```
1. Go to https://lmstudio.ai/
2. Download for your OS
3. Install and open
```

### Step 2: Get a Model (2 min)
```
1. Click "Discover" tab in LM Studio
2. Search for "Mistral 7B Instruct"
3. Click download (wait for it to finish)
4. Click on the model to load it
```

### Step 3: Start Server (30 sec)
```
1. Click "Developer" tab
2. Click "Start Server"
3. Wait for "Server running on http://localhost:1234"
```

### Step 4: Test It! (30 sec)
```bash
# Install dependencies
pip install requests python-chess

# Run demo
python demo_llm_chess.py
```

## 🎮 Using the Demo

```
Game Start:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI: "Hey! Ready for a game? I'm playing 
         Black. Good luck! 👋"

Your Turn:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
  a b c d e f g h

Move: e4

AI Response:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI: "Strong opening! I'll meet you in 
         the center with e5."

Chat Feature:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Move: chat: What's your plan?
💬 You: What's your plan?
🤖 AI: "I'm aiming for quick development 
        and central control. Watch for my 
        knight coming to f6!"
```

## 📁 Files Overview

**For Testing:**
- `demo_llm_chess.py` - Standalone demo to test setup

**For Integration:**
- `llm_chat_client.py` - Core LLM client
- `ai_chat_game_presenter.py` - Game logic with chat

**Documentation:**
- `README.md` - Main documentation (START HERE!)
- `IMPLEMENTATION_GUIDE.md` - Technical details
- `INTEGRATION_GUIDE.md` - Integration steps

## 🎯 What You Get

✅ AI opponent that chats during games
✅ Move commentary and explanations
✅ Strategic hints and analysis
✅ Multiple personality types
✅ 100% local and private
✅ Works offline

## ⚡ Recommended Models

**Fastest** (Good for testing)
- Phi-3 Mini 4K (2.4GB)
- Response time: 1-2 seconds

**Best Balance**
- Mistral 7B Instruct (4.4GB)
- Response time: 2-4 seconds

**Highest Quality**
- Llama 3 8B (4.7GB)
- Response time: 3-5 seconds

## 🔧 Troubleshooting One-Liners

**Can't connect?**
```bash
curl http://localhost:1234/v1/models
# Should return JSON. If error, restart LM Studio server.
```

**Too slow?**
```
1. Use Phi-3 Mini model
2. Close other apps
3. Reduce max_tokens in config
```

**Weird responses?**
```
1. Try different model
2. Restart LM Studio
3. Check model is fully loaded
```

## 📊 Quick Comparison

### Before (Standard cli-chess):
```
You: e4
[Computer plays e5]
[Silence...]
You: Nf3
[Computer plays Nc6]
[More silence...]
```

### After (With LM Studio):
```
You: e4

🤖 AI: "Strong opening! I'll meet you in 
        the center. This should be fun!"
AI plays: e5

You: Nf3

🤖 AI: "Developing knights first, solid 
        strategy! I'll do the same."
AI plays: Nc6

You: "What are you planning?"

🤖 AI: "I'm eyeing that e4 pawn and 
        thinking about a Sicilian setup. 
        We'll see how it develops!"
```

## 🎓 Learning Features

Ask the AI:
```
"Why did you play that?"
"What would you do in my position?"
"Is this a good move?"
"What's the plan in this position?"
```

## 🎮 Commands During Game

- Type moves: `e4`, `Nf3`, `O-O`
- Chat: `chat: <your message>`
- Quit: `quit`

## ⏱️ Typical Timeline

```
Install LM Studio:      2 minutes
Download model:         2 minutes
Setup & config:         1 minute
Test demo:             30 seconds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total:                 ~6 minutes
```

## 🎉 That's It!

You're ready to play chess with an AI companion!

For full integration with cli-chess, see:
- `README.md` for overview
- `INTEGRATION_GUIDE.md` for step-by-step

---

**Questions?** Check the main README.md
**Issues?** Run the demo first to test setup
**Having fun?** Enjoy your games! ♟️🤖
