# Implementation Plan: Division 3 - Counselling Orchestrator

## Overview

This implementation plan creates the core intelligence layer for the PS 26241 AI-Enabled Career Counselling Platform. Division 3 orchestrates the main counselling endpoint `POST /api/counselling/message`, coordinating concern classification (LLM-based), evidence retrieval (Division 2), speaker-aware response generation (Groq API), multi-turn state management (Division 1), deterministic escalation decision-making (5 rules), and edge case detection (echo chambers, guardian vetoes, third-party mentors, reality checks, gender context).

**Technology Stack**: FastAPI (async), Groq API (llama-3.1-8b-instant), httpx (async HTTP), Jinja2 (prompt templates), Hypothesis (property-based testing), Tenacity (retries), Python 3.11+

**Key Architecture**: 9 components in 3 layers (Core Orchestration, Intelligence, State Management) with 21 correctness properties for property-based testing.

## Tasks

- [ ] 1. Set up project structure and configuration
  - Create directory structure: `backend/app/services/` for orchestration components, `backend/app/prompts/` for Jinja2 templates
  - Create configuration module `backend/app/config.py` with GroqConfig, EscalationConfig, DivisionEndpoints using pydantic-settings
  - Add environment variable validation: GROQ_API_KEY (required), GROQ_MODEL_NAME (default: llama-3.1-8b-instant), CONFIDENCE_THRESHOLD (default: 0.7), TURN_LIMIT (default: 5), ECHO_CHAMBER_THRESHOLD (default: 70.0)
  - Install dependencies: groq, httpx, jinja2, hypothesis, tenacity
  - Create pytest configuration in `backend/pytest.ini` with hypothesis settings (max_examples=100)
  - _Requirements: 19.1, 19.2_

- [ ] 2. Implement Concern Classifier with LLM integration
  - [ ] 2.1 Create ConcernClassifier class in `backend/app/services/concern_classifier.py`
    - Implement `__init__` accepting groq_client and optional ollama_client
    - Define category taxonomy: 7 categories (income, employment, safety, social_perception, education_progression, gender_family, information_gap) with 20+ intents as class attribute
    - Implement `async def classify(message: str, speaker: str, context: SessionContext) -> ClassificationResult`
    - Build classification prompt with taxonomy, speaker context, trades_of_interest, district, state
    - Call Groq API with timeout=2.0s, extract structured JSON output
    - Implement fallback to Ollama if Groq fails
    - Set low_confidence flag if confidence < 0.7
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ] 2.2 Implement classification prompt template in `backend/app/prompts/concern_classification.py`
    - Define CLASSIFICATION_TAXONOMY constant with all 7 categories and intents
    - Build prompt structure: system role, context (speaker, trades, location), taxonomy, output format (strict JSON)
    - Include example few-shot classification for each category
    - _Requirements: 1.3, 1.4_

  - [ ] 2.3 Implement classification parser with error handling
    - Implement `_parse_classification(response: str) -> ClassificationResult`
    - Handle valid JSON, malformed JSON (regex extraction), missing fields (defaults)
    - Validate category in taxonomy, validate intent matches category
    - Clamp confidence to [0.0, 1.0]
    - Raise ParseException for completely invalid output
    - _Requirements: 1.7_

  - [ ]* 2.4 Write property test for classification parser robustness
    - **Property 1: Classification Parser Robustness**
    - **Validates: Requirements 1.3, 1.4, 1.5**
    - Use Hypothesis to generate random LLM-like outputs: valid JSON, malformed JSON, missing fields, extra fields, empty strings, extremely long strings
    - Verify parser either returns valid ClassificationResult (category in taxonomy, confidence in [0.0, 1.0]) OR raises ParseException without crashing
    - Test with 100 iterations

  - [ ]* 2.5 Write property test for confidence threshold flagging
    - **Property 2: Confidence Threshold Flagging**
    - **Validates: Requirements 1.6**
    - Use Hypothesis to generate confidence scores c in range [-1.0, 2.0]
    - Verify low_confidence flag is True if 0.0 <= c < 0.7, False if c >= 0.7, and invalid values are handled
    - Test with 100 iterations

  - [ ]* 2.6 Write integration test for concern classification with Groq API
    - Mock Groq API with 3 test messages: income concern, safety concern, information_gap concern
    - Verify correct category and intent extracted
    - Verify confidence scores are valid floats
    - Test Ollama fallback when Groq fails
    - _Requirements: 1.1, 1.8_

- [ ] 3. Checkpoint - Verify classification component
  - Ensure property tests pass (Properties 1-2), integration test passes, classification prompt template renders correctly
  - Ask user if questions arise about LLM integration or taxonomy structure

