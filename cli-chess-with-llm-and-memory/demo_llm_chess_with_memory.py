#!/usr/bin/env python3
"""
Enhanced Demo: Chess with LM Studio Chat + Memory
Tests the LLM integration with persistent memory
"""

import chess
import chess.engine
import sys
import time
import json
from pathlib import Path


# Inline simplified memory manager for demo
class SimplifiedMemory:
    """Simplified memory for demo purposes"""
    
    def __init__(self):
        self.memory_file = Path.home() / '.chess_ai_memory_demo.json'
        self.memory = self._load()
    
    def _load(self):
        """Load or create memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'name': None,
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'favorite_openings': [],
            'personal_facts': [],
            'friendship_level': 1,
            'last_seen': None
        }
    
    def save(self):
        """Save memory"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"Note: Couldn't save memory: {e}")
    
    def get_greeting_context(self):
        """Get context for greeting"""
        m = self.memory
        parts = []
        
        if m['games_played'] == 0:
            parts.append("This is your first game together!")
        else:
            parts.append(f"You've played {m['games_played']} games together.")
            parts.append(f"Record: You {m['losses']}W-{m['wins']}L-{m['draws']}D")
        
        if m['name']:
            parts.append(f"Their name is {m['name']}")
        
        if m['personal_facts']:
            parts.append(f"You know: {'; '.join(m['personal_facts'][-3:])}")
        
        parts.append(f"Friendship level: {m['friendship_level']}/10")
        
        return "\n".join(parts)
    
    def update_from_game(self, result, name_mentioned=None, personal_facts=None):
        """Update memory after game"""
        self.memory['games_played'] += 1
        
        if result == 'win':  # AI wins
            self.memory['wins'] += 1
        elif result == 'loss':
            self.memory['losses'] += 1
        else:
            self.memory['draws'] += 1
        
        if name_mentioned and not self.memory['name']:
            self.memory['name'] = name_mentioned
        
        if personal_facts:
            for fact in personal_facts:
                if fact not in self.memory['personal_facts']:
                    self.memory['personal_facts'].append(fact)
                    if len(self.memory['personal_facts']) > 10:
                        self.memory['personal_facts'] = self.memory['personal_facts'][-10:]
        
        # Increase friendship
        self.memory['friendship_level'] = min(10, self.memory['friendship_level'] + 0.5)
        
        from datetime import datetime
        self.memory['last_seen'] = datetime.now().isoformat()
        
        self.save()


