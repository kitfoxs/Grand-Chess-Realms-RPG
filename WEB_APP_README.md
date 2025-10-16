# Grand Chess Realms - Web Application

A local desktop web application for solo tabletop RPG play of "Grand Chess Realms" - where all combat is resolved through chess matches and NPCs are powered by local LLM conversations.

## 🎮 Features

### Core Systems
- **Chess Integration**: Full chess board with move validation and game tracking
- **NPC Conversations**: AI-powered NPCs that remember your interactions
- **Character System**: Create and manage your character
- **Journal**: Track your campaign progress
- **Dice Roller**: Standard RPG dice with modifiers and history
- **Oracle**: Yes/No oracle for solo play decisions
- **World Reference**: Explore locations, campaigns, and factions

### NPCs Available
- Knight Roland (Elo 1800) - White Kingdom
- King Alden XIV (Elo 2200) - White Kingdom
- Princess Elara (Elo 1900) - White Kingdom
- Emperor Darius Blackbourne (Elo 2300) - Black Kingdom
- Empress Selene Blackbourne (Elo 2250) - Black Kingdom
- Ambassador Corvus (Elo 1650) - Black Kingdom
- Grandmaster Altan (Elo 2400) - Neutral
- Grandmaster Rionn (Elo 2450) - Neutral

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- LM Studio installed and running (for AI conversations)
- macOS with Apple Silicon (M1/M2/M3/M4) recommended

### Setup

1. **Install LM Studio**
   - Download from https://lmstudio.ai/
   - Install and open LM Studio
   - Download a model (recommended: Mistral 7B or Llama 3.1 8B)
   - Load the model and start the server
   - Ensure it's running at http://127.0.0.1:1234

2. **Install Backend Dependencies**
   ```bash
   cd server
   npm install
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd client
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd server
   node index.js
   ```
   The server will start on http://localhost:3001

2. **Start the Frontend (in a new terminal)**
   ```bash
   cd client
   npm run dev
   ```
   The client will start on http://localhost:5173

3. **Open your browser**
   Navigate to http://localhost:5173

## 🎯 How to Use

### 1. Create Your Character
- Go to the "Character" tab
- Fill in your character details
- Set your honest chess Elo rating
- Save your character

### 2. Meet NPCs
- Browse the "NPCs" tab
- Select an NPC to talk or challenge to chess
- Each NPC has unique personality and chess style

### 3. Have Conversations
- Click "Talk" on any NPC
- NPCs remember your conversations and chess matches
- Build relationships through repeated interactions

### 4. Play Chess
- Click "Challenge" to start a chess match
- Games are saved to your history
- Results affect NPC relationships

### 5. Use Tools
- **Dice Roller**: Roll standard RPG dice for skill checks
- **Oracle**: Get yes/no answers for solo play decisions
- **Journal**: Record your campaign notes

### 6. Explore the World
- Read about locations, campaigns, and factions
- Use the world reference for inspiration

## 🏗️ Project Structure

```
grand-chess-realms/
├── server/
│   ├── index.js              # Express server
│   ├── routes/
│   │   ├── npc.js           # NPC endpoints
│   │   ├── memory.js        # Memory/relationship tracking
│   │   └── game.js          # Game state management
│   ├── db/
│   │   ├── schema.sql       # Database schema
│   │   └── database.js      # SQLite connection
│   ├── prompts/
│   │   └── npcPrompts.js    # LLM system prompts
│   └── data/
│       └── npcs.json        # NPC database
├── client/
│   ├── src/
│   │   ├── App.jsx          # Main application
│   │   └── components/
│   │       ├── ChessBoard.jsx
│   │       ├── NPCConversation.jsx
│   │       ├── NPCDatabase.jsx
│   │       ├── CharacterSheet.jsx
│   │       ├── DiceRoller.jsx
│   │       ├── Oracle.jsx
│   │       ├── Journal.jsx
│   │       └── WorldReference.jsx
│   └── package.json
└── README.md
```

## 🔧 Configuration

### LM Studio Settings
- **API URL**: http://127.0.0.1:1234
- **Model**: Any 7B-8B parameter model
- **Temperature**: 0.8 (adjustable in server/routes/npc.js)
- **Max Tokens**: 400

### Server Port
- Default: 3001
- Change in server/index.js if needed

### Client Port
- Default: 5173 (Vite default)
- Configure in client/vite.config.js

## 💾 Data Storage

### SQLite Database
- Location: `server/db/grand_chess_realms.db`
- Stores:
  - NPC conversations
  - Relationship levels
  - Chess match history
  - Character data
  - Journal entries

### localStorage
- Character sheet data backed up locally
- Automatic saves

## 🐛 Troubleshooting

### LM Studio Not Connected
- Ensure LM Studio is running
- Check that a model is loaded
- Verify server is at http://127.0.0.1:1234
- App will still work but conversations will be limited

### Chess Board Not Loading
- Check browser console for errors
- Ensure all dependencies are installed
- Try refreshing the page

### Database Errors
- Database is auto-created on first run
- Check server/db/ directory permissions
- Delete database file to reset

### Port Conflicts
- Change server port in server/index.js
- Change client port in client/vite.config.js
- Update API calls in client components

## 🎨 Customization

### Adding New NPCs
1. Edit `server/data/npcs.json`
2. Add NPC with required fields:
   - id, name, title, elo, faction, location
   - chessStyle, personality, speechPattern
   - backstory, conversationTopics

### Adjusting AI Responses
- Edit prompts in `server/prompts/npcPrompts.js`
- Modify temperature/max_tokens in `server/routes/npc.js`

### Changing Theme
- Edit colors in `client/tailwind.config.js`
- Modify styles in component files

## 📚 Tech Stack

### Backend
- Node.js + Express
- SQLite3 for database
- CORS for cross-origin requests
- node-fetch for LM Studio API

### Frontend
- React 18
- Vite for build tool
- Tailwind CSS for styling
- chess.js for game logic
- react-chessboard for UI

### AI/ML
- LM Studio (local LLM server)
- OpenAI-compatible API

## 🤝 Contributing

This application is part of the Grand Chess Realms RPG project. Contributions welcome!

- Add new NPCs
- Improve UI/UX
- Add features (Stockfish integration, better AI, etc.)
- Fix bugs
- Improve documentation

## 📝 License

MIT License - see main repository README for details

## 🎮 Gameplay Tips

1. **Build Relationships**: Talk to NPCs regularly to build trust and friendship
2. **Match Your Skill**: Challenge NPCs near your Elo rating
3. **Use the Journal**: Record your story for better immersion
4. **Try the Oracle**: It's great for solo play decisions
5. **Experiment**: Try different factions and character concepts

## 🚧 Future Enhancements

- Stockfish integration for adjustable AI difficulty
- Voice chat integration (TTS/STT)
- Save/load multiple campaigns
- Quest tracking system
- Achievement system
- Multiplayer support
- Mobile-friendly design

## 💡 Support

For issues, questions, or suggestions:
- Check this README
- Review the main repository documentation
- Test LM Studio connection
- Check browser console for errors

---

**Ready to play?** Start LM Studio, run the servers, and begin your adventure in the Grand Chess Realms! ♟️👑✨
