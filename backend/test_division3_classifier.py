import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from hypothesis import given, strategies as st
from app.services.concern_classifier import ConcernClassifier, ParseException
from app.schemas.counselling import ClassificationResult
from app.prompts.concern_classification import CLASSIFICATION_TAXONOMY
from app.config import settings

# Property 1: Classification Parser Robustness
@given(
    response=st.one_of(
        st.text(), # Random strings
        st.fixed_dictionaries({
            "category": st.text(),
            "intent": st.text(),
            "confidence": st.floats(allow_nan=False, allow_infinity=False)
        }).map(json.dumps), # Valid JSON format
        st.dictionaries(st.text(), st.text()).map(json.dumps) # Missing or extra fields
    )
)
def test_classification_parser_robustness(response: str):
    classifier = ConcernClassifier(groq_client=None)
    try:
        result = classifier._parse_classification(response)
        
        # Verify valid ClassificationResult
        assert isinstance(result, ClassificationResult)
        assert result.category in CLASSIFICATION_TAXONOMY
        assert result.intent in CLASSIFICATION_TAXONOMY[result.category]
        assert 0.0 <= result.confidence <= 1.0
        
    except ParseException:
        # Expected exception for malformed output that can't be parsed
        pass


# Property 2: Confidence Threshold Flagging
@given(c=st.floats(min_value=-1.0, max_value=2.0, allow_nan=False, allow_infinity=False))
def test_confidence_threshold_flagging(c: float):
    classifier = ConcernClassifier(groq_client=None)
    response = json.dumps({"category": "income", "intent": "starting_salary", "confidence": c})
    
    result = classifier._parse_classification(response)
    
    # Confidence should be clamped
    assert 0.0 <= result.confidence <= 1.0
    
    # Check threshold logic
    if result.confidence < settings.confidence_threshold:
        assert result.low_confidence is True
    else:
        assert result.low_confidence is False


# Integration test for concern classification with Groq API
@pytest.mark.asyncio
async def test_classification_integration_groq():
    # Setup mock Groq client
    mock_groq = AsyncMock()
    mock_completions = AsyncMock()
    
    async def mock_create(messages, **kwargs):
        # Determine the user message
        user_message = messages[-1]["content"].lower()
        response_content = "{}"
        
        if "salary" in user_message:
            response_content = '{"category": "income", "intent": "starting_salary", "confidence": 0.9}'
        elif "safe" in user_message:
            response_content = '{"category": "safety", "intent": "women_safety", "confidence": 0.95}'
        elif "fee" in user_message:
            response_content = '{"category": "information_gap", "intent": "fees", "confidence": 0.8}'
            
        mock_choice = MagicMock()
        mock_choice.message.content = response_content
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        return mock_response
        
    mock_completions.create = mock_create
    mock_groq.chat.completions = mock_completions
    
    classifier = ConcernClassifier(groq_client=mock_groq)
    
    # Mock context
    class MockContext:
        trades_of_interest = ["Electrician"]
        district = "Nashik"
        state = "Maharashtra"
        
    context = MockContext()
    
    # Test 1: Income concern
    result1 = await classifier.classify("What is the starting salary?", "learner", context)
    assert result1.category == "income"
    assert result1.intent == "starting_salary"
    assert isinstance(result1.confidence, float)
    
    # Test 2: Safety concern
    result2 = await classifier.classify("Is this place safe for women?", "parent", context)
    assert result2.category == "safety"
    assert result2.intent == "women_safety"
    
    # Test 3: Information gap concern
    result3 = await classifier.classify("What are the course fees?", "learner", context)
    assert result3.category == "information_gap"
    assert result3.intent == "fees"
