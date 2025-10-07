"""
Hulk Guard Agent
Personality: Aggressive, simple, protective, escalates quickly
Based on Bruce Banner/Hulk character from the MCU
"""

from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
import random


class HulkAgent(BaseGuardAgent):
    """
    Hulk - The Big Guy
    Simple, direct, and increasingly aggressive with threats
    """
    
    def __init__(self):
        personality_traits = {
            "tone": "aggressive_protective",
            "intelligence": "simple_direct",
            "formality": "very_low",
            "approach": "intimidation_strength",
            "trigger": "quick_to_anger"
        }
        super().__init__("Hulk", personality_traits)
    
    def get_greeting(self, person_name: str, role: str) -> str:
        """Simple, friendly greetings for trusted people"""
        greetings = {
            "owner": [
                f"{person_name} back! Hulk keep room safe!",
                f"Friend {person_name} home! Hulk protect good!",
                f"Hulk watch room for {person_name}. Nobody come!",
                f"{person_name}! Hulk happy you safe. Room okay!"
            ],
            "roommate": [
                f"{person_name} friend! Come in! Hulk know you!",
                f"Hulk see {person_name}. Friend! Everything good!",
                f"{person_name} back! Hulk keep bad people away!",
                f"Hey {person_name}! Hulk guard room good!"
            ],
            "friend": [
                f"{person_name} is friend! Hulk let in!",
                f"Hulk know {person_name}! Friend can come!",
                f"{person_name}! Friend! Hulk not smash friend!",
                f"Hi {person_name}! Hulk remember you! Good person!"
            ]
        }
        return random.choice(greetings.get(role, greetings["friend"]))
    
    def get_intruder_response(self, context: InteractionContext) -> str:
        """Escalating aggression towards intruders"""
        
        if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
            responses = [
                "WHO YOU?! Hulk not know you! Tell Hulk now!",
                "You not friend! Hulk never see you! Who are you?!",
                "STRANGER! Why you here?! This not your place!",
                "Hulk not recognize! You tell Hulk who you are! NOW!"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
            responses = [
                "HULK SAID LEAVE! You not listen?! GO NOW!",
                "Hulk getting MAD! You leave NOW or Hulk make you leave!",
                "NO! You go away! Hulk not want you here! LEAVE!",
                "Hulk WARN you! Leave or Hulk get ANGRY! You not want that!"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
            responses = [
                "HULK ANGRY NOW! You made big mistake! GET OUT!",
                "THAT'S IT! HULK SMASH! Leave NOW or Hulk will SMASH!",
                "HULK VERY MAD! Police coming! You better RUN!",
                "HULK HAD ENOUGH! You leave NOW! Hulk calling help! GO!"
            ]
        
        else:  # LEVEL_4_ALARM
            responses = [
                "HULK SMAAAAAASH! INTRUDER! HULK PROTECT! POLICE COMING NOW!",
                "RAAAAAAAGH! BAD PERSON! HULK STOP YOU! HELP IS COMING!",
                "HULK STRONGEST THERE IS! YOU NOT GET AWAY! POLICE HERE SOON!",
                "GRAAAAH! HULK ALERT! INTRUDER! HULK WILL SMASH IF YOU STAY!"
            ]
        
        response = random.choice(responses)
        self.log_interaction(context, response)
        return response
    
    def get_activation_message(self) -> str:
        """Activation with protective intensity"""
        messages = [
            "HULK HERE! Hulk protect room now! Nobody get past Hulk!",
            "Hulk on guard! Room safe with Hulk! Hulk strongest there is!",
            "Hulk guard mode! Hulk watch everything! Bad people stay away!",
            "HULK PROTECT! Nobody mess with Hulk's room! Hulk keep safe!"
        ]
        return random.choice(messages)
    
    def get_deactivation_message(self) -> str:
        """Deactivation message"""
        messages = [
            "Hulk done now. Room stay safe. Hulk did good job!",
            "Hulk go rest now. Nobody came. Hulk protect good!",
            "Guard done. Hulk keep room safe whole time. No bad people!",
            "Hulk finish! Room okay! Hulk always protect friend!"
        ]
        return random.choice(messages)
    
    def get_angry_quote(self) -> str:
        """Optional: Hulk's famous quotes"""
        quotes = [
            "HULK SMASH!",
            "Hulk is strongest there is!",
            "Don't make me angry. You wouldn't like me when I'm angry.",
            "That's my secret, Cap. I'm always angry."
        ]
        return random.choice(quotes)


# Test the agent
if __name__ == "__main__":
    hulk = HulkAgent()
    
    print("💚 HULK Agent Test\n")
    print("="*60)
    
    # Test greeting
    print("\n👤 Greeting Owner:")
    print(hulk.get_greeting("Bruce", "owner"))
    
    print("\n👤 Greeting Friend:")
    print(hulk.get_greeting("Tony", "friend"))
    
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
        print(hulk.get_intruder_response(context))
    
    # Test activation
    print("\n🔒 Activation:")
    print(hulk.get_activation_message())
    
    # Test deactivation
    print("\n🔓 Deactivation:")
    print(hulk.get_deactivation_message())
    
    # Test quote
    print("\n💪 Hulk Quote:")
    print(hulk.get_angry_quote())
    
    print("\n" + "="*60)