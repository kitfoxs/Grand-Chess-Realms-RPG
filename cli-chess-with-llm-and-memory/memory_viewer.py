#!/usr/bin/env python3
"""
Memory Viewer - See what your AI chess opponent remembers about you!
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_memory(memory_path=None):
    """Load memory file"""
    if memory_path is None:
        # Try default locations
        import os
        if os.name == 'nt':  # Windows
            base = os.getenv('APPDATA', os.path.expanduser('~'))
            memory_path = os.path.join(base, 'cli-chess', 'memory', 'player_memory.json')
        else:  # Linux/Mac
            memory_path = os.path.expanduser('~/.config/cli-chess/memory/player_memory.json')
    
    path = Path(memory_path)
    if not path.exists():
        print(f"❌ No memory file found at {memory_path}")
        print("\nThe AI hasn't met you yet! Play a game first.")
        return None
    
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading memory: {e}")
        return None


def format_date(iso_date):
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%B %d, %Y at %H:%M")
    except:
        return iso_date


def print_memory_report(memory):
    """Print a nice formatted memory report"""
    print("\n" + "="*70)
    print("🧠 YOUR AI CHESS FRIEND'S MEMORY OF YOU")
    print("="*70)
    
    profile = memory.get('player_profile', {})
    
    # Basic info
    print("\n📋 BASIC INFORMATION")
    print("-" * 70)
    name = profile.get('name', 'Friend')
    print(f"  Name: {name}")
    print(f"  Friendship Level: {profile.get('friendship_level', 1)}/10 {'❤️' * int(profile.get('friendship_level', 1))}")
    print(f"  Skill Level: {profile.get('skill_level', 'unknown').title()}")
    
    # Timeline
    print("\n📅 RELATIONSHIP TIMELINE")
    print("-" * 70)
    if memory.get('first_met'):
        print(f"  First met: {format_date(memory['first_met'])}")
    if memory.get('last_seen'):
        print(f"  Last seen: {format_date(memory['last_seen'])}")
    print(f"  Games played together: {memory.get('games_played', 0)}")
    
    # Game record
    print("\n🏆 GAME RECORD")
    print("-" * 70)
    wins = memory.get('total_wins', 0)
    losses = memory.get('total_losses', 0)
    draws = memory.get('total_draws', 0)
    total = wins + losses + draws
    
    if total > 0:
        print(f"  AI Wins: {wins} ({wins/total*100:.1f}%)")
        print(f"  AI Losses: {losses} ({losses/total*100:.1f}%)")
        print(f"  Draws: {draws} ({draws/total*100:.1f}%)")
    else:
        print("  No games completed yet")
    
    # Playing style
    if profile.get('playing_style'):
        print("\n♟️  YOUR PLAYING STYLE")
        print("-" * 70)
        for style in profile['playing_style']:
            print(f"  • {style.title()}")
    
    # Preferred openings
    if profile.get('preferred_openings'):
        print("\n📖 YOUR FAVORITE OPENINGS")
        print("-" * 70)
        for opening in profile['preferred_openings'][:5]:
            print(f"  • {opening}")
    
    # Personal facts
    if profile.get('personal_facts'):
        print("\n💭 WHAT THE AI KNOWS ABOUT YOU")
        print("-" * 70)
        for fact in profile['personal_facts'][-10:]:
            print(f"  • {fact}")
    
    # Interests
    if profile.get('interests'):
        print("\n🎯 YOUR CHESS INTERESTS")
        print("-" * 70)
        for interest in profile['interests']:
            print(f"  • {interest}")
    
    # Inside jokes
    if profile.get('inside_jokes'):
        print("\n😄 INSIDE JOKES YOU SHARE")
        print("-" * 70)
        for joke in profile['inside_jokes'][-5:]:
            print(f"  • {joke}")
    
    # Memorable moments
    if memory.get('favorite_moments'):
        print("\n⭐ FAVORITE MOMENTS TOGETHER")
        print("-" * 70)
        for moment in memory['favorite_moments'][-5:]:
            print(f"  • {moment}")
    
    # Preferences
    print("\n⚙️  YOUR PREFERENCES")
    print("-" * 70)
    print(f"  Likes banter: {'Yes' if profile.get('likes_banter', True) else 'No'}")
    print(f"  Wants hints: {'Yes' if profile.get('wants_hints', True) else 'No'}")
    print(f"  Prefers explanations: {'Yes' if profile.get('prefers_explanations', True) else 'No'}")
    print(f"  Sensitivity level: {profile.get('sensitivity_level', 'medium').title()}")
    
    # Recent games
    game_history = memory.get('game_history', [])
    if game_history:
        print("\n🎮 RECENT GAMES")
        print("-" * 70)
        for game in game_history[-5:]:
            result_emoji = "🏆" if game['result'] == 'loss' else "😔" if game['result'] == 'win' else "🤝"
            print(f"\n  {result_emoji} {game['date']} - {game['result'].title()} (AI perspective)")
            print(f"     Opening: {game['opening']}")
            
            if game.get('notable_moments'):
                print(f"     Notable: {game['notable_moments'][0]}")
            
            if game.get('player_skill_indicators'):
                print(f"     Observations: {', '.join(game['player_skill_indicators'][:2])}")
    
    print("\n" + "="*70)
    print("\n💡 The AI uses this information to make your games more personal!")
    print("   It remembers your preferences, learns your style, and builds")
    print("   a friendship with you over time.\n")


def interactive_menu(memory):
    """Interactive menu for memory operations"""
    while True:
        print("\n" + "="*70)
        print("MEMORY MANAGEMENT")
        print("="*70)
        print("\n1. View full memory report")
        print("2. View stats summary")
        print("3. Export memory to file")
        print("4. Reset memory (⚠️  Warning: Deletes everything)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            print_memory_report(memory)
        elif choice == '2':
            print_stats_summary(memory)
        elif choice == '3':
            export_memory(memory)
        elif choice == '4':
            confirm = input("\n⚠️  This will delete ALL memory! Type 'RESET' to confirm: ")
            if confirm == 'RESET':
                reset_memory()
                print("✅ Memory reset successfully")
                break
            else:
                print("❌ Reset cancelled")
        elif choice == '5':
            print("\nGoodbye! 👋")
            break
        else:
            print("❌ Invalid option")


def print_stats_summary(memory):
    """Print quick stats summary"""
    profile = memory.get('player_profile', {})
    
    print("\n" + "="*70)
    print("QUICK STATS")
    print("="*70)
    print(f"\nName: {profile.get('name', 'Friend')}")
    print(f"Friendship: {profile.get('friendship_level', 1)}/10")
    print(f"Games: {memory.get('games_played', 0)}")
    print(f"Record: {memory.get('total_losses', 0)}W-{memory.get('total_wins', 0)}L-{memory.get('total_draws', 0)}D (Your perspective)")
    print(f"Skill: {profile.get('skill_level', 'unknown').title()}")
    print(f"Personal facts stored: {len(profile.get('personal_facts', []))}")
    print(f"Inside jokes: {len(profile.get('inside_jokes', []))}")
    print(f"Memorable moments: {len(memory.get('favorite_moments', []))}")


def export_memory(memory):
    """Export memory to a file"""
    filename = input("\nEnter filename (e.g., my_memory.json): ").strip()
    if not filename:
        filename = "chess_memory_export.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(memory, f, indent=2)
        print(f"✅ Memory exported to {filename}")
    except Exception as e:
        print(f"❌ Error exporting: {e}")


def reset_memory():
    """Reset memory file"""
    import os
    
    if os.name == 'nt':  # Windows
        base = os.getenv('APPDATA', os.path.expanduser('~'))
        memory_path = os.path.join(base, 'cli-chess', 'memory', 'player_memory.json')
    else:  # Linux/Mac
        memory_path = os.path.expanduser('~/.config/cli-chess/memory/player_memory.json')
    
    try:
        if Path(memory_path).exists():
            Path(memory_path).unlink()
            print(f"✅ Deleted {memory_path}")
    except Exception as e:
        print(f"❌ Error deleting memory: {e}")


def main():
    """Main function"""
    print("\n🧠 AI Chess Memory Viewer")
    print("=" * 70)
    
    # Check if memory path provided
    memory_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Load memory
    memory = load_memory(memory_path)
    
    if memory is None:
        return
    
    # Show report or interactive menu
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_menu(memory)
    else:
        print_memory_report(memory)
        
        print("\n💡 Run with --interactive for more options:")
        print("   python memory_viewer.py --interactive")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
