#!/bin/bash

# Grand Chess Realms - Startup Script
# This script starts both the backend and frontend servers

echo "🎮 Starting Grand Chess Realms..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Check if dependencies are installed
if [ ! -d "server/node_modules" ]; then
    echo "📦 Installing server dependencies..."
    cd server && npm install && cd ..
fi

if [ ! -d "client/node_modules" ]; then
    echo "📦 Installing client dependencies..."
    cd client && npm install && cd ..
fi

echo ""
echo "🚀 Starting servers..."
echo ""
echo "📡 Backend will run on: http://localhost:3001"
echo "🌐 Frontend will run on: http://localhost:5173"
echo ""
echo "💡 Make sure LM Studio is running at http://127.0.0.1:1234"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
cd server
node index.js &
SERVER_PID=$!
cd ..

# Wait a moment for server to start
sleep 2

# Start frontend
cd client
npm run dev &
CLIENT_PID=$!
cd ..

# Wait for both processes
wait $SERVER_PID $CLIENT_PID
