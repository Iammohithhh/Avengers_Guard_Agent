"""
Avengers Guard Web Interface - Flask Server
Wraps existing system without modifying it
"""

from flask import Flask, render_template, Response, jsonify, request
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
import json
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import your existing system (don't modify anything)
from src.core.state_machine import EscalationStateMachine
from src.agents.agent_manager import AgentManager
from src.agents.base_agent import ThreatLevel
from src.audio.sound_effects import SoundEffectsManager
from src.notifications.telegram_bot import TelegramNotifier

# Import from milestone notebooks if available
try:
    from src.integration.milestone2_classes import FaceEnrollmentSystem, FaceRecognitionEngine
    FACE_RECOGNITION_AVAILABLE = True
except:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️  Face recognition not available")

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'avengers-guard-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global system state
class WebGuardSystem:
    """Wrapper around your existing system for web interface"""
    
    def __init__(self):
        self.state_machine = EscalationStateMachine()
        self.agent_manager = AgentManager(rotation_mode="threat_based")
        self.current_agent = "jarvis"
        self.agent_manager.set_active_agent(self.current_agent)
        
        # Initialize face recognition if available
        if FACE_RECOGNITION_AVAILABLE:
            import os
            os.chdir(str(Path(__file__).parent / 'notebooks')) 

            self.enrollment = FaceEnrollmentSystem()
            os.chdir(str(Path(__file__).parent))  # Change back

            self.face_engine = FaceRecognitionEngine(self.enrollment)
        else:
            self.enrollment = None
            self.face_engine = None
        
        self.is_active = False
        self.frame_count = 0
        self.last_response_time = {}
        
        print("✅ Web Guard System initialized")
    
    def activate(self):
        """Activate guard mode"""
        self.state_machine.activate()
        self.is_active = True
        agent_name, message = self.agent_manager.get_activation_message()
        
        return {
            'status': 'activated',
            'agent': agent_name,
            'message': message
        }
    
    def deactivate(self):
        """Deactivate guard mode"""
        duration = self.state_machine.deactivate()
        self.is_active = False
        agent_name, message = self.agent_manager.get_deactivation_message()
        
        stats = self.state_machine.get_statistics()
        
        return {
            'status': 'deactivated',
            'agent': agent_name,
            'message': message,
            'duration': int(duration),
            'stats': stats
        }
    
    def process_frame(self, frame_data):
        """Process frame from webcam"""
        self.frame_count += 1
        
        # Decode base64 frame
        try:
            img_data = base64.b64decode(frame_data.split(',')[1])
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            return {'error': str(e)}
        
        if not self.is_active:
            return {'status': 'inactive', 'frame': frame_data}
        
        # Skip frames for performance
        if self.frame_count % 3 != 0:
            return {'status': 'skipped', 'frame': frame_data}
        
        # Process with face recognition
        detections = []
        if self.face_engine:
            annotated_frame, dets = self.face_engine.process_frame(frame)
            
            for det in dets:
                if det['trusted']:
                    person = self.enrollment.trusted_persons[det['name']]
                    agent_name, greeting = self.agent_manager.get_greeting(
                        det['name'], person.role
                    )
                    detections.append({
                        'type': 'trusted',
                        'name': det['name'],
                        'role': person.role,
                        'message': greeting,
                        'agent': agent_name
                    })
                else:
                    # Handle intruder
                    response_data = self._handle_intruder(det, frame)
                    if response_data:
                        detections.append(response_data)
            
            # Encode annotated frame back to base64
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            frame_data = f"data:image/jpeg;base64,{frame_base64}"
        
        # Cleanup old intruders
        self.state_machine.cleanup_old_intruders()
        
        return {
            'status': 'processed',
            'frame': frame_data,
            'detections': detections,
            'current_agent': self.current_agent
        }
    
    def _handle_intruder(self, detection, frame):
        """Handle intruder detection"""
        import time
        
        loc = detection['location']
        intruder_id = f"intruder_{loc[0]}_{loc[1]}"
        
        # Process in state machine
        info = self.state_machine.process_detection(intruder_id, loc)
        threat_level = info['threat_level']
        time_present = info['time_present']
        
        # Check if should respond
        current_time = time.time()
        if intruder_id in self.last_response_time:
            time_since = current_time - self.last_response_time[intruder_id]
            intervals = {1: 8, 2: 5, 3: 3, 4: 1}
            if time_since < intervals.get(threat_level, 5):
                return None
        
        # Select agent
        agent_map = {1: "jarvis", 2: "captain_america", 3: "hulk", 4: "thor"}
        selected_agent = agent_map.get(threat_level, "jarvis")
        
        if selected_agent != self.current_agent:
            self.current_agent = selected_agent
            self.agent_manager.set_active_agent(selected_agent)
        
        # Get response
        from src.agents.base_agent import InteractionContext
        context = InteractionContext(
            person_name=None,
            is_trusted=False,
            threat_level=ThreatLevel(threat_level),
            interaction_count=threat_level,
            time_since_first_detection=time_present,
            previous_responses=[]
        )
        agent_name, response = self.agent_manager.get_intruder_response(context)
        
        self.last_response_time[intruder_id] = current_time
        self.state_machine.add_response(intruder_id, response)
        
        return {
            'type': 'intruder',
            'threat_level': threat_level,
            'agent': selected_agent,
            'message': response,
            'time_present': int(time_present)
        }
    
    def get_status(self):
        """Get current system status"""
        stats = self.state_machine.get_statistics()
        enrolled = len(self.enrollment.trusted_persons) if self.enrollment else 0
        
        return {
            'is_active': self.is_active,
            'current_agent': self.current_agent,
            'enrolled_persons': enrolled,
            'stats': stats
        }

# Initialize system
guard_system = WebGuardSystem()

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify(guard_system.get_status())

@app.route('/api/activate', methods=['POST'])
def activate():
    """Activate guard mode"""
    result = guard_system.activate()
    return jsonify(result)

@app.route('/api/deactivate', methods=['POST'])
def deactivate():
    """Deactivate guard mode"""
    result = guard_system.deactivate()
    return jsonify(result)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print('Client connected')
    emit('status', guard_system.get_status())

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print('Client disconnected')

@socketio.on('frame')
def handle_frame(data):
    """Process video frame"""
    result = guard_system.process_frame(data['frame'])
    emit('result', result)

@socketio.on('activate')
def handle_activate():
    """Activate via websocket"""
    result = guard_system.activate()
    emit('activation_result', result, broadcast=True)

@socketio.on('deactivate')
def handle_deactivate():
    """Deactivate via websocket"""
    result = guard_system.deactivate()
    emit('deactivation_result', result, broadcast=True)

if __name__ == '__main__':
    print("\n🦾 Starting Avengers Guard Web Interface...")
    print("="*60)
    print("Open browser to: http://localhost:5000")
    print("="*60 + "\n")
    
    socketio.run(app, debug=False, host='127.0.0.1', port=5000, use_reloader=False)