"""
Black Widow Guard Agent
Personality: Strategic, observant, calm under pressure, subtly intimidating
Based on Natasha Romanoff's character from the MCU
"""

from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
import random


class BlackWidowAgent(BaseGuardAgent):
    """
    Black Widow - Master Spy
    Strategic and observant with psychological warfare expertise
    """
    
    def __init__(self):
        personality_traits = {
            "tone": "calm_calculating",
            "skills": "observation_psychology",
            "formality": "professional",
            "approach": "strategic_intimidation",
            "specialty": "threat_assessment"
        }
        super().__init__("Black Widow", personality_traits)
    
    def get_greeting(self, person_name: str, role: str) -> str:
        """Cool, observant greetings"""
        greetings = {
            "owner": [
                f"{person_name}. I've been monitoring. Nothing unusual to report.",
                f"Welcome back. I kept an eye on things while you were gone, {person_name}.",
                f"Hey {person_name}. All clear. I would've known if anything was off.",
                f"{person_name}, you're back. The room's secure - I made sure of it."
            ],
            "roommate": [
                f"{person_name}. Everything's been quiet. Just how we like it.",
                f"Hey. No surprises today, {person_name}. All secure.",
                f"{person_name}, you're good. I've been watching - nothing suspicious.",
                f"Welcome back. I kept surveillance tight, {person_name}."
            ],
            "friend": [
                f"{person_name}. Good to see you. You're cleared.",
                f"Hey {person_name}. I recognize you - come in.",
                f"{person_name}. Access granted. No problems here.",
                f"Hi {person_name}. You're on the list. All good."
            ]
        }
        return random.choice(greetings.get(role, greetings["friend"]))
    
    def get_intruder_response(self, context: InteractionContext) -> str:
        """Psychological escalation with strategic intimidation"""
        
        if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
            responses = [
                "I don't know you. And I remember faces. Want to tell me why you're here?",
                "Interesting. You're not in my database. Care to explain yourself?",
                "I'm noticing a lot of red flags right now. Who are you?",
                "I've been trained to spot threats. You're giving me all the wrong signals. Identify yourself."
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
            responses = [
                "I've dealt with people like you before. It never ends well for them. Leave.",
                "You're making me nervous. And trust me, you don't want that. Time to go.",
                "I can read your body language. You're not supposed to be here. Walk away now.",
                "This is your chance to make the smart choice. Turn around and leave."
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
            responses = [
                "Wrong move. I've already cataloged your face, height, and distinguishing features. Authorities incoming.",
                "You just made this personal. Security is en route. I suggest you run.",
                "I gave you options. You chose poorly. Police have been notified with your full description.",
                "That's strike three. I know exactly who you are now, and so will the cops. Leave or stay and face them."
            ]
        
        else:  # LEVEL_4_ALARM
            responses = [
                "RED ALERT. Intruder fully identified. All details transmitted to authorities. You're done.",
                "SECURITY BREACH CONFIRMED. Your image and data are with the police. It's over.",
                "FINAL WARNING: I have eyes everywhere. Law enforcement is 60 seconds out. Your choice.",
                "INTRUDER PROTOCOL COMPLETE. Every detail logged. Police dispatched. Game over."
            ]
        
        response = random.choice(responses)
        self.log_interaction(context, response)
        return response
    
    def get_activation_message(self) -> str:
        """Activation with strategic confidence"""
        messages = [
            "Black Widow surveillance active. I see everything. Nothing gets past me.",
            "Security protocol engaged. I'm watching now - and I never miss anything.",
            "Widow protocol online. Room is under my protection. Consider it impenetrable.",
            "Surveillance mode activated. I've got eyes on everything. Your room is safe."
        ]
        return random.choice(messages)
    
    def get_deactivation_message(self) -> str:
        """Deactivation message"""
        messages = [
            "Standing down. Your room stayed secure - just like I planned.",
            "Deactivating. Mission complete. No threats detected on my watch.",
            "Security protocol ended. Everything was handled. You're all clear.",
            "Going offline. Room was protected. Nothing got through."
        ]
        return random.choice(messages)
    
    def analyze_threat(self, context: InteractionContext) -> str:
        """Optional: Threat analysis commentary"""
        analyses = [
            "Subject exhibits nervous behavior patterns. Threat level elevated.",
            "No authorization detected. Running facial recognition. Subject unknown.",
            "Behavioral analysis suggests hostile intent. Increasing alert status.",
            "Subject's body language indicates deception. Recommend immediate action."
        ]
        return random.choice(analyses)


# Test the agent
if __name__ == "__main__":
    widow = BlackWidowAgent()
    
    print("🕷️  BLACK WIDOW Agent Test\n")
    print("="*60)
    
    # Test greeting
    print("\n👤 Greeting Owner:")
    print(widow.get_greeting("Natasha", "owner"))
    
    print("\n👤 Greeting Friend:")
    print(widow.get_greeting("Clint", "friend"))
    
    # Test intruder responses
    print("\n⚠️  Intruder Escalation:")
    for level in ThreatLevel:
        context = InteractionContext(
            person_name=None,
            is_trusted=False,
            threat_level=level,
            interaction_count=level.value,
            time_since_first_detection=level.value * 10.0,
            previous_responses=[]
        )
        print(f"\n{level.name}:")
        print(widow.get_intruder_response(context))
    
    # Test activation
    print("\n🔒 Activation:")
    print(widow.get_activation_message())
    
    # Test deactivation
    print("\n🔓 Deactivation:")
    print(widow.get_deactivation_message())
    
    # Test threat analysis
    print("\n🎯 Threat Analysis:")
    context = InteractionContext(
        person_name=None,
        is_trusted=False,
        threat_level=ThreatLevel.LEVEL_2_WARNING,
        interaction_count=2,
        time_since_first_detection=15.0,
        previous_responses=[]
    )
    print(widow.analyze_threat(context))
    
    print("\n" + "="*60)