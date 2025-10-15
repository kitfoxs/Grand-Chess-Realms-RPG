#!/usr/bin/env python3
"""
AI Chess Opponent with LM Studio Integration
Uses local LLM for personality and Stockfish for moves
"""

import requests
import json
import chess
import chess.engine
from pathlib import Path


class AIOpponent:
    """Conversational AI chess opponent"""

    def __init__(self,
                 name="Chess Friend",
                 personality="friendly",
                 elo=1500,
                 engine_path=None,
                 lm_studio_url="http://localhost:1234/v1"):

        self.name = name
        self.personality = personality
        self.elo = elo
        self.lm_studio_url = lm_studio_url
        self.engine_path = engine_path or self._find_stockfish()
        self.engine = None
        self.conversation_history = []

        # Personality prompts
        self.personalities = {
            "friendly": {
                "system": f"You are {name}, a friendly chess AI. You love playing chess and enjoy encouraging your opponent. Comment on moves positively, share chess wisdom, and make the game fun. Keep responses to 1-2 sentences.",
                "style": "encouraging and warm"
            },
            "coach": {
                "system": f"You are {name}, a chess coach. Provide helpful tactical advice and point out good and bad moves. Teach as you play. Keep responses to 1-2 sentences.",
                "style": "educational and constructive"
            },
            "competitive": {
                "system": f"You are {name}, a competitive chess player. You're confident, maybe a bit cocky, but respectful. Enjoy good moves and point out mistakes. Keep responses to 1-2 sentences.",
                "style": "confident and playful"
            },
            "grandmaster": {
                "system": f"You are {name}, a chess grandmaster. Analyze positions deeply, discuss strategy, and appreciate brilliant moves. Keep responses to 1-2 sentences.",
                "style": "analytical and appreciative"
            }
        }

    def _find_stockfish(self):
        """Try to find Stockfish installation"""
        possible_paths = [
            "/usr/local/bin/stockfish",
            "/usr/bin/stockfish",
            "/opt/homebrew/bin/stockfish",
            "stockfish",
        ]

        for path in possible_paths:
            if Path(path).exists() or path == "stockfish":
                return path

        return None

    async def initialize_engine(self, skill_level=None):
        """Initialize the chess engine"""
        if not self.engine_path:
            raise Exception("Stockfish not found. Please install: brew install stockfish")

        try:
            self.engine = await chess.engine.popen_uci(self.engine_path)

            # Set skill level based on Elo
            if skill_level is None:
                skill_level = self._elo_to_skill_level(self.elo)

            await self.engine.configure({"Skill Level": skill_level})
            print(f"✅ Chess engine initialized (Skill Level: {skill_level})")

        except Exception as e:
            print(f"⚠️  Could not initialize engine: {e}")
            self.engine = None

    def _elo_to_skill_level(self, elo):
        """Convert Elo rating to Stockfish skill level (0-20)"""
        # Rough mapping: 1000 Elo = skill 0, 2800 Elo = skill 20
        skill = int((elo - 1000) / 90)
        return max(0, min(20, skill))

    def _get_personality_system_prompt(self):
        """Get the system prompt for current personality"""
        return self.personalities.get(self.personality, self.personalities["friendly"])["system"]

    async def get_move(self, board, time_limit=1.0):
        """Get next move from engine"""
        if not self.engine:
            raise Exception("Engine not initialized")

        result = await self.engine.play(board, chess.engine.Limit(time=time_limit))
        return result.move

    def generate_comment(self, context, max_tokens=100):
        """Generate a comment using LM Studio"""
        try:
            # Build messages
            messages = [
                {"role": "system", "content": self._get_personality_system_prompt()},
            ]

            # Add conversation history (last 4 messages)
            messages.extend(self.conversation_history[-4:])

            # Add current context
            messages.append({"role": "user", "content": context})

            # Call LM Studio API
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "model": "local-model",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                comment = data["choices"][0]["message"]["content"].strip()

                # Update conversation history
                self.conversation_history.append({"role": "user", "content": context})
                self.conversation_history.append({"role": "assistant", "content": comment})

                return comment
            else:
                return None

        except requests.exceptions.ConnectionError:
            # LM Studio not running - return None
            return None
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return None

    def comment_on_game_start(self):
        """Generate opening comment"""
        context = f"We're starting a new chess game. You are playing as {self.name} (Elo {self.elo}). Greet your opponent warmly and express excitement about the game."
        comment = self.generate_comment(context)
        return comment or f"Hello! I'm {self.name}. Ready for a good game?"

    def comment_on_player_move(self, move, board):
        """Comment on player's move"""
        san = board.san(move)
        position_info = self._analyze_position(board)

        context = f"Your opponent just played {san}. {position_info} React to this move briefly."
        comment = self.generate_comment(context)

        return comment

    def comment_on_own_move(self, move, board):
        """Comment on AI's move"""
        san = board.san(move)
        position_info = self._analyze_position(board)

        context = f"You just played {san}. {position_info} Briefly explain your thinking."
        comment = self.generate_comment(context)

        return comment

    def comment_on_game_over(self, result, reason):
        """Comment on game end"""
        context = f"The game ended: {result} ({reason}). Share your thoughts on the game briefly."
        comment = self.generate_comment(context)

        return comment or "Good game!"

    def _analyze_position(self, board):
        """Quick position analysis for context"""
        info = []

        if board.is_check():
            info.append("You're giving check!")
        if board.is_checkmate():
            info.append("That's checkmate!")

        # Count material
        white_material = sum(self._piece_value(board.piece_at(sq))
                            for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).color == chess.WHITE)
        black_material = sum(self._piece_value(board.piece_at(sq))
                            for sq in chess.SQUARES if board.piece_at(sq) and board.piece_at(sq).color == chess.BLACK)

        material_diff = white_material - black_material
        if abs(material_diff) >= 3:
            if material_diff > 0:
                info.append("White is up material.")
            else:
                info.append("Black is up material.")

        return " ".join(info) if info else "The position looks interesting."

    def _piece_value(self, piece):
        """Get piece value"""
        if not piece:
            return 0
        values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                 chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
        return values.get(piece.piece_type, 0)

    async def cleanup(self):
        """Clean up engine"""
        if self.engine:
            await self.engine.quit()
            self.engine = None


# Test AI opponent
if __name__ == "__main__":
    import asyncio

    async def test():
        ai = AIOpponent(name="Friendly Bot", personality="friendly", elo=1500)

        print("Testing AI Opponent...")
        print()

        # Test LLM
        print("1. Testing LM Studio connection...")
        comment = ai.comment_on_game_start()
        print(f"   AI: \"{comment}\"")
        print()

        # Test engine
        print("2. Testing Stockfish engine...")
        await ai.initialize_engine()

        board = chess.Board()
        move = await ai.get_move(board, time_limit=0.5)
        print(f"   AI's first move: {board.san(move)}")

        # Test move commentary
        board.push(move)
        comment = ai.comment_on_own_move(move, board)
        if comment:
            print(f"   AI: \"{comment}\"")

        await ai.cleanup()
        print("\n✅ AI Opponent test complete!")

    asyncio.run(test())
