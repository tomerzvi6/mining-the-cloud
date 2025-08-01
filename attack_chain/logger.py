import logging
import datetime
from typing import Dict, Any

class AttackLogger:
    """
    Handles logging of attack activities for demonstration and detection purposes.
    This logger simulates suspicious activities that would be captured by security tools.
    """
    
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger('AttackSimulation')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_attack_step(self, step_name: str, action: str, details: Dict[str, Any] = None):
        """Log an attack step with details"""
        details = details or {}
        message = f"ATTACK STEP: {step_name} - {action}"
        if details:
            message += f" | Details: {details}"
        self.logger.warning(message)
    
    def log_reconnaissance(self, target: str, method: str):
        """Log reconnaissance activities"""
        self.log_attack_step(
            "RECONNAISSANCE", 
            f"Enumerating {target} using {method}",
            {"target": target, "method": method, "timestamp": datetime.datetime.now().isoformat()}
        )
    
    def log_privilege_escalation(self, role_name: str):
        """Log privilege escalation attempts"""
        self.log_attack_step(
            "PRIVILEGE_ESCALATION",
            f"Attempting to create elevated role: {role_name}",
            {"role_name": role_name, "threat_level": "HIGH"}
        )
    
    def log_lateral_movement(self, target_resource: str):
        """Log lateral movement activities"""
        self.log_attack_step(
            "LATERAL_MOVEMENT",
            f"Exploring target resource: {target_resource}",
            {"target": target_resource, "activity": "environment_mapping"}
        )
    
    def log_impact(self, impact_type: str, target: str):
        """Log impact activities"""
        self.log_attack_step(
            "IMPACT",
            f"{impact_type} operation on {target}",
            {"impact_type": impact_type, "target": target, "threat_level": "CRITICAL"}
        )
    
    def log_cloudtrail_event(self, event_name: str, resource: str):
        """Log activities that would appear in CloudTrail"""
        self.logger.critical(
            f"CLOUDTRAIL EVENT: {event_name} on {resource} - "
            f"This action is logged in AWS CloudTrail and should trigger security alerts"
        ) 