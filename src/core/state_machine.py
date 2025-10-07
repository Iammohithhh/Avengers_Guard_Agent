"""
State Machine for Escalation Logic
Manages threat levels and auto-escalation based on intruder behavior
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


class SystemState(Enum):
    """Overall system states"""
    IDLE = "idle"
    ARMED = "armed"
    MONITORING = "monitoring"
    ALERT = "alert"
    ALARM = "alarm"


class ThreatLevel(Enum):
    """Threat escalation levels"""
    LEVEL_1_INQUIRY = 1      # Polite questioning
    LEVEL_2_WARNING = 2      # Firm warning
    LEVEL_3_ALERT = 3        # Stern alert, notify authorities
    LEVEL_4_ALARM = 4        # Maximum alert, loud alarm


@dataclass
class IntruderTracker:
    """Tracks an individual intruder"""
    intruder_id: str
    first_seen: float
    last_seen: float
    detection_count: int = 0
    threat_level: ThreatLevel = ThreatLevel.LEVEL_1_INQUIRY
    responses_given: List[str] = field(default_factory=list)
    location: tuple = (0, 0, 0, 0)  # (top, right, bottom, left)
    
    def time_present(self) -> float:
        """Get how long intruder has been present (seconds)"""
        return self.last_seen - self.first_seen
    
    def update_seen(self):
        """Update last seen timestamp"""
        self.last_seen = time.time()
        self.detection_count += 1


class EscalationStateMachine:
    """
    Manages system state and threat escalation logic
    Auto-escalates based on time and intruder persistence
    """
    
    def __init__(self):
        """Initialize state machine"""
        self.system_state = SystemState.IDLE
        self.intruders: dict[str, IntruderTracker] = {}
        self.activation_time: Optional[float] = None
        self.event_log: List[dict] = []
        
        # Escalation timing (seconds)
        self.escalation_thresholds = {
            ThreatLevel.LEVEL_1_INQUIRY: 0,      # Immediate
            ThreatLevel.LEVEL_2_WARNING: 10,     # After 10 seconds
            ThreatLevel.LEVEL_3_ALERT: 25,       # After 25 seconds total
            ThreatLevel.LEVEL_4_ALARM: 45        # After 45 seconds total
        }
        
        # Configuration
        self.auto_escalate = True
        self.max_intruders_before_alarm = 2
        self.intruder_timeout = 5.0  # Remove intruder if not seen for 5 sec
    
    def activate(self):
        """Activate the guard system"""
        self.system_state = SystemState.ARMED
        self.activation_time = time.time()
        self.log_event("system_activated", {"state": "armed"})
        print("🛡️  System ARMED")
    
    def deactivate(self):
        """Deactivate the guard system"""
        duration = self.get_active_duration()
        self.system_state = SystemState.IDLE
        self.intruders.clear()
        self.log_event("system_deactivated", {"duration_seconds": duration})
        print(f"🔓 System DEACTIVATED (was active for {int(duration)}s)")
        return duration
    
    def is_active(self) -> bool:
        """Check if system is active"""
        return self.system_state != SystemState.IDLE
    
    def get_active_duration(self) -> float:
        """Get how long system has been active (seconds)"""
        if self.activation_time:
            return time.time() - self.activation_time
        return 0.0
    
    def process_detection(self, intruder_id: str, location: tuple = (0, 0, 0, 0)) -> dict:
        """
        Process a detection event
        
        Args:
            intruder_id: Unique ID for intruder (use "intruder_1", "intruder_2", etc.)
            location: Face bounding box (top, right, bottom, left)
        
        Returns:
            dict with detection info and recommended action
        """
        current_time = time.time()
        
        # Get or create intruder tracker
        if intruder_id not in self.intruders:
            # New intruder detected
            intruder = IntruderTracker(
                intruder_id=intruder_id,
                first_seen=current_time,
                last_seen=current_time,
                location=location
            )
            self.intruders[intruder_id] = intruder
            self.system_state = SystemState.ALERT
            
            self.log_event("intruder_detected", {
                "intruder_id": intruder_id,
                "threat_level": 1
            })
            
            print(f"🚨 NEW INTRUDER: {intruder_id}")
        else:
            # Existing intruder still present
            intruder = self.intruders[intruder_id]
            intruder.update_seen()
            intruder.location = location
        
        # Auto-escalate if enabled
        if self.auto_escalate:
            self._check_escalation(intruder)
        
        # Check if we need to trigger alarm
        if len(self.intruders) >= self.max_intruders_before_alarm:
            self.system_state = SystemState.ALARM
        
        # Prepare response info
        response_info = {
            "intruder_id": intruder_id,
            "threat_level": intruder.threat_level.value,
            "time_present": intruder.time_present(),
            "detection_count": intruder.detection_count,
            "system_state": self.system_state.value,
            "action": self._get_recommended_action(intruder)
        }
        
        return response_info
    
    def _check_escalation(self, intruder: IntruderTracker):
        """Check if intruder should be escalated to next threat level"""
        time_present = intruder.time_present()
        current_level = intruder.threat_level
        
        # Check each escalation threshold
        for level, threshold in self.escalation_thresholds.items():
            if time_present >= threshold and level.value > current_level.value:
                # Escalate!
                old_level = current_level.value
                intruder.threat_level = level
                
                self.log_event("threat_escalated", {
                    "intruder_id": intruder.intruder_id,
                    "from_level": old_level,
                    "to_level": level.value,
                    "time_present": time_present
                })
                
                print(f"⚠️  ESCALATION: {intruder.intruder_id} → Level {level.value}")
                
                # Update system state
                if level == ThreatLevel.LEVEL_4_ALARM:
                    self.system_state = SystemState.ALARM
                elif level == ThreatLevel.LEVEL_3_ALERT:
                    self.system_state = SystemState.ALERT
                
                break  # Only escalate one level at a time
    
    def _get_recommended_action(self, intruder: IntruderTracker) -> str:
        """Get recommended action based on threat level"""
        level = intruder.threat_level
        
        actions = {
            ThreatLevel.LEVEL_1_INQUIRY: "speak_inquiry",
            ThreatLevel.LEVEL_2_WARNING: "speak_warning",
            ThreatLevel.LEVEL_3_ALERT: "speak_alert_and_notify",
            ThreatLevel.LEVEL_4_ALARM: "trigger_alarm"
        }
        
        return actions.get(level, "speak_inquiry")
    
    def cleanup_old_intruders(self):
        """Remove intruders that haven't been seen recently"""
        current_time = time.time()
        to_remove = []
        
        for intruder_id, intruder in self.intruders.items():
            time_since_seen = current_time - intruder.last_seen
            if time_since_seen > self.intruder_timeout:
                to_remove.append(intruder_id)
                self.log_event("intruder_left", {
                    "intruder_id": intruder_id,
                    "total_time": intruder.time_present(),
                    "max_threat_level": intruder.threat_level.value
                })
                print(f"✅ INTRUDER LEFT: {intruder_id}")
        
        for intruder_id in to_remove:
            del self.intruders[intruder_id]
        
        # Update system state if no more intruders
        if len(self.intruders) == 0 and self.system_state in [SystemState.ALERT, SystemState.ALARM]:
            self.system_state = SystemState.MONITORING
            print("✅ All clear - back to monitoring")
    
    def add_response(self, intruder_id: str, response: str):
        """Log a response given to an intruder"""
        if intruder_id in self.intruders:
            self.intruders[intruder_id].responses_given.append(response)
    
    def get_intruder_info(self, intruder_id: str) -> Optional[dict]:
        """Get information about a specific intruder"""
        if intruder_id in self.intruders:
            intruder = self.intruders[intruder_id]
            return {
                "intruder_id": intruder_id,
                "first_seen": intruder.first_seen,
                "time_present": intruder.time_present(),
                "detection_count": intruder.detection_count,
                "threat_level": intruder.threat_level.value,
                "responses_count": len(intruder.responses_given)
            }
        return None
    
    def get_all_intruders(self) -> List[dict]:
        """Get info about all current intruders"""
        return [self.get_intruder_info(iid) for iid in self.intruders.keys()]
    
    def log_event(self, event_type: str, data: dict):
        """Log an event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.event_log.append(event)
    
    def get_event_log(self) -> List[dict]:
        """Get event log"""
        return self.event_log
    
    def get_statistics(self) -> dict:
        """Get system statistics"""
        return {
            "system_state": self.system_state.value,
            "active_duration": self.get_active_duration(),
            "total_intruders_detected": len([e for e in self.event_log if e["event_type"] == "intruder_detected"]),
            "current_intruders": len(self.intruders),
            "total_escalations": len([e for e in self.event_log if e["event_type"] == "threat_escalated"]),
            "total_events": len(self.event_log)
        }
    
    def reset(self):
        """Reset state machine (keep in current state)"""
        self.intruders.clear()
        if self.system_state in [SystemState.ALERT, SystemState.ALARM]:
            self.system_state = SystemState.MONITORING
        print("🔄 State machine reset")


# Test the state machine
if __name__ == "__main__":
    print("🎮 STATE MACHINE TEST\n")
    print("="*60)
    
    # Create state machine
    sm = EscalationStateMachine()
    
    # Activate
    print("\n1️⃣ ACTIVATING SYSTEM")
    sm.activate()
    time.sleep(1)
    
    # Detect intruder
    print("\n2️⃣ INTRUDER DETECTED")
    info = sm.process_detection("intruder_1")
    print(f"   Threat Level: {info['threat_level']}")
    print(f"   Action: {info['action']}")
    
    # Simulate time passing and re-detection
    print("\n3️⃣ INTRUDER STILL PRESENT (5 seconds later)")
    time.sleep(5)
    for i in range(3):
        info = sm.process_detection("intruder_1")
        time.sleep(2)
    
    print(f"   Threat Level: {info['threat_level']}")
    print(f"   Time Present: {info['time_present']:.1f}s")
    print(f"   Action: {info['action']}")
    
    # More time passes
    print("\n4️⃣ CONTINUING ESCALATION (10 more seconds)")
    for i in range(5):
        info = sm.process_detection("intruder_1")
        time.sleep(2)
    
    print(f"   Threat Level: {info['threat_level']}")
    print(f"   Time Present: {info['time_present']:.1f}s")
    print(f"   Action: {info['action']}")
    
    # Show statistics
    print("\n5️⃣ STATISTICS")
    stats = sm.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Intruder leaves
    print("\n6️⃣ INTRUDER LEAVES (waiting...)")
    time.sleep(6)
    sm.cleanup_old_intruders()
    
    # Deactivate
    print("\n7️⃣ DEACTIVATING SYSTEM")
    duration = sm.deactivate()
    
    print("\n" + "="*60)
    print("✅ State machine test complete!")