import os
import json
import logging
from typing import Optional
from groq import AsyncGroq
from app.schemas.counselling import ConcernResult
from app.prompts.concern_classification import SYSTEM_PROMPT, TAXONOMY
from app.config import settings

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class ParseException(Exception):
    pass

class ConcernClassifier:
    def __init__(self, groq_client: Optional[AsyncGroq] = None):
        self.groq_client = groq_client
        self.income_kws = ["salary", "earn", "money", "pay", "paise", "₹", "rupee", "पगार", "कमाई", "रुपये", "पैसा", "fees", "kharcha", "income", "stipend"]
        self.employment_kws = ["job", "work", "naukri", "placement", "hire", "नौकरी", "काम", "rozgar", "kaam", "vacancy", "company", "career", "future", "scope", "milega", "lagti"]
        self.safety_kws = ["safe", "security", "danger", "girl", "female", "suraksha", "सुरक्षित", "khatra", "mahila", "ladki", "protection", "accident", "risk", "injur"]
        self.social_kws = ["respect", "status", "log", "society", "izzat", "इज्जत", "समाज", "reputation", "shame", "dignity", "standard", "prestige"]
        self.education_kws = ["course", "syllabus", "admission", "eligibility", "degree", "diploma", "nsqf", "padhai", "study", "duration", "iti", "qualification"]
        self.gender_kws = ["women", "girls", "female", "ladki", "mahila", "aurat", "gender", "suitable for girls", "ladies"]

    async def classify(self, message: str, speaker: str, family_context: dict) -> ConcernResult:
        trades = family_context.get("trades_of_interest", ["Unknown"])
        trades_str = ", ".join(trades) if trades else "Unknown"
        district = family_context.get("district", "Unknown")
        state = family_context.get("state", "Unknown")

        prompt = SYSTEM_PROMPT.format(
            TAXONOMY=json.dumps(TAXONOMY),
            speaker=speaker,
            trades=trades_str,
            district=district,
            state=state,
            message=message
        )

        # Try Groq first
        groq_key = getattr(settings, "groq_api_key", None) or os.environ.get("GROQ_API_KEY")
        if self.groq_client and groq_key:
            try:
                response = await self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=getattr(settings, "groq_model", getattr(settings, "groq_model_name", "qwen/qwen3.8-27b")),
                    temperature=0.1,
                    max_tokens=200,
                    response_format={"type": "json_object"},
                    timeout=5.0
                )
                content = response.choices[0].message.content
                data = json.loads(content)
                cat = data.get("category", "")
                intent = data.get("intent", "")
                conf = float(data.get("confidence", 0.85))
                if cat in TAXONOMY and intent in TAXONOMY.get(cat, []):
                    return ConcernResult(category=cat, intent=intent, confidence=max(0.1, min(1.0, conf)), raw_text=message)
            except Exception as e:
                logger.warning(f"Groq classification failed: {e}")

        # Try Gemini if key available
        gemini_key = getattr(settings, "gemini_api_key", None) or os.environ.get("GEMINI_API_KEY")
        if genai and gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel(
                    model_name=getattr(settings, "gemini_model_name", "gemini-1.5-flash"),
                    generation_config={"response_mime_type": "application/json"}
                )
                res = model.generate_content(prompt)
                if res and res.text:
                    data = json.loads(res.text)
                    cat = data.get("category", "")
                    intent = data.get("intent", "")
                    conf = float(data.get("confidence", 0.8))
                    if cat in TAXONOMY and intent in TAXONOMY.get(cat, []):
                        return ConcernResult(category=cat, intent=intent, confidence=max(0.1, min(1.0, conf)), raw_text=message)
            except Exception as e:
                logger.warning(f"Gemini classification failed: {e}")

        return self._fallback_classify(message)

    def _fallback_classify(self, message: str) -> ConcernResult:
        msg_lower = message.lower()
        
        if any(kw in msg_lower for kw in self.gender_kws):
            return ConcernResult(category="gender_family", intent="female_participation", confidence=0.8, raw_text=message)
        if any(kw in msg_lower for kw in self.income_kws):
            return ConcernResult(category="income", intent="starting_salary", confidence=0.8, raw_text=message)
        if any(kw in msg_lower for kw in self.employment_kws):
            return ConcernResult(category="employment", intent="placement_probability", confidence=0.85, raw_text=message)
        if any(kw in msg_lower for kw in self.safety_kws):
            return ConcernResult(category="safety", intent="workplace_safety", confidence=0.8, raw_text=message)
        if any(kw in msg_lower for kw in self.social_kws):
            return ConcernResult(category="social_perception", intent="status_of_trade", confidence=0.8, raw_text=message)
        if any(kw in msg_lower for kw in self.education_kws):
            return ConcernResult(category="education_progression", intent="higher_education_eligibility", confidence=0.75, raw_text=message)
            
        return ConcernResult(category="information_gap", intent="course_content", confidence=0.7, raw_text=message)

