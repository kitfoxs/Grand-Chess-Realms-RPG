# Grand Chess Realms - Installation Guide

Complete step-by-step guide to get Grand Chess Realms web application running on your machine.

## 📋 Prerequisites

### Required Software

1. **Node.js 18+**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version` (should show v18 or higher)
   - Verify npm: `npm --version`

2. **LM Studio** (for AI conversations)
   - Download from: https://lmstudio.ai/
   - Compatible with: macOS (Apple Silicon recommended), Windows, Linux
   - Requires: 6GB+ RAM for basic models

### System Requirements

- **Minimum**: 8GB RAM, 10GB free disk space
- **Recommended**: 16GB RAM, 20GB free disk space
- **OS**: macOS, Windows 10+, Linux
- **Browser**: Chrome, Firefox, Safari, or Edge (latest version)

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone or navigate to the repository
cd Grand-Chess-Realms-RPG

# Run the start script (installs dependencies and starts servers)
./start.sh
```

### Option 2: Manual Setup

```bash
# 1. Install server dependencies
cd server
npm install

# 2. Install client dependencies
cd ../client
npm install

# 3. Return to root
cd ..
```

## 🔧 Detailed Setup Steps

### Step 1: Clone/Download Repository

```bash
# If using git
git clone https://github.com/yourusername/Grand-Chess-Realms-RPG.git
cd Grand-Chess-Realms-RPG

# Or download and extract ZIP file
```

### Step 2: Install Backend Dependencies

```bash
cd server
npm install
```

**Expected packages installed:**
- express (web server)
- sqlite3 (database)
- cors (cross-origin requests)
- body-parser (request parsing)
- node-fetch@2 (HTTP requests)

### Step 3: Install Frontend Dependencies

```bash
cd ../client
npm install
```

**Expected packages installed:**
- react & react-dom
- vite (build tool)
- chess.js (chess logic)
- react-chessboard (chess UI)
- tailwindcss (styling)
- And other dependencies (~150+ packages total)

### Step 4: Set Up LM Studio

1. **Download and Install LM Studio**
   - Visit https://lmstudio.ai/
   - Download for your platform
   - Install and open the application

2. **Download a Model**
   - Click "Discover" or "Search"
   - Recommended models:
     - **Mistral 7B Instruct** (4.4GB) - Best balance
     - **Llama 3.1 8B** (4.7GB) - High quality
     - **Phi-3 Mini** (2.4GB) - Fast, lower quality
   - Click download and wait for completion

3. **Load the Model**
   - Click on the downloaded model
   - Click "Load Model"
   - Wait for it to load (shows in green when ready)

4. **Start Local Server**
   - Click "Developer" tab (or "Local Server")
   - Click "Start Server"
   - Default address: http://127.0.0.1:1234
   - Keep this window open while playing!

### Step 5: Initialize Database

The database is automatically created when you first start the server. No manual setup needed!

### Step 6: Verify Installation

Run this command to test everything:

```bash
# From project root
npm run verify
```

Or manually check:

```bash
# Test backend
cd server
node index.js
# Should see: "Grand Chess Realms Server is running!"
# Press Ctrl+C to stop

# Test frontend build
cd ../client
npm run build
# Should complete without errors
```

## ▶️ Running the Application

### Development Mode (Recommended)

**Terminal 1 - Backend:**
```bash
cd server
node index.js
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

**Open Browser:**
Navigate to http://localhost:5173

### Using the Start Script

```bash
# From project root
./start.sh
```

This starts both servers automatically!

### Production Build

```bash
# Build frontend
cd client
npm run build

