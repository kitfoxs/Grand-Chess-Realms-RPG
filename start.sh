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

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    [ ! -z "$SERVER_PID" ] && kill $SERVER_PID 2>/dev/null
    [ ! -z "$CLIENT_PID" ] && kill $CLIENT_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C and other termination signals
trap cleanup INT TERM

# Get absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/server"
CLIENT_DIR="$SCRIPT_DIR/client"

# Start backend in background
if [ -d "$SERVER_DIR" ]; then
    cd "$SERVER_DIR" || { echo "❌ Failed to enter server directory"; exit 1; }
    node index.js &
    SERVER_PID=$!
    cd "$SCRIPT_DIR" || exit 1
else
    echo "❌ Server directory not found"
    exit 1
fi

# Wait a moment for server to start
sleep 2

# Start frontend
if [ -d "$CLIENT_DIR" ]; then
    cd "$CLIENT_DIR" || { echo "❌ Failed to enter client directory"; cleanup; }
    npm run dev &
    CLIENT_PID=$!
    cd "$SCRIPT_DIR" || exit 1
else
    echo "❌ Client directory not found"
    cleanup
fi

# Wait for both processes
wait $SERVER_PID
wait $CLIENT_PID
