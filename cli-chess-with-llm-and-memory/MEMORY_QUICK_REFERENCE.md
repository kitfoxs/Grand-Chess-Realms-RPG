# 🧠 AI Memory Quick Reference Card

## What Your AI Friend Remembers

### 👤 About You
```
✓ Your name (if mentioned)
✓ Where you're from
✓ What you do
✓ Your interests
✓ Personal facts you share
```

### ♟️ Your Chess
```
✓ Playing style (aggressive/tactical/positional)
✓ Favorite openings
✓ Skill level
✓ Improvement areas
✓ Strong points
```

### 🤝 Your Friendship
```
✓ Games played: 42
✓ Record: 18W-20L-4D
✓ Friendship level: 8/10
✓ Inside jokes: 5
✓ Memorable moments: 12
```

## How to Teach Your AI

### Share Personal Info
```
❌ Don't: Stay silent
✅ Do: "Hi! I'm Alex from Seattle"
```

### Mention Preferences
```
❌ Don't: Just play moves
✅ Do: "I love the King's Gambit!"
```

### Have Conversations
```
❌ Don't: Only enter moves
✅ Do: chat: What's your plan?
```

### Complete Games
```
❌ Don't: Quit mid-game often
✅ Do: Finish games to help AI learn
```

## Commands You Can Use

```
/hint       → Get strategic advice
/explain    → Understand AI's move
/analyze    → Position analysis
/quiet      → Toggle commentary
/help       → Show commands
chat: msg   → Regular conversation
```

## View Your Memory

```bash
# See what AI remembers
python memory_viewer.py

# Interactive management
python memory_viewer.py --interactive
```

## Memory Grows When You:

```
✓ Play more games        → +0.5 friendship
✓ Have good chats        → +0.2 friendship
✓ Share personal stuff   → Stored as facts
✓ Create funny moments   → Inside jokes
✓ Have epic games        → Memorable moments
```

## Friendship Levels

```
1-3:  New friends          "Nice to meet you!"
4-6:  Good friends         "Good to see you again!"
7-9:  Close friends        "I missed you!"
10:   Best chess friends   "My favorite opponent!"
```

## Privacy & Control

```
✓ 100% stored locally
✓ View anytime
✓ Export/backup easily
✓ Reset if desired
✓ No cloud sync
✓ You're in control
```

## Memory Location

```
Linux/Mac:  ~/.config/cli-chess/memory/player_memory.json
Windows:    %APPDATA%\cli-chess\memory\player_memory.json
```

## Example Evolution

### Game 1
```
AI: "Hello! Nice to meet you!"
```

### Game 10
```
AI: "Hey! Your Sicilian is improving!"
```

### Game 50
```
AI: "Alex! Remember that crazy game last week? 
     Ready for another battle, my friend?"
```

## Quick Tips

1. **Chat naturally** - Just be yourself
2. **Play regularly** - Builds relationship
3. **Finish games** - Helps AI learn
4. **Share thoughts** - AI remembers
5. **Check memory** - See what's stored
6. **Backup** - Export important memories

## Troubleshooting One-Liners

```bash
# View memory
python memory_viewer.py

# Check file exists
ls ~/.config/cli-chess/memory/player_memory.json

# Export backup
python memory_viewer.py --interactive
# Choose option 3

# Reset memory
python memory_viewer.py --interactive
# Choose option 4, type RESET
```

## What Makes It Special

```
Standard Chess Engine:
  You: e4
  Engine: e5
  [Silence...]
  
With Memory:
  You: e4
  AI: "Alex! Nice opening! Remember when 
       you beat me with this? Not today! 😉"
  AI plays: e5
```

---

💡 **Pro Tip:** The more you interact, the better your AI friend knows you!

🎮 **Start Building Memories:** 
```bash
python demo_llm_chess_with_memory.py
```

📊 **Check Progress:**
```bash
python memory_viewer.py
```

---

**Your AI chess friend is waiting to meet you! 🤖♟️❤️**
