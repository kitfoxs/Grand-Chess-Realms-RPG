#!/usr/bin/env python3
"""
GRAND CHESS REALMS - Terminal RPG
A MUD-style chess adventure with physical board integration
"""

import asyncio
import sys
import chess
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from npcs_database import NPCS, get_npc, get_starter_npcs
from game_master import GameMaster
from chessnut_board import ChessnutBoard
from ai_opponent import AIOpponent


class ChessRPG:
    """Main RPG game class"""

    def __init__(self):
        self.board = None  # Chess board connection
        self.gm = GameMaster()
        self.player_name = "Traveler"
        self.current_location = "Castle Lumina"
        self.current_npc = None
        self.game_state = chess.Board()
        self.in_chess_battle = False
        self.ai_opponent = None

    async def start(self):
        """Start the RPG"""
        self._print_title()
        await self._character_creation()
        await self._game_loop()

    def _print_title(self):
        """Print game title"""
        print("\n" + "="*60)
        print("║" + " "*58 + "║")
        print("║" + "     GRAND CHESS REALMS     ".center(58) + "║")
        print("║" + "  A Terminal Chess RPG Adventure  ".center(58) + "║")
        print("║" + " "*58 + "║")
        print("="*60 + "\n")

    async def _character_creation(self):
        """Character creation"""
        print("Welcome, traveler, to the Grand Chess Realms!")
        print("A world where kingdoms clash over the chessboard,")
        print("where strategy determines fate, and where you")
        print("will forge your legend piece by piece.\n")

        # Get player name
        name_input = input("What is your name? ").strip()
        self.player_name = name_input if name_input else "Traveler"
        self.gm.set_player_name(self.player_name)

        print(f"\nWelcome, {self.player_name}!")
        print("\nYour journey begins at Castle Lumina,")
        print("seat of the White Kingdom...")

        # Opening narration
        narration = self.gm.describe_location("Castle Lumina")
        if narration:
            print(f"\n📖 {narration}\n")

        input("Press ENTER to continue...")

    async def _game_loop(self):
        """Main game loop"""
        print("\n" + "="*60)
        print("  GAME START")
        print("="*60)

        running = True
        while running:
            # Show location and options
            self._show_location()

            # Get player command
            command = input("\n> ").strip().lower()

            if command in ["quit", "exit", "q"]:
                confirm = input("Are you sure you want to quit? (y/n): ").strip().lower()
                if confirm == "y":
                    running = False
                    break

            elif command in ["help", "h", "?"]:
                self._show_help()

            elif command in ["look", "l"]:
                narration = self.gm.describe_location(self.current_location)
                if narration:
                    print(f"\n📖 {narration}")

            elif command in ["npcs", "n"]:
                self._list_npcs()

            elif command.startswith("talk") or command.startswith("challenge"):
                await self._handle_npc_interaction(command)

            elif command in ["status", "s"]:
                self._show_status()

            else:
                print("❓ Unknown command. Type 'help' for options.")

        print("\n" + "="*60)
        print(f"Farewell, {self.player_name}!")
        print("May the pieces always fall in your favor.")
        print("="*60 + "\n")

    def _show_location(self):
        """Show current location info"""
        print("\n" + "-"*60)
        print(f"📍 Location: {self.current_location}")
        print(f"👤 {self.player_name}")
        print(f"🏆 Record: {self.gm.world_state['games_won']}W - {self.gm.world_state['games_lost']}L")
        print("-"*60)

    def _show_help(self):
        """Show available commands"""
        print("\n" + "="*60)
        print("  COMMANDS")
        print("="*60)
        print("\nExploration:")
        print("  look (l)         - Examine your surroundings")
        print("  npcs (n)         - List NPCs at this location")
        print("  status (s)       - View your game statistics")
        print("\nInteraction:")
        print("  challenge <npc>  - Challenge an NPC to chess")
        print("  talk <npc>       - Talk to an NPC")
        print("\nSystem:")
        print("  help (h/?)       - Show this help")
        print("  quit (q)         - Exit the game")
        print("="*60)

    def _list_npcs(self):
        """List NPCs at current location"""
        npcs_here = [npc for npc in NPCS.values()
                     if npc.get("location") == self.current_location]

        if not npcs_here:
            print("\n👥 No one else is here.")
            return

        print("\n👥 NPCs at this location:")
        for npc in npcs_here:
            print(f"\n  • {npc['name']} - {npc['title']}")
            print(f"    Elo: {npc['elo']} | Style: {npc['chess_style']}")

    async def _handle_npc_interaction(self, command):
        """Handle NPC interaction"""
        # Parse NPC name from command
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            print("❓ Who do you want to interact with?")
            self._list_npcs()
            return

        npc_query = parts[1].lower()

        # Find NPC
        found_npc = None
        for npc_id, npc in NPCS.items():
            if npc_query in npc["name"].lower() or npc_query in npc_id:
                if npc.get("location") == self.current_location:
                    found_npc = (npc_id, npc)
                    break

        if not found_npc:
            print(f"❓ Could not find '{npc_query}' here.")
            self._list_npcs()
            return

        npc_id, npc = found_npc

        if command.startswith("talk"):
            self._talk_to_npc(npc)
        elif command.startswith("challenge"):
            await self._challenge_npc(npc_id, npc)

    def _talk_to_npc(self, npc):
        """Talk to an NPC"""
        print("\n" + "="*60)
        print(f"💬 Conversation with {npc['name']}")
        print("="*60)

        # Greeting
        print(f'\n{npc["name"]}: "{npc["greeting"]}"')

        # GM introduces NPC if first meeting
        if npc["name"] not in self.gm.world_state["npcs_met"]:
            narration = self.gm.introduce_npc(npc)
            if narration:
                print(f"\n📖 {narration}")
            self.gm.world_state["npcs_met"].append(npc["name"])

        print(f'\n💡 Type "challenge {npc["name"].split()[0].lower()}" to play chess')

    async def _challenge_npc(self, npc_id, npc):
        """Challenge NPC to chess"""
        print("\n" + "="*60)
        print(f"⚔️  CHESS BATTLE: {self.player_name} vs {npc['name']}")
        print("="*60)

        # Challenge quote
        print(f'\n{npc["name"]}: "{npc["challenge_quote"]}"')

        # GM narration
        narration = self.gm.describe_chess_battle_start(npc["name"])
        if narration:
            print(f"\n📖 {narration}")

        print("\n💡 Preparing chess board...")

        # Connect to physical board
        try:
            if not self.board:
                self.board = ChessnutBoard()
                await self.board.connect()
                print("✅ Board connected!")
            else:
                print("✅ Board already connected!")

            # Play the game
            result = await self._play_chess_battle(npc)

            # Handle result
            await self._handle_battle_result(npc, result)

        except Exception as e:
            print(f"\n❌ Error during chess battle: {e}")
            print("   Returning to exploration...\n")

    async def _play_chess_battle(self, npc):
        """Play a chess battle against NPC"""
        # Initialize AI opponent
        self.ai_opponent = AIOpponent(
            name=npc["name"],
            personality=npc["personality"],
            elo=npc["elo"]
        )

        try:
            await self.ai_opponent.initialize_engine()
        except Exception as e:
            print(f"⚠️  Could not initialize AI engine: {e}")
            return "cancelled"

        # Set up game
        self.game_state = chess.Board()
        player_color = chess.WHITE  # Player is always white for now

        # Welcome animation
        await self.board.set_leds('all')
        await asyncio.sleep(0.3)
        await self.board.set_leds('none')

        # Game loop
        self.in_chess_battle = True
        move_count = 0

        def on_move(detected_move):
            """Handle detected moves (placeholder for async handling)"""
            pass

        self.board.on_move = on_move

        # Start listening
        listen_task = asyncio.create_task(self.board.start_listening())

        try:
            while not self.game_state.is_game_over() and self.in_chess_battle:
                # Display board
                self._print_chess_board()

                if self.game_state.turn == player_color:
                    # Player's turn
                    print(f"\n👤 Your turn ({move_count // 2 + 1})")
                    print("   Move a piece on the board...")

                    # Wait for move
                    player_move = await self._wait_for_player_move()

                    if player_move == "cancelled":
                        return "cancelled"

                    if player_move:
                        # AI comments
                        comment = self.ai_opponent.comment_on_player_move(player_move, self.game_state)
                        if comment:
                            print(f'\n🤖 {npc["name"]}: "{comment}"')

                else:
                    # AI's turn
                    print(f"\n🤖 {npc['name']} is thinking...")

                    # Show thinking LEDs
                    await self.board.set_leds(['d4', 'e4', 'd5', 'e5'])

                    # Get AI move
                    ai_move = await self.ai_opponent.get_move(self.game_state, time_limit=1.0)
                    await self.board.set_leds('none')

                    if ai_move:
                        san = self.game_state.san(ai_move)
                        self.game_state.push(ai_move)

                        print(f"🤖 {npc['name']} plays: {san}")

                        # Highlight move
                        from_sq = chess.square_name(ai_move.from_square)
                        to_sq = chess.square_name(ai_move.to_square)
                        await self.board.highlight_move(from_sq, to_sq, duration=2.0)

                        # AI comments
                        comment = self.ai_opponent.comment_on_own_move(ai_move, self.game_state)
                        if comment:
                            print(f'🤖 {npc["name"]}: "{comment}"')

                move_count += 1
                await asyncio.sleep(0.5)

            # Determine result
            if self.game_state.is_checkmate():
                winner = "player" if self.game_state.turn != player_color else "ai"
                return "victory" if winner == "player" else "defeat"
            elif self.game_state.is_game_over():
                return "draw"
            else:
                return "cancelled"

        except KeyboardInterrupt:
            print("\n\n⚠️  Battle cancelled")
            return "cancelled"
        finally:
            self.in_chess_battle = False
            listen_task.cancel()
            await self.ai_opponent.cleanup()

    async def _wait_for_player_move(self):
        """Wait for player to make a move on physical board"""
        move_detected = asyncio.Event()
        detected_move_data = []

        async def move_handler(move_data):
            # Parse and validate move
            try:
                from_square = chess.parse_square(move_data['from'])
                to_square = chess.parse_square(move_data['to'])
                move = chess.Move(from_square, to_square)

                # Check for promotion
                piece = self.game_state.piece_at(from_square)
                if piece and piece.piece_type == chess.PAWN:
                    if chess.square_rank(to_square) in [0, 7]:
                        move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

                if move in self.game_state.legal_moves:
                    san = self.game_state.san(move)
                    self.game_state.push(move)
                    detected_move_data.append(move)
                    print(f"✅ Move: {san}")

                    # Highlight
                    await self.board.highlight_move(move_data['from'], move_data['to'], duration=0.5)

                    move_detected.set()
                else:
                    print("❌ Illegal move!")
                    await self._show_error()

            except Exception as e:
                print(f"⚠️  Error: {e}")

        # Temporarily override move handler
        original_handler = self.board.on_move
        self.board.on_move = lambda m: asyncio.create_task(move_handler(m))

        # Wait for move (with timeout)
        try:
            await asyncio.wait_for(move_detected.wait(), timeout=300)  # 5 min timeout
            return detected_move_data[0] if detected_move_data else None
        except asyncio.TimeoutError:
            print("\n⏱️  Move timeout")
            return "cancelled"
        finally:
            self.board.on_move = original_handler

    async def _show_error(self):
        """Show error with LEDs"""
        for _ in range(2):
            await self.board.set_leds('all')
            await asyncio.sleep(0.1)
            await self.board.set_leds('none')
            await asyncio.sleep(0.1)

    def _print_chess_board(self):
        """Print current chess position"""
        print("\n   a b c d e f g h")
        print("  ┌─────────────────┐")

        for rank in range(7, -1, -1):
            print(f"{rank+1} │ ", end="")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.game_state.piece_at(square)
                print(f"{piece.symbol() if piece else '.'} ", end="")
            print(f"│ {rank+1}")

        print("  └─────────────────┘")
        print("   a b c d e f g h")

    async def _handle_battle_result(self, npc, result):
        """Handle chess battle result"""
        print("\n" + "="*60)
        print("  BATTLE COMPLETE")
        print("="*60)

        if result == "victory":
            print(f"\n🏆 Victory! You defeated {npc['name']}!")
            print(f'{npc["name"]}: "{npc["defeat_quote"]}"')

            # Victory animation
            for _ in range(5):
                await self.board.set_leds('all')
                await asyncio.sleep(0.2)
                await self.board.set_leds('none')
                await asyncio.sleep(0.2)

            self.gm.record_game_result(npc["name"], True)

            # GM narration
            narration = self.gm.describe_chess_battle_end(True, npc["name"])
            if narration:
                print(f"\n📖 {narration}")

        elif result == "defeat":
            print(f"\n💔 Defeat. {npc['name']} has bested you.")
            print(f'{npc["name"]}: "{npc["victory_quote"]}"')

            self.gm.record_game_result(npc["name"], False)

            # GM narration
            narration = self.gm.describe_chess_battle_end(False, npc["name"])
            if narration:
                print(f"\n📖 {narration}")

        elif result == "draw":
            print(f"\n🤝 The game ends in a draw.")
            print("   A respectable outcome!")

        else:
            print("\n⚠️  Battle was cancelled.")

        print("\n" + "="*60)
        input("\nPress ENTER to continue...")

    def _show_status(self):
        """Show player status"""
        print("\n" + "="*60)
        print(f"  {self.player_name.upper()}'S STATUS")
        print("="*60)
        print(f"\n📍 Location: {self.current_location}")
        print(f"🏆 Games Won: {self.gm.world_state['games_won']}")
        print(f"💔 Games Lost: {self.gm.world_state['games_lost']}")
        print(f"\n👥 NPCs Met: {len(self.gm.world_state['npcs_met'])}")

        if self.gm.world_state['npcs_met']:
            for npc_name in self.gm.world_state['npcs_met']:
                print(f"   • {npc_name}")

        print("="*60)


# Main entry point
if __name__ == "__main__":
    async def main():
        game = ChessRPG()
        try:
            await game.start()
        except KeyboardInterrupt:
            print("\n\n⚠️  Game interrupted")
        finally:
            if game.board:
                await game.board.disconnect()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nFarewell, traveler! ♟️\n")
