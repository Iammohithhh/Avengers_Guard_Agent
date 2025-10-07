"""
Base Agent Class for Avengers Guard System
Defines the personality and behavior interface for all guard agents
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ThreatLevel(Enum):
    """Escalation levels for intruder interaction"""
    LEVEL_1_INQUIRY = 1      # Polite questioning
    LEVEL_2_WARNING = 2      # Firm warning
    LEVEL_3_ALERT = 3        # Stern alert
    LEVEL_4_ALARM = 4        # Final warning / alarm


@dataclass
class InteractionContext:
    """Context for agent interactions"""
    person_name: Optional[str]
    is_trusted: bool
    threat_level: ThreatLevel
    interaction_count: int
    time_since_first_detection: float
    previous_responses: List[str]


class BaseGuardAgent(ABC):
    """
    Abstract base class for all Avengers guard agents
    Each agent has a unique personality and interaction style
    """
    
    def __init__(self, agent_name: str, personality_traits: Dict[str, str]):
        """
        Initialize guard agent
        
        Args:
            agent_name: Name of the agent (e.g., "JARVIS", "FRIDAY")
            personality_traits: Dict describing personality
        """
        self.agent_name = agent_name
        self.personality_traits = personality_traits
        self.interaction_history = []
    
    @abstractmethod
    def get_greeting(self, person_name: str, role: str) -> str:
        """
        Get greeting message for trusted person
        
        Args:
            person_name: Name of the person
            role: Role (owner/roommate/friend)
        
        Returns:
            Greeting message string
        """
        pass
    
    @abstractmethod
    def get_intruder_response(self, context: InteractionContext) -> str:
        """
        Get escalating response for intruder based on context
        
        Args:
            context: Current interaction context with threat level
        
        Returns:
            Response message string
        """
        pass
    
    @abstractmethod
    def get_activation_message(self) -> str:
        """
        Get message when guard mode is activated
        
        Returns:
            Activation message string
        """
        pass
    
    @abstractmethod
    def get_deactivation_message(self) -> str:
        """
        Get message when guard mode is deactivated
        
        Returns:
            Deactivation message string
        """
        pass
    
    def get_personality_description(self) -> str:
        """Get description of agent personality"""
        return f"{self.agent_name}: " + ", ".join(
            f"{k}={v}" for k, v in self.personality_traits.items()
        )
    
    def log_interaction(self, context: InteractionContext, response: str):
        """Log an interaction for analysis"""
        self.interaction_history.append({
            'context': context,
            'response': response,
            'agent': self.agent_name
        })
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt for LLM integration (Milestone 3)
        This will be used to maintain personality consistency
        """
        return f"""You are {self.agent_name}, an AI guard agent with the following personality:
{self.get_personality_description()}

Your role is to protect this room and interact with intruders in character.
Be consistent with your personality traits in all responses."""


# Example usage and testing
if __name__ == "__main__":
    # This will be implemented by concrete agent classes
    print("Base Agent Module - Use this as parent class for specific agents")