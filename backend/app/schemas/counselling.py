from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ConcernResult(BaseModel):
    category: str
    intent: str
    confidence: float
    raw_text: str

class CounsellingMessageRequest(BaseModel):
    session_id: str
    speaker: str = Field(..., pattern="^(learner|parent|guardian)$")
    message: str = Field(..., min_length=1)
    language: str = Field(default="en")

class CounsellingMessageResponse(BaseModel):
    message_id: str
    response: str
    response_translated: str
    concern: Optional[ConcernResult] = None
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    concern_state: Dict[str, Any]
    escalated: bool = False
    escalation_id: Optional[str] = None
    counsellor_brief: Optional[Dict[str, Any]] = None