- [ ] 4. Implement Prompt Manager with speaker-aware templates
  - [ ] 4.1 Create PromptManager class in `backend/app/services/prompt_manager.py`
    - Implement `__init__` loading three Jinja2 templates: learner_prompts.jinja2, parent_prompts.jinja2, guardian_prompts.jinja2
    - Implement `select_template(speaker: str, speakers_present: List[str]) -> Template` with precedence: guardian > parent > learner
    - Implement `build_system_prompt(speaker, district, state, concern_category, concern_intent) -> str`
    - Include template placeholders: speaker, district, state, concern_category, concern_intent
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.7_

  - [ ] 4.2 Create learner prompt template in `backend/app/prompts/learner_prompts.jinja2`
    - Tone: Empowering, career-focused, encouraging
    - Focus: Future opportunities, skill development, personal growth
    - Example opening: "Let's explore what this trade offers for your future..."
    - Include placeholders for speaker, district, state, concern_category, concern_intent
    - _Requirements: 2.2_

  - [ ] 4.3 Create parent prompt template in `backend/app/prompts/parent_prompts.jinja2`
    - Tone: Practical, outcome-focused, data-driven
    - Focus: Job placement, earnings, return on investment
    - Example opening: "Here's the verified data on job placement and earnings..."
    - _Requirements: 2.3_

  - [ ] 4.4 Create guardian prompt template in `backend/app/prompts/guardian_prompts.jinja2`
    - Tone: Respectful, evidence-first, culturally sensitive
    - Focus: Family security, long-term stability, social acceptance
    - Example opening: "The government outcome data shows the following verified results..."
    - _Requirements: 2.4_

  - [ ]* 4.5 Write property test for speaker template selection determinism
    - **Property 3: Speaker Template Selection Determinism**
    - **Validates: Requirements 2.2, 2.3, 2.4**
    - Use Hypothesis to generate speaker types: learner, parent, guardian
    - Verify template selection is deterministic: learner → learner_template, parent → parent_template, guardian → guardian_template
    - Test with 100 iterations

  - [ ]* 4.6 Write property test for multi-speaker prompt precedence
    - **Property 4: Multi-Speaker Prompt Precedence**
    - **Validates: Requirements 2.7**
    - Use Hypothesis to generate sets of speakers_present with multiple speaker types
    - Verify precedence order: guardian > parent > learner (if guardian in set, use guardian_template; else if parent in set, use parent_template; else learner_template)
    - Test with 100 iterations

  - [ ]* 4.7 Write unit test for prompt template rendering
    - Test each template renders with all required placeholders
    - Verify tone and framing differences between learner/parent/guardian templates
    - Test multi-speaker scenario precedence
    - _Requirements: 2.1, 2.7_

- [ ] 5. Implement Response Generator with evidence grounding
  - [ ] 5.1 Create ResponseGenerator class in `backend/app/services/response_generator.py`
    - Implement `__init__` accepting groq_client and prompt_manager
    - Implement `async def generate_response(classification, evidence, conversation_history, speaker, session_context, edge_case_flags) -> str`
    - Build system prompt using prompt_manager with speaker-aware template
    - Add edge case context to system prompt (echo chamber, guardian veto)
    - Format conversation history (last 5 turns)
    - Format evidence array with provenance (trade, district, placement_rate, earnings, source, data_period)
    - Include reality_check fields (physical_demand, typical_day, trainee_quote) when available
    - Include gender context fields (female_enrollment_pct, safety_infrastructure) for gender_family concerns
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ] 5.2 Implement LLM call with retry logic
    - Implement `_call_groq_with_retry(system_prompt, user_prompt, temperature=0.7, max_tokens=300) -> str`
    - Use tenacity for 3 retries with exponential backoff (1s, 2s, 4s)
    - Set LLM parameters: temperature=0.7, max_tokens=300, top_p=0.9
    - Fallback to Ollama if Groq fails after retries
    - Raise HTTPException(503) if both fail
    - _Requirements: 4.10, 15.1, 15.2_

  - [ ] 5.3 Implement response validation and truncation
    - Implement `_validate_and_truncate(response: str) -> str`
    - Count words using len(response.split())
    - Log warning if word_count < 50
    - Truncate at last complete sentence if word_count > 400
    - Ensure truncated response ends with '.'
    - _Requirements: 4.8, 4.9_

  - [ ] 5.4 Implement evidence formatting with provenance
    - Implement `_format_evidence(evidence: List[Evidence], concern_category: str) -> str`
    - Format each evidence item: trade, location, placement_rate, earnings, source, data_period, nsqf_level, progression_path
    - Include reality_check fields (physical_demand, typical_day, trainee_quote with source validation) when available
    - Include gender context fields (female_enrollment_pct, safety_infrastructure) for gender_family concerns
    - Return "No verified outcome data available" if evidence is empty
    - _Requirements: 3.3, 4.5, 4.6, 12.2, 12.3, 13.2, 13.3_

  - [ ]* 5.5 Write property test for response length validation
    - **Property 5: Response Length Validation**
    - **Validates: Requirements 4.8**
    - Use Hypothesis to generate response strings with varying word counts
    - Verify word_count computed as len(response.split())
    - Verify warning logged if word_count > 400
    - Test with 100 iterations

  - [ ]* 5.6 Write property test for response truncation preserves sentences
    - **Property 6: Response Truncation Preserves Sentences**
    - **Validates: Requirements 4.9**
    - Use Hypothesis to generate response strings with word_count > 400
    - Verify truncation produces response where: word_count <= 400, ends with '.', no partial sentences at end
    - Test with 100 iterations

  - [ ]* 5.7 Write integration test for response generation with evidence grounding
    - Mock Groq API to return sample evidence-grounded response
    - Verify response includes evidence citations ("According to MSDE data...")
    - Test reality_check data inclusion for under-18 learners
    - Test gender context data inclusion for gender_family concerns
    - Verify response length within 50-400 words
    - _Requirements: 4.1, 4.4, 4.5, 4.6_

- [ ] 6. Checkpoint - Verify response generation component
  - Ensure property tests pass (Properties 5-6), integration test passes, speaker-aware prompts render correctly with evidence
  - Ask user if questions arise about LLM response generation or evidence formatting

