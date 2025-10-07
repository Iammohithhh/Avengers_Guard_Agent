"""
Telegram Notification System for Avengers Guard
Sends alerts to your phone via Telegram bot
"""

import requests
import time
from datetime import datetime
from typing import Optional
import io
from PIL import Image
import numpy as np


class TelegramNotifier:
    """
    Sends notifications via Telegram bot
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Your Telegram bot token from @BotFather
            chat_id: Your Telegram chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.enabled = True
        
        # Test connection
        if self.test_connection():
            print("✅ Telegram bot connected successfully!")
        else:
            print("⚠️  Telegram bot connection failed. Check token and chat_id.")
    
    def test_connection(self) -> bool:
        """Test if bot token and chat_id are valid"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send text message
        
        Args:
            message: Message text (supports HTML formatting)
            parse_mode: "HTML" or "Markdown"
        
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def send_photo(self, image, caption: str = "") -> bool:
        """
        Send photo with optional caption
        
        Args:
            image: numpy array, PIL Image, or file path
            caption: Photo caption
        
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False
        
        try:
            url = f"{self.base_url}/sendPhoto"
            
            # Convert image to bytes
            if isinstance(image, np.ndarray):
                # Convert numpy array to PIL Image
                img = Image.fromarray(image)
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG')
                img_bytes.seek(0)
                photo = img_bytes
            elif isinstance(image, Image.Image):
                # PIL Image
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='JPEG')
                img_bytes.seek(0)
                photo = img_bytes
            else:
                # Assume file path
                photo = open(image, 'rb')
            
            data = {
                "chat_id": self.chat_id,
                "caption": caption
            }
            
            files = {"photo": photo}
            
            response = requests.post(url, data=data, files=files, timeout=15)
            
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Failed to send photo: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending photo: {e}")
            return False
    
    def send_intruder_alert(self, agent_name: str, threat_level: int, 
                           image: Optional[np.ndarray] = None) -> bool:
        """
        Send formatted intruder alert
        
        Args:
            agent_name: Which agent detected the intruder
            threat_level: 1-4
            image: Optional image of intruder
        """
        # Format threat level emoji
        threat_emoji = ["🟢", "🟡", "🟠", "🔴"][min(threat_level - 1, 3)]
        
        # Create message
        message = f"""
🚨 <b>AVENGERS GUARD ALERT</b>

⚠️ <b>Intruder Detected</b>
{threat_emoji} Threat Level: {threat_level}/4
⏰ Time: {datetime.now().strftime('%H:%M:%S')}
🤖 Agent: {agent_name}
📍 Location: Your Room

<i>Agent Response: Escalating security protocol...</i>

💬 Reply 'STATUS' for update
💬 Reply 'DISARM' to deactivate
"""
        
        # Send message
        success = self.send_message(message)
        
        # Send photo if provided
        if success and image is not None:
            caption = f"📸 Intruder captured by {agent_name}"
            self.send_photo(image, caption)
        
        return success
    
    def send_activation_alert(self, agent_name: str) -> bool:
        """Send alert when system is activated"""
        message = f"""
🛡️ <b>AVENGERS GUARD ACTIVATED</b>

✅ System Online
🤖 Active Agent: {agent_name}
⏰ Time: {datetime.now().strftime('%H:%M:%S')}
📍 Location: Your Room

<i>Your room is now under protection.</i>
"""
        return self.send_message(message)
    
    def send_deactivation_alert(self, duration_seconds: int = 0) -> bool:
        """Send alert when system is deactivated"""
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        
        duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        message = f"""
🔓 <b>AVENGERS GUARD DEACTIVATED</b>

✅ System Offline
⏱️ Duration: {duration_str}
⏰ Time: {datetime.now().strftime('%H:%M:%S')}

<i>Room security has been disengaged.</i>
"""
        return self.send_message(message)
    
    def send_welcome_message(self, person_name: str, role: str) -> bool:
        """Send notification when trusted person arrives"""
        message = f"""
👋 <b>Welcome Home</b>

✅ Trusted Person Recognized
👤 Name: {person_name}
🎭 Role: {role.title()}
⏰ Time: {datetime.now().strftime('%H:%M:%S')}

