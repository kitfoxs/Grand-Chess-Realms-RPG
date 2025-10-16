# Quick Start Guide - Grand Chess Realms Web App

Get up and running in 5 minutes!

## Prerequisites Check

Before you start, make sure you have:

- [ ] **Node.js 18+** installed ([Download](https://nodejs.org/))
  ```bash
  node --version  # Should show v18 or higher
  ```

- [ ] **LM Studio** downloaded ([Get it](https://lmstudio.ai/))

## 🚀 5-Minute Setup

### Step 1: Install LM Studio & Model (3 minutes)

1. Open LM Studio
2. Click "Discover" or search tab
3. Download **Mistral 7B Instruct** (4.4GB)
4. Click on the model → "Load Model"
5. Go to "Developer" or "Local Server" tab
6. Click "Start Server"
7. Verify it shows "Server Running at http://127.0.0.1:1234"

### Step 2: Run the Application (2 minutes)

#### Option A: Automated (Recommended)

```bash
cd Grand-Chess-Realms-RPG
./start.sh
```

The script will:
- Install dependencies if needed
- Start backend server (port 3001)
- Start frontend dev server (port 5173)
- Open in your browser automatically

#### Option B: Manual

**Terminal 1 - Backend:**
```bash
cd server
npm install  # First time only
npm start
```

**Terminal 2 - Frontend:**
```bash
cd client
npm install  # First time only
npm run dev
```

### Step 3: Open & Play

Open your browser to: **http://localhost:5173**

You should see:
- ✅ "Grand Chess Realms" header
- ✅ Green "LM Studio connected" indicator
- ✅ Tabs for NPCs, Talk, Chess, Character, etc.

## 🎮 First Steps in the App

### 1. Create Your Character (1 minute)

1. Click "Character" tab
2. Fill in:
   - **Name**: Your character's name
   - **Concept**: e.g., "Noble Strategist"
   - **Faction**: White Kingdom, Black Kingdom, or Neutral
   - **Race**: Human, Elf, Dwarf, etc.
   - **Elo Rating**: Your honest chess rating (800-2800)
   - **Backstory**: Write a brief story
3. Click "Save Character"

### 2. Meet Your First NPC (2 minutes)

1. Click "NPCs" tab
2. Find **Knight Roland** (Elo 1800 - good for beginners)
3. Click "💬 Talk"
4. Type: "Hello, I'm new here and seeking guidance"
5. Watch the NPC respond!

### 3. Play Your First Chess Match (5-10 minutes)

1. From NPCs tab, click "♟️ Challenge" on Knight Roland
2. Choose your color (White or Black)
3. Make moves by dragging pieces
4. The AI will respond (currently random moves)
5. Game is saved automatically when finished

### 4. Explore Other Features

**Dice Roller:**
- Click "Tools" tab
- Roll d20, d6, or other dice
- Add modifiers (+/- numbers)
- Try quick actions (Persuasion, Insight, etc.)

**Oracle (Solo Play Helper):**
- Click "Tools" tab
- Ask a yes/no question
- Get oracle answer based on d20 roll
- Try "Random Event" or "Plot Twist"

**Journal:**
- Click "Journal" tab
- Write session notes
- Entries are automatically saved

**World Reference:**
- Click "World" tab
- Explore locations (Castle Lumina, etc.)
- Read about campaigns
- Learn about factions

## 🎯 Usage Tips

### NPCs & Relationships

- **Talk regularly**: NPCs remember your conversations
- **Check relationships**: See Trust/Respect/Friendship bars
- **Play chess**: Match results affect relationships
- **Higher Elo = Harder**: Start with lower-rated NPCs

### Chess Tips

- **Match your skill**: Challenge NPCs near your Elo
- **Switch sides**: Try playing as Black for variety
- **Learn from losses**: All matches are learning experiences
- **Take your time**: No rush in solo play

### Solo Play with Oracle

Use the Oracle to answer questions:
- "Does the guard believe me?" → Roll
- "Do I find the item?" → Roll
- "Is the NPC friendly?" → Roll

Results guide your narrative!

## 🛠️ Troubleshooting

### "LM Studio not connected" appears

**Fix:**
1. Open LM Studio
2. Make sure a model is loaded (green indicator)
3. Click "Start Server" in Developer tab
4. Refresh your browser

**Still not working?**
```bash
# Test LM Studio manually
curl http://127.0.0.1:1234/v1/models
# Should return JSON
```

### Chess board not appearing

**Fix:**
```bash
cd client
npm install chess.js react-chessboard
npm run dev
```

### Page is blank

**Fix:**
1. Open browser developer tools (F12)
2. Check Console tab for errors
3. Make sure both servers are running
4. Try clearing cache and reload

### Server won't start

**Check ports:**
```bash
# macOS/Linux
lsof -ti:3001 | xargs kill -9  # Kill process on port 3001

# Then restart
cd server && npm start
```

## 📚 Next Steps

Once you're comfortable:

1. **Challenge different NPCs**
   - Each has unique personality
   - Higher Elo = better conversations

2. **Build your story**
   - Write in journal after each session
   - Track character development

3. **Use all tools**
   - Dice for skill checks
   - Oracle for decisions
   - World reference for inspiration

4. **Read the docs**
   - `WEB_APP_README.md` - Full feature guide
   - `INSTALLATION.md` - Detailed setup
   - `PROJECT_SUMMARY.md` - Technical details

## 🎉 You're Ready!

You now have:
- ✅ Working application
- ✅ AI-powered NPCs
- ✅ Interactive chess
- ✅ Full RPG toolkit
- ✅ Your first character

**Start your adventure in Grand Chess Realms!**

---

## 📞 Quick Help

**Common Questions:**

**Q: Do I need internet?**  
A: Only for initial setup. Once running, it's fully offline.

**Q: Can I play without LM Studio?**  
A: Yes, but NPC conversations will be limited.

**Q: Is my data saved?**  
A: Yes! Everything is saved to local database.

**Q: Can I delete and start over?**  
A: Yes! Delete `server/db/grand_chess_realms.db` to reset.

**Q: How do I stop the servers?**  
A: Press `Ctrl+C` in each terminal (or use the start script).

**Q: Can friends play?**  
A: Currently single-player only on each computer.

---

**Happy gaming! May Caissa guide your pieces!** ♔♕♟️
