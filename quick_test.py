#!/usr/bin/env python3
"""Quick test of all components"""

import sys
import asyncio

print("="*60)
print("GRAND CHESS REALMS - QUICK TEST")
print("="*60)

# Test 1: Imports
print("\n1. Testing imports...")
try:
    from chessnut_board import ChessnutBoard
    from ai_opponent import AIOpponent
    import chess
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Board class
print("\n2. Testing board class...")
try:
    board = ChessnutBoard()
    print("   ✅ ChessnutBoard initialized")
except Exception as e:
    print(f"   ❌ Board error: {e}")
    sys.exit(1)

# Test 3: AI class
print("\n3. Testing AI class...")
try:
    ai = AIOpponent(name="Test AI", elo=1500)
    print("   ✅ AIOpponent initialized")
except Exception as e:
    print(f"   ❌ AI error: {e}")
    sys.exit(1)

# Test 4: Chess logic
print("\n4. Testing chess logic...")
try:
    game = chess.Board()
    move = chess.Move.from_uci("e2e4")
    san = game.san(move)  # Get notation before pushing
    game.push(move)
    print(f"   ✅ Chess logic works: {san}")
except Exception as e:
    print(f"   ❌ Chess error: {e}")
    sys.exit(1)

# Test 5: NPC database
print("\n5. Testing NPC database...")
try:
    sys.path.insert(0, 'src')
    from npcs_database import NPCS, get_npc
    elara = get_npc("princess_elara")
    print(f"   ✅ NPCs loaded: {len(NPCS)} characters")
    print(f"   ✅ Sample NPC: {elara['name']} (Elo {elara['elo']})")
except Exception as e:
    print(f"   ❌ NPC error: {e}")
    sys.exit(1)

# Test 6: Game Master
print("\n6. Testing Game Master...")
try:
    from game_master import GameMaster
    gm = GameMaster()
    gm.set_player_name("Test Player")
    print("   ✅ Game Master initialized")
except Exception as e:
    print(f"   ❌ GM error: {e}")
    sys.exit(1)

# Test 7: Stockfish
print("\n7. Testing Stockfish...")
try:
    import subprocess
    result = subprocess.run(['which', 'stockfish'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ Stockfish found: {result.stdout.strip()}")
    else:
        print("   ⚠️  Stockfish not found (games will still work)")
except Exception as e:
    print(f"   ⚠️  Could not check Stockfish: {e}")

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nReady to play:")
print("  python3 chess_game.py        - Simple chess")
print("  python3 ai_chess_game.py     - AI opponent")
print("  python3 chess_rpg.py         - Full RPG")
print()
