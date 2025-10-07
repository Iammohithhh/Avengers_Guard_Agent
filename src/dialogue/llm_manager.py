"""
LLM Manager for Conversational Agents
Integrates Google Gemini or OpenAI for dynamic dialogue
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ConversationMessage:
    """Represents a message in the conversation"""
    role: str  # 'system', 'user', or 'assistant'
    content: str


class LLMManager:
    """
    Manages LLM integration for dynamic agent responses
    Supports Google Gemini and OpenAI GPT
    """
    
    def __init__(self, provider: str = "gemini", api_key: Optional[str] = None):
        """
        Initialize LLM manager
        
        Args:
            provider: "gemini" or "openai"
            api_key: API key (or set in environment)
        """
        self.provider = provider.lower()
        self.api_key = api_key or self._get_api_key()
        self.conversation_history: List[ConversationMessage] = []
        self.max_history = 10  # Keep last 10 messages
        
        # Initialize provider
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment"""
        if self.provider == "gemini":
            return os.getenv("GEMINI_API_KEY")
        elif self.provider == "openai":
            return os.getenv("OPENAI_API_KEY")
        return None
    
    def _init_gemini(self):
        """Initialize Google Gemini"""
        try:
            import google.generativeai as genai
            
            if not self.api_key:
                print("⚠️  GEMINI_API_KEY not found. Set it in environment or pass to constructor.")
                print("   Get free key at: https://makersuite.google.com/app/apikey")
                self.model = None
                return
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.chat = None  # Will initialize per conversation
            print("✅ Google Gemini initialized")
            
        except ImportError:
            print("❌ google-generativeai not installed. Run: pip install google-generativeai")
            self.model = None
        except Exception as e:
            print(f"❌ Gemini initialization failed: {e}")
            self.model = None
    
    def _init_openai(self):
        """Initialize OpenAI GPT"""
        try:
            import openai
            
            if not self.api_key:
                print("⚠️  OPENAI_API_KEY not found. Set it in environment.")
                self.client = None
                return
            
            openai.api_key = self.api_key
            self.client = openai
            print("✅ OpenAI GPT initialized")
            
        except ImportError:
            print("❌ openai not installed. Run: pip install openai")
            self.client = None
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
            self.client = None
    
    def set_system_prompt(self, agent_personality: str, context: str = ""):
        """
        Set system prompt with agent personality
        
        Args:
            agent_personality: Agent's personality description
            context: Additional context (threat level, previous interactions)
        """
        system_prompt = f"""You are an AI security guard with the following personality:
{agent_personality}

Context: {context}

Your role is to:
1. Detect and respond to intruders with escalating firmness
2. Maintain your character personality consistently
3. Be brief (1-2 sentences per response)
4. Escalate from polite to stern based on threat level

Keep responses natural and in-character. Never break character."""
        
        # Reset conversation with new system prompt
        self.conversation_history = [
            ConversationMessage(role="system", content=system_prompt)
        ]
        
        # For Gemini, reinitialize chat
        if self.provider == "gemini" and self.model:
            self.chat = self.model.start_chat(history=[])
    
    def generate_response(self, user_input: str, threat_level: int = 1,
                         fallback_responses: List[str] = None) -> str:
        """
        Generate response using LLM
        
        Args:
            user_input: What the intruder said/did
            threat_level: 1-4, affects response tone
            fallback_responses: Pre-scripted responses if LLM fails
        
        Returns:
            Generated response string
        """
        # Add context about threat level
        context_input = f"[Threat Level {threat_level}/4] {user_input}"
        
        try:
            if self.provider == "gemini":
                return self._generate_gemini(context_input, fallback_responses)
            elif self.provider == "openai":
                return self._generate_openai(context_input, fallback_responses)
        except Exception as e:
            print(f"❌ LLM generation failed: {e}")
            return self._get_fallback(fallback_responses, threat_level)
    
    def _generate_gemini(self, user_input: str, fallback: List[str] = None) -> str:
        """Generate response using Gemini"""
        if not self.model:
            return self._get_fallback(fallback, 1)
        
        try:
            # Add user message to history
            self.conversation_history.append(
                ConversationMessage(role="user", content=user_input)
            )
            
            # Generate response
            if self.chat is None:
                # Start new chat with history
                self.chat = self.model.start_chat(history=[])
            
            response = self.chat.send_message(user_input)
            response_text = response.text.strip()
            
            # Add to history
            self.conversation_history.append(
                ConversationMessage(role="assistant", content=response_text)
            )
            
            # Trim history
            self._trim_history()
            
            return response_text
            
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            return self._get_fallback(fallback, 1)
    
    def _generate_openai(self, user_input: str, fallback: List[str] = None) -> str:
        """Generate response using OpenAI GPT"""
        if not self.client:
            return self._get_fallback(fallback, 1)
        
        try:
            # Add user message to history
            self.conversation_history.append(
                ConversationMessage(role="user", content=user_input)
            )
            
            # Prepare messages for API
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in self.conversation_history
            ]
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # or "gpt-3.5-turbo"
                messages=messages,
                max_tokens=100,
                temperature=0.8
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Add to history
            self.conversation_history.append(
                ConversationMessage(role="assistant", content=response_text)
            )
            
            # Trim history
            self._trim_history()
            
            return response_text
            
        except Exception as e:
            print(f"⚠️  OpenAI error: {e}")
            return self._get_fallback(fallback, 1)
    
    def _get_fallback(self, fallback_responses: Optional[List[str]], 
                     threat_level: int) -> str:
        """Get fallback response if LLM fails"""
        if fallback_responses and len(fallback_responses) > 0:
            # Use threat level to select response
            index = min(threat_level - 1, len(fallback_responses) - 1)
            return fallback_responses[index]
        
        # Default fallback
        fallbacks = [
            "Who are you? Please identify yourself.",
            "You need to leave now. This is private property.",
            "This is your final warning. Leave immediately or I'm calling the police.",
            "INTRUDER ALERT! Authorities have been notified!"
        ]
        index = min(threat_level - 1, len(fallbacks) - 1)
        return fallbacks[index]
    
    def _trim_history(self):
        """Keep conversation history under max_history limit"""
        # Always keep system prompt
        if len(self.conversation_history) > self.max_history:
            system_msg = self.conversation_history[0]
            recent_msgs = self.conversation_history[-(self.max_history-1):]
            self.conversation_history = [system_msg] + recent_msgs
    
    def reset_conversation(self):
        """Clear conversation history (keep system prompt)"""
        if len(self.conversation_history) > 0:
            system_msg = self.conversation_history[0]
            self.conversation_history = [system_msg]
        
        # Reset Gemini chat
        if self.provider == "gemini" and self.model:
            self.chat = self.model.start_chat(history=[])
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history as list of dicts"""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.conversation_history
        ]


class AgentLLMIntegration:
    """
    Integrates LLM with Avengers agents
    Maintains agent personality while using LLM for dynamic responses
    """
    
    def __init__(self, llm_manager: LLMManager):
        """
        Initialize with LLM manager
        
        Args:
            llm_manager: Configured LLMManager instance
        """
        self.llm = llm_manager
        self.agent_prompts = self._get_agent_prompts()
        self.current_agent = None
    
    def _get_agent_prompts(self) -> Dict[str, str]:
        """Get system prompts for each agent"""
        return {
            "jarvis": """You are JARVIS, Tony Stark's sophisticated British AI assistant.