- [ ] 7. Implement Conversation State Manager
  - [ ] 7.1 Create ConversationStateManager class in `backend/app/services/conversation_state_manager.py`
    - Implement `__init__` accepting division1_client
    - Implement `async def get_session_context(session_id) -> SessionContext` calling Division 1 GET /api/session/{session_id}
    - Implement `async def get_conversation_history(session_id, limit=5) -> List[Message]` calling Division 1 internal API
    - Implement `async def get_evidence_shown(session_id) -> List[str]` returning list of evidence_ids already shown
    - Implement `async def store_message(session_id, speaker, text_original, text_english, language, message_type) -> str` calling Division 1 POST /api/internal/session/{session_id}/messages
    - Implement turn counter tracking per concern intent (dict mapping (category, intent) to turn count)
    - Reset turn counter when concern status → 'resolved'
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.8, 5.9_

  - [ ] 7.2 Implement evidence deduplication logic
    - Implement `filter_new_evidence(evidence_shown: List[str], new_evidence: List[Evidence]) -> List[Evidence]`
    - Filter out evidence_ids already in evidence_shown history
    - Return filtered evidence array
    - _Requirements: 5.6_

  - [ ] 7.3 Implement concern repetition detection
    - Implement `detect_concern_repetition(concern_history: List[Concern]) -> bool`
    - Count occurrences of same (category, intent) pair with status 'open' or 'partially_resolved'
    - Return True if count >= 3
    - _Requirements: 5.7_

  - [ ]* 7.4 Write property test for evidence deduplication
    - **Property 7: Evidence Deduplication**
    - **Validates: Requirements 5.6**
    - Use Hypothesis to generate evidence_shown history (list of evidence_ids) and new_evidence array
    - Verify filtered result contains no evidence_ids from evidence_shown
    - Test with 100 iterations

  - [ ]* 7.5 Write property test for concern repetition detection
    - **Property 8: Concern Repetition Detection**
    - **Validates: Requirements 5.7**
    - Use Hypothesis to generate concern_history with varying (category, intent) pairs and statuses
    - Verify repetition_detected is True if same (category, intent) appears 3+ times with status 'open' or 'partially_resolved'
    - Test with 100 iterations

  - [ ]* 7.6 Write property test for turn counter per intent
    - **Property 9: Turn Counter Per Intent**
    - **Validates: Requirements 5.8**
    - Use Hypothesis to generate concern_history grouped by (category, intent) pairs
    - Verify turn counter equals number of times intent detected with status != 'resolved'
    - Test with 100 iterations

  - [ ]* 7.7 Write integration test for conversation state management
    - Mock Division 1 API calls (get session context, get conversation history, store message)
    - Test evidence deduplication filters correctly
    - Test concern repetition detection identifies patterns
    - Test turn counter increments and resets
    - _Requirements: 5.1, 5.4, 5.6, 5.7, 5.8_

- [ ] 8. Implement Concern State Calculator with hierarchical logic
  - [ ] 8.1 Create ConcernStateCalculator class in `backend/app/services/concern_state_calculator.py`
    - Implement `__init__` accepting division1_client
    - Implement `async def store_concern(session_id, message_id, category, intent, confidence, raw_text) -> None` calling Division 1 POST /api/internal/session/{session_id}/concerns
    - Implement concern resolution heuristic evaluation logic
    - Implement `compute_intent_status(evidence_retrieved, evidence_shown, response_length, intent_match, confidence) -> str` returning 'resolved', 'partially_resolved', or 'open'
    - Implement `compute_category_status(intent_statuses: Dict[str, str]) -> str` for hierarchical status calculation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.7_

  - [ ] 8.2 Implement concern resolution heuristic
    - Define heuristic conditions: (a) evidence_retrieved AND evidence_shown, (b) response_length > 100 words, (c) intent_match (evidence matches concern intent), (d) confidence >= 0.7
    - Return 'resolved' if ALL conditions True, 'partially_resolved' if SOME conditions True, else 'open'
    - Handle concern status reversion: if user asks follow-up about same intent, revert from 'resolved' to 'open'
    - _Requirements: 6.3, 6.4, 6.5, 6.6_

  - [ ] 8.3 Implement hierarchical concern state calculation
    - Implement category status calculation from intent statuses:
      - If no intents exist → 'not_raised'
      - If any intent is 'open' → category is 'open'
      - If all intents are 'resolved' → category is 'resolved'
      - Otherwise → category is 'partially_resolved'
    - Update Division 1 concern_state in real-time after each message
    - _Requirements: 6.7, 6.8, 6.9_

  - [ ]* 8.4 Write property test for concern resolution heuristic
    - **Property 10: Concern Resolution Heuristic**
    - **Validates: Requirements 6.3**
    - Use Hypothesis to generate inputs: evidence_retrieved (bool), evidence_shown (bool), response_length (int), intent_match (bool), confidence (float)
    - Verify status is 'resolved' if ALL True, 'partially_resolved' if SOME True, else 'open'
    - Test with 100 iterations

  - [ ]* 8.5 Write property test for hierarchical concern state calculation
    - **Property 11: Hierarchical Concern State Calculation**
    - **Validates: Requirements 6.7**
    - Use Hypothesis to generate intent_statuses dict (mapping intent names to statuses: 'open', 'partially_resolved', 'resolved')
    - Verify category status: 'not_raised' if empty, 'open' if any intent 'open', 'resolved' if all 'resolved', else 'partially_resolved'
    - Test with 100 iterations

  - [ ]* 8.6 Write integration test for concern state updates
    - Mock Division 1 API calls (store concern, update concern status)
    - Test intent status calculation with various heuristic inputs
    - Test category status calculation from multiple intent statuses
    - Test concern status reversion when follow-up question asked
    - _Requirements: 6.1, 6.3, 6.7, 6.8_

