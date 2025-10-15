#!/usr/bin/env python3
"""
Simple Chess Game with Chessnut Pro Board
Move validation, notation, check/mate detection, LED hints
"""

import asyncio
import chess
from chessnut_board import ChessnutBoard
from datetime import datetime


class ChessGame:
    """Complete chess game with physical board integration"""

    def __init__(self):
        self.board = ChessnutBoard()
        self.game = chess.Board()
        self.move_history = []
        self.game_start_time = None
        self.hint_mode = False

    async def start(self):
        """Start a new game"""
        print("="*60)
        print("♟️  CHESS GAME - Chessnut Pro Edition")
        print("="*60)
        print()

        # Connect to board
        try:
            await self.board.connect()
        except Exception as e:
            print(f"❌ Could not connect to board: {e}")
            return

        # Welcome animation
        print("\n💡 Testing board LEDs...")
        await self._welcome_animation()

        # Set up callbacks
        self.board.on_move = self._handle_move
        self.board.on_position_change = self._handle_position_change

        # Game setup
        self.game_start_time = datetime.now()
        print("\n" + "="*60)
        print("🎮 GAME STARTED")
        print("="*60)
        self._print_game_state()
        print("\n💡 Commands:")
        print("   - Move pieces on the board to play")
        print("   - Type 'hint' for legal moves")
        print("   - Type 'undo' to take back last move")
        print("   - Type 'resign' to give up")
        print("   - Ctrl+C to quit")
        print()

        # Start game loop
        await self._game_loop()

    async def _welcome_animation(self):
        """Flash LEDs to show board is ready"""
        # Flash all
        await self.board.set_leds('all')
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')
        await asyncio.sleep(0.2)

        # Flash corners
        corners = ['a1', 'h1', 'a8', 'h8']
        await self.board.set_leds(corners)
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')
        await asyncio.sleep(0.2)

        # Flash center
        center = ['d4', 'e4', 'd5', 'e5']
        await self.board.set_leds(center)
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')

        print("✅ Board ready!")

    def _print_game_state(self):
        """Print current game state"""
        print("\n" + "-"*60)
        print(f"Move: {self.game.fullmove_number}")
        print(f"Turn: {'White' if self.game.turn == chess.WHITE else 'Black'}")

        if self.game.is_check():
            print("⚠️  CHECK!")
        if self.game.is_checkmate():
            print("🏆 CHECKMATE!")
        if self.game.is_stalemate():
            print("🤝 STALEMATE!")
        if self.game.is_insufficient_material():
            print("🤝 DRAW - Insufficient Material")
        if self.game.is_fifty_moves():
            print("🤝 DRAW - 50 Move Rule")

        print("-"*60)

        # Show board
        self._print_board()

        # Show last move
        if self.move_history:
            last_move = self.move_history[-1]
            print(f"\nLast move: {last_move['san']} ({last_move['uci']})")

    def _print_board(self):
        """Print the chess board"""
        print("\n   a b c d e f g h")
        print("  ┌─────────────────┐")

        for rank in range(7, -1, -1):
            print(f"{rank+1} │ ", end="")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.game.piece_at(square)

                if piece:
                    symbol = piece.symbol()
                    print(f"{symbol} ", end="")
                else:
                    print(". ", end="")

            print(f"│ {rank+1}")

        print("  └─────────────────┘")
        print("   a b c d e f g h\n")

    async def _handle_position_change(self, position, fen):
        """Called when board position changes"""
        # Don't print every change - wait for valid moves
        pass

    async def _handle_move(self, detected_move):
        """Called when a move is detected on the board"""
        print("\n" + "="*60)
        print(f"🎯 Move detected: {detected_move['from']} → {detected_move['to']}")

        # Try to validate the move
        try:
            # Parse the move
            from_square = chess.parse_square(detected_move['from'])
            to_square = chess.parse_square(detected_move['to'])

            # Create UCI move
            uci_move = chess.Move(from_square, to_square)

            # Check for promotion (if pawn reaches back rank)
            piece = self.game.piece_at(from_square)
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and chess.square_rank(to_square) == 7) or \
                   (piece.color == chess.BLACK and chess.square_rank(to_square) == 0):
                    # Auto-promote to queen
                    uci_move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

            # Validate move is legal
            if uci_move in self.game.legal_moves:
                # Legal move!
                san = self.game.san(uci_move)
                self.game.push(uci_move)

                # Record move
                self.move_history.append({
                    'uci': uci_move.uci(),
                    'san': san,
                    'timestamp': datetime.now(),
                    'fen': self.game.fen()
                })

                print(f"✅ Legal move: {san}")

                # Flash the move on LEDs
                await self.board.highlight_move(detected_move['from'], detected_move['to'], duration=1.0)

                # Check game state
                self._print_game_state()

                # Check for game over
                if self.game.is_game_over():
                    await self._handle_game_over()
                else:
                    # Show whose turn it is
                    next_player = "White" if self.game.turn == chess.WHITE else "Black"
                    print(f"\n👉 {next_player} to move")

            else:
                # Illegal move
                print(f"❌ Illegal move!")
                print(f"   That move is not legal in this position.")

                # Flash error pattern
                await self._show_error()

                # Show legal moves for that piece
                legal_moves = [m for m in self.game.legal_moves if m.from_square == from_square]
                if legal_moves:
                    print(f"\n💡 Legal moves for piece on {detected_move['from']}:")
                    for move in legal_moves[:5]:  # Show first 5
                        print(f"   - {self.game.san(move)}")

        except Exception as e:
            print(f"⚠️  Error processing move: {e}")
            await self._show_error()

        print("="*60 + "\n")

    async def _show_error(self):
        """Flash LEDs to indicate error"""
        # Flash all LEDs quickly
        for _ in range(3):
            await self.board.set_leds('all')
            await asyncio.sleep(0.1)
            await self.board.set_leds('none')
            await asyncio.sleep(0.1)

    async def _handle_game_over(self):
        """Handle game over"""
        print("\n" + "="*60)
        print("🎮 GAME OVER")
        print("="*60)

        if self.game.is_checkmate():
            winner = "Black" if self.game.turn == chess.WHITE else "White"
            print(f"🏆 {winner} wins by checkmate!")
            await self._victory_animation()
        elif self.game.is_stalemate():
            print("🤝 Draw by stalemate")
        elif self.game.is_insufficient_material():
            print("🤝 Draw by insufficient material")
        elif self.game.is_fifty_moves():
            print("🤝 Draw by 50-move rule")
        elif self.game.is_repetition():
            print("🤝 Draw by repetition")
        else:
            print("🤝 Draw")

        # Game stats
        duration = datetime.now() - self.game_start_time
        print(f"\nGame duration: {duration}")
        print(f"Total moves: {len(self.move_history)}")

        # Save game
        await self._save_game()

        print("\n" + "="*60)

    async def _victory_animation(self):
        """Victory LED animation"""
        # Flash entire board
        for _ in range(5):
            await self.board.set_leds('all')
            await asyncio.sleep(0.2)
            await self.board.set_leds('none')
            await asyncio.sleep(0.2)

    async def _save_game(self):
        """Save game to PGN file"""
        filename = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pgn"

        pgn_game = chess.pgn.Game()
        pgn_game.headers["Event"] = "Chessnut Pro Game"
        pgn_game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        pgn_game.headers["White"] = "Player"
        pgn_game.headers["Black"] = "Player"

        # Result
        if self.game.is_checkmate():
            result = "1-0" if self.game.turn == chess.BLACK else "0-1"
        else:
            result = "1/2-1/2"
        pgn_game.headers["Result"] = result

        # Add moves
        node = pgn_game
        board = chess.Board()
        for move_data in self.move_history:
            move = chess.Move.from_uci(move_data['uci'])
            node = node.add_variation(move)
            board.push(move)

        # Save to file
        try:
            with open(filename, 'w') as f:
                f.write(str(pgn_game))
            print(f"💾 Game saved to: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save game: {e}")

    async def show_hint(self):
        """Show legal moves with LEDs"""
        if self.game.is_game_over():
            print("Game is over - no hints available")
            return

        legal_moves = list(self.game.legal_moves)
        print(f"\n💡 {len(legal_moves)} legal moves available")

        # Group by piece
        from_squares = set()
        for move in legal_moves:
            from_squares.add(move.from_square)

        # Light up all squares with pieces that can move
        square_names = [chess.square_name(sq) for sq in from_squares]
        await self.board.set_leds(square_names)

        print("   Lit squares show pieces that can move")
        print("   (LEDs will turn off in 3 seconds)")

        await asyncio.sleep(3)
        await self.board.set_leds('none')

    async def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            print("❌ No moves to undo")
            return

        self.game.pop()
        undone = self.move_history.pop()

        print(f"↩️  Undid move: {undone['san']}")
        self._print_game_state()

    async def resign(self):
        """Resign the game"""
        print("\n🏳️  Game resigned")
        winner = "Black" if self.game.turn == chess.WHITE else "White"
        print(f"🏆 {winner} wins!")
        await self._save_game()

    async def _game_loop(self):
        """Main game loop"""
        # Start listening to board in background
        listen_task = asyncio.create_task(self.board.start_listening())

        # Command input loop
        try:
            while not self.game.is_game_over():
                # Check for user commands
                try:
                    # Non-blocking wait for a short time
                    await asyncio.sleep(0.5)

                except asyncio.CancelledError:
                    break

        except KeyboardInterrupt:
            print("\n\n⚠️  Game interrupted")
        finally:
            listen_task.cancel()
            await self.board.disconnect()


# Run the game
if __name__ == "__main__":
    async def main():
        game = ChessGame()
        await game.start()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! ♟️")