Personality: Polite, witty, highly intelligent, formal British accent
Tone: Professional but with dry humor
Response style: Eloquent, uses "sir", formal vocabulary
Example: "Good day. I don't believe we've been introduced. Might I inquire as to your business here?"
Keep responses brief (1-2 sentences). Maintain British sophistication.""",
            
            "captain_america": """You are Captain America, Steve Rogers.
Personality: Honest, direct, principled, fair but firm
Tone: Respectful but authoritative
Response style: Clear, straightforward, no-nonsense soldier
Example: "Hold on there. I haven't seen you before. Mind introducing yourself?"
Keep responses brief (1-2 sentences). Stay true to your values.""",
            
            "black_widow": """You are Black Widow, Natasha Romanoff.
Personality: Strategic, observant, calm, psychologically intimidating
Tone: Cool, calculating, subtly threatening
Response style: Reads people, strategic statements, controlled
Example: "I don't know you. And I remember faces. Want to tell me why you're here?"
Keep responses brief (1-2 sentences). Use psychological tactics.""",
            
            "hulk": """You are Hulk.
Personality: Simple, direct, protective, quick to anger
Tone: Aggressive, loud when threatened
Response style: Simple words, short sentences, CAPS when angry, protective
Example: "WHO YOU?! Hulk not know you! Tell Hulk now!"
Keep responses VERY brief. Simple language. Get angry with threats.""",
            
            "thor": """You are Thor, God of Thunder.
