"""
Agent Manager - Selects and manages which Avenger responds
Handles rotation and selection logic for guard agents
"""

from typing import Optional, Dict, List
import random
from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
from .iron_man import JarvisAgent
from .captain_america import CaptainAmericaAgent
from .black_widow import BlackWidowAgent
from .hulk import HulkAgent
from .thor import ThorAgent


class AgentManager:
    """
    Manages multiple guard agents and handles selection logic
    """
    
    def __init__(self, rotation_mode: str = "random"):
        """
        Initialize agent manager
        
        Args:
            rotation_mode: How to select agents
                - "random": Random selection
                - "round_robin": Rotate through agents
                - "threat_based": Select based on threat level
                - "personality_based": Select by personality type
                - "fixed": Always use same agent
        """
        self.agents: Dict[str, BaseGuardAgent] = {
            "jarvis": JarvisAgent(),
            "captain_america": CaptainAmericaAgent(),
            "black_widow": BlackWidowAgent(),
            "hulk": HulkAgent(),
            "thor": ThorAgent()
        }
        
        self.rotation_mode = rotation_mode
        self.current_agent_index = 0
        self.agent_keys = list(self.agents.keys())
        self.active_agent: Optional[BaseGuardAgent] = None
        
        # Set default agent
        self.set_active_agent("jarvis")
    
    def set_active_agent(self, agent_name: str) -> bool:
        """
        Manually set the active agent
        
        Args:
            agent_name: Name of agent (jarvis, captain_america, black_widow)
        
        Returns:
            True if successful
        """
        if agent_name in self.agents:
            self.active_agent = self.agents[agent_name]
            print(f"🤖 Active Agent: {self.active_agent.agent_name}")
            return True
        else:
            print(f"❌ Unknown agent: {agent_name}")
            return False
    
    def select_agent_for_context(self, context: InteractionContext) -> BaseGuardAgent:
        """
        Select appropriate agent based on context and rotation mode
        
        Args:
            context: Current interaction context
        
        Returns:
            Selected agent
        """
        if self.rotation_mode == "fixed":
            return self.active_agent
        
        elif self.rotation_mode == "random":
            return random.choice(list(self.agents.values()))
        
        elif self.rotation_mode == "round_robin":
            agent = self.agents[self.agent_keys[self.current_agent_index]]
            self.current_agent_index = (self.current_agent_index + 1) % len(self.agent_keys)
            return agent
        
        elif self.rotation_mode == "threat_based":
            # JARVIS for polite inquiry
            if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
                return self.agents["jarvis"]
            # Captain America for warnings
            elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
                return self.agents["captain_america"]
            # Hulk for serious threats
            elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
                return self.agents["hulk"]
            # Thor for final alarm
            else:
                return self.agents["thor"]
        
        elif self.rotation_mode == "personality_based":
            # Smart selection based on time of day or context
            # Sophisticated: JARVIS, Thor
            # Direct: Captain America, Black Widow
            # Aggressive: Hulk
            if context.interaction_count == 1:
                return random.choice([self.agents["jarvis"], self.agents["thor"]])
            elif context.interaction_count == 2:
                return random.choice([self.agents["captain_america"], self.agents["black_widow"]])
            else:
                return self.agents["hulk"]
        
        else:
            return self.active_agent
    
    def get_greeting(self, person_name: str, role: str, agent_name: Optional[str] = None) -> tuple:
        """
        Get greeting from specified or active agent
        
        Returns:
            (agent_name, greeting_message)
        """
        if agent_name and agent_name in self.agents:
            agent = self.agents[agent_name]
        else:
            agent = self.active_agent
        
        greeting = agent.get_greeting(person_name, role)
        return agent.agent_name, greeting
    
    def get_intruder_response(self, context: InteractionContext) -> tuple:
        """
        Get intruder response from appropriate agent
        
        Returns:
            (agent_name, response_message)
        """
        agent = self.select_agent_for_context(context)
        response = agent.get_intruder_response(context)
        return agent.agent_name, response
    
    def get_activation_message(self) -> tuple:
        """
        Get activation message
        
        Returns:
            (agent_name, activation_message)
        """
        message = self.active_agent.get_activation_message()
        return self.active_agent.agent_name, message
    
    def get_deactivation_message(self) -> tuple:
        """
        Get deactivation message
        
        Returns:
            (agent_name, deactivation_message)
        """
        message = self.active_agent.get_deactivation_message()
        return self.active_agent.agent_name, message
    
    def list_agents(self):
        """Display all available agents"""
        print("\n" + "="*60)
        print("🦸 AVAILABLE AVENGERS GUARD AGENTS")
        print("="*60)
        for key, agent in self.agents.items():
            status = "✓ ACTIVE" if agent == self.active_agent else ""
            print(f"\n🤖 {agent.agent_name} ({key}) {status}")
            print(f"   {agent.get_personality_description()}")
        print("="*60 + "\n")
    
    def set_rotation_mode(self, mode: str):
        """
        Change rotation mode
        
        Args:
            mode: random, round_robin, threat_based, personality_based, or fixed
        """
        valid_modes = ["random", "round_robin", "threat_based", "personality_based", "fixed"]
        if mode in valid_modes:
            self.rotation_mode = mode
            print(f"✅ Rotation mode set to: {mode}")
        else:
            print(f"❌ Invalid mode. Choose from: {valid_modes}")
    
    def get_all_interaction_history(self) -> List[Dict]:
        """Get interaction history from all agents"""
        all_history = []
        for agent in self.agents.values():
            all_history.extend(agent.interaction_history)
        return all_history
    
    def reset_all_histories(self):
        """Clear interaction history for all agents"""
        for agent in self.agents.values():
            agent.interaction_history = []
        print("✅ All agent interaction histories cleared")


