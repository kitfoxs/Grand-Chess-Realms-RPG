#!/usr/bin/env python3
"""
Standalone Demo: Chess with LM Studio Chat
Tests the LLM integration without full cli-chess installation
"""

import chess
import chess.engine
import sys
import time


class SimpleLMStudioClient:
    """Simplified LM Studio client for demo purposes"""
    
    def __init__(self, api_url="http://localhost:1234/v1"):
        self.api_url = api_url
        self.conversation = []
        
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
            self.conversation.append({
                "role": "system",
                "content": system_prompt
            })
        
        self.conversation.append({
            "role": "user",
            "content": message
        })
        
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


def print_board(board):
    """Print the chess board"""
    print("\n" + "="*40)
    print(board)
    print("="*40)


def get_stockfish_move(board, stockfish_path=None):
    """Get move from Stockfish engine"""
    try:
        # Try to use system Stockfish if available
        if stockfish_path is None:
            # Common Stockfish locations
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
    """Run the demo"""
    print("="*60)
    print("Chess with LM Studio Chat - Demo")
    print("="*60)
    
    # Check dependencies
    try:
        import requests
    except ImportError:
        print("\n❌ Missing dependency: requests")
        print("Install with: pip install requests")
        return
    
    # Initialize LM Studio client
    print("\n📡 Checking LM Studio connection...")
    client = SimpleLMStudioClient()
    
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
    print("="*60)
    
    # Initialize board
    board = chess.Board()
    
    # System prompt for the AI
    system_prompt = """You are a friendly chess opponent playing as Black. 
You're conversational, supportive, and make chess fun. React to moves naturally,
comment on the game, and engage in friendly banter. Keep responses to 1-2 sentences.
You use Stockfish to calculate your moves."""
    
    # AI greeting
    greeting = client.chat(
        "The game is starting. You're playing Black. Greet your opponent briefly.",
        system_prompt=system_prompt
    )
    print(f"\n🤖 AI: {greeting}")
    
    move_count = 0
    
    # Game loop
    while not board.is_game_over():
        print_board(board)
        
        if board.turn == chess.WHITE:
            # Human's turn
            print("\n🎮 Your turn (White)")
            print("Enter move in SAN (e.g., 'e4', 'Nf3') or UCI (e.g., 'e2e4')")
            print("Type 'quit' to exit, 'chat: <message>' to chat")
            
            user_input = input("Move: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nThanks for playing!")
                break
            
            if user_input.lower().startswith('chat:'):
                # Chat message
                message = user_input[5:].strip()
                print(f"\n💬 You: {message}")
                
                context = f"""Current position: {board.fen()}
Last moves: {' '.join([board.san(m) for m in list(board.move_stack)[-5:]])}
Respond to: {message}"""
                
                response = client.chat(context)
                print(f"🤖 AI: {response}")
                continue
            
            # Try to make the move
            try:
                move = board.parse_san(user_input)
                board.push(move)
                move_count += 1
                
                # AI comments on user's move
                comment_prompt = f"""Your opponent (White) just played {board.san(move)}.
Position: {board.fen()}
React briefly to this move (1 sentence)."""
                
                comment = client.chat(comment_prompt)
                print(f"\n🤖 AI: {comment}")
                
            except ValueError:
                print("❌ Invalid move! Try again.")
                continue
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        else:
            # AI's turn (Black)
            print("\n🤖 AI is thinking...")
            
            # Get move from Stockfish
            engine_move, error = get_stockfish_move(board)
            
            if error:
                print(f"❌ Engine error: {error}")
                break
            
            if engine_move:
                move_san = board.san(engine_move)
                board.push(engine_move)
                move_count += 1
                
                # AI presents its move
                present_prompt = f"""You just played {move_san}.
Position: {board.fen()}
Present your move naturally with brief reasoning (1-2 sentences)."""
                
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
            elif board.is_insufficient_material():
                print("Insufficient material!")
            
            # AI's closing message
            game_over_prompt = f"""The game ended: {result}
{'You won!' if result == '0-1' else 'You lost!' if result == '1-0' else 'Draw!'}
React to the game ending (1-2 sentences)."""
            
            closing = client.chat(game_over_prompt)
            print(f"\n🤖 AI: {closing}")
            print("="*60)
    
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
