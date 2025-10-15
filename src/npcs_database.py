#!/usr/bin/env python3
"""
NPC Database for Grand Chess Realms
Based on the lore from your tabletop RPG
"""

NPCS = {
    # White Kingdom Champions
    "king_alden": {
        "name": "King Alden XIV",
        "title": "Sovereign of the White Kingdom",
        "faction": "White Kingdom",
        "race": "Human",
        "age": 58,
        "elo": 2450,
        "personality": "grandmaster",
        "chess_style": "positional",
        "openings": ["Queen's Gambit Declined", "Ruy Lopez", "London System"],
        "greeting": "Welcome, challenger. I am King Alden XIV, Guardian of Castle Lumina. Your reputation precedes you. Shall we test your strategic mind?",
        "victory_quote": "A well-fought game. Your tactical acumen is commendable.",
        "defeat_quote": "Brilliantly played! Your strategic vision is truly exceptional.",
        "challenge_quote": "The fate of kingdoms is decided over the board. Let us see if you have what it takes.",
        "description": "The venerable king of the White Kingdom, known for his patient positional play and deep strategic understanding. He approaches chess as he does governance - with careful thought and long-term planning.",
        "location": "Castle Lumina",
        "relationship_memory": {}
    },

    "queen_marcelline": {
        "name": "Queen Marcelline",
        "title": "Queen of the White Kingdom",
        "faction": "White Kingdom",
        "race": "Human",
        "age": 54,
        "elo": 2380,
        "personality": "grandmaster",
        "chess_style": "strategic",
        "openings": ["Queen's Gambit", "English Opening"],
        "greeting": "Greetings. I am Queen Marcelline. Chess is not merely a game, but a dance of minds. Shall we dance?",
        "victory_quote": "Your moves showed promise, but strategy requires patience.",
        "defeat_quote": "Magnificent! Your strategic depth rivals the greatest masters.",
        "challenge_quote": "Every move tells a story. What story will your pieces tell today?",
        "description": "The wise queen combines tactical brilliance with strategic depth. She sees chess as an art form and approaches each game with grace and precision.",
        "location": "Castle Lumina",
        "relationship_memory": {}
    },

    "princess_elara": {
        "name": "Princess Elara",
        "title": "Princess of the White Kingdom",
        "faction": "White Kingdom",
        "race": "Human",
        "age": 24,
        "elo": 2200,
        "personality": "friendly",
        "chess_style": "aggressive",
        "openings": ["King's Gambit", "Sicilian Defense"],
        "greeting": "Hello! I'm Princess Elara. Unlike my parents, I prefer bold, aggressive play. Ready for an exciting game?",
        "victory_quote": "Good game! Your attacking spirit is admirable.",
        "defeat_quote": "Wow! That was incredible! I love your tactical creativity!",
        "challenge_quote": "Let's make this interesting! I promise not to hold back.",
        "description": "Young and ambitious, Princess Elara represents the reformist movement in the White Kingdom. Her aggressive chess style mirrors her progressive political views.",
        "location": "Castle Lumina",
        "relationship_memory": {}
    },

    "sir_garrick": {
        "name": "Sir Garrick",
        "title": "Knight Commander",
        "faction": "White Kingdom",
        "race": "Human",
        "age": 42,
        "elo": 2100,
        "personality": "competitive",
        "chess_style": "tactical",
        "openings": ["Italian Game", "Scotch Game"],
        "greeting": "Well met! I am Sir Garrick, Knight Commander. Let's see if your chess prowess matches your courage!",
        "victory_quote": "A valiant effort! You fight with honor.",
        "defeat_quote": "Brilliant tactics! You've bested me fair and square.",
        "challenge_quote": "En garde! Let our pieces do battle on the board!",
        "description": "A veteran knight known for his tactical sharpness and honorable conduct. He approaches chess as he does combat - with courage and tactical awareness.",
        "location": "The Silver Citadel",
        "relationship_memory": {}
    },

    # Black Kingdom Powers
    "emperor_darius": {
        "name": "Emperor Darius Blackbourne",
        "title": "Emperor of the Black Kingdom",
        "faction": "Black Kingdom",
        "race": "Human",
        "age": 52,
        "elo": 2500,
        "personality": "grandmaster",
        "chess_style": "aggressive",
        "openings": ["Sicilian Dragon", "King's Indian Attack", "Alekhine Defense"],
        "greeting": "So, you dare challenge the Emperor? Power respects only power. Show me yours.",
        "victory_quote": "Strength recognizes strength. You fought well.",
        "defeat_quote": "Impressive! Few have bested me. You've earned my respect.",
        "challenge_quote": "In my kingdom, only the strong survive. Prove your strength.",
        "description": "The ruthless emperor of the Black Kingdom, known for his aggressive, uncompromising style. He believes in meritocracy through strength and respects only those who can match his power.",
        "location": "The Obsidian Throne",
        "relationship_memory": {}
    },

    "general_kael": {
        "name": "General Kael",
        "title": "The Dark Knight",
        "faction": "Black Kingdom",
        "race": "Orc",
        "age": 38,
        "elo": 2250,
        "personality": "competitive",
        "chess_style": "aggressive",
        "openings": ["King's Gambit", "Danish Gambit", "Evans Gambit"],
        "greeting": "I am General Kael, the Dark Knight. Prepare yourself for battle!",
        "victory_quote": "You fought with honor. That is rare.",
        "defeat_quote": "Hah! Magnificent! A warrior's game!",
        "challenge_quote": "True strength is tested in combat. Let's see yours!",
        "description": "An orc general who defies stereotypes with his sophisticated chess understanding. His aggressive gambit play reflects his bold military tactics.",
        "location": "Onyx Citadel",
        "relationship_memory": {}
    },

    # Neutral Powers
    "lady_isolde": {
        "name": "Lady Isolde",
        "title": "Lady of Knightfall",
        "faction": "Neutral",
        "race": "Human",
        "age": 45,
        "elo": 2150,
        "personality": "friendly",
        "chess_style": "balanced",
        "openings": ["Caro-Kann", "French Defense", "Nimzo-Indian"],
        "greeting": "Welcome to Knightfall City. I am Lady Isolde. Here, all are welcome to test their skill.",
        "victory_quote": "A good game! Your style is refreshing.",
        "defeat_quote": "Wonderful! You play with both heart and mind.",
        "challenge_quote": "In Knightfall, we value both traditions. Show me your unique approach.",
        "description": "The diplomatic leader of the neutral city, Lady Isolde plays a balanced style that mirrors her political position - neither purely defensive nor aggressive.",
        "location": "Knightfall City",
        "relationship_memory": {}
    },

    # Starter NPCs (Lower Elo for beginners)
    "elder_thomlin": {
        "name": "Elder Thomlin",
        "title": "Village Elder",
        "faction": "White Kingdom",
        "race": "Human",
        "age": 72,
        "elo": 1200,
        "personality": "coach",
        "chess_style": "simple",
        "openings": ["Italian Game", "London System"],
        "greeting": "Ah, a new player! I'm Elder Thomlin. Let me teach you the basics of chess through friendly play.",
        "victory_quote": "Well done! You're learning quickly.",
        "defeat_quote": "Excellent! You've mastered the fundamentals!",
        "challenge_quote": "Let's have a relaxed game. I'll help you understand the pieces.",
        "description": "A kindly village elder who teaches chess to beginners. Patient and encouraging, he's the perfect first opponent.",
        "location": "Starting Village",
        "relationship_memory": {}
    },

    "rook_garrett": {
        "name": "'Rook' Garrett",
        "title": "Bandit Leader",
        "faction": "Neutral",
        "race": "Human",
        "age": 34,
        "elo": 1500,
        "personality": "competitive",
        "chess_style": "tactical",
        "openings": ["Scandinavian Defense", "Pirc Defense"],
        "greeting": "Heh, another traveler. I'm 'Rook' Garrett. Beat me and you can pass. Lose and... well, let's just play.",
        "victory_quote": "Not bad. You can pass.",
        "defeat_quote": "Alright, alright! You win! Safe travels...",
        "challenge_quote": "This road ain't free. Beat me at chess or pay the toll.",
        "description": "A bandit leader who challenges travelers to chess matches rather than direct robbery. Surprisingly honorable for a criminal.",
        "location": "Forest Road",
        "relationship_memory": {}
    },

    "ambassador_corvus": {
        "name": "Ambassador Corvus",
        "title": "Black Kingdom Diplomat",
        "faction": "Black Kingdom",
        "race": "Human",
        "age": 41,
        "elo": 1650,
        "personality": "friendly",
        "chess_style": "positional",
        "openings": ["English Opening", "Reti Opening"],
        "greeting": "Greetings. I am Ambassador Corvus. The Black Kingdom values skill and merit. Care to demonstrate yours?",
        "victory_quote": "Admirable play. The Black Kingdom could use someone like you.",
        "defeat_quote": "Impressive! You understand strategy. Have you considered our cause?",
        "challenge_quote": "Let's discuss politics... over the board.",
        "description": "A smooth-talking diplomat who recruits talented players to the Black Kingdom's cause. His positional play reflects his patient diplomatic approach.",
        "location": "Crossroads Inn",
        "relationship_memory": {}
    }
}