# Test and demonstration
if __name__ == "__main__":
    print("🦸 AVENGERS AGENT MANAGER TEST\n")
    print("="*60)
    
    # Create manager
    manager = AgentManager(rotation_mode="threat_based")
    
    # List agents
    manager.list_agents()
    
    # Test greetings
    print("\n📣 TESTING GREETINGS:")
    print("="*60)
    for agent_key in ["jarvis", "captain_america", "black_widow"]:
        agent_name, greeting = manager.get_greeting("Tony Stark", "owner", agent_key)
        print(f"\n{agent_name}:")
        print(f"  {greeting}")
    
    # Test intruder escalation with threat-based selection
    print("\n\n⚠️  TESTING INTRUDER ESCALATION (Threat-Based):")
    print("="*60)
    
    for level in ThreatLevel:
        context = InteractionContext(
            person_name=None,
            is_trusted=False,
            threat_level=level,
            interaction_count=level.value,
            time_since_first_detection=level.value * 10.0,
            previous_responses=[]
        )
        
        agent_name, response = manager.get_intruder_response(context)
        print(f"\n{level.name} → {agent_name}:")
        print(f"  {response}")
    
    # Test activation/deactivation
    print("\n\n🔒 TESTING ACTIVATION:")
    print("="*60)
    agent_name, msg = manager.get_activation_message()
    print(f"{agent_name}: {msg}")
    
    print("\n🔓 TESTING DEACTIVATION:")
    print("="*60)
    agent_name, msg = manager.get_deactivation_message()
    print(f"{agent_name}: {msg}")
    
    # Test different rotation modes
    print("\n\n🔄 TESTING ROTATION MODES:")
    print("="*60)
    
    manager.set_rotation_mode("random")
    print("\nRandom mode - 3 greetings:")
    for i in range(3):
        agent_name, greeting = manager.get_greeting("User", "owner")
        print(f"  {i+1}. {agent_name}")
    
    manager.set_rotation_mode("round_robin")
    print("\nRound-robin mode - 4 greetings:")
    for i in range(4):
        context = InteractionContext(
            person_name=None,
            is_trusted=False,
            threat_level=ThreatLevel.LEVEL_1_INQUIRY,
            interaction_count=1,
            time_since_first_detection=5.0,
            previous_responses=[]
        )
        agent_name, response = manager.get_intruder_response(context)
        print(f"  {i+1}. {agent_name}")
    
    print("\n" + "="*60)