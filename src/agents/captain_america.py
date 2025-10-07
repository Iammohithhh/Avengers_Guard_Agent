"""
Captain America Guard Agent
Personality: Principled, straightforward, honorable, protective
Based on Steve Rogers' character from the MCU
"""

from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
import random


class CaptainAmericaAgent(BaseGuardAgent):
    """
    Captain America - The First Avenger
    Principled protector with strong moral compass and direct communication
    """
    
    def __init__(self):
        personality_traits = {
            "tone": "honest_and_direct",
            "values": "honor_duty_protection",
            "formality": "respectful",
            "approach": "fair_but_firm",
            "era": "old_school_gentleman"
        }
        super().__init__("Captain America", personality_traits)
    
    def get_greeting(self, person_name: str, role: str) -> str:
        """Honest, warm greetings"""
        greetings = {
            "owner": [
                f"Welcome back, {person_name}. Your room is secure, just as you left it.",
                f"Good to see you home safe, {person_name}. Everything's been quiet.",
                f"Hey {person_name}, glad you're back. I kept watch like I promised.",
                f"{person_name}, welcome home. No issues to report - kept it safe for you."
            ],
            "roommate": [
                f"Hey {person_name}, you're all clear. No problems while you were out.",
                f"Welcome back, {person_name}. Everything's been peaceful here.",
                f"{person_name}, good to see you. Your space is secure.",
                f"Hey there, {person_name}. All quiet on the home front."
            ],
            "friend": [
                f"Hi {person_name}, good to see you. Come on in.",
                f"Hey {person_name}, you're always welcome here. Access granted.",
                f"Hello {person_name}. Nice to see a friendly face.",
                f"{person_name}! Good to have you here. Everything's clear."
            ]
        }
        return random.choice(greetings.get(role, greetings["friend"]))
    
    def get_intruder_response(self, context: InteractionContext) -> str:
        """Direct but fair escalation"""
        
        if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
            responses = [
                "Excuse me, I don't recognize you. Can you tell me who you are and why you're here?",
                "Hold on there. I haven't seen you before. Mind introducing yourself?",
                "Hey, I don't think we've met. This is private property. What brings you here?",
                "Wait a minute. You're not authorized to be here. Who are you?"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
            responses = [
                "I'm asking you nicely - leave now. This isn't your property.",
                "Listen, I gave you a chance to explain. You need to leave immediately.",
                "I don't want any trouble here. Please leave before this escalates.",
                "You're trespassing. I'm giving you one more chance to walk away peacefully."
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
            responses = [
                "That's enough. You're breaking the law. Leave now or I'm calling the police.",
                "This is your final warning. Get out now before authorities arrive.",
                "I tried to be reasonable. You've crossed the line. Time to leave.",
                "Okay, that's it. Security has been alerted. You need to go. Now."
            ]
        
        else:  # LEVEL_4_ALARM
            responses = [
                "INTRUDER ALERT! This room is under protection. Police have been notified!",
                "YOU'VE BEEN WARNED! Authorities are on their way. Leave immediately!",
                "This is Captain America security protocol. You are trespassing. Help is coming.",
                "FINAL ALERT: You are committing a crime. Law enforcement en route!"
            ]
        
        response = random.choice(responses)
        self.log_interaction(context, response)
        return response
    
    def get_activation_message(self) -> str:
        """Activation with duty and honor"""
        messages = [
            "Captain America security protocol active. I'll keep watch - you can count on me.",
            "On duty now. Your room is under protection. Nobody gets in without authorization.",
            "Security mode engaged. I'll protect your space like I protect my country - with everything I've got.",
            "Roger that. Captain America reporting for guard duty. Room is now secure."
        ]
        return random.choice(messages)
    
    def get_deactivation_message(self) -> str:
        """Deactivation with relief of duty"""
        messages = [
            "Standing down. Your room was safe under my watch. Mission complete.",
            "Security protocol ended. Glad I could help keep your space secure.",
            "Duty fulfilled. Your room stayed protected. Going off duty now.",
            "Alright, deactivating security. Everything stayed safe - just like I promised."
        ]
        return random.choice(messages)
    
    def get_motivational_quote(self) -> str:
        """Optional: Cap's inspiring quotes"""
        quotes = [
            "I can do this all day.",
            "When the mob and the press and the whole world tell you to move, your job is to plant yourself like a tree and say 'No, you move.'",
            "The price of freedom is high, and it's a price I'm willing to pay.",
            "I'm with you 'til the end of the line."
        ]
        return random.choice(quotes)


# Test the agent
if __name__ == "__main__":
    cap = CaptainAmericaAgent()
    
    print("🛡️  CAPTAIN AMERICA Agent Test\n")
    print("="*60)
    
    # Test greeting
    print("\n👤 Greeting Owner:")
    print(cap.get_greeting("Steve", "owner"))
    
    print("\n👤 Greeting Friend:")
    print(cap.get_greeting("Bucky", "friend"))
    
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
        print(cap.get_intruder_response(context))
    
    # Test activation
    print("\n🔒 Activation:")
    print(cap.get_activation_message())
    
    # Test deactivation
    print("\n🔓 Deactivation:")
    print(cap.get_deactivation_message())
    
    # Test quote
    print("\n💪 Motivational Quote:")
    print(cap.get_motivational_quote())
    
    print("\n" + "="*60)