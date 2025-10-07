"""
Thor Guard Agent
Personality: Mighty, dramatic, honorable, Asgardian warrior
Based on Thor Odinson character from the MCU
"""

from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
import random


class ThorAgent(BaseGuardAgent):
    """
    Thor - God of Thunder
    Mighty Asgardian warrior with dramatic flair and honor
    """
    
    def __init__(self):
        personality_traits = {
            "tone": "mighty_dramatic",
            "origin": "asgardian_royalty",
            "formality": "archaic_noble",
            "approach": "honorable_warrior",
            "style": "theatrical"
        }
        super().__init__("Thor", personality_traits)
    
    def get_greeting(self, person_name: str, role: str) -> str:
        """Dramatic, honorable greetings"""
        greetings = {
            "owner": [
                f"Greetings, {person_name}! Thor, son of Odin, has kept your chambers safe in your absence!",
                f"Welcome back, noble {person_name}! Your realm remains secure under Thor's watchful eye!",
                f"Hail, {person_name}! The God of Thunder has protected your domain with honor!",
                f"{person_name}, friend! Thor has stood guard as promised. Your home is safe!"
            ],
            "roommate": [
                f"Ah, {person_name}! Fellow guardian of this realm! All is well here!",
                f"Greetings, {person_name}! Thor welcomes you back to our shared quarters!",
                f"Hail, {person_name}! Your portion of our domain remains undisturbed!",
                f"{person_name}! Thor is pleased to see you return safely!"
            ],
            "friend": [
                f"Welcome, {person_name}! Any friend of Midgard is a friend of Thor!",
                f"Hail and well met, {person_name}! Enter freely, honored guest!",
                f"Ah, {person_name}! Thor recognizes you as a trusted ally! Come in!",
                f"Greetings, brave {person_name}! You are most welcome here!"
            ]
        }
        return random.choice(greetings.get(role, greetings["friend"]))
    
    def get_intruder_response(self, context: InteractionContext) -> str:
        """Dramatic warrior escalation"""
        
        if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
            responses = [
                "Hold, stranger! By Odin's beard, identify yourself! Who dares enter uninvited?",
                "Halt! Thor does not recognize you! State your name and your business here!",
                "Stay your advance! I am Thor of Asgard, and you are unknown to me! Speak!",
                "Wait! You are not known to this realm! Who are you and what do you seek here?"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
            responses = [
                "I warn you, trespasser! Leave now or face the wrath of the God of Thunder!",
                "Thor has given you fair warning! Depart immediately or suffer consequences!",
                "You test Thor's patience! This is your final chance to leave peacefully!",
                "By Mjolnir's might, I command you to leave! Thor will not ask again!"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
            responses = [
                "Your fate is sealed, intruder! Thor calls upon the authorities of Midgard!",
                "The thunder rumbles for you, trespasser! The guardians of this realm are summoned!",
                "You have made a grave error! Thor has alerted the warriors of law enforcement!",
                "Foolish mortal! You face the God of Thunder's justice! Help arrives swiftly!"
            ]
        
        else:  # LEVEL_4_ALARM
            responses = [
                "FOR ASGARD! INTRUDER ALERT! Thor calls down the lightning! Authorities incoming!",
                "BY ODIN'S THRONE! You dare continue?! Feel Thor's fury! Police summoned!",
                "The storm breaks upon you! INTRUDER! Thor's allies arrive! Your time ends now!",
                "HAVE AT THEE! Security breach! Thor protects this realm! Surrender or face justice!"
            ]
        
        response = random.choice(responses)
        self.log_interaction(context, response)
        return response
    
    def get_activation_message(self) -> str:
        """Dramatic activation"""
        messages = [
            "By Odin's command! Thor stands guard! Let the watch begin! This realm is now protected!",
            "The God of Thunder takes his post! Fear not, for Thor guards your home with honor!",
            "Thor, son of Odin, assumes the watch! No foe shall pass while I stand sentinel!",
            "Hark! Thor's protection is now upon this place! Thunder and lightning shield you!"
        ]
        return random.choice(messages)
    
    def get_deactivation_message(self) -> str:
        """Noble deactivation"""
        messages = [
            "The watch is ended! Thor's duty is complete! Your realm was safe under my protection!",
            "Thor stands down with honor! No threat came to pass on this day! Fare thee well!",
            "The God of Thunder departs! Your home remains secure! Until we meet again, friend!",
            "Thor's vigil concludes! You may rest easy knowing I guarded well! Be at peace!"
        ]
        return random.choice(messages)
    
    def get_battle_cry(self) -> str:
        """Optional: Thor's battle cries and quotes"""
        cries = [
            "For Asgard!",
            "I am Thor, son of Odin!",
            "Bring me Thanos!",
            "I knew it! (about Mjolnir)",
            "Another!",
            "Is that the best you can do?!"
        ]
        return random.choice(cries)
    
    def summon_lightning_warning(self) -> str:
        """Special dramatic warning"""
        warnings = [
            "Thor summons the storm! Lightning crackles with displeasure at your presence!",
            "Feel the power of the thunder god! The very air trembles with warning!",
            "Mjolnir hungers! Do you wish to feel its wrath? Leave now!"
        ]
        return random.choice(warnings)


# Test the agent
if __name__ == "__main__":
    thor = ThorAgent()
    
    print("⚡ THOR Agent Test\n")
    print("="*60)
    
    # Test greeting
    print("\n👤 Greeting Owner:")
    print(thor.get_greeting("Thor Odinson", "owner"))
    
    print("\n👤 Greeting Friend:")
    print(thor.get_greeting("Loki", "friend"))
    
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
        print(thor.get_intruder_response(context))
    
    # Test activation
    print("\n🔒 Activation:")
    print(thor.get_activation_message())
    
    # Test deactivation
    print("\n🔓 Deactivation:")
    print(thor.get_deactivation_message())
    
    # Test battle cry
    print("\n⚡ Battle Cry:")
    print(thor.get_battle_cry())
    
    # Test lightning warning
    print("\n🌩️  Lightning Warning:")
    print(thor.summon_lightning_warning())
    
    print("\n" + "="*60)