- [ ] 9. Checkpoint - Verify state management components
  - Ensure property tests pass (Properties 7-11), integration tests pass, concern state correctly tracks resolution progress
  - Ask user if questions arise about hierarchical state calculation or turn counter logic

- [ ] 10. Implement Escalation Rules Engine with 5 deterministic rules
  - [ ] 10.1 Create EscalationRulesEngine class in `backend/app/services/escalation_engine.py`
    - Implement `__init__` accepting config (CONFIDENCE_THRESHOLD, TURN_LIMIT)
    - Define keyword lists: explicit_request_keywords, frustration_keywords
    - Implement `async def evaluate_escalation(classification, evidence, concern_history, message_text, session_context) -> EscalationDecision`
    - Evaluate rules in precedence order: Rule 1 → Rule 2 → Rule 3 → Rule 4 → Rule 5
    - Return EscalationDecision with escalated, trigger_rule, reason, primary_concern, secondary_concern
    - _Requirements: 7.1_

  - [ ] 10.2 Implement Rule 1: Explicit human counsellor request
    - Implement `_check_explicit_request(message_text: str) -> bool`
    - Check for keywords: "talk to counsellor", "human counsellor", "speak to someone", "real person" (case-insensitive)
    - Return True if any keyword found
    - Trigger with reason "explicit_human_counsellor_request"
    - _Requirements: 7.2_

  - [ ] 10.3 Implement Rule 2: Required evidence unavailable
    - Implement `_check_required_evidence_unavailable(classification, evidence) -> bool`
    - Check if evidence array is empty AND (category='employment' with intent='placement_probability' OR category='safety')
    - Return True if condition met
    - Trigger with reason "required_evidence_unavailable"
    - _Requirements: 7.3, 3.4, 3.5_

  - [ ] 10.4 Implement Rule 3: Safety concern + insufficient evidence
    - Implement `_check_safety_insufficient_evidence(classification, evidence) -> bool`
    - Check if category='safety' AND evidence array length < 2
    - Return True if condition met
    - Trigger with reason "safety_concern_insufficient_evidence"
    - _Requirements: 7.4_

  - [ ] 10.5 Implement Rule 4: Turn limit exceeded
    - Implement `_check_turn_limit_exceeded(concern_history) -> bool`
    - Count occurrences of each (category, intent) pair with status 'open' or 'partially_resolved'
    - Return True if any concern >= TURN_LIMIT (default 5)
    - Trigger with reason "concern_unresolved_after_turn_limit"
    - _Requirements: 7.5_

  - [ ] 10.6 Implement Rule 5: Low confidence + user dissatisfaction
    - Implement `_check_low_confidence_dissatisfaction(classification, message_text) -> bool`
    - Check if confidence < 0.5 AND message contains frustration keywords ("not helpful", "don't understand", "this isn't working")
    - Return True if both conditions met
    - Trigger with reason "low_confidence_with_user_dissatisfaction"
    - _Requirements: 7.6_

  - [ ] 10.7 Implement primary and secondary concern identification
    - Implement `_get_primary_concern(concern_history) -> Concern` returning most recent 'open' concern
    - Implement `_get_secondary_concern(concern_history) -> Optional[Concern]` returning second most recent unresolved concern
    - _Requirements: 8.2, 8.3_

  - [ ]* 10.8 Write property test for escalation rule precedence
    - **Property 12: Escalation Rule Precedence**
    - **Validates: Requirements 7.1**
    - Use Hypothesis to generate inputs triggering multiple rules simultaneously
    - Verify FIRST triggered rule in precedence order (Rule 1 → 2 → 3 → 4 → 5) is the escalation trigger
    - Verify subsequent rules NOT evaluated after first trigger
    - Test with 100 iterations

  - [ ]* 10.9 Write property test for Rule 1: Explicit Request Detection
    - **Property 13: Escalation Rule 1 - Explicit Request Detection**
    - **Validates: Requirements 7.2**
    - Use Hypothesis to generate message_text containing explicit request keywords (case-insensitive)
    - Verify Rule 1 triggers with reason "explicit_human_counsellor_request"
    - Test with 100 iterations

  - [ ]* 10.10 Write property test for Rule 2: Required Evidence Unavailable
    - **Property 14: Escalation Rule 2 - Required Evidence Unavailable**
    - **Validates: Requirements 7.3**
    - Use Hypothesis to generate classification (category='employment' intent='placement_probability' OR category='safety') with empty evidence array
    - Verify Rule 2 triggers with reason "required_evidence_unavailable"
    - Test with 100 iterations

  - [ ]* 10.11 Write property test for Rule 3: Safety Insufficient Evidence
    - **Property 15: Escalation Rule 3 - Safety Insufficient Evidence**
    - **Validates: Requirements 7.4**
    - Use Hypothesis to generate classification (category='safety') with evidence array length < 2
    - Verify Rule 3 triggers with reason "safety_concern_insufficient_evidence"
    - Test with 100 iterations

  - [ ]* 10.12 Write property test for Rule 4: Turn Limit Exceeded
    - **Property 16: Escalation Rule 4 - Turn Limit Exceeded**
    - **Validates: Requirements 7.5**
    - Use Hypothesis to generate concern_history where (category, intent) pair appears >= 5 times with status 'open' or 'partially_resolved'
    - Verify Rule 4 triggers with reason "concern_unresolved_after_turn_limit"
    - Test with 100 iterations

  - [ ]* 10.13 Write property test for Rule 5: Low Confidence + Dissatisfaction
    - **Property 17: Escalation Rule 5 - Low Confidence + Dissatisfaction**
    - **Validates: Requirements 7.6**
    - Use Hypothesis to generate classification (confidence < 0.5) and message_text containing frustration keywords
    - Verify Rule 5 triggers with reason "low_confidence_with_user_dissatisfaction"
    - Test with 100 iterations

  - [ ]* 10.14 Write integration test for escalation rules evaluation
    - Test each rule triggers correctly with appropriate inputs
    - Test rule precedence: Rule 1 takes priority over Rule 2-5
    - Test no escalation when no rules trigger
    - Test primary and secondary concern identification
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 11. Implement Counsellor Brief Builder
  - [ ] 11.1 Create CounsellorBriefBuilder class in `backend/app/services/counsellor_brief_builder.py`
    - Implement `__init__` accepting division1_client
    - Implement `async def build_brief(escalation_decision, session_context, evidence_shown, concern_state) -> CounsellorBrief`
    - Identify primary concern (from escalation_decision)
    - Identify secondary concern (from escalation_decision)
    - Compile information_already_provided list from evidence_shown
    - Generate escalation_reason (human-readable explanation)
    - Generate recommended_action (specific next steps for counsellor)
    - Call Division 1 POST /api/internal/session/{session_id}/escalations to create escalation record
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.9_

  - [ ] 11.2 Implement information already provided compilation
    - Implement `_compile_data_shown(evidence_shown: List[Evidence]) -> List[str]`
    - Check each evidence for: placement_rate, earnings_range (earnings_min and earnings_max), nsqf_level, career_progression (progression_path), reality_check, gender_context (female_enrollment_pct or safety_infrastructure)
    - Return sorted list of unique evidence types shown
    - _Requirements: 8.4_

  - [ ] 11.3 Implement escalation reason generation
    - Implement `_generate_escalation_reason(escalation_decision) -> str`
    - Map trigger_rule to human-readable explanation with context
    - Example: "User explicitly requested to speak with a human counsellor"
    - _Requirements: 8.5_

  - [ ] 11.4 Implement recommended action generation
    - Implement `_generate_recommended_action(escalation_decision, session_context, data_shown) -> str`
    - Tailor action to trigger rule and primary concern category
    - Rule 2 (evidence unavailable): "Research local [trade] employers in [district] district. Arrange site visit or employer interaction if possible."
    - Rule 3 (safety): "Discuss workplace safety measures for [trade]. Arrange training center visit to see safety infrastructure."
    - social_perception: "Address social perception concerns. Share local success stories and connect family with current trainees/graduates."
    - gender_family: "Discuss gender-specific concerns. Highlight female enrollment data, safety measures, connect with female trainees/graduates."
    - _Requirements: 8.6_

  - [ ]* 11.5 Write property test for information already provided compilation
    - **Property 18: Information Already Provided Compilation**
    - **Validates: Requirements 8.4**
    - Use Hypothesis to generate evidence_shown array with varying field combinations
    - Verify list contains unique types: 'placement_rate' if any placement_rate != None, 'earnings_range' if any has both min/max, etc.
    - Test with 100 iterations

  - [ ]* 11.6 Write integration test for counsellor brief generation
    - Mock Division 1 API call to create escalation record
    - Test brief contains all required fields: learner_education, district, state, trade_interest, primary/secondary concerns, data_already_shown, concern_status, escalation_reason, recommended_action
    - Test recommended action tailored to trigger rule and concern category
    - _Requirements: 8.1, 8.5, 8.6_