# Serve everything from backend
cd ../server
NODE_ENV=production node index.js
```

Access at: http://localhost:3001

## 🔍 Verification Checklist

After installation, verify:

- [ ] Node.js version is 18+
- [ ] Server starts without errors
- [ ] Client builds successfully
- [ ] LM Studio is installed
- [ ] A model is downloaded in LM Studio
- [ ] LM Studio server is running
- [ ] Database file created at `server/db/grand_chess_realms.db`
- [ ] Browser opens to http://localhost:5173
- [ ] Application loads (no errors in console)
- [ ] Green "LM Studio connected" indicator appears

## 🐛 Troubleshooting

### "Command not found: node"

**Solution:** Install Node.js from https://nodejs.org/

### "npm install" fails

**Solutions:**
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and `package-lock.json`
3. Run `npm install` again
4. If still failing, check internet connection

### Port already in use

**Error:** `EADDRINUSE: address already in use :::3001`

**Solutions:**
1. Kill process on port: `lsof -ti:3001 | xargs kill -9` (macOS/Linux)
2. Or change port in `server/index.js`: `const PORT = 3002;`
3. Update client API calls to new port

### LM Studio not connecting

**Checklist:**
1. Is LM Studio open? ✓
2. Is a model loaded? ✓
3. Is the server started? ✓
4. Is it on port 1234? ✓

**Test manually:**
```bash
curl http://127.0.0.1:1234/v1/models
```

Should return JSON with model info.

### Database errors

**Solution:** Delete and recreate database
```bash
cd server/db
rm grand_chess_realms.db
cd ..
node index.js
# Database will be recreated
```

### Build fails with Tailwind error

**Solution:**
```bash
cd client
npm install -D @tailwindcss/postcss
npm run build
```

### Client page is blank

**Checklist:**
1. Check browser console for errors (F12)
2. Verify server is running
3. Check Network tab in dev tools
4. Clear browser cache and reload

### Chess board not appearing

**Solution:**
```bash
cd client
npm install chess.js react-chessboard
npm run dev
```

## 📊 Expected File Structure After Installation

```
Grand-Chess-Realms-RPG/
├── server/
│   ├── node_modules/      ← Created by npm install
│   ├── db/
│   │   └── grand_chess_realms.db  ← Created on first run
│   ├── routes/
│   ├── data/
│   ├── prompts/
│   ├── index.js
│   └── package.json
├── client/
│   ├── node_modules/      ← Created by npm install
│   ├── dist/              ← Created by npm run build
│   ├── src/
│   ├── public/
│   ├── index.html
│   └── package.json
├── start.sh
└── README.md
```

## 💾 Disk Space Usage

- **Server dependencies**: ~50MB
- **Client dependencies**: ~250MB
- **LM Studio app**: ~500MB
- **Models**: 2-5GB each
- **Database**: Grows with use (starts <1MB)
- **Total**: ~3-6GB minimum

## 🔄 Updating

To update to a new version:

```bash
# Pull latest code
git pull origin main

# Update server dependencies
cd server
npm install

# Update client dependencies
cd ../client
npm install

# Rebuild client
npm run build
```

## 🧪 Testing Your Setup

### 1. Test Backend

```bash
cd server
node index.js
```

Expected output:
```
Connected to SQLite database
Database schema initialized
Database initialized successfully
🎮 Grand Chess Realms Server is running!
📡 API: http://localhost:3001
```

### 2. Test Frontend

```bash
cd client
npm run dev
```

Expected output:
```
VITE v7.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### 3. Test LM Studio

Visit: http://127.0.0.1:1234/v1/models

Should return JSON (not an error).

### 4. Test Full System

1. Start both servers
2. Open http://localhost:5173 in browser
3. Check for green "LM Studio connected" indicator
4. Navigate to NPCs tab - should show 8 NPCs
5. Click on an NPC - should open conversation
6. Send a test message

## 📞 Getting Help

If you're still having issues:

1. Check the `WEB_APP_README.md` for usage instructions
2. Review error messages carefully
3. Check browser console (F12) for errors
4. Verify all prerequisites are met
5. Try the manual setup instead of automated
6. Check GitHub Issues for similar problems

## 🎉 Success!

If you see:
- ✅ Server running on port 3001
- ✅ Client running on port 5173
- ✅ Green LM Studio indicator
- ✅ NPCs loading correctly

**Congratulations!** You're ready to play Grand Chess Realms! 🎮♟️

---

**Next Steps:**
1. Read `WEB_APP_README.md` for usage guide
2. Create your character
3. Talk to Knight Roland for your first interaction
4. Challenge an NPC to chess
5. Start your adventure!

**May Caissa guide your pieces!** ♔♕
