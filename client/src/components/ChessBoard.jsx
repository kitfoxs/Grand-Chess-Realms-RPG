import { useState, useEffect } from 'react';
import { Chess } from 'chess.js';
import { Chessboard } from 'react-chessboard';

function ChessBoardComponent({ npc, character }) {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState(game.fen());
  const [gameStatus, setGameStatus] = useState('');
  const [moveHistory, setMoveHistory] = useState([]);
  const [playerColor, setPlayerColor] = useState('white');
  const [aiElo, setAiElo] = useState(npc?.elo || 1500);
  const [thinking, setThinking] = useState(false);

  useEffect(() => {
    if (npc) {
      setAiElo(npc.elo);
      updateGameStatus();
    }
  }, [npc]);

  useEffect(() => {
    updateGameStatus();
    
    // If it's AI's turn, make a move
    if (!game.isGameOver() && 
        ((playerColor === 'white' && game.turn() === 'b') || 
         (playerColor === 'black' && game.turn() === 'w'))) {
      makeAIMove();
    }
  }, [fen, playerColor]);

  const updateGameStatus = () => {
    if (game.isCheckmate()) {
      const winner = game.turn() === 'w' ? 'Black' : 'White';
      setGameStatus(`Checkmate! ${winner} wins!`);
      saveGameResult(winner.toLowerCase() === playerColor ? 'player_won' : 'npc_won');
    } else if (game.isDraw()) {
      setGameStatus('Game drawn!');
      saveGameResult('draw');
    } else if (game.isCheck()) {
      setGameStatus('Check!');
    } else {
      setGameStatus(`${game.turn() === 'w' ? 'White' : 'Black'} to move`);
    }
  };

  const saveGameResult = async (result) => {
    if (!npc) return;

    try {
      await fetch('http://localhost:3001/api/game/chess-match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          npcId: npc.id,
          playerColor: playerColor,
          result: result,
          moves: moveHistory.length,
          pgn: game.pgn(),
          notableMoments: ''
        })
      });
    } catch (error) {
      console.error('Error saving game:', error);
    }
  };

  const makeAIMove = async () => {
    setThinking(true);
    
    // Simulate thinking time based on Elo
    const thinkTime = Math.min(2000, Math.max(500, aiElo / 2));
    
    await new Promise(resolve => setTimeout(resolve, thinkTime));

    // Simple AI: make a random legal move
    // In a real implementation, you would integrate Stockfish here
    const moves = game.moves();
    if (moves.length > 0) {
      const randomMove = moves[Math.floor(Math.random() * moves.length)];
      const newGame = new Chess(game.fen());
      newGame.move(randomMove);
      setGame(newGame);
      setFen(newGame.fen());
      setMoveHistory([...moveHistory, randomMove]);
    }

    setThinking(false);
  };

  const onDrop = (sourceSquare, targetSquare) => {
    // Check if it's player's turn
    if ((playerColor === 'white' && game.turn() !== 'w') ||
        (playerColor === 'black' && game.turn() !== 'b')) {
      return false;
    }

    try {
      const move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: 'q' // always promote to queen for simplicity
      });

      if (move === null) return false;

      setFen(game.fen());
      setMoveHistory([...moveHistory, move.san]);
      return true;
    } catch (error) {
      return false;
    }
  };

  const resetGame = () => {
    const newGame = new Chess();
    setGame(newGame);
    setFen(newGame.fen());
    setMoveHistory([]);
    setGameStatus('');
  };

  const switchSides = () => {
    setPlayerColor(playerColor === 'white' ? 'black' : 'white');
  };

  if (!npc) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-gray-400">
          <p className="text-xl mb-2">No opponent selected</p>
          <p>Please select an NPC to challenge from the NPC Database</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-white">
        Chess Match vs {npc.name} (Elo {npc.elo})
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chess Board */}
        <div className="lg:col-span-2">
          <div className="bg-gray-800 rounded-lg p-6">
            <div className="mb-4 flex justify-between items-center">
              <div>
                <p className="text-lg font-semibold text-white">{gameStatus}</p>
                {thinking && (
                  <p className="text-sm text-yellow-400">AI is thinking...</p>
                )}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={switchSides}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors"
                  disabled={moveHistory.length > 0}
                >
                  Switch Sides
                </button>
                <button
                  onClick={resetGame}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                >
                  New Game
                </button>
              </div>
            </div>

            <div className="aspect-square max-w-2xl mx-auto">
              <Chessboard
                position={fen}
                onPieceDrop={onDrop}
                boardOrientation={playerColor}
                customBoardStyle={{
                  borderRadius: '4px',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)'
                }}
              />
            </div>

            <div className="mt-4 text-center text-gray-400 text-sm">
              Playing as {playerColor === 'white' ? '⚪ White' : '⚫ Black'}
            </div>
          </div>
        </div>

        {/* Move History & Info */}
        <div className="space-y-6">
          {/* Opponent Info */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Opponent</h3>
            <p className="text-gray-300 font-semibold mb-2">{npc.name}</p>
            <p className="text-sm text-gray-400 mb-2">Elo: {npc.elo}</p>
            <p className="text-sm text-gray-400 mb-2">Style: {npc.chessStyle}</p>
            <p className="text-sm text-gray-500 italic">{npc.personality}</p>
          </div>

          {/* Move History */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Move History</h3>
            <div className="max-h-96 overflow-y-auto">
              {moveHistory.length === 0 && (
                <p className="text-gray-400 text-sm">No moves yet</p>
              )}
              <div className="grid grid-cols-2 gap-2">
                {moveHistory.map((move, index) => (
                  <div key={index} className="text-sm">
                    <span className="text-gray-500">{Math.floor(index / 2) + 1}.</span>
                    <span className="text-white ml-2">{move}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Game Info */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-white mb-4">Game Info</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Total Moves:</span>
                <span className="text-white">{moveHistory.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Turn:</span>
                <span className="text-white">{game.turn() === 'w' ? 'White' : 'Black'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChessBoardComponent;
