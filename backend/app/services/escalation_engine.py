from typing import List, Dict, Any, Tuple
from app.schemas.counselling import ConcernResult

class EscalationEngine:
    def __init__(self):
        self.explicit_kws = [
            "human counsellor", "real person", "speak to someone", 
            "counsellor chahiye", "phone pe baat", "मानव सलाहकार", "इंसान से बात"
        ]
        self.frustration_kws = ["useless", "not helpful", "bakwaas", "bekaar", "बेकार"]
        
    async def should_escalate(self, concern: ConcernResult, evidence_list: List[Dict[str, Any]], 
                              history: List[Dict[str, Any]], message: str) -> Tuple[bool, str]:
        
        msg_lower = message.lower()
        
        # Rule 1 — Explicit request
        if any(kw in msg_lower for kw in self.explicit_kws):
            return True, "user_request"
            
        # Rule 2 — Safety with no evidence
        if concern.category in ["safety", "gender_family"] and len(evidence_list) == 0:
            return True, "safety_no_evidence"
            
        # Rule 3 — Turn limit exceeded
        # History contains messages for this session
        if len(history) >= 8:
            # We don't have direct access to category status here unless we fetch it
            # Or assume if it reaches here and history >= 8, the concern might be open
            # We can just escalate for now or checking the concern state passed in
            return True, "unresolved_after_turns"
            
        # Rule 4 — Low confidence
        if concern.confidence < 0.4 and any(kw in msg_lower for kw in self.frustration_kws):
            return True, "low_confidence_frustration"
            
        # Rule 5 — Default: no escalation
        return False, None
