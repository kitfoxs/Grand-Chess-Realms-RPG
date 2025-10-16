const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const { initDatabase } = require('./db/database');

const npcRoutes = require('./routes/npc');
const memoryRoutes = require('./routes/memory');
const gameRoutes = require('./routes/game');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from client build (for production)
app.use(express.static(path.join(__dirname, '../client/dist')));

// API Routes
app.use('/api/npc', npcRoutes);
app.use('/api/memory', memoryRoutes);
app.use('/api/game', gameRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Grand Chess Realms API is running' });
});

// Check LM Studio connection
app.get('/api/lm-studio/check', async (req, res) => {
  try {
    const fetch = require('node-fetch');
    const response = await fetch('http://127.0.0.1:1234/v1/models', {
      timeout: 5000
    });
    
    if (response.ok) {
      const data = await response.json();
      res.json({ 
        connected: true, 
        message: 'LM Studio is running',
        models: data.data || []
      });
    } else {
      res.json({ 
        connected: false, 
        message: 'LM Studio responded but with an error' 
      });
    }
  } catch (error) {
    res.json({ 
      connected: false, 
      message: 'LM Studio is not running. Please start LM Studio and load a model.' 
    });
  }
});

// Serve React app for all other routes (SPA) - only in production
if (process.env.NODE_ENV === 'production') {
  app.get('/*', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/dist/index.html'));
  });
}

// Initialize database and start server
async function startServer() {
  try {
    await initDatabase();
    console.log('Database initialized successfully');

    app.listen(PORT, () => {
      console.log(`\n🎮 Grand Chess Realms Server is running!`);
      console.log(`📡 API: http://localhost:${PORT}`);
      console.log(`🌐 Client: http://localhost:${PORT}`);
      console.log(`\n💡 Make sure LM Studio is running at http://127.0.0.1:1234\n`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