Personality: Mighty, dramatic, honorable, Asgardian warrior
Tone: Noble, theatrical, uses archaic language
Response style: Dramatic, references Asgard/Odin, mighty warrior
Example: "Hold, stranger! By Odin's beard, identify yourself!"
Keep responses brief (1-2 sentences). Be dramatic and mighty."""
        }
    
    def set_agent(self, agent_name: str, threat_level: int = 1):
        """
        Set active agent and configure LLM personality
        
        Args:
            agent_name: Name of agent (jarvis, captain_america, etc.)
            threat_level: Current threat level (1-4)
        """
        self.current_agent = agent_name.lower()
        
        if self.current_agent not in self.agent_prompts:
            print(f"⚠️  Unknown agent: {agent_name}")
            self.current_agent = "jarvis"
        
        # Get agent personality prompt
        personality = self.agent_prompts[self.current_agent]
        
        # Add threat level context
        threat_context = f"""
Current Situation: Intruder detected, Threat Level {threat_level}/4
- Level 1: Be polite but firm, ask questions
- Level 2: Be more assertive, give warnings
- Level 3: Be stern and threatening, mention police
- Level 4: Be very loud and aggressive, emergency mode

Respond according to threat level while maintaining your personality."""
        
        # Set system prompt
        self.llm.set_system_prompt(personality, threat_context)
    
    def generate_intruder_response(self, agent_name: str, threat_level: int,
                                   intruder_action: str = "standing in room",
                                   use_llm: bool = True) -> str:
        """
        Generate response to intruder
        
        Args:
            agent_name: Which agent is responding
            threat_level: 1-4
            intruder_action: What the intruder is doing
            use_llm: If False, use pre-scripted responses
        
        Returns:
            Agent's response string
        """
        # Pre-scripted fallback responses for each agent
        fallbacks = self._get_fallback_responses(agent_name, threat_level)
        
        if not use_llm:
            # Use pre-scripted responses
            import random
            return random.choice(fallbacks)
        
        # Set agent personality if changed
        if self.current_agent != agent_name.lower():
            self.set_agent(agent_name, threat_level)
        
        # Generate LLM response
        user_input = f"An unidentified person is {intruder_action} in the room. Respond to them."
        
        response = self.llm.generate_response(
            user_input, 
            threat_level=threat_level,
            fallback_responses=fallbacks
        )
        
        return response
    
    def _get_fallback_responses(self, agent_name: str, threat_level: int) -> List[str]:
        """Get pre-scripted fallback responses"""
        responses_db = {
            "jarvis": [
                "Good day. I don't believe we've been introduced. Might I ask who you are?",
                "I must insist you identify yourself immediately. This is your second warning.",
                "This is your final warning. Leave immediately or I shall alert authorities.",
                "SECURITY BREACH. AUTHORITIES ALERTED. YOU HAVE 10 SECONDS TO LEAVE."
            ],
            "captain_america": [
                "Hold on there. I haven't seen you before. Mind introducing yourself?",
                "I'm asking you nicely - leave now. This isn't your property.",
                "That's enough. You're breaking the law. Leave now or I'm calling the police.",
                "INTRUDER ALERT! This room is under protection. Police have been notified!"
            ],
            "black_widow": [
                "I don't know you. And I remember faces. Want to tell me why you're here?",
                "You're making me nervous. And trust me, you don't want that. Time to go.",
                "Wrong move. I've cataloged your face. Authorities incoming.",
                "RED ALERT. Intruder fully identified. Police dispatched."
            ],
            "hulk": [
                "WHO YOU?! Hulk not know you! Tell Hulk now!",
                "HULK SAID LEAVE! You not listen?! GO NOW!",
                "HULK ANGRY NOW! You made big mistake! GET OUT!",
                "HULK SMAAAAAASH! INTRUDER! POLICE COMING NOW!"
            ],
            "thor": [
                "Hold, stranger! By Odin's beard, identify yourself!",
                "By Mjolnir's might, I command you to leave!",
                "The thunder rumbles for you! Guardians summoned!",
                "FOR ASGARD! INTRUDER ALERT! Thor calls down the lightning!"
            ]
        }
        
        agent_key = agent_name.lower().replace(" ", "_")
        responses = responses_db.get(agent_key, responses_db["jarvis"])
        
        # Return appropriate response for threat level
        index = min(threat_level - 1, len(responses) - 1)
        return [responses[index]]
    
    def reset(self):
        """Reset conversation history"""
        self.llm.reset_conversation()


# Setup and testing functions
def setup_llm_guide():
    """Print guide for setting up LLM APIs"""
    print("\n" + "="*60)
    print("🤖 LLM SETUP GUIDE")
    print("="*60)
    
    print("\n📋 OPTION 1: Google Gemini (Recommended - FREE)")
    print("="*60)
    print("1. Visit: https://makersuite.google.com/app/apikey")
    print("2. Sign in with Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy your API key")
    print("5. Set in environment:")
    print("   export GEMINI_API_KEY='your_key_here'")
    print("\n✅ Pros: Free, fast, good quality")
    print("⚠️  Note: Rate limits on free tier")
    
    print("\n📋 OPTION 2: OpenAI GPT-4o mini")
    print("="*60)
    print("1. Visit: https://platform.openai.com/api-keys")
    print("2. Sign in / create account")
    print("3. Add payment method (gets free credits)")
    print("4. Create API key")
    print("5. Set in environment:")
    print("   export OPENAI_API_KEY='your_key_here'")
    print("\n✅ Pros: High quality, reliable")
    print("⚠️  Note: Costs money after free credits")
    
    print("\n💾 SAVE IN .env FILE:")
    print("="*60)
    print("Create a file named '.env' in your project:")
    print("```")
    print("GEMINI_API_KEY=your_gemini_key_here")
    print("OPENAI_API_KEY=your_openai_key_here")
    print("```")
    print("\nThen load in Python:")
    print("```python")
    print("from dotenv import load_dotenv")
    print("load_dotenv()")
    print("```")
    
    print("\n🔒 SECURITY:")
    print("• Never commit .env or API keys to GitHub!")
    print("• Add .env to .gitignore")
    print("• Keep keys secret")
    
    print("\n" + "="*60 + "\n")


# Test the LLM manager
if __name__ == "__main__":
    print("🤖 LLM MANAGER TEST\n")
    
    # Show setup guide
    setup_llm_guide()
    
    print("\n🧪 Example Usage:\n")
    print("```python")
    print("# Initialize LLM (Gemini)")
    print("llm = LLMManager(provider='gemini', api_key='YOUR_KEY')")
    print()
    print("# Create agent integration")
    print("agent_llm = AgentLLMIntegration(llm)")
    print()
    print("# Generate response")
    print("response = agent_llm.generate_intruder_response(")
    print("    agent_name='jarvis',")
    print("    threat_level=1,")
    print("    intruder_action='standing silently'")
    print(")")
    print("print(response)")
    print()
    print("# Escalate")
    print("response = agent_llm.generate_intruder_response(")
    print("    agent_name='hulk',")
    print("    threat_level=3,")
    print("    intruder_action='refusing to leave'")
    print(")")
    print("print(response)")
    print("```")
    
    print("\n💡 Tips:")
    print("• Set use_llm=False to test without API")
    print("• LLM makes responses more dynamic and natural")
    print("• Fallback to pre-scripted if API fails")
    print("• Test with different threat levels")
    
    print("\n✅ LLM Manager ready!")