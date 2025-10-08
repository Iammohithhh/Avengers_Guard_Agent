# Avengers Guard Agent

<div align="center">

**Multi-Modal AI Security Agent with Personality**

Voice Activation • Face Recognition • Dynamic Dialogue • Escalating Threat Response

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[Demo Video](#) • [Documentation](#) • [Report](docs/report.md)

</div>

---

## What is This?

An AI-powered room security system inspired by Marvel's JARVIS that:

1. Activates by voice: Say "Jarvis, guard my room" or "Avengers assemble"
2. Recognizes faces: Welcomes trusted users, detects intruders
3. Engages with personality*: 4 distinct AI agents (JARVIS → Captain America → Hulk → Thor)
4. Escalates threats: Polite inquiry → Firm warning → Stern threat → Loud alarm

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Clone and install
git clone https://github.com/yourusername/avengers-guard
cd avengers-guard
pip install -r requirements.txt

# 2. Enroll your face
python scripts/enroll_face.py --name "YourName" --role owner

# 3. Run the system
python scripts/run_guard.py --duration 60
```

##  Performance

| Metric | Target | Achieved |
|--------|--------|----------|
| Voice Activation | 90% | **95%** ✅ |
| Face Recognition | 80% | **87%** ✅ |
| Escalation Levels | 3+ | **4** ✅ |

##  Demo

<div align="center">

### Level 1: JARVIS (Polite)
> *"Good day. I don't believe we've been introduced. Might I inquire as to your business here?"*

### Level 2: Captain America (Firm)
> *"I'm asking you nicely - leave now. This isn't your property."*

### Level 3: Hulk (Threatening)
> *"HULK ANGRY NOW! You made big mistake! GET OUT!"*

### Level 4: Thor (Alarm)
> *"FOR ASGARD! INTRUDER ALERT! Thor calls down the lightning!"*

</div>

##  Architecture

```
Speech (Whisper) ──┐
                   ├──► State Machine ──► Escalation Logic
Vision (dlib)   ───┤         │
                   │         ├──► Agent Selection
LLM (Gemini)    ───┘         │    (JARVIS/Cap/Hulk/Thor)
                             │
                             └──► Output
                                  ├─ TTS (Edge TTS)
                                  ├─ Sound Effects
                                  └─ Telegram Alerts
```

##  Installation

### Prerequisites
- Python 3.9+
- Webcam
- Microphone
- (Optional) Gemini API key for dynamic dialogue

### Detailed Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Configure API keys
cp .env.example .env
# Edit .env with your keys:
# GEMINI_API_KEY=your_key_here
# TELEGRAM_BOT_TOKEN=your_token_here
```

### Sound Files (Optional)

Download sound effects and place in `sounds/` directory:
- `sounds/agents/` - Agent-specific sounds (jarvis_alert.mp3, hulk_smash.mp3, etc.)
- `sounds/system/` - System sounds (avengers_theme.mp3, alarm.mp3)

##  Usage

### Method 1: Jupyter Notebooks (Recommended for Testing)

```bash
jupyter notebook notebooks/milestone3.ipynb
```

Then run cells to:
1. Enroll faces
2. Test components
3. Run full system

### Method 2: Python Scripts

```python
from src.integration.milestone3 import AvengersGuardSystem, AvengersGuardConfig

# Initialize
config = AvengersGuardConfig()
system = AvengersGuardSystem(config)

# Option A: Voice activation
system.listen_for_activation(timeout=30)

# Option B: Manual activation
system.run_monitoring(duration=60)
```

### Method 3: Command Line

```bash
# Enroll faces
python -m src.scripts.enroll --name "John" --role owner

# Run system
python -m src.scripts.run_guard --duration 60 --voice-activation

# Test components
python -m src.scripts.test_all
```

## Configuration

Edit `src/integration/milestone3.ipynb` or create a config:

```python
class AvengersGuardConfig:
    # Feature toggles
    ENABLE_LLM = True           # Dynamic dialogue (needs API key)
    ENABLE_SOUND_FX = True      # Sound effects
    ENABLE_NOTIFICATIONS = True  # Telegram alerts
    
    # Timing
    ESCALATION_TIMES = {
        1: 0,   # JARVIS: Immediate
        2: 5,   # Cap: After 5s
        3: 15,  # Hulk: After 15s
        4: 25   # Thor: After 25s
    }
    
    # Recognition
    RECOGNITION_CONFIDENCE = 0.6  # Lower = stricter
    FRAME_SKIP = 3                # Process every Nth frame
```

##  Testing

```bash
# Test voice activation
python -m pytest tests/test_voice.py

# Test face recognition
python -m pytest tests/test_vision.py

# Test escalation
python -m pytest tests/test_escalation.py

# Run all tests
python -m pytest tests/ -v
```

## 📁 Project Structure

```
avengers-guard/
├── src/
│   ├── agents/          # Agent personalities (JARVIS, Cap, Hulk, Thor)
│   ├── audio/           # Sound effects manager
│   ├── core/            # State machine & escalation logic
│   ├── dialogue/        # LLM integration (Gemini)
│   ├── integration/     # Complete system classes
│   └── notifications/   # Telegram notifications
├── notebooks/
│   ├── milestone1.ipynb # Voice activation demo
│   ├── milestone2.ipynb # Face recognition demo
│   └── milestone3.ipynb # Complete system demo
├── sounds/              # Audio files
├── data/                # Face database               
└── docs/
    └── report.md        # Full project report
```

##  Milestones

### ✅ Milestone 1: Voice Activation
- **Goal:** Activate system via voice commands
- **Tech:** Faster-Whisper, Google Speech API
- **Accuracy:** 95% (19/20 commands)

### ✅ Milestone 2: Face Recognition
- **Goal:** Recognize trusted users, detect intruders
- **Tech:** dlib, face_recognition library
- **Accuracy:** 87% (44/50 correct IDs)

### ✅ Milestone 3: Escalating Dialogue
- **Goal:** 4-level threat response with personality
- **Tech:** Google Gemini LLM, pre-scripted fallbacks
- **Result:** 100% agent switching, 95% in-character responses



## Contact

Questions? Open an issue or reach out:
- Email: mohithiitb23@gmail.com

---

<div align="center">

**Built with ❤️ as part of EE 782 - Advanced Machine Learning Course**

*"I am Iron Man... but you can call me JARVIS."*

</div>