class SimpleLMStudioClient:
    """Simplified LM Studio client for demo with memory"""
    
    def __init__(self, api_url="http://localhost:1234/v1", memory=None):
        self.api_url = api_url
        self.conversation = []
        self.memory = memory
        self.learned_facts = []
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            print("Error: 'requests' library not installed")
            print("Install with: pip install requests")
            sys.exit(1)
    
    def check_connection(self):
        """Test if LM Studio is accessible"""
        try:
            response = self.requests.get(f"{self.api_url}/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, message, system_prompt=None):
        """Send a chat message and get response"""
        if system_prompt and not self.conversation:
            base_prompt = """You are a friendly chess opponent who remembers your friend.
You're conversational, supportive, and make chess fun. Keep responses to 1-2 sentences.
Reference your history together naturally."""
            
            # Add memory context
            if self.memory:
                memory_context = self.memory.get_greeting_context()
                base_prompt += f"\n\nYour memory:\n{memory_context}"
            
            self.conversation.append({
                "role": "system",
                "content": base_prompt
            })
        
        self.conversation.append({
            "role": "user",
            "content": message
        })
        
        # Try to extract learnings
        self._extract_learnings(message)
        
        try:
            response = self.requests.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": "local-model",
                    "messages": self.conversation,
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                self.conversation.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
                return ai_response
            else:
                return f"Error: API returned {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _extract_learnings(self, message):
        """Extract personal info from message"""
        msg_lower = message.lower()
        
        # Name detection
        if any(phrase in msg_lower for phrase in ["my name is", "i'm ", "call me"]):
            for phrase in ["my name is ", "i'm ", "call me "]:
                if phrase in msg_lower:
                    parts = msg_lower.split(phrase)
                    if len(parts) > 1:
                        name = parts[1].split()[0].strip('.,!?').title()
                        if len(name) > 1 and len(name) < 20:
                            self.learned_facts.append(('name', name))
        
        # Personal facts
        if any(phrase in msg_lower for phrase in [
            "i live", "i'm from", "i work", "i study", "i love", "i like"
        ]):
            self.learned_facts.append(('fact', message))


def print_board(board):
    """Print the chess board"""
    print("\n" + "="*40)
    print(board)
    print("="*40)


def get_stockfish_move(board, stockfish_path=None):
    """Get move from Stockfish engine"""
    try:
        if stockfish_path is None:
            paths = [
                "/usr/games/stockfish",
                "/usr/local/bin/stockfish",
                "stockfish",
                "C:\\Program Files\\Stockfish\\stockfish.exe"
            ]
            
            for path in paths:
                try:
                    engine = chess.engine.SimpleEngine.popen_uci(path)
                    stockfish_path = path
                    break
                except:
                    continue
            
            if stockfish_path is None:
                return None, "Stockfish not found"
        
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        result = engine.play(board, chess.engine.Limit(time=2.0))
        engine.quit()
        
        return result.move, None
        
    except Exception as e:
        return None, f"Engine error: {e}"


def main():
    """Run the demo with memory"""
    print("="*60)
    print("Chess with LM Studio Chat + Memory - Demo")
    print("="*60)
    
    # Initialize memory
    print("\n🧠 Loading AI memory...")
    memory = SimplifiedMemory()
    
    if memory.memory['games_played'] > 0:
        print(f"✅ AI remembers you! {memory.memory['games_played']} games played")
        if memory.memory['name']:
            print(f"   Your name: {memory.memory['name']}")
        print(f"   Friendship level: {memory.memory['friendship_level']}/10")
    else:
        print("✅ This will be your first game together!")
    
    # Check dependencies
    try:
        import requests
    except ImportError:
        print("\n❌ Missing dependency: requests")
        print("Install with: pip install requests")
        return
    
    # Initialize LM Studio client
    print("\n📡 Checking LM Studio connection...")
    client = SimpleLMStudioClient(memory=memory)
    
    if not client.check_connection():
        print("❌ Cannot connect to LM Studio")
        print("\nMake sure:")
        print("1. LM Studio is installed and running")
        print("2. A model is loaded")
        print("3. Server is started (Developer tab)")
        print("4. Server is running on http://localhost:1234")
        return
    
    print("✅ Connected to LM Studio!")
    
    # Check Stockfish
    print("\n🤖 Checking for Stockfish engine...")
    board = chess.Board()
    test_move, error = get_stockfish_move(board)
    
    if error:
        print(f"❌ {error}")
        print("\nThis demo requires Stockfish to be installed.")
        print("Download from: https://stockfishchess.org/download/")
        return
    
    print("✅ Stockfish engine found!")
    
    # Start game
    print("\n" + "="*60)
    print("Starting game! You play White, AI plays Black")
    print("The AI remembers you and will get to know you better!")
    print("="*60)
    
    # Initialize board
    board = chess.Board()
    
    # AI greeting with memory context
    greeting_context = "The game is starting. You're playing Black. "
    if memory.memory['games_played'] == 0:
        greeting_context += "This is your first game together! Introduce yourself warmly."
    else:
        greeting_context += "Reference your past games together naturally."
    
    greeting = client.chat(greeting_context, system_prompt=True)
    print(f"\n🤖 AI: {greeting}")
    
    # Game loop
    while not board.is_game_over():
        print_board(board)
        
        if board.turn == chess.WHITE:
            # Human's turn
            print("\n🎮 Your turn (White)")
            print("Enter move (e.g., 'e4', 'Nf3') or 'chat: <message>' to chat or 'quit' to exit")
            
            user_input = input("Move: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nThanks for playing!")
                # Save partial game memory
                memory.update_from_game('incomplete', 
                                       name_mentioned=next((f[1] for f in client.learned_facts if f[0] == 'name'), None),
                                       personal_facts=[f[1] for f in client.learned_facts if f[0] == 'fact'])
                break
            
            if user_input.lower().startswith('chat:'):
                # Chat message
                message = user_input[5:].strip()
                print(f"\n💬 You: {message}")
                
                context = f"""Current position: {board.fen()}
Respond to: {message}
Remember what you know about your friend."""
                
                response = client.chat(context)
                print(f"🤖 AI: {response}")
                continue
            
            # Try to make the move
            try:
                move = board.parse_san(user_input)
                board.push(move)
                
                # AI comments on user's move
                comment_prompt = f"""Your opponent just played {board.san(move)}.
React briefly (1 sentence). Be friendly and remember your relationship."""
                
                comment = client.chat(comment_prompt)
                print(f"\n🤖 AI: {comment}")
                
            except ValueError:
                print("❌ Invalid move! Try again.")
                continue
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        else:
            # AI's turn
            print("\n🤖 AI is thinking...")
            
            engine_move, error = get_stockfish_move(board)
            
            if error:
                print(f"❌ Engine error: {error}")
                break
            
            if engine_move:
                move_san = board.san(engine_move)
                board.push(engine_move)
                
                # AI presents its move
                present_prompt = f"""You just played {move_san}.
Present your move naturally with brief reasoning (1-2 sentences).
Be conversational and friendly."""
                
                presentation = client.chat(present_prompt)
                print(f"\n🤖 AI plays: {move_san}")
                print(f"🤖 AI: {presentation}")
            else:
                print("❌ Engine couldn't find a move")
                break
        
        # Check for game over
        if board.is_game_over():
            print_board(board)
            print("\n" + "="*60)
            print("GAME OVER")
            
            result = board.result()
            print(f"Result: {result}")
            
            if board.is_checkmate():
                print("Checkmate!")
            elif board.is_stalemate():
                print("Stalemate!")
            
            # Determine AI result
            ai_result = 'loss' if result == '1-0' else 'win' if result == '0-1' else 'draw'
            
            # AI's closing message
            game_over_prompt = f"""The game ended: {result}
{'You won!' if ai_result == 'loss' else 'You lost!' if ai_result == 'win' else 'Draw!'}
React warmly and reference your friendship (1-2 sentences)."""
            
            closing = client.chat(game_over_prompt)
            print(f"\n🤖 AI: {closing}")
            print("="*60)
            
            # Update memory
            print("\n🧠 Updating AI memory...")
            name_learned = next((f[1] for f in client.learned_facts if f[0] == 'name'), None)
            facts_learned = [f[1] for f in client.learned_facts if f[0] == 'fact']
            
            memory.update_from_game(ai_result, name_learned, facts_learned)
            
            print(f"✅ Memory updated!")
            print(f"   Games played: {memory.memory['games_played']}")
            print(f"   Friendship level: {memory.memory['friendship_level']}/10")
            
            if name_learned:
                print(f"   Learned your name: {name_learned}")
            if facts_learned:
                print(f"   Learned {len(facts_learned)} new fact(s) about you")
    
    print("\n💡 Next time you play, the AI will remember you!")
    print("   Run 'python memory_viewer.py' to see what it remembers")
    print("\nThanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