- [ ] 12. Checkpoint - Verify escalation and counsellor brief components
  - Ensure property tests pass (Properties 12-18), integration tests pass, all 5 escalation rules trigger correctly, counsellor briefs contain complete context
  - Ask user if questions arise about escalation logic or brief generation

- [ ] 13. Implement Edge Case Detectors suite
  - [ ] 13.1 Create EdgeCaseDetectors class in `backend/app/services/edge_case_detectors.py`
    - Implement `__init__` accepting division5_client and config (ECHO_CHAMBER_THRESHOLD)
    - Implement `async def detect_all(classification, session_context, conversation_history, concern_history) -> EdgeCaseFlags` running all detectors in parallel
    - Return EdgeCaseFlags with boolean flags: echo_chamber_detected, guardian_veto_detected, third_party_mentor_detected, reality_check_needed, gender_context_needed
    - _Requirements: 9, 10, 11, 12, 13_

  - [ ] 13.2 Implement Echo Chamber Detector
    - Implement `async def detect_echo_chamber(classification, session_context) -> bool`
    - Call Division 5 GET /api/internal/analytics/cross-session?district={}&trade={}&concern_category={}
    - Compare dominant_percentage against ECHO_CHAMBER_THRESHOLD (default 70.0)
    - Return True if dominant_percentage >= threshold
    - Handle Division 5 unavailability gracefully (log warning, return False)
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.8_

  - [ ] 13.3 Implement Guardian Veto Detector
    - Implement `async def detect_guardian_veto(conversation_history, concern_history, session_context) -> bool`
    - Check if 'guardian' and 'learner' both in speakers_present
    - Count concerns by speaker (using message_id references)
    - Detect pattern: guardian raised >= 3 concerns, learner raised 0 concerns, >= 2 guardian concerns in {social_perception, income, employment}
    - Return True if pattern detected
    - _Requirements: 10.1, 10.2, 10.3_

  - [ ] 13.4 Implement Third-Party Mentor Detector
    - Implement `async def detect_third_party_mentor(conversation_history) -> bool`
    - Define mentor keywords: "teacher said", "uncle suggested", "counsellor recommended", "someone told me", "mentor advised", "relative said"
    - Count messages containing any mentor keyword (case-insensitive)
    - Return True if mention_count >= 2
    - _Requirements: 11.1, 11.2_

  - [ ] 13.5 Implement Reality Check Presenter
    - Implement `async def detect_reality_check_needed(session_context) -> bool`
    - Check learner_education for under-18 indicators: "class 10", "class 12", "10th", "12th", "secondary" (case-insensitive)
    - Return True if any indicator found
    - _Requirements: 12.1_

  - [ ] 13.6 Implement Gender Context Handler
    - Implement `async def detect_gender_context_needed(classification) -> bool`
    - Return True if classification.category == 'gender_family'
    - _Requirements: 13.1_

  - [ ]* 13.7 Write property test for echo chamber threshold detection
    - **Property 19: Echo Chamber Threshold Detection**
    - **Validates: Requirements 9.4**
    - Use Hypothesis to generate analytics data with dominant_percentage and ECHO_CHAMBER_THRESHOLD
    - Verify echo_chamber_detected is True if percentage >= threshold, else False
    - Test with 100 iterations

  - [ ]* 13.8 Write property test for guardian veto pattern detection
    - **Property 20: Guardian Veto Pattern Detection**
    - **Validates: Requirements 10.3**
    - Use Hypothesis to generate conversation_history with speaker annotations and concern_history
    - Verify guardian_veto_detected is True if: guardian raised >= 3 concerns, learner raised 0 concerns, >= 2 guardian concerns in {social_perception, income, employment}
    - Test with 100 iterations

  - [ ]* 13.9 Write property test for third-party mentor keyword detection
    - **Property 21: Third-Party Mentor Keyword Detection**
    - **Validates: Requirements 11.2**
    - Use Hypothesis to generate conversation_history with varying numbers of messages containing mentor keywords
    - Verify third_party_mentor_detected is True if >= 2 messages contain keywords (case-insensitive)
    - Test with 100 iterations

  - [ ]* 13.10 Write integration test for edge case detection suite
    - Mock Division 5 API call for echo chamber analytics
    - Test echo chamber detection with percentage above/below threshold
    - Test guardian veto detection with various speaker patterns
    - Test third-party mentor detection with varying keyword counts
    - Test reality check detection with various education levels
    - Test gender context detection with gender_family concerns
    - _Requirements: 9, 10, 11, 12, 13_

- [ ] 14. Implement Counselling Orchestration Controller (main entry point)
  - [ ] 14.1 Create CounsellingOrchestrationController class in `backend/app/services/counselling_orchestrator.py`
    - Implement `__init__` accepting all service dependencies: concern_classifier, prompt_manager, response_generator, escalation_engine, counsellor_brief_builder, conversation_state_manager, concern_state_calculator, edge_case_detectors
    - Implement `async def process_message(session_id, speaker, message, language) -> CounsellingResponse` orchestrating complete pipeline
    - Add 15-second request timeout
    - Implement circuit breakers for external services (Division 2, 5)
    - Track performance metrics: classification_time, retrieval_time, generation_time, total_time
    - _Requirements: 16.1, 16.2, 16.3, 16.5, 15.8_

  - [ ] 14.2 Implement translation integration with Division 4
    - If language != 'en', call Division 4 POST /api/internal/language/translate to translate message to English
    - Store both text_original and text_english
    - After generating response in English, call Division 4 to translate response to user's language
    - Handle Division 4 unavailability gracefully: proceed with English-only, log warning
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 15.4_

  - [ ] 14.3 Implement main pipeline orchestration
    - Step 1: Translate message to English (if needed)
    - Step 2: Retrieve session context from Division 1
    - Step 3: Classify concern using LLM
    - Step 4: Retrieve evidence from Division 2 (parallel with analytics)
    - Step 5: Get cross-session analytics from Division 5 (parallel with evidence)
    - Step 6: Detect edge case patterns
    - Step 7: Generate speaker-aware response using LLM
    - Step 8: Update concern state
    - Step 9: Store message, concern, evidence in Division 1
    - Step 10: Evaluate escalation rules
    - Step 11: Generate counsellor brief (if escalated)
    - Step 12: Translate response to user language
    - Step 13: Return complete API response
    - _Requirements: 16.3_

  - [ ] 14.4 Implement parallel execution optimizations
    - Run evidence retrieval and analytics retrieval in parallel using asyncio.gather
    - Run translation of user message and session context retrieval in parallel
    - Use connection pooling for all HTTP clients (max 100 connections)
    - _Requirements: 16.2, 16.3, 16.6_

  - [ ] 14.5 Implement error handling and graceful degradation
    - Groq API failure → Retry 3x → Fallback to Ollama → Return 503
    - Division 2 unavailable → Generate response acknowledging limitation → Offer escalation
    - Division 4 unavailable → Proceed with English-only → Log warning
    - Division 5 unavailable → Skip echo chamber detection → Continue
    - Division 1 database error → Return 500
    - Log all service failures with error details
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7_

  - [ ] 14.6 Implement performance logging
    - Log timing breakdown: translation_time_ms, classification_time_ms, retrieval_time_ms, generation_time_ms, total_time_ms
    - Log performance warning if total_time > 5 seconds
    - Include session_id, concern_category, concern_intent in performance logs
    - _Requirements: 16.7, 16.8, 18.5_

  - [ ]* 14.7 Write integration test for complete counselling flow (no escalation)
    - Mock all Division APIs (1, 2, 4, 5) and Groq API
    - Test complete pipeline: translate → classify → retrieve → generate → update state → return response
    - Verify response contains all required fields: message_id, response, concern, evidence, concern_state, escalated=False
    - _Requirements: 17.1, 17.2, 17.3, 17.4_

  - [ ]* 14.8 Write integration test for complete counselling flow (with escalation)
    - Mock escalation scenario (e.g., evidence unavailable for safety concern)
    - Verify escalation triggered, counsellor brief generated
    - Verify response contains escalated=True, escalation_id, counsellor_brief
    - _Requirements: 17.1, 17.5, 8.9_

- [ ] 15. Create FastAPI router and endpoint
  - [ ] 15.1 Create router in `backend/app/routers/counselling.py`
    - Define POST /api/counselling/message endpoint
    - Validate request schema: session_id, speaker (learner/parent/guardian), message (1-2000 chars), language
    - Call counselling_orchestrator.process_message()
    - Return response with schema validation
    - Handle exceptions: 503 (LLM unavailable), 500 (internal error), 408 (timeout), 404 (session not found), 422 (validation error)
    - _Requirements: 17.1, 17.6, 17.7, 17.8, 17.9_

  - [ ] 15.2 Implement request and response schemas
    - Create CounsellingMessageRequest in `backend/app/schemas/counselling.py`
    - Create ConcernResponse, CounsellorBriefResponse, CounsellingMessageResponse
    - Validate all responses against Pydantic v2 schemas before returning
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

  - [ ] 15.3 Register router in `backend/app/main.py`
    - Import counselling router
    - Register with app.include_router(counselling_router)
    - Add to API documentation

  - [ ]* 15.4 Write end-to-end test for POST /api/counselling/message endpoint
    - Test valid request returns 200 with complete response schema
    - Test session_id not found returns 404
    - Test invalid request body returns 422
    - Test LLM service unavailable returns 503
    - _Requirements: 17.8, 17.9_

- [ ] 16. Checkpoint - Verify complete orchestration pipeline
  - Ensure all integration tests pass, end-to-end flow works from API endpoint to response
  - Test with multiple concurrent requests (simulate 10 concurrent sessions)
  - Ask user if questions arise about orchestration flow or error handling

- [ ] 17. Implement logging and observability
  - [ ] 17.1 Configure structured logging in `backend/app/config.py`
    - Set up Python logging with structured JSON output
    - Define log levels: INFO (requests, classifications, escalations), WARNING (low confidence, service failures), ERROR (API failures, exceptions)
    - Include standard fields: timestamp, log_level, session_id, message_id, concern_category, concern_intent, speaker, district, trade, service_name="division-3"
    - _Requirements: 18.1, 18.2, 18.3, 18.4_

  - [ ] 17.2 Add logging throughout pipeline
    - Log at INFO: request received, concern classification, evidence retrieval, escalation triggered, response returned
    - Log at WARNING: low confidence classification (< 0.5), evidence unavailable, translation failure, analytics unavailable
    - Log at ERROR: LLM API failure, Division API failures, database errors, unexpected exceptions with stack traces
    - Log performance metrics for each request
    - _Requirements: 18.1, 18.2, 18.3, 18.5_

  - [ ] 17.3 Implement sensitive data filtering
    - Do NOT log full message content at INFO level (use DEBUG level only)
    - Do NOT log family names or PII at INFO level
    - Log message_id and summary information only
    - _Requirements: 18.6_

  - [ ] 17.4 Configure debug logging for development
    - Log all API request/response payloads at DEBUG level
    - Enable debug logging only in development/staging environments (not production)
    - _Requirements: 18.7_

- [ ] 18. Write scenario-based end-to-end tests for 5 edge cases
  - [ ]* 18.1 Write E2E test: Echo Chamber → Escalation
    - Precondition: Division 5 analytics shows 75% of Nashik + Wireman sessions have social_perception concerns
    - Simulate 4 turns with social_perception concerns
    - Verify echo chamber context included in responses ("common in Nashik")
    - Verify escalation triggered after turn limit with reason "echo_chamber_pattern_requires_community_intervention"
    - Verify counsellor brief recommended_action includes "community information session"
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [ ]* 18.2 Write E2E test: Guardian Veto → Escalation
    - Simulate session with guardian and learner speakers
    - Guardian raises 3+ concerns (social_perception, income, employment) across turns 1-4
    - Learner does not raise objections
    - Verify guardian veto pattern detected
    - Verify prompts adjusted to respectful, evidence-first framing
    - Verify escalation triggered after turn limit with reason "guardian_veto_requires_counsellor_mediation"
    - Verify counsellor brief recommended_action includes "individual conversations with learner and guardian separately"
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [ ]* 18.3 Write E2E test: Third-Party Mentor Pattern → Session Summary
    - Simulate session with learner speaker mentioning "teacher said" and "uncle suggested" in turns 1-2
    - Verify third-party mentor pattern detected
    - User requests summary: "Can you summarize this for my teacher?"
    - Verify session summary generated with: trades_discussed, concerns_raised, concerns_resolved, key_evidence, recommendation
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.7_

  - [ ]* 18.4 Write E2E test: Reality Check for Under-18 Learner
    - Simulate session with learner_education="Class 10"
    - Ask information_gap concern: "What will I learn in Solar Technician training?"
    - Verify reality check fields included in response: physical_demand, typical_day, trainee_quote
    - Verify evidence prioritizes non-null reality_check fields
    - Verify trainee_quote includes source validation
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.6, 12.7_

  - [ ]* 18.5 Write E2E test: Gender Context for Gender_Family Concern
    - Simulate session with gender_family concern: "Is electrician suitable for my daughter?"
    - Verify evidence prioritizes female_enrollment_pct and safety_infrastructure fields
    - Verify response includes: "Currently, [X]% of trainees are female" and "The training center provides: [safety measures]"
    - Test low female enrollment (<20%): verify transparent acknowledgment
    - Test adequate female enrollment (>=20%): verify positive framing
    - Verify escalation if gender data unavailable on 2nd turn
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7_

- [ ] 19. Checkpoint - Verify all edge cases work end-to-end
  - Ensure all E2E scenario tests pass (5 edge cases)
  - Verify property-based tests pass (21 properties, 100 iterations each)
  - Ask user if questions arise about edge case detection or E2E flows

- [ ] 20. Performance testing and optimization
  - [ ]* 20.1 Write performance test for 50 concurrent sessions
    - Use pytest-asyncio with 50 concurrent requests
    - Measure 95th percentile latency (target: < 5 seconds)
    - Measure average latency (target: < 3 seconds)
    - Verify no performance degradation at 50 concurrent sessions
    - _Requirements: 16.1, 16.4_

  - [ ] 20.2 Optimize parallel execution
    - Ensure evidence retrieval and analytics retrieval run in parallel
    - Ensure translation and session context retrieval run in parallel
    - Profile timing breakdown to identify bottlenecks
    - _Requirements: 16.2, 16.3_

  - [ ] 20.3 Implement connection pooling
    - Configure httpx clients with connection limits (max 100 connections, 20 keepalive)
    - Test connection reuse reduces latency
    - _Requirements: 16.6_

  - [ ] 20.4 Verify timeout handling
    - Test 15-second request timeout returns 408
    - Test Groq API timeout (10s) triggers fallback or 503
    - Test Division API timeouts don't crash the service
    - _Requirements: 16.5, 15.8_

- [ ] 21. Final integration and deployment preparation
  - [ ] 21.1 Create environment configuration
    - Document all required environment variables in `.env.example`
    - Create startup validation for required variables (GROQ_API_KEY, DIVISION_*_BASE_URL)
    - Configure default values for thresholds (CONFIDENCE_THRESHOLD=0.7, TURN_LIMIT=5, ECHO_CHAMBER_THRESHOLD=70.0)
    - _Requirements: 19.1, 19.2, 19.3, 19.4_

  - [ ] 21.2 Write deployment documentation
    - Document Docker configuration (Dockerfile, docker-compose if needed)
    - Document health check endpoint setup
    - Document production readiness checklist: environment variables, prompt templates, circuit breakers, logging, monitoring
    - _Requirements: 19.1_

  - [ ] 21.3 Verify all tests pass
    - Run all property-based tests (21 properties, 100 iterations each)
    - Run all integration tests (Groq API, Division 1-5 integrations)
    - Run all E2E scenario tests (5 edge cases)
    - Run performance test (50 concurrent sessions)
    - Verify test coverage >= 80% for internal logic

  - [ ] 21.4 Final checkpoint - Deployment readiness
    - All tests passing (property tests, integration tests, E2E tests, performance tests)
    - All 19 requirements validated through tests
    - All 21 correctness properties verified
    - Logging configured and tested
    - Error handling tested for all failure modes
    - Performance targets met (95th percentile < 5s, average < 3s, 50 concurrent sessions)
    - Ask user if ready to deploy or if additional testing needed

## Notes

- **Property-Based Testing**: 21 properties covering internal logic (concern classification parser, escalation rules, hierarchical concern state, edge case detection). Each property runs 100 iterations using Hypothesis.
- **Integration Testing**: All Division API interactions (1, 2, 4, 5) and Groq API tested with mocks.
- **End-to-End Testing**: 5 edge-case scenarios (echo chamber, guardian veto, third-party mentor, reality check, gender context) tested with live LLM and database.
- **Optional Tasks**: All tasks marked with `*` are optional (primarily testing tasks). Core implementation tasks are NOT optional.
- **Requirements Traceability**: Each task references specific requirements (e.g., _Requirements: 1.1, 1.2_) for full coverage.
- **Checkpoints**: 6 checkpoints ensure incremental validation and user feedback at reasonable breaks.
- **Technology Stack**: FastAPI, Groq API (llama-3.1-8b-instant), httpx, Jinja2, Hypothesis, Tenacity, Python 3.11+
- **Performance Targets**: 95th percentile < 5s, average < 3s, 50 concurrent sessions supported
- **Escalation Rules**: 5 deterministic rules evaluated in precedence order (Rule 1 → Rule 2 → Rule 3 → Rule 4 → Rule 5)
- **Edge Cases**: 5 critical patterns detected (echo chamber, guardian veto, third-party mentor, reality check, gender context)

## Workflow Completion

This workflow creates the design and planning artifacts for Division 3 - Counselling Orchestrator. **Implementation is NOT part of this workflow.**

To begin executing tasks:
1. Open this tasks.md file
2. Click "Start task" next to any task item
3. The agent will implement the task according to the specifications

The complete orchestration pipeline will be functional once all tasks are executed, integrating concern classification, evidence retrieval, speaker-aware response generation, escalation decision-making, and edge case detection into a cohesive counselling experience.
