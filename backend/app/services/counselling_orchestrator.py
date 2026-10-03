import uuid
import httpx
from fastapi import HTTPException
from typing import Dict, Any, Optional
from groq import AsyncGroq
from app.schemas.counselling import CounsellingMessageRequest, CounsellingMessageResponse
from app.services.concern_classifier import ConcernClassifier
from app.services.response_generator import ResponseGenerator
from app.services.escalation_engine import EscalationEngine
from app.config import settings

class CounsellingOrchestrator:
    def __init__(self):
        self.groq_client = AsyncGroq(api_key=settings.groq_api_key)
        self.classifier = ConcernClassifier(self.groq_client)
        self.generator = ResponseGenerator(self.groq_client)
        self.escalator = EscalationEngine()
        # Internal base URL defaults to division1_base_url if INTERNAL_BASE_URL isn't set separately
        self.internal_base_url = getattr(settings, "internal_base_url", "http://127.0.0.1:8000")

    async def _http_get(self, url: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
            
    async def _http_post(self, url: str, json_data: dict) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=json_data)
            resp.raise_for_status()
            return resp.json()
            
    async def _http_patch(self, url: str, json_data: dict) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.patch(url, json=json_data)
            resp.raise_for_status()
            return resp.json()

    async def orchestrate(self, request: CounsellingMessageRequest, db=None) -> CounsellingMessageResponse:
        session_id = request.session_id
        
        # Step 1 — Load session
        try:
            session_data = await self._http_get(f"{self.internal_base_url}/api/session/{session_id}")
            family_context = session_data["family_context"]
            concern_state = session_data["concern_state"]
            history = session_data.get("messages", [])[-5:]
        except Exception:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Step 2 — Translate input to English if needed
        message_english = request.message
        if request.language != "en":
            try:
                trans = await self._http_post(
                    f"{self.internal_base_url}/api/internal/language/translate",
                    {"text": request.message, "source_lang": request.language, "target_lang": "en"}
                )
                message_english = trans.get("translated_text", request.message)
            except Exception:
                pass # Translation failure shouldn't block
                
        # Step 3 — Classify concern
        concern = await self.classifier.classify(message_english, request.speaker, family_context)
        
        # Step 4 — Retrieve evidence conditionally based on concern relevance
        evidence_list = []
        trades = family_context.get("trades_of_interest", [""])
        
        # Evidence cards are only relevant for outcome/data-driven concerns
        evidence_relevant_categories = {"employment", "income", "safety", "gender_family", "education_progression"}
        
        if concern.category in evidence_relevant_categories:
            try:
                evidence_resp = await self._http_post(
                    f"{self.internal_base_url}/api/internal/evidence/retrieve",
                    {
                        "trade": trades[0] if trades else "",
                        "district": family_context.get("district", ""),
                        "state": family_context.get("state", ""),
                        "concern_category": concern.category,
                        "concern_intent": concern.intent,
                        "query_text": message_english,
                        "top_k": 3
                    }
                )
                evidence_list = evidence_resp.get("evidence", evidence_resp.get("results", [])) if isinstance(evidence_resp, dict) else (evidence_resp or [])
            except Exception:
                pass # Continue without evidence
        else:
            evidence_list = []
            
        # Step 5 — Generate response
        try:
            english_response = await self.generator.generate(
                request.speaker, message_english, concern, evidence_list, history, family_context
            )
        except Exception:
            raise HTTPException(status_code=503, detail="LLM unavailable after retries")
            
        # Step 6 — Translate response if needed
        response_translated = english_response
        if request.language != "en":
            try:
                trans = await self._http_post(
                    f"{self.internal_base_url}/api/internal/language/translate",
                    {"text": english_response, "source_lang": "en", "target_lang": request.language}
                )
                response_translated = trans.get("translated_text", english_response)
            except Exception:
                pass
                
        # Step 7 — Check escalation
        escalate, trigger_reason = await self.escalator.should_escalate(
            concern, evidence_list, session_data.get("messages", []), message_english
        )
        
        # Step 8 — Persist to Division 1
        user_msg_id = str(uuid.uuid4())
        asst_msg_id = str(uuid.uuid4())
        
        try:
            await self._http_post(
                f"{self.internal_base_url}/api/internal/session/{session_id}/messages",
                {"messages": [
                    {"message_id": user_msg_id, "speaker": request.speaker, "message_type": "user", "text_original": request.message, "text_english": message_english, "language": request.language},
                    {"message_id": asst_msg_id, "speaker": None, "message_type": "assistant", "text_original": response_translated, "text_english": english_response, "language": request.language}
                ]}
            )
            
            await self._http_post(
                f"{self.internal_base_url}/api/internal/session/{session_id}/concerns",
                {"message_id": user_msg_id, "category": concern.category, "intent": concern.intent, "confidence": concern.confidence, "raw_text": concern.raw_text}
            )
            
            for e in evidence_list:
                await self._http_post(
                    f"{self.internal_base_url}/api/internal/session/{session_id}/evidence",
                    {"evidence_id": e.get("evidence_id", ""), "message_id": asst_msg_id, "trade": e.get("trade", ""), "district": e.get("district", ""), "state": e.get("state", "")}
                )
        except Exception:
            pass # Non-blocking on DB error? Spec doesn't strictly say to raise here
            
        # Step 9 — Handle escalation if triggered
        escalation_id = None
        counsellor_brief = None
        if escalate:
            try:
                esc_resp = await self._http_post(
                    f"{self.internal_base_url}/api/internal/session/{session_id}/escalations",
                    {
                        "trigger_reason": trigger_reason,
                        "primary_concern_category": concern.category,
                        "primary_concern_intent": concern.intent,
                        "concern_status": "open",
                        "escalation_reason": trigger_reason,
                        "recommended_action": "Review session context."
                    }
                )
                escalation_id = esc_resp.get("escalation_id")
                counsellor_brief = esc_resp.get("counsellor_brief")
            except Exception:
                pass
                
        # Step 10 — Update concern state
        new_status = "open"
        if len(evidence_list) > 0 and concern.category in ["income", "employment", "information_gap"]:
            new_status = "partially_resolved"
            
        try:
            await self._http_patch(
                f"{self.internal_base_url}/api/internal/session/{session_id}/concerns",
                {"category": concern.category, "intent": concern.intent, "status": new_status}
            )
        except Exception:
            pass
            
        # Step 11 — Reload concern state
        try:
            session_data = await self._http_get(f"{self.internal_base_url}/api/session/{session_id}")
            concern_state = session_data["concern_state"]
        except Exception:
            pass
            
        # Step 12 — Return
        return CounsellingMessageResponse(
            message_id=asst_msg_id,
            response=english_response,
            response_translated=response_translated,
            concern=concern,
            evidence=evidence_list,
            concern_state=concern_state,
            escalated=escalate,
            escalation_id=escalation_id,
            counsellor_brief=counsellor_brief
        )