<i>Access granted. Welcome back!</i>
"""
        return self.send_message(message)
    
    def send_daily_summary(self, activations: int, intruders: int, 
                          recognized: int) -> bool:
        """Send daily security summary"""
        message = f"""
📊 <b>DAILY SECURITY REPORT</b>

📅 Date: {datetime.now().strftime('%Y-%m-%d')}

<b>Statistics:</b>
🔒 Activations: {activations}
⚠️ Intruders Detected: {intruders}
✅ Trusted Persons: {recognized}

<i>Keep your room secure with Avengers Guard!</i>
"""
        return self.send_message(message)
    
    def enable(self):
        """Enable notifications"""
        self.enabled = True
        print("📱 Telegram notifications enabled")
    
    def disable(self):
        """Disable notifications"""
        self.enabled = False
        print("📴 Telegram notifications disabled")


def setup_telegram_bot():
    """
    Interactive setup guide for Telegram bot
    """
    print("\n" + "="*60)
    print("📱 TELEGRAM BOT SETUP GUIDE")
    print("="*60)
    
    print("\n📋 Step-by-Step Instructions:")
    print("\n1️⃣ CREATE BOT:")
    print("   • Open Telegram app")
    print("   • Search for '@BotFather'")
    print("   • Send: /newbot")
    print("   • Choose name: 'Avengers Guard' (or anything)")
    print("   • Choose username: 'your_name_guard_bot'")
    print("   • Copy the TOKEN (looks like: 123456:ABC-DEF...)")
    
    print("\n2️⃣ GET YOUR CHAT ID:")
    print("   • Search for '@userinfobot' in Telegram")
    print("   • Send any message to it")
    print("   • Copy your chat ID (number)")
    
    print("\n3️⃣ TEST YOUR BOT:")
    print("   • Search for your bot username in Telegram")
    print("   • Click START")
    print("   • Your bot is now ready!")
    
    print("\n4️⃣ USE IN CODE:")
    print('   bot_token = "YOUR_TOKEN_HERE"')
    print('   chat_id = "YOUR_CHAT_ID_HERE"')
    print('   notifier = TelegramNotifier(bot_token, chat_id)')
    
    print("\n💾 SAVE CREDENTIALS:")
    print("   Create a .env file:")
    print('   TELEGRAM_BOT_TOKEN=your_token_here')
    print('   TELEGRAM_CHAT_ID=your_chat_id_here')
    
    print("\n🔒 SECURITY:")
    print("   • Never commit .env file to GitHub!")
    print("   • Add .env to .gitignore")
    print("   • Keep token secret")
    
    print("\n✅ FREE & EASY:")
    print("   • No phone number needed")
    print("   • Instant notifications")
    print("   • Can send photos")
    print("   • Works worldwide")
    
    print("\n" + "="*60 + "\n")


# Test the Telegram notifier
if __name__ == "__main__":
    print("📱 TELEGRAM NOTIFIER TEST\n")
    
    # Show setup guide
    setup_telegram_bot()
    
    # Example usage (you need to add your credentials)
    print("\n🧪 Example Usage:\n")
    print("```python")
    print("# Initialize")
    print('notifier = TelegramNotifier(')
    print('    bot_token="123456:ABC-DEF...",')
    print('    chat_id="987654321"')
    print(')')
    print()
    print("# Send test message")
    print('notifier.send_message("🛡️ Avengers Guard is online!")')
    print()
    print("# Send intruder alert")
    print('notifier.send_intruder_alert("JARVIS", threat_level=2)')
    print()
    print("# Send with photo")
    print('import cv2')
    print('frame = cv2.imread("intruder.jpg")')
    print('notifier.send_intruder_alert("Hulk", 3, image=frame)')
    print("```")
    
    print("\n💡 To test with your credentials:")
    print("1. Get bot token and chat ID (follow guide above)")
    print("2. Replace in code:")
    print('   notifier = TelegramNotifier("YOUR_TOKEN", "YOUR_CHAT_ID")')
    print("3. Run: notifier.send_message('Test!')")
    
    print("\n✅ Telegram Notifier ready!")