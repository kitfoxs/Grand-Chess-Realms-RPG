#!/usr/bin/env python3
"""
AI Chess Game - Play against conversational AI opponent
Combines Chessnut Pro board + LM Studio AI + Stockfish engine
"""

import asyncio
import chess
from datetime import datetime
from chessnut_board import ChessnutBoard
from ai_opponent import AIOpponent


class AIChessGame:
    """Chess game against AI opponent"""

    def __init__(self, ai_personality="friendly", ai_elo=1500, player_color=chess.WHITE):
        self.board = ChessnutBoard()
        self.game = chess.Board()
        self.player_color = player_color
        self.ai_color = not player_color

        # Create AI opponent
        self.ai = AIOpponent(
            name="Chess Bot",
            personality=ai_personality,
            elo=ai_elo
        )

        self.move_history = []
        self.game_start_time = None
        self.ai_thinking = False

    async def start(self):
        """Start game against AI"""
        print("="*60)
        print("♟️  AI CHESS GAME - Chessnut Pro Edition")
        print("="*60)
        print()

        # Connect to board
        try:
            await self.board.connect()
        except Exception as e:
            print(f"❌ Could not connect to board: {e}")
            return

        # Initialize AI engine
        try:
            await self.ai.initialize_engine()
        except Exception as e:
            print(f"❌ Could not initialize AI: {e}")
            return

        # Welcome animation
        print("\n💡 Preparing board...")
        await self._welcome_animation()

        # Set up callbacks
        self.board.on_move = self._handle_player_move

        # Game setup
        self.game_start_time = datetime.now()
        player_color_name = "White" if self.player_color == chess.WHITE else "Black"

        print("\n" + "="*60)
        print("🎮 GAME STARTED")
        print("="*60)
        print(f"\n👤 You: {player_color_name}")
        print(f"🤖 AI: {self.ai.name} (Elo {self.ai.elo}, {self.ai.personality})")

        # AI greeting
        greeting = self.ai.comment_on_game_start()
        if greeting:
            print(f'\n🤖 {self.ai.name}: "{greeting}"')

        self._print_game_state()

        print("\n💡 Tips:")
        print("   - Move pieces on the board to play")
        print("   - AI will respond automatically")
        print("   - Watch for LED highlights")
        print("   - Ctrl+C to quit")
        print()

        # Start game loop
        await self._game_loop()

    async def _welcome_animation(self):
        """Welcome animation"""
        # Flash all
        await self.board.set_leds('all')
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')
        await asyncio.sleep(0.2)

        # Flash player's side
        if self.player_color == chess.WHITE:
            ranks = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
        else:
            ranks = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

        await self.board.set_leds(ranks)
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')

        print("✅ Board ready!")

    def _print_game_state(self):
        """Print current game state"""
        print("\n" + "-"*60)
        print(f"Move: {self.game.fullmove_number}")

        current_turn = "White" if self.game.turn == chess.WHITE else "Black"
        is_player_turn = self.game.turn == self.player_color

        if is_player_turn:
            print(f"Turn: {current_turn} (👤 YOU)")
        else:
            print(f"Turn: {current_turn} (🤖 AI)")

        if self.game.is_check():
            print("⚠️  CHECK!")
        if self.game.is_checkmate():
            winner = "You" if self.game.turn != self.player_color else "AI"
            print(f"🏆 CHECKMATE! {winner} win!")
        if self.game.is_stalemate():
            print("🤝 STALEMATE!")

        print("-"*60)

        # Show board
        self._print_board()

        # Show last move
        if self.move_history:
            last_move = self.move_history[-1]
            print(f"\nLast move: {last_move['san']} by {last_move['player']}")

    def _print_board(self):
        """Print chess board"""
        print("\n   a b c d e f g h")
        print("  ┌─────────────────┐")

        for rank in range(7, -1, -1):
            print(f"{rank+1} │ ", end="")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.game.piece_at(square)

                if piece:
                    print(f"{piece.symbol()} ", end="")
                else:
                    print(". ", end="")

            print(f"│ {rank+1}")

        print("  └─────────────────┘")
        print("   a b c d e f g h\n")

    async def _handle_player_move(self, detected_move):
        """Handle move detected on board"""
        # Only process if it's player's turn
        if self.game.turn != self.player_color:
            print("⚠️  Not your turn!")
            await self._show_error()
            return

        if self.ai_thinking:
            print("⚠️  AI is thinking, please wait...")
            return

        print("\n" + "="*60)
        print(f"🎯 Move detected: {detected_move['from']} → {detected_move['to']}")

        try:
            # Parse move
            from_square = chess.parse_square(detected_move['from'])
            to_square = chess.parse_square(detected_move['to'])
            uci_move = chess.Move(from_square, to_square)

            # Check for promotion
            piece = self.game.piece_at(from_square)
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and chess.square_rank(to_square) == 7) or \
                   (piece.color == chess.BLACK and chess.square_rank(to_square) == 0):
                    uci_move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

            # Validate
            if uci_move in self.game.legal_moves:
                # Legal move!
                san = self.game.san(uci_move)
                self.game.push(uci_move)

                # Record
                self.move_history.append({
                    'uci': uci_move.uci(),
                    'san': san,
                    'player': 'Player',
                    'timestamp': datetime.now()
                })

                print(f"✅ Legal move: {san}")

                # Highlight move
                await self.board.highlight_move(detected_move['from'], detected_move['to'], duration=0.5)

                # AI comments on player's move
                comment = self.ai.comment_on_player_move(uci_move, self.game)
                if comment:
                    print(f'\n🤖 {self.ai.name}: "{comment}"')

                # Check game state
                self._print_game_state()

                # Check for game over
                if self.game.is_game_over():
                    await self._handle_game_over()
                else:
                    # AI's turn
                    print(f"\n🤖 {self.ai.name} is thinking...")
                    await self._ai_move()

            else:
                print(f"❌ Illegal move!")
                await self._show_error()

        except Exception as e:
            print(f"⚠️  Error: {e}")
            await self._show_error()

        print("="*60 + "\n")

    async def _ai_move(self):
        """AI makes a move"""
        if self.game.is_game_over():
            return

        self.ai_thinking = True

        try:
            # Show AI is thinking with LEDs
            thinking_squares = ['d4', 'e4', 'd5', 'e5']
            await self.board.set_leds(thinking_squares)

            # Get AI move
            ai_move = await self.ai.get_move(self.game, time_limit=1.0)

            # Turn off thinking LEDs
            await self.board.set_leds('none')

            if ai_move:
                san = self.game.san(ai_move)

                # Make the move
                self.game.push(ai_move)

                # Record
                self.move_history.append({
                    'uci': ai_move.uci(),
                    'san': san,
                    'player': 'AI',
                    'timestamp': datetime.now()
                })

                print(f"\n🤖 {self.ai.name} plays: {san}")

                # Highlight AI's move with LEDs
                from_sq = chess.square_name(ai_move.from_square)
                to_sq = chess.square_name(ai_move.to_square)
                await self.board.highlight_move(from_sq, to_sq, duration=2.0)

                # AI comments on own move
                comment = self.ai.comment_on_own_move(ai_move, self.game)
                if comment:
                    print(f'🤖 {self.ai.name}: "{comment}"')

                # Show game state
                self._print_game_state()

                # Check for game over
                if self.game.is_game_over():
                    await self._handle_game_over()
                else:
                    print(f"\n👤 Your turn!")

        except Exception as e:
            print(f"⚠️  AI error: {e}")

        finally:
            self.ai_thinking = False

    async def _show_error(self):
        """Flash error"""
        for _ in range(2):
            await self.board.set_leds('all')
            await asyncio.sleep(0.1)
            await self.board.set_leds('none')
            await asyncio.sleep(0.1)

    async def _handle_game_over(self):
        """Handle game over"""
        print("\n" + "="*60)
        print("🎮 GAME OVER")
        print("="*60)

        result = None
        reason = None

        if self.game.is_checkmate():
            winner = "You" if self.game.turn != self.player_color else self.ai.name
            result = f"{winner} wins!"
            reason = "checkmate"
            print(f"🏆 {result}")

            if winner == "You":
                await self._victory_animation()
        elif self.game.is_stalemate():
            result = "Draw"
            reason = "stalemate"
            print("🤝 Draw by stalemate")
        elif self.game.is_insufficient_material():
            result = "Draw"
            reason = "insufficient material"
            print("🤝 Draw by insufficient material")
        else:
            result = "Draw"
            reason = "unknown"
            print("🤝 Draw")

        # AI's final comment
        comment = self.ai.comment_on_game_over(result, reason)
        if comment:
            print(f'\n🤖 {self.ai.name}: "{comment}"')

        # Stats
        duration = datetime.now() - self.game_start_time
        print(f"\nGame duration: {duration}")
        print(f"Total moves: {len(self.move_history)}")

        # Save
        await self._save_game()

        print("\n" + "="*60)

    async def _victory_animation(self):
        """Victory animation"""
        for _ in range(5):
            await self.board.set_leds('all')
            await asyncio.sleep(0.2)
            await self.board.set_leds('none')
            await asyncio.sleep(0.2)

    async def _save_game(self):
        """Save game to PGN"""
        filename = f"game_vs_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pgn"

        pgn_game = chess.pgn.Game()
        pgn_game.headers["Event"] = "AI Chess Game"
        pgn_game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")

        if self.player_color == chess.WHITE:
            pgn_game.headers["White"] = "Player"
            pgn_game.headers["Black"] = f"{self.ai.name} (AI)"
        else:
            pgn_game.headers["White"] = f"{self.ai.name} (AI)"
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

        # Save
        try:
            with open(filename, 'w') as f:
                f.write(str(pgn_game))
            print(f"💾 Game saved to: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save: {e}")

    async def _game_loop(self):
        """Main game loop"""
        listen_task = asyncio.create_task(self.board.start_listening())

        try:
            # If AI plays first
            if self.game.turn == self.ai_color:
                print(f"\n🤖 {self.ai.name} plays first...")
                await self._ai_move()

            # Keep running
            while not self.game.is_game_over():
                await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\n⚠️  Game interrupted")
        finally:
            listen_task.cancel()
            await self.ai.cleanup()
            await self.board.disconnect()


# Run the AI game
if __name__ == "__main__":
    async def main():
        print("\n" + "="*60)
        print("  AI CHESS GAME SETUP")
        print("="*60)

        # Choose settings
        print("\n1. Choose your color:")
        print("   [1] White (you move first)")
        print("   [2] Black (AI moves first)")

        try:
            color_choice = input("\nYour choice (1 or 2): ").strip()
            player_color = chess.WHITE if color_choice == "1" else chess.BLACK
        except:
            player_color = chess.WHITE

        print("\n2. Choose AI difficulty:")
        print("   [1] Beginner (Elo 1000)")
        print("   [2] Intermediate (Elo 1500)")
        print("   [3] Advanced (Elo 2000)")
        print("   [4] Master (Elo 2400)")

        try:
            diff_choice = input("\nYour choice (1-4): ").strip()
            elo_map = {"1": 1000, "2": 1500, "3": 2000, "4": 2400}
            ai_elo = elo_map.get(diff_choice, 1500)
        except:
            ai_elo = 1500

        print("\n3. Choose AI personality:")
        print("   [1] Friendly - Encouraging and warm")
        print("   [2] Coach - Educational and helpful")
        print("   [3] Competitive - Confident and playful")
        print("   [4] Grandmaster - Analytical and deep")

        try:
            pers_choice = input("\nYour choice (1-4): ").strip()
            pers_map = {"1": "friendly", "2": "coach", "3": "competitive", "4": "grandmaster"}
            personality = pers_map.get(pers_choice, "friendly")
        except:
            personality = "friendly"

        print("\n⚙️  Starting game...")
        print(f"   Color: {'White' if player_color == chess.WHITE else 'Black'}")
        print(f"   AI Elo: {ai_elo}")
        print(f"   AI Personality: {personality}")
        print()

        # Start game
        game = AIChessGame(
            ai_personality=personality,
            ai_elo=ai_elo,
            player_color=player_color
        )

        await game.start()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! ♟️")
