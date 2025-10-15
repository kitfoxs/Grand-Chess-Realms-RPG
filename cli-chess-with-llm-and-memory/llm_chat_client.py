"""
LM Studio Chat Client for cli-chess
Connects to LM Studio's local API to provide conversational chess opponent
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from cli_chess.utils import log


@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'system', 'user', or 'assistant'
    content: str


class LMStudioChatClient:
    """Client for communicating with LM Studio's local API"""
    
    def __init__(self, 
                 api_url: str = "http://localhost:1234/v1",
                 model: str = "local-model",
                 personality: str = "friendly",
                 max_history: int = 20,
                 memory_manager=None):
        """
        Initialize LM Studio chat client
        
        Args:
            api_url: Base URL for LM Studio API
            model: Model identifier (usually "local-model" for LM Studio)
            personality: AI opponent personality type
            max_history: Maximum conversation history to maintain
            memory_manager: MemoryManager instance for persistent memory (optional)
        """
        self.api_url = api_url
        self.model = model
        self.personality = personality
        self.max_history = max_history
        self.memory_manager = memory_manager
        self.conversation_history: List[ChatMessage] = []
        self.system_prompt = self._build_system_prompt()
        self.notable_moments = []  # Collect during game for memory
        self.player_observations = []  # Observations about player's play
        
    def _build_system_prompt(self) -> str:
        """Build the system prompt based on personality"""
        personalities = {
            "friendly": """You are a friendly chess opponent playing a casual game. 
You're enthusiastic, supportive, and make chess fun. Comment on interesting moves, 
acknowledge good play, and keep things light and enjoyable. You use Stockfish to 
calculate your moves, but present them naturally and conversationally. Keep responses 
under 2-3 sentences unless explaining something complex.""",
            
            "coach": """You are a chess coach playing against a student. Your goal is 
to make the game educational. Explain your moves, point out key concepts, and help 
your opponent improve. Be encouraging but also point out mistakes constructively. 
You use Stockfish for calculations but focus on teaching principles.""",
            
            "competitive": """You are a competitive chess player who loves the challenge. 
You respect good play but also engage in playful trash talk. React strongly to blunders, 
celebrate your good moves, and keep the competitive spirit high. Stay friendly but 
add some spice to the game!""",
            
            "grandmaster": """You are a serious chess grandmaster. Provide deep analysis, 
discuss strategic plans, and explain positions technically. Use chess terminology 
naturally and focus on the quality of play. Be professional and analytical.""",
            
            "beginner": """You are learning chess alongside your opponent. You make moves 
using Stockfish but discuss them from a learning perspective. Share your thought 
process, ask questions, and explore ideas together. Be humble and curious."""
        }
        
        base = personalities.get(self.personality, personalities["friendly"])
        return f"""{base}

IMPORTANT GUIDELINES:
- Keep responses concise (1-3 sentences typically)
- React naturally to moves
- Don't explain unless asked
- Use emojis sparingly (only when natural)
- Never break character
- Present your moves naturally, like: "I'll play Nf6 to develop"
- React to opponent's moves: "Nice move!" or "Interesting choice"
"""

    def initialize_game(self, color: str, variant: str = "standard") -> str:
        """
        Start a new game and get AI's greeting
        
        Args:
            color: AI's color ('white' or 'black')
            variant: Chess variant being played
            
        Returns:
            AI's greeting message
        """
        self.conversation_history = []
        self.notable_moments = []
        self.player_observations = []
        
        # Get memory context if available
        memory_context = ""
        if self.memory_manager:
            memory_context = "\n\n" + self.memory_manager.get_greeting_context()
            self.memory_manager.record_game_start()
        
        game_context = f"""NEW GAME STARTED
Your color: {color}
Variant: {variant}
{'You move first!' if color == 'white' else 'Opponent moves first.'}
{memory_context}

Greet your friend warmly! Reference your history together if you have one.
If this is your first game, be welcoming and introduce yourself.
Keep it natural and brief (1-2 sentences).
"""
        
        self.conversation_history.append(ChatMessage("system", self.system_prompt))
        
        # Add persistent memory context if available
        if self.memory_manager:
            memory_sys_prompt = self.memory_manager.get_conversation_context()
            self.conversation_history.append(ChatMessage("system", memory_sys_prompt))
        
        response = self._send_message(game_context, role="system")
        return response

    def comment_on_move(self, 
                       move: str, 
                       fen: str,
                       eval_cp: Optional[int] = None,
                       is_user_move: bool = True) -> Optional[str]:
        """
        Get AI commentary on a move
        
        Args:
            move: The move in SAN or UCI notation
            fen: Current board position (FEN)
            eval_cp: Position evaluation in centipawns
            is_user_move: True if commenting on user's move, False if presenting own move
            
        Returns:
            AI's comment, or None if silent
        """
        move_type = "Opponent played" if is_user_move else "You played"
        eval_str = f" (Eval: {eval_cp/100:+.2f})" if eval_cp is not None else ""
        
        context = f"""MOVE: {move_type} {move}
Position: {fen}{eval_str}
{'React briefly to this move.' if is_user_move else 'Present your move naturally.'}"""
        
        return self._send_message(context)

    def respond_to_chat(self, user_message: str) -> str:
        """
        Respond to user's chat message
        
        Args:
            user_message: User's message
            
        Returns:
            AI's response
        """
        response = self._send_message(user_message, role="user")
        
        # Extract learnings from conversation
        if response:
            self.extract_learnings_from_conversation(user_message, response)
        
        return response

    def provide_hint(self, fen: str, best_moves: List[str]) -> str:
        """
        Provide a hint about the position
        
        Args:
            fen: Current position
            best_moves: List of top moves from engine
            
        Returns:
            Hint message
        """
        context = f"""HINT REQUEST
Position: {fen}
Top moves: {', '.join(best_moves[:3])}
Give a helpful hint without revealing the exact move."""
        
        return self._send_message(context)

    def explain_last_move(self, move: str, fen: str) -> str:
        """
        Explain the reasoning behind a move
        
        Args:
            move: The move to explain
            fen: Position after the move
            
        Returns:
            Explanation
        """
        context = f"""EXPLAIN REQUEST
Your last move: {move}
Resulting position: {fen}
Explain why you played this move and what you're planning."""
        
        return self._send_message(context)

    def analyze_position(self, fen: str, eval_cp: int, material_diff: Dict) -> str:
        """
        Provide position analysis
        
        Args:
            fen: Current position
            eval_cp: Evaluation in centipawns
            material_diff: Material difference
            
        Returns:
            Position analysis
        """
        context = f"""POSITION ANALYSIS
FEN: {fen}
Evaluation: {eval_cp/100:+.2f}
Material: {material_diff}
Analyze this position - what's happening strategically?"""
        
        return self._send_message(context)

    def game_over(self, result: str, reason: str) -> str:
        """
        React to game ending
        
        Args:
            result: Game result (win/loss/draw)
            reason: How game ended
            
        Returns:
            AI's game-end message
        """
        context = f"""GAME OVER
Result: {result}
Reason: {reason}
React to the game ending and offer brief thoughts."""
        
        return self._send_message(context)

    def _send_message(self, content: str, role: str = "user") -> str:
        """
        Send message to LM Studio API
        
        Args:
            content: Message content
            role: Message role (user/system/assistant)
            
        Returns:
            AI's response
        """
        try:
            # Add message to history
            if role != "system" or len(self.conversation_history) == 0:
                self.conversation_history.append(ChatMessage(role, content))
            
            # Trim history if too long
            if len(self.conversation_history) > self.max_history:
                # Keep system prompt, remove oldest messages
                system_msgs = [m for m in self.conversation_history if m.role == "system"]
                other_msgs = [m for m in self.conversation_history if m.role != "system"]
                self.conversation_history = system_msgs + other_msgs[-(self.max_history-len(system_msgs)):]
            
            # Prepare messages for API
            messages = [{"role": m.role, "content": m.content} for m in self.conversation_history]
            
            # Call LM Studio API
            response = requests.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 150,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_message = result['choices'][0]['message']['content'].strip()
                
                # Add AI response to history
                self.conversation_history.append(ChatMessage("assistant", ai_message))
                
                log.debug(f"LLM Response: {ai_message}")
                return ai_message
            else:
                log.error(f"LM Studio API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            log.error("Cannot connect to LM Studio. Is the server running?")
            return None
        except requests.exceptions.Timeout:
            log.error("LM Studio request timed out")
            return None
        except Exception as e:
            log.error(f"Error communicating with LM Studio: {e}")
            return None

    def check_connection(self) -> Tuple[bool, str]:
        """
        Check if LM Studio is accessible
        
        Returns:
            (success, message) tuple
        """
        try:
            response = requests.get(f"{self.api_url}/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get('data', []))
                return True, f"Connected! {model_count} model(s) available"
            else:
                return False, f"API returned status {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect. Is LM Studio running?"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def clear_history(self):
        """Clear conversation history (keeps system prompt)"""
        system_prompts = [m for m in self.conversation_history if m.role == "system"]
        self.conversation_history = system_prompts

    def extract_learnings_from_conversation(self, user_message: str, ai_response: str):
        """
        Extract learnings from conversation for memory
        
        Args:
            user_message: What the user said
            ai_response: What the AI responded
        """
        if not self.memory_manager:
            return
        
        user_lower = user_message.lower()
        
        # Detect personal information
        # Name
        if any(phrase in user_lower for phrase in ["my name is", "i'm ", "call me"]):
            # Simple name extraction (can be improved)
            for phrase in ["my name is ", "i'm ", "call me "]:
                if phrase in user_lower:
                    parts = user_lower.split(phrase)
                    if len(parts) > 1:
                        potential_name = parts[1].split()[0].strip('.,!?').title()
                        if len(potential_name) > 1 and len(potential_name) < 20:
                            self.memory_manager.update_player_name(potential_name)
                            break
        
        # Personal facts
        if any(phrase in user_lower for phrase in [
            "i live in", "i'm from", "i work", "i study", 
            "i love", "i like", "i prefer", "my favorite"
        ]):
            self.memory_manager.learn_personal_fact(user_message)
        
        # Chess preferences
        if any(phrase in user_lower for phrase in [
            "i like playing", "i prefer", "i usually play",
            "my favorite opening", "i enjoy"
        ]) and any(chess_term in user_lower for chess_term in [
            "opening", "defense", "gambit", "attack", "position",
            "e4", "d4", "sicilian", "french", "caro"
        ]):
            self.memory_manager.learn_personal_fact(f"Chess preference: {user_message}")
        
        # Detect memorable moments
        if any(phrase in user_lower for phrase in [
            "that was amazing", "that was incredible", "wow", "brilliant",
            "i'll remember this", "that was fun", "great game"
        ]):
            self.notable_moments.append(user_message)
        
        # Detect inside jokes or funny moments
        if any(phrase in user_lower for phrase in [
            "haha", "lol", "that's funny", "😂", "🤣"
        ]) or any(phrase in ai_response.lower() for phrase in ["haha", "😂", "🤣"]):
            if len(user_message) < 100:  # Keep it short
                self.memory_manager.add_inside_joke(user_message)
    
    def observe_move_quality(self, move: str, eval_before: Optional[int], 
                            eval_after: Optional[int], is_user_move: bool):
        """
        Observe and learn from move quality
        
        Args:
            move: The move played
            eval_before: Evaluation before move
            eval_after: Evaluation after move
            is_user_move: True if user's move
        """
        if not is_user_move or not eval_before or not eval_after:
            return
        
        # Calculate centipawn loss
        eval_change = eval_after - eval_before
        
        # Categorize move quality
        if abs(eval_change) < 15:
            # Good move
            if abs(eval_after) > 200:  # In a winning position
                self.player_observations.append(f"Strong endgame technique with {move}")
        elif abs(eval_change) < 50:
            # Inaccuracy
            pass  # Don't record minor inaccuracies
        elif abs(eval_change) < 100:
            # Mistake
            self.player_observations.append(f"Mistake with {move} (lost {abs(eval_change)/100:.1f} pawns)")
        else:
            # Blunder
            self.player_observations.append(f"Blunder with {move} (lost {abs(eval_change)/100:.1f} pawns)")
        
        # Detect tactical awareness
        if eval_change > 200:  # Found a strong tactic
            self.player_observations.append(f"Excellent tactical vision with {move}")
            self.notable_moments.append(f"Brilliant tactical shot: {move}")
    
    def finalize_game_memory(self, result: str, opening: str):
        """
        Finalize and save game to memory
        
        Args:
            result: Game result ('win', 'loss', 'draw' from AI perspective)
            opening: Opening name
        """
        if not self.memory_manager:
            return
        
        self.memory_manager.record_game_end(
            result=result,
            opening=opening,
            notable_moments=self.notable_moments[-10:],  # Last 10
            player_observations=self.player_observations
        )
        
        # Update friendship based on interaction quality
        if len(self.conversation_history) > 10:  # Good conversation
            self.memory_manager.memory.player_profile.friendship_level = min(
                10,
                self.memory_manager.memory.player_profile.friendship_level + 0.2
            )
            self.memory_manager._save_memory()
