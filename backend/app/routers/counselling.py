from fastapi import APIRouter, Depends
from app.schemas.counselling import CounsellingMessageRequest, CounsellingMessageResponse
from app.services.counselling_orchestrator import CounsellingOrchestrator

router = APIRouter()
orchestrator = CounsellingOrchestrator()

@router.post("/counselling/message", response_model=CounsellingMessageResponse)
async def handle_counselling_message(request: CounsellingMessageRequest):
    return await orchestrator.orchestrate(request)
