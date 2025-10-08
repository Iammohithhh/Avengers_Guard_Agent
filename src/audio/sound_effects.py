"""
Sound Effects Manager for Avengers Guard System
Plays agent-specific sounds and system alerts
"""

import pygame
import os
from pathlib import Path
from typing import Optional
import time


class SoundEffectsManager:
    """
    Manages sound effects for the Avengers Guard system
    Plays agent-specific sounds, alerts, and themes
    """
    
    def __init__(self, sounds_dir: str = "sounds", volume: float = 0.7):
        """
        Initialize sound effects manager
        
        Args:
            sounds_dir: Directory containing sound files
            volume: Default volume (0.0 to 1.0)
        """
        self.sounds_dir = Path(sounds_dir)
        self.volume = volume
        self.enabled = True
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.mixer_available = True
            print("✅ Sound system initialized")
        except Exception as e:
            print(f"⚠️  Sound system unavailable: {e}")
            self.mixer_available = False
        
        # Sound file paths
        self.sounds = {
            # Agent activation sounds
            "jarvis_activate": self.sounds_dir / "agents" / "jarvis_activate.mp3",
            "cap_activate": self.sounds_dir / "agents" / "cap_shield.mp3",
            "widow_activate": self.sounds_dir / "agents" / "widow_stealth.mp3",
            "hulk_activate": self.sounds_dir / "agents" / "hulk_roar.mp3",
            "thor_activate": self.sounds_dir / "agents" / "thor_thunder.mp3",
            
            # Agent alert sounds
            "jarvis_alert": self.sounds_dir / "agents" / "jarvis_alert.mp3",
            "cap_alert": self.sounds_dir / "agents" / "cap_shield.mp3",
            "widow_alert": self.sounds_dir / "agents" / "widow_stealth.mp3",
            "hulk_alert": self.sounds_dir / "agents" / "hulk_smash.mp3",
            "thor_alert": self.sounds_dir / "agents" / "thor_mjolnir.mp3",
            
            # System sounds
            "system_beep": self.sounds_dir / "system" / "beep.mp3",
            "system_alert": self.sounds_dir / "system" / "alert.mp3",
            "system_alarm": self.sounds_dir / "system" / "alarm.mp3",
            
            # Theme music
            "avengers_theme": self.sounds_dir / "themes" / "avengers_theme.mp3",
            "alarm_siren": self.sounds_dir / "themes" / "alarm_siren.mp3"
        }
        
        # Check which sounds are available
        self.available_sounds = {}
        for name, path in self.sounds.items():
            if path.exists():
                self.available_sounds[name] = path
        
        if self.available_sounds:
            print(f"✅ Loaded {len(self.available_sounds)} sound effects")
        else:
            print("⚠️  No sound files found. Please download and place in 'sounds/' directory")
    
    def play_sound(self, sound_name: str, volume: Optional[float] = None, wait: bool = False) -> bool:
        """
        Play a sound effect
        
        Args:
            sound_name: Name of the sound to play
            volume: Override default volume
            wait: Wait for sound to finish before returning
        
        Returns:
            True if sound played successfully
        """
        if not self.enabled or not self.mixer_available:
            return False
        
        # Get sound path
        sound_path = self.available_sounds.get(sound_name)
        
        if not sound_path:
            print(f"⚠️  Sound not found: {sound_name}")
            return False
        
        try:
            # Stop any currently playing sound first
            pygame.mixer.music.stop()
            time.sleep(0.1)  # Small delay
            # Load and play sound
            pygame.mixer.music.load(str(sound_path))
            pygame.mixer.music.set_volume(volume if volume is not None else self.volume)
            pygame.mixer.music.play()
            
            # Wait if requested
            if wait:
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"❌ Error playing sound {sound_name}: {e}")
            return False
    
    def play_agent_activation(self, agent_name: str) -> bool:
        """
        Play activation sound for specific agent
        
        Args:
            agent_name: Name of agent (jarvis, captain_america, etc.)
        """
        sound_map = {
            "jarvis": "jarvis_activate",
            "captain_america": "cap_activate",
            "hulk": "hulk_activate",
            "thor": "thor_activate"
        }
        
        sound_name = sound_map.get(agent_name.lower())
        if sound_name:
            return self.play_sound(sound_name)
        return False
    
    def play_agent_alert(self, agent_name: str, threat_level: int = 1) -> bool:
        """
        Play alert sound for specific agent
        
        Args:
            agent_name: Name of agent
            threat_level: 1-4, increases volume with level
        """
        sound_map = {
            "jarvis": "jarvis_alert",
            "captain_america": "cap_alert",
            "hulk": "hulk_alert",
            "thor": "thor_alert"
        }
        
        sound_name = sound_map.get(agent_name.lower())
        if sound_name:
            # Increase volume with threat level
            volume = min(self.volume * (0.5 + threat_level * 0.15), 1.0)
            return self.play_sound(sound_name, volume=volume)
        return False
    
    def play_alarm(self, duration: float = 3.0) -> bool:
        """
        Play alarm siren for serious threats
        
        Args:
            duration: How long to play (seconds)
        """
        if self.play_sound("alarm_siren", volume=0.8):
            time.sleep(duration)
            self.stop()
            return True
        return False
    
    def play_theme(self) -> bool:
        """Play Avengers theme music"""
        return self.play_sound("avengers_theme", volume=0.6)
    
    def stop(self):
        """Stop currently playing sound"""
        if self.mixer_available:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def set_volume(self, volume: float):
        """
        Set default volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.mixer_available:
            pygame.mixer.music.set_volume(self.volume)
    
    def enable(self):
        """Enable sound effects"""
        self.enabled = True
        print("🔊 Sound effects enabled")
    
    def disable(self):
        """Disable sound effects"""
        self.enabled = False
        self.stop()
        print("🔇 Sound effects disabled")
    
    def get_missing_sounds(self) -> list:
        """Get list of sound files that are missing"""
        missing = []
        for name, path in self.sounds.items():
            if not path.exists():
                missing.append(str(path))
        return missing
    
    def create_sound_directories(self):
        """Create sound directory structure"""
        dirs = [
            self.sounds_dir / "agents",
            self.sounds_dir / "system",
            self.sounds_dir / "themes"
        ]
        
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Sound directories created at {self.sounds_dir}")
    
    def print_setup_guide(self):
        """Print guide for setting up sound files"""
        print("\n" + "="*60)
        print("🎵 SOUND EFFECTS SETUP GUIDE")
        print("="*60)
        print("\nDownload these sound effects and place them in the 'sounds/' directory:")
        print("\n📁 sounds/agents/ (Agent-specific sounds)")
        print("  • jarvis_activate.mp3 - Computer startup/AI activation")
        print("  • jarvis_alert.mp3 - Warning beep")
        print("  • cap_shield.mp3 - Shield clang/impact")
        print("  • widow_stealth.mp3 - Spy theme/electric shock")
        print("  • hulk_roar.mp3 - Hulk roaring")
        print("  • hulk_smash.mp3 - Smashing/destruction")
        print("  • thor_thunder.mp3 - Thunder crack")
        print("  • thor_mjolnir.mp3 - Hammer whoosh/impact")
        
        print("\n📁 sounds/system/ (System sounds)")
        print("  • beep.mp3 - Simple notification beep")
        print("  • alert.mp3 - Alert/warning sound")
        print("  • alarm.mp3 - Loud alarm/siren")
        
        print("\n📁 sounds/themes/ (Theme music)")
        print("  • avengers_theme.mp3 - Avengers theme (short)")
        print("  • alarm_siren.mp3 - Emergency siren")
        
        print("\n🌐 Where to find sounds:")
        print("  • Zapsplat.com (free sound effects)")
        print("  • Freesound.org (creative commons)")
        print("  • YouTube Audio Library (free music)")
        print("  • Pixabay (free sounds)")
        print("  • Search: 'marvel sound effects', 'thunder sound', etc.")
        
        print("\n💡 Tips:")
        print("  • Keep files short (1-3 seconds for effects)")
        print("  • MP3 format recommended")
        print("  • Normalize volume levels")
        print("  • Test before demo!")
        
        print("\n" + "="*60 + "\n")


# Test the sound effects manager
if __name__ == "__main__":
    print("🎵 SOUND EFFECTS MANAGER TEST\n")
    
    # Create manager
    sfx = SoundEffectsManager()
    
    # Create directories
    sfx.create_sound_directories()
    
    # Print setup guide
    sfx.print_setup_guide()
    
    # Show missing sounds
    missing = sfx.get_missing_sounds()
    if missing:
        print(f"⚠️  Missing {len(missing)} sound files:")
        for sound in missing[:5]:  # Show first 5
            print(f"   • {sound}")
        if len(missing) > 5:
            print(f"   ... and {len(missing) - 5} more")
    
    # Test available sounds
    if sfx.available_sounds:
        print(f"\n✅ Testing available sounds:")
        for sound_name in list(sfx.available_sounds.keys())[:3]:
            print(f"   Playing: {sound_name}")
            sfx.play_sound(sound_name, wait=True)
            time.sleep(0.5)
    
    print("\n✅ Sound Effects Manager ready!")