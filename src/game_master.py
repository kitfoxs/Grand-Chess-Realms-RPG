#!/usr/bin/env python3
"""
Game Master - AI-powered narrator for Grand Chess Realms
Uses LM Studio to generate dynamic narrative
"""

import requests
import random


class GameMaster:
    """AI-powered game master for RPG narration"""

    def __init__(self, lm_studio_url="http://localhost:1234/v1"):
        self.lm_studio_url = lm_studio_url
        self.conversation_history = []
        self.world_state = {
            "location": "Castle Lumina",
            "faction_reputation": {"White Kingdom": 0, "Black Kingdom": 0, "Neutral": 0},
            "player_name": "Traveler",
            "quests_completed": [],
            "npcs_met": [],
            "games_won": 0,
            "games_lost": 0
        }

    def set_player_name(self, name):
        """Set the player's name"""
        self.world_state["player_name"] = name

    def update_location(self, location):
        """Update current location"""
        self.world_state["location"] = location

    def record_game_result(self, npc_name, won):
        """Record result of a chess game"""
        if won:
            self.world_state["games_won"] += 1
        else:
            self.world_state["games_lost"] += 1

        if npc_name not in self.world_state["npcs_met"]:
            self.world_state["npcs_met"].append(npc_name)

    def _build_system_prompt(self):
        """Build system prompt with world context"""
        return f"""You are the Game Master for Grand Chess Realms, a chess-based RPG.

WORLD CONTEXT:
- Location: {self.world_state['location']}
- Player: {self.world_state['player_name']}
- Games Won: {self.world_state['games_won']}
- Games Lost: {self.world_state['games_lost']}
- NPCs Met: {', '.join(self.world_state['npcs_met']) or 'None yet'}

STYLE GUIDELINES:
- Write in immersive, descriptive prose
- Keep responses concise (2-4 sentences)
- Emphasize chess themes and imagery
- Make the player feel like a hero in a chess world
- Be dramatic but not overly verbose
- Reference past events when relevant

Your role is to narrate the adventure, describe scenes, and bring the world to life."""

    def narrate(self, prompt, style="descriptive", max_tokens=150):
        """Generate narrative using LM Studio"""
        try:
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
            ]

            # Add conversation history (last 4 exchanges)
            messages.extend(self.conversation_history[-8:])

            # Add current prompt
            messages.append({"role": "user", "content": prompt})

            # Call LM Studio
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "model": "local-model",
                    "messages": messages,
                    "temperature": 0.8,  # More creative for narration
                    "max_tokens": max_tokens,
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                narration = data["choices"][0]["message"]["content"].strip()

                # Update history
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": narration})

                return narration
            else:
                return None

        except requests.exceptions.ConnectionError:
            # LM Studio not running - use fallback
            return self._fallback_narration(prompt, style)
        except Exception as e:
            return self._fallback_narration(prompt, style)

    def _fallback_narration(self, prompt, style):
        """Fallback narration when LM Studio unavailable"""
        # Simple template-based narration
        if "welcome" in prompt.lower():
            return f"Welcome to the Grand Chess Realms, {self.world_state['player_name']}! Your journey begins at {self.world_state['location']}, where legends are born over the chessboard."

        elif "victory" in prompt.lower() or "won" in prompt.lower():
            phrases = [
                "A brilliant victory! Your strategic prowess shines through.",
                "The pieces fall in your favor. Well played!",
                "Your opponent concedes. Victory is yours!",
            ]
            return random.choice(phrases)

        elif "defeat" in prompt.lower() or "lost" in prompt.lower():
            phrases = [
                "Defeat tastes bitter, but wisdom grows from such losses.",
                "Your opponent's strategy proves superior this time.",
                "A hard-fought game, though fortune favors your opponent today.",
            ]
            return random.choice(phrases)

        else:
            return "The adventure continues..."

    def describe_location(self, location_name):
        """Describe a location"""
        prompt = f"Describe {location_name} in the Grand Chess Realms. Set the scene for the player."
        return self.narrate(prompt)

    def introduce_npc(self, npc_data):
        """Introduce an NPC"""
        prompt = f"The player encounters {npc_data['name']}, {npc_data['title']} of {npc_data['faction']}. {npc_data['description']} Describe this encounter dramatically."
        return self.narrate(prompt)

    def describe_chess_battle_start(self, npc_name, stakes=""):
        """Describe the start of a chess battle"""
        prompt = f"A chess battle begins against {npc_name}. {stakes} Describe the tension as the board is set."
        return self.narrate(prompt)

    def describe_chess_battle_end(self, won, npc_name):
        """Describe the end of a chess battle"""
        result = "victory" if won else "defeat"
        prompt = f"The chess battle against {npc_name} ends in {result}. Describe the conclusion dramatically."
        return self.narrate(prompt)

    def describe_move(self, move_san, is_critical=False):
        """Describe a significant move"""
        if is_critical:
            prompt = f"A critical move is played: {move_san}. Describe its impact dramatically."
            return self.narrate(prompt, max_tokens=80)
        return None  # Don't narrate every move

    def generate_quest_hook(self, npc_name, quest_type="chess_challenge"):
        """Generate a quest introduction"""
        prompt = f"{npc_name} has a quest for the player: a {quest_type}. Describe their offer compellingly."
        return self.narrate(prompt)

    def describe_consequences(self, action, outcome):
        """Describe consequences of player actions"""
        prompt = f"The player {action}, resulting in {outcome}. Describe the consequences."
        return self.narrate(prompt)


# Test the Game Master
if __name__ == "__main__":
    print("=== GAME MASTER TEST ===\n")

    gm = GameMaster()
    gm.set_player_name("Alex")

    print("1. Welcome Narration:")
    print(f"   {gm.narrate('welcome the player to the game')}\n")

    print("2. Location Description:")
    print(f"   {gm.describe_location('Castle Lumina')}\n")

    print("3. NPC Introduction (Princess Elara):")
    npc = {
        "name": "Princess Elara",
        "title": "Princess of the White Kingdom",
        "faction": "White Kingdom",
        "description": "Young and ambitious, she represents the reformist movement."
    }
    print(f"   {gm.introduce_npc(npc)}\n")

    print("4. Battle Start:")
    print(f"   {gm.describe_chess_battle_start('Sir Garrick', 'The stakes are high.')}\n")

    print("5. Victory:")
    print(f"   {gm.describe_chess_battle_end(True, 'Sir Garrick')}\n")

    print("✅ Game Master test complete!")
    print("\nNote: If LM Studio is not running, fallback narration was used.")
