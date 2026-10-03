"""
Language Service router for Division 4 - Translation & TTS.
Provides internal endpoints for Sarvam AI translation and text-to-speech.
These endpoints are consumed by Division 3 (Counselling Orchestrator) only.
"""

from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import logging

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/internal/language", include_in_schema=False)


# ===== Schemas =====

class TranslateRequest(BaseModel):
    """Request schema for translation."""
    text: str
    source_lang: str  # BCP-47 e.g. "mr", "hi", "en"
    target_lang: str


class TranslateResponse(BaseModel):
    """Response schema for translation."""
    translated_text: str
    detected_lang: str


class TTSRequest(BaseModel):
    """Request schema for text-to-speech."""
    text: str
    language: str


class TTSResponse(BaseModel):
    """Response schema for text-to-speech."""
    audio_base64: str
    format: str = "mp3"


# ===== Constants =====

SARVAM_TRANSLATE_URL = "https://api.sarvam.ai/translate"
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"


# ===== Endpoints =====

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(payload: TranslateRequest):
    """
    Translate text between English and a regional language via Sarvam AI.

    If source and target languages are the same, returns text unchanged.
    On any Sarvam API failure, returns the original text as a graceful fallback
    so that translation errors never crash the counselling flow.
    """
    # Short-circuit: same language → no translation needed
    if payload.source_lang == payload.target_lang:
        return TranslateResponse(
            translated_text=payload.text,
            detected_lang=payload.source_lang,
        )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                SARVAM_TRANSLATE_URL,
                headers={
                    "api-subscription-key": settings.sarvam_api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "input": payload.text,
                    "source_language_code": payload.source_lang,
                    "target_language_code": payload.target_lang,
                    "speaker_gender": "Female",
                    "mode": "formal",
                    "model": "mayura:v1",
                    "enable_preprocessing": False,
                },
            )
            response.raise_for_status()
            data = response.json()

            translated = data.get("translated_text", payload.text)
            logger.info(
                f"Translated {payload.source_lang}→{payload.target_lang} "
                f"({len(payload.text)} chars → {len(translated)} chars)"
            )
            return TranslateResponse(
                translated_text=translated,
                detected_lang=payload.source_lang,
            )

    except Exception as e:
        logger.error(f"Sarvam translate call failed: {e}", exc_info=True)
        # Graceful fallback — return original text unchanged
        return TranslateResponse(
            translated_text=payload.text,
            detected_lang=payload.source_lang,
        )


@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(payload: TTSRequest):
    """
    Convert text to speech audio via Sarvam AI TTS.

    Returns base64-encoded MP3 audio. On any Sarvam API failure, returns
    an empty audio string so that TTS errors never crash the counselling flow.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                SARVAM_TTS_URL,
                headers={
                    "api-subscription-key": settings.sarvam_api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": [payload.text],
                    "target_language_code": payload.language,
                    "speaker": "meera",
                    "pitch": 0,
                    "pace": 1.0,
                    "loudness": 1.5,
                    "speech_sample_rate": 8000,
                    "enable_preprocessing": False,
                    "model": "bulbul:v1",
                },
            )
            response.raise_for_status()
            data = response.json()

            audios = data.get("audios", [])
            audio_base64 = audios[0] if audios else ""
            logger.info(
                f"TTS generated for lang={payload.language} "
                f"({len(payload.text)} chars, audio_len={len(audio_base64)})"
            )
            return TTSResponse(
                audio_base64=audio_base64,
                format="mp3",
            )

    except Exception as e:
        logger.error(f"Sarvam TTS call failed: {e}", exc_info=True)
        # Graceful fallback — return empty audio
        return TTSResponse(
            audio_base64="",
            format="mp3",
        )