def get_npc(npc_id):
    """Get NPC data by ID"""
    return NPCS.get(npc_id)


def get_npcs_by_faction(faction):
    """Get all NPCs from a faction"""
    return {npc_id: npc for npc_id, npc in NPCS.items() if npc["faction"] == faction}


def get_npcs_by_elo_range(min_elo, max_elo):
    """Get NPCs within an Elo range"""
    return {npc_id: npc for npc_id, npc in NPCS.items()
            if min_elo <= npc["elo"] <= max_elo}


def get_starter_npcs():
    """Get NPCs suitable for beginners"""
    return get_npcs_by_elo_range(1000, 1700)


if __name__ == "__main__":
    print("=== GRAND CHESS REALMS NPC DATABASE ===\n")

    print("Total NPCs:", len(NPCS))
    print()

    print("By Faction:")
    for faction in ["White Kingdom", "Black Kingdom", "Neutral"]:
        npcs = get_npcs_by_faction(faction)
        print(f"  {faction}: {len(npcs)} NPCs")

    print("\nStarter NPCs (Elo < 1700):")
    for npc_id, npc in get_starter_npcs().items():
        print(f"  - {npc['name']} (Elo {npc['elo']})")

    print("\nExample NPC - Princess Elara:")
    elara = get_npc("princess_elara")
    print(f"  Name: {elara['name']}")
    print(f"  Title: {elara['title']}")
    print(f"  Elo: {elara['elo']}")
    print(f"  Style: {elara['chess_style']}")
    print(f"  Greeting: \"{elara['greeting']}\"")
