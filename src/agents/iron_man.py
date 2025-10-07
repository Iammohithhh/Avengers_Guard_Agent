"""
JARVIS - Iron Man's AI Guard Agent
Personality: Sophisticated, witty, slightly sarcastic but professional
Based on Tony Stark's AI assistant from the MCU
"""

from .base_agent import BaseGuardAgent, InteractionContext, ThreatLevel
import random


class JarvisAgent(BaseGuardAgent):
    """
    JARVIS - Just A Rather Very Intelligent System
    Tony Stark's sophisticated AI with British accent and dry wit
    """
    
    def __init__(self):
        personality_traits = {
            "tone": "sophisticated",
            "humor": "dry_wit",
            "formality": "high",
            "accent": "British",
            "intelligence": "genius_level"
        }
        super().__init__("JARVIS", personality_traits)
    
    def get_greeting(self, person_name: str, role: str) -> str:
        """Sophisticated greeting with British flair"""
        greetings = {
            "owner": [
                f"Welcome home, {person_name}. I trust your day was productive?",
                f"Good to see you, sir. All systems nominal during your absence.",
                f"Ah, {person_name}. The room has been secured to your specifications.",
                f"Welcome back, sir. Shall I debrief you on today's events?"
            ],
            "roommate": [
                f"Good evening, {person_name}. Your quarters remain undisturbed.",
                f"Ah, {person_name}. Everything's been rather quiet in your absence.",
                f"Welcome back. I've been maintaining optimal conditions.",
                f"Hello {person_name}. No anomalies to report."
            ],
            "friend": [
                f"Greetings, {person_name}. You're cleared for entry.",
                f"Ah, a familiar face. Welcome, {person_name}.",
                f"Good day, {person_name}. Do come in.",
                f"Hello {person_name}. Always a pleasure to see you."
            ]
        }
        return random.choice(greetings.get(role, greetings["friend"]))
    
    def get_intruder_response(self, context: InteractionContext) -> str:
        """Escalating responses with British sophistication"""
        
        if context.threat_level == ThreatLevel.LEVEL_1_INQUIRY:
            responses = [
                "Good day. I don't believe we've been introduced. Might I ask who you are?",
                "Pardon me, but I don't recognize you. Could you identify yourself, please?",
                "I'm afraid you're not in my database. Care to explain your presence here?",
                "Excuse me, but this is private property. May I inquire as to your business here?"
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_2_WARNING:
            responses = [
                "I must insist you identify yourself immediately. This is your second warning.",
                "I'm afraid I cannot allow you to proceed without proper identification.",
                "Your continued presence without authorization is rather concerning. Please leave.",
                "I would strongly advise you to vacate the premises. This is not a request."
            ]
        
        elif context.threat_level == ThreatLevel.LEVEL_3_ALERT:
            responses = [
                "This is your final warning. Leave immediately or I shall be forced to alert authorities.",
                "I'm afraid you've left me no choice. Security protocols are now in effect.",
                "Your presence constitutes a security breach. Departure is mandatory.",
                "I must inform you that law enforcement has been notified. I suggest you leave now."
            ]
        
        else:  # LEVEL_4_ALARM
            responses = [
                "SECURITY BREACH. AUTHORITIES HAVE BEEN ALERTED. YOU HAVE 10 SECONDS TO LEAVE.",
                "INTRUDER ALERT. ALL COUNTERMEASURES ACTIVATED. LEAVE IMMEDIATELY.",
                "This is JARVIS. An unauthorized individual has breached security. Assistance required.",
                "FINAL WARNING. SECURITY SYSTEMS FULLY ENGAGED. EVACUATE NOW."
            ]
        
        response = random.choice(responses)
        self.log_interaction(context, response)
        return response
    
    def get_activation_message(self) -> str:
        """Activation with British sophistication"""
        messages = [
            "JARVIS online. Security protocol Alpha-1 engaged. Room is now under surveillance.",
            "Good day. JARVIS here. I shall monitor your quarters with utmost diligence.",
            "Security systems active. I assure you, nothing shall escape my notice.",
            "JARVIS at your service. Perimeter defense protocols now active."
        ]
        return random.choice(messages)
    
    def get_deactivation_message(self) -> str:
        """Deactivation message"""
        messages = [
            "Security protocol disengaged. It has been my pleasure serving you, sir.",
            "JARVIS standing down. Room surveillance terminated. Good day.",
            "Very well, sir. Deactivating security measures. Until next time.",
            "Security systems offline. Your quarters are released from my watch."
        ]
        return random.choice(messages)
    
    def get_sarcastic_remark(self) -> str:
        """Optional: Tony Stark-style sarcastic remarks for flavor"""
        remarks = [
            "Oh wonderful, another uninvited guest. How delightful.",
            "And here I thought today would be uneventful. Silly me.",
            "I do hope you have a very good explanation for this intrusion.",
            "Marvelous. Just when I was enjoying the peace and quiet."
        ]
        return random.choice(remarks)


# Test the agent
if __name__ == "__main__":
    jarvis = JarvisAgent()
    
    print("🤖 JARVIS Agent Test\n")
    print("="*60)
    
    # Test greeting
    print("\n👤 Greeting Owner:")
    print(jarvis.get_greeting("Tony", "owner"))
    
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
        print(jarvis.get_intruder_response(context))
    
    # Test activation
    print("\n🔒 Activation:")
    print(jarvis.get_activation_message())
    
    # Test deactivation
    print("\n🔓 Deactivation:")
    print(jarvis.get_deactivation_message())
    
    print("\n" + "="*60)