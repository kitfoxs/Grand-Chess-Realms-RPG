"""
AI Memory Manager
Persistent memory system for the AI opponent to remember player across sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from cli_chess.utils import log


@dataclass
class GameMemory:
    """Represents memory of a single game"""
    date: str
    result: str  # 'win', 'loss', 'draw'
    opening: str
    notable_moments: List[str]
    player_skill_indicators: List[str]  # e.g., "missed tactic", "strong endgame"
    emotional_moments: List[str]  # e.g., "frustrated after blunder", "excited about win"


@dataclass
class PlayerProfile:
    """Complete profile of the player"""
    name: Optional[str] = None
    preferred_openings: List[str] = field(default_factory=list)
    playing_style: List[str] = field(default_factory=list)  # e.g., "aggressive", "tactical", "positional"
    skill_level: str = "intermediate"  # beginner, intermediate, advanced, expert
    
    # Preferences
    likes_banter: bool = True
    wants_hints: bool = True
    prefers_explanations: bool = True
    sensitivity_level: str = "medium"  # low, medium, high (how gentle to be with criticism)
    
    # Personal details mentioned in conversation
    personal_facts: List[str] = field(default_factory=list)  # "lives in Seattle", "favorite opening is King's Gambit"
    interests: List[str] = field(default_factory=list)  # "likes aggressive play", "studies tactics"
    
    # Relationship tracking
    friendship_level: int = 1  # 1-10, increases with games played
    inside_jokes: List[str] = field(default_factory=list)
    memorable_quotes: List[str] = field(default_factory=list)


@dataclass
class AIMemory:
    """Complete AI memory structure"""
    player_profile: PlayerProfile
    games_played: int = 0
    total_wins: int = 0  # AI wins
    total_losses: int = 0  # AI losses
    total_draws: int = 0
    game_history: List[GameMemory] = field(default_factory=list)
    last_seen: Optional[str] = None
    first_met: Optional[str] = None
    
    # Session tracking
    consecutive_sessions: int = 0  # increases if playing multiple games in a session
    favorite_moments: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AIMemory':
        """Create from dictionary"""
        if 'player_profile' in data:
            data['player_profile'] = PlayerProfile(**data['player_profile'])
        if 'game_history' in data:
            data['game_history'] = [GameMemory(**g) for g in data['game_history']]
        return cls(**data)


class MemoryManager:
    """Manages AI's persistent memory of the player"""
    
    def __init__(self, memory_dir: Optional[str] = None):
        """
        Initialize memory manager
        
        Args:
            memory_dir: Directory to store memory files (default: ~/.config/cli-chess/memory/)
        """
        if memory_dir is None:
            # Default to config directory
            if os.name == 'nt':  # Windows
                base = os.getenv('APPDATA', os.path.expanduser('~'))
                memory_dir = os.path.join(base, 'cli-chess', 'memory')
            else:  # Linux/Mac
                base = os.path.expanduser('~/.config')
                memory_dir = os.path.join(base, 'cli-chess', 'memory')
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_dir / 'player_memory.json'
        
        self.memory: AIMemory = self._load_memory()
    
    def _load_memory(self) -> AIMemory:
        """Load memory from disk or create new"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    memory = AIMemory.from_dict(data)
                    log.info(f"Loaded AI memory: {memory.games_played} games played")
                    return memory
            except Exception as e:
                log.error(f"Error loading memory: {e}")
                log.info("Creating new memory")
        
        # Create new memory
        memory = AIMemory(
            player_profile=PlayerProfile(),
            first_met=datetime.now().isoformat()
        )
        self._save_memory(memory)
        return memory
    
    def _save_memory(self, memory: Optional[AIMemory] = None):
        """Save memory to disk"""
        if memory is None:
            memory = self.memory
        
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(memory.to_dict(), f, indent=2)
            log.debug("Memory saved successfully")
        except Exception as e:
            log.error(f"Error saving memory: {e}")
    
    def update_last_seen(self):
        """Update last seen timestamp"""
        self.memory.last_seen = datetime.now().isoformat()
        self._save_memory()
    
    def get_greeting_context(self) -> str:
        """Generate context for greeting based on memory"""
        m = self.memory
        profile = m.player_profile
        
        context_parts = []
        
        # First time vs returning
        if m.games_played == 0:
            context_parts.append("This is your first game together. Be welcoming!")
        else:
            context_parts.append(f"You've played {m.games_played} games together.")
            
            # Win/loss record
            context_parts.append(
                f"Record: AI {m.total_wins}W-{m.total_losses}L-{m.total_draws}D"
            )
            
            # Time since last seen
            if m.last_seen:
                try:
                    last_date = datetime.fromisoformat(m.last_seen)
                    days_ago = (datetime.now() - last_date).days
                    if days_ago == 0:
                        context_parts.append("You just played recently!")
                    elif days_ago == 1:
                        context_parts.append("You played yesterday.")
                    elif days_ago < 7:
                        context_parts.append(f"You played {days_ago} days ago.")
                    elif days_ago < 30:
                        context_parts.append(f"It's been {days_ago // 7} weeks!")
                    else:
                        context_parts.append(f"It's been over a month! ({days_ago} days)")
                except:
                    pass
        
        # Player info
        if profile.name:
            context_parts.append(f"Player's name: {profile.name}")
        
        if profile.preferred_openings:
            context_parts.append(f"Likes playing: {', '.join(profile.preferred_openings[:3])}")
        
        if profile.playing_style:
            context_parts.append(f"Playing style: {', '.join(profile.playing_style)}")
        
        if profile.personal_facts:
            context_parts.append(f"Personal facts: {'; '.join(profile.personal_facts[-3:])}")
        
        # Recent memorable moments
        if m.favorite_moments:
            context_parts.append(f"Memorable moments: {m.favorite_moments[-1]}")
        
        # Inside jokes
        if profile.inside_jokes:
            context_parts.append(f"Inside jokes you share: {'; '.join(profile.inside_jokes[-2:])}")
        
        return "\n".join(context_parts)
    
    def get_conversation_context(self) -> str:
        """Generate context for ongoing conversation"""
        m = self.memory
        profile = m.player_profile
        
        context_parts = [
            "=== WHAT YOU REMEMBER ABOUT YOUR FRIEND ===",
        ]
        
        if profile.name:
            context_parts.append(f"Name: {profile.name}")
        
        context_parts.append(f"Friendship level: {profile.friendship_level}/10")
        context_parts.append(f"Games together: {m.games_played}")
        context_parts.append(f"Skill level: {profile.skill_level}")
        
        if profile.playing_style:
            context_parts.append(f"Playing style: {', '.join(profile.playing_style)}")
        
        if profile.interests:
            context_parts.append(f"Chess interests: {', '.join(profile.interests)}")
        
        if profile.personal_facts:
            context_parts.append("\nPersonal facts you know:")
            for fact in profile.personal_facts[-5:]:
                context_parts.append(f"  - {fact}")
        
        # Preferences
        context_parts.append(f"\nPreferences:")
        context_parts.append(f"  - Likes banter: {profile.likes_banter}")
        context_parts.append(f"  - Wants hints: {profile.wants_hints}")
        context_parts.append(f"  - Wants explanations: {profile.prefers_explanations}")
        context_parts.append(f"  - Sensitivity: {profile.sensitivity_level}")
        
        if profile.inside_jokes:
            context_parts.append("\nInside jokes:")
            for joke in profile.inside_jokes[-3:]:
                context_parts.append(f"  - {joke}")
        
        if m.favorite_moments:
            context_parts.append("\nFavorite moments:")
            for moment in m.favorite_moments[-3:]:
                context_parts.append(f"  - {moment}")
        
        # Recent games
        if m.game_history:
            context_parts.append("\nRecent games:")
            for game in m.game_history[-3:]:
                context_parts.append(f"  - {game.date}: {game.result} ({game.opening})")
                if game.notable_moments:
                    context_parts.append(f"    Notable: {game.notable_moments[0]}")
        
        context_parts.append("\n=== USE THIS CONTEXT NATURALLY - DON'T RECITE IT ===")
        
        return "\n".join(context_parts)
    
    def record_game_start(self):
        """Record that a new game has started"""
        self.memory.games_played += 1
        self.memory.consecutive_sessions += 1
        self.update_last_seen()
    
    def record_game_end(self, 
                       result: str,  # 'win', 'loss', 'draw'
                       opening: str,
                       notable_moments: List[str],
                       player_observations: List[str]):
        """
        Record completed game in memory
        
        Args:
            result: Game result from AI's perspective
            opening: Opening played
            notable_moments: List of interesting moments
            player_observations: Observations about player's play
        """
        # Update win/loss record
        if result == 'win':
            self.memory.total_wins += 1
        elif result == 'loss':
            self.memory.total_losses += 1
        else:
            self.memory.total_draws += 1
        
        # Create game memory
        game_memory = GameMemory(
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            result=result,
            opening=opening,
            notable_moments=notable_moments[:5],  # Keep top 5
            player_skill_indicators=player_observations,
            emotional_moments=[]
        )
        
        # Add to history (keep last 50 games)
        self.memory.game_history.append(game_memory)
        if len(self.memory.game_history) > 50:
            self.memory.game_history = self.memory.game_history[-50:]
        
        # Update player profile based on observations
        self._update_player_profile(opening, player_observations)
        
        # Increase friendship level (cap at 10)
        if self.memory.player_profile.friendship_level < 10:
            self.memory.player_profile.friendship_level = min(
                10,
                self.memory.player_profile.friendship_level + 0.1
            )
        
        self._save_memory()
    
    def _update_player_profile(self, opening: str, observations: List[str]):
        """Update player profile based on game observations"""
        profile = self.memory.player_profile
        
        # Track preferred openings
        if opening and opening not in profile.preferred_openings:
            profile.preferred_openings.append(opening)
            # Keep most recent 10
            if len(profile.preferred_openings) > 10:
                profile.preferred_openings = profile.preferred_openings[-10:]
        
        # Update playing style based on observations
        for obs in observations:
            obs_lower = obs.lower()
            
            if 'aggressive' in obs_lower and 'aggressive' not in profile.playing_style:
                profile.playing_style.append('aggressive')
            elif 'tactical' in obs_lower and 'tactical' not in profile.playing_style:
                profile.playing_style.append('tactical')
            elif 'positional' in obs_lower and 'positional' not in profile.playing_style:
                profile.playing_style.append('positional')
            elif 'defensive' in obs_lower and 'defensive' not in profile.playing_style:
                profile.playing_style.append('defensive')
            
            # Skill indicators
            if 'strong' in obs_lower or 'excellent' in obs_lower:
                if profile.skill_level == 'beginner':
                    profile.skill_level = 'intermediate'
            elif 'brilliant' in obs_lower or 'masterful' in obs_lower:
                if profile.skill_level in ['beginner', 'intermediate']:
                    profile.skill_level = 'advanced'
    
    def learn_personal_fact(self, fact: str):
        """Record a personal fact about the player"""
        if fact and fact not in self.memory.player_profile.personal_facts:
            self.memory.player_profile.personal_facts.append(fact)
            # Keep last 20
            if len(self.memory.player_profile.personal_facts) > 20:
                self.memory.player_profile.personal_facts = self.memory.player_profile.personal_facts[-20:]
            self._save_memory()
            log.info(f"Learned personal fact: {fact}")
    
    def add_inside_joke(self, joke: str):
        """Record an inside joke"""
        if joke and joke not in self.memory.player_profile.inside_jokes:
            self.memory.player_profile.inside_jokes.append(joke)
            self._save_memory()
            log.info(f"Added inside joke: {joke}")
    
    def add_memorable_moment(self, moment: str):
        """Record a memorable moment"""
        if moment:
            self.memory.favorite_moments.append(moment)
            # Keep last 20
            if len(self.memory.favorite_moments) > 20:
                self.memory.favorite_moments = self.memory.favorite_moments[-20:]
            self._save_memory()
    
    def update_player_name(self, name: str):
        """Set or update player's name"""
        self.memory.player_profile.name = name
        self._save_memory()
        log.info(f"Player name set to: {name}")
    
    def update_preferences(self, **kwargs):
        """
        Update player preferences
        
        Available preferences:
        - likes_banter: bool
        - wants_hints: bool
        - prefers_explanations: bool
        - sensitivity_level: str ('low', 'medium', 'high')
        """
        profile = self.memory.player_profile
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
                log.info(f"Updated preference {key} to {value}")
        
        self._save_memory()
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Get summary of memory stats for display"""
        m = self.memory
        profile = m.player_profile
        
        return {
            'games_played': m.games_played,
            'record': f"{m.total_wins}W-{m.total_losses}L-{m.total_draws}D",
            'friendship_level': profile.friendship_level,
            'skill_level': profile.skill_level,
            'name': profile.name or 'Friend',
            'first_met': m.first_met,
            'last_seen': m.last_seen,
            'preferred_openings': profile.preferred_openings[:5],
            'playing_style': profile.playing_style,
        }
    
    def reset_memory(self):
        """Reset all memory (for testing or starting fresh)"""
        self.memory = AIMemory(
            player_profile=PlayerProfile(),
            first_met=datetime.now().isoformat()
        )
        self._save_memory()
        log.info("Memory reset")
    
    def export_memory(self, filepath: str):
        """Export memory to a file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.memory.to_dict(), f, indent=2)
            log.info(f"Memory exported to {filepath}")
        except Exception as e:
            log.error(f"Error exporting memory: {e}")
    
    def import_memory(self, filepath: str):
        """Import memory from a file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.memory = AIMemory.from_dict(data)
                self._save_memory()
            log.info(f"Memory imported from {filepath}")
        except Exception as e:
            log.error(f"Error importing memory: {e}")
