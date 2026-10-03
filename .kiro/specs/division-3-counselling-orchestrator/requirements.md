# Requirements Document: Division 3 - Counselling Orchestrator

## Introduction

This document specifies the requirements for Division 3 of the PS 26241 AI-Enabled Career Counselling Platform. Division 3 implements the Counselling Orchestrator, which is the **core intelligence layer** of the platform. It orchestrates the main counselling interaction endpoint POST /api/counselling/message and is responsible for multi-turn conversation management, concern classification using LLM-based zero-shot/few-shot classification, speaker-aware prompt engineering (learner vs parent vs guardian perspectives), evidence retrieval integration with Division 2, LLM response generation using Groq API with evidence grounding, hierarchical concern state tracking and updates, deterministic escalation decision logic implementing 5 escalation rules, counsellor brief generation with structured context, echo chamber detection using Division 5 analytics, and guardian veto detection from speaker position analysis. This division transforms family questions into evidence-grounded responses while handling five critical real-world edge cases: village/peer echo chambers, third-party mentor guidance, fascination vs reality gaps for under-18 learners, gender isolation fears in male-dominated trades, and guardian veto situations requiring human counsellor intervention.

## Glossary

- **Counselling_Orchestrator**: The backend service responsible for processing user messages, classifying concerns, retrieving evidence, generating LLM responses, and managing escalations
- **Concern_Classifier**: LLM-based component that classifies user messages into one of 7 categories and 20+ intents with confidence scores
- **Speaker_Aware_Prompts**: Differentiated prompt templates that adjust tone and framing based on whether the speaker is a learner, parent, or guardian
- **Evidence_Grounded_Response**: An LLM-generated response that explicitly references verified MSDE outcome data and includes evidence citations
- **Multi_Turn_Conversation**: Conversation state management across multiple messages within a single session, tracking concern history and evidence shown
- **Concern_State_Update**: The process of updating intent-level and category-level concern statuses from 'open' → 'partially_resolved' → 'resolved' based on LLM response and evidence coverage
- **Escalation_Rules_Engine**: Deterministic logic that evaluates 5 escalation rules and triggers counsellor brief generation when conditions are met
- **Counsellor_Brief**: Structured case file containing family context, primary/secondary concerns, evidence already shown, escalation reason, and recommended counsellor actions
- **Echo_Chamber_Detection**: Analysis of cross-session analytics from Division 5 to identify repetitive concern patterns driven by village/peer pressure rather than individual reasoning
- **Guardian_Veto_Detection**: Analysis of speaker positions and concern patterns to identify situations where a guardian (typically father/uncle) is blocking vocational training despite learner interest
- **Third_Party_Mentor_Pattern**: Detection of non-family speakers (teachers, relatives) guiding decisions, requiring session summary generation for external stakeholders
- **Reality_Check_Presentation**: Surfacing physical demand, typical workday, and trainee quotes from Division 2 enhanced evidence to address fascination vs reality gaps
- **Gender_Context_Handling**: Prioritizing female enrollment and safety infrastructure evidence from Division 2 when addressing gender_family concerns
- **Groq_API_Client**: Client for Groq LLM API using llama-3.1-8b-instant model with fallback to Ollama
- **Confidence_Threshold**: Configurable threshold (default 0.7) below which LLM classification triggers escalation
- **Turn_Limit**: Configurable maximum turns for a concern to remain unresolved (default 5) before escalation
- **Session_Summary_Generator**: Component that generates structured summaries for third-party mentors, including trades discussed, concerns raised/resolved, key evidence, and recommendations

## Requirements

### Requirement 1: Concern Classification with LLM-Based Zero-Shot Classifier

**User Story:** As the Counselling Orchestrator, I want to classify user messages into concern categories and intents, so that I can retrieve relevant evidence and tailor responses appropriately.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL classify user messages using Groq API with llama-3.1-8b-instant model
2. THE Concern_Classifier SHALL accept inputs: message text, speaker type (learner/parent/guardian), and session context (trades_of_interest, district, state)
3. THE Concern_Classifier SHALL classify messages into exactly one of 7 categories: income, employment, safety, social_perception, education_progression, gender_family, information_gap
4. THE Concern_Classifier SHALL classify messages into exactly one intent within the detected category (20+ total intents across categories)
5. THE Concern_Classifier SHALL return a confidence score between 0.0 and 1.0 indicating classification certainty
6. WHEN the confidence score is below 0.7, THE Counselling_Orchestrator SHALL flag the classification as low-confidence for potential escalation
7. THE Concern_Classifier SHALL use structured output format: category (string), intent (string), confidence (float), reasoning (string)
8. WHEN the LLM API fails or times out, THE Counselling_Orchestrator SHALL return HTTP 503 with error message "LLM service unavailable"
9. THE Concern_Classifier SHALL complete classification within 2 seconds for 95% of requests
10. THE Concern_Classifier SHALL log all classification results with message_id, category, intent, confidence, and reasoning for debugging and quality improvement

### Requirement 2: Speaker-Aware Prompt Engineering

**User Story:** As the Counselling Orchestrator, I want to adjust prompt tone and framing based on speaker type, so that responses resonate appropriately with learners, parents, and guardians.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL maintain three prompt template sets: learner_prompts, parent_prompts, guardian_prompts
2. WHEN the speaker is 'learner', THE Counselling_Orchestrator SHALL use prompts with empowering, career-focused framing (e.g., "Let's explore what this trade offers for your future")
3. WHEN the speaker is 'parent', THE Counselling_Orchestrator SHALL use prompts with practical, outcomes-focused framing (e.g., "Here's the verified data on job placement and earnings")
4. WHEN the speaker is 'guardian', THE Counselling_Orchestrator SHALL use prompts with respectful, evidence-first framing (e.g., "The government outcome data shows the following verified results")
5. THE prompt templates SHALL include placeholders for: speaker_name, concern_category, concern_intent, trade, district, state, evidence_summary
6. THE Counselling_Orchestrator SHALL include speaker context in system prompt: "You are counselling a [learner/parent/guardian] about vocational education in [district], [state]"
7. WHEN multiple speakers are present in speakers_present array, THE Counselling_Orchestrator SHALL select the most conservative prompt template (guardian > parent > learner) for primary responses
8. THE Counselling_Orchestrator SHALL log which prompt template was used for each response to enable A/B testing and optimization

### Requirement 3: Evidence Retrieval Integration with Division 2

**User Story:** As the Counselling Orchestrator, I want to retrieve filtered evidence from Division 2 based on concern classification, so that I can provide location-specific, concern-relevant data to families.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL call Division 2 endpoint POST /api/internal/evidence/retrieve after concern classification
2. THE Counselling_Orchestrator SHALL pass filtering parameters: trade (from trades_of_interest), district, state, concern_category, concern_intent, top_k=3
3. WHEN Division 2 returns evidence array with length > 0, THE Counselling_Orchestrator SHALL proceed with evidence-grounded response generation
4. WHEN Division 2 returns empty evidence array, THE Counselling_Orchestrator SHALL check if the concern is a safety concern or requires verified data
5. WHEN Division 2 returns empty evidence array AND the concern is 'safety' OR 'employment' with intent 'placement_probability', THE Counselling_Orchestrator SHALL trigger escalation with reason "required_evidence_unavailable"
6. WHEN Division 2 returns empty evidence array for other concern categories, THE Counselling_Orchestrator SHALL generate a response acknowledging data limitations without escalation
7. THE Counselling_Orchestrator SHALL extract reality_check fields (physical_demand, typical_day, trainee_quote) from enhanced evidence schema when available
8. THE Counselling_Orchestrator SHALL extract gender context fields (female_enrollment_pct, safety_infrastructure) from enhanced evidence schema when concern_category is 'gender_family'
9. WHEN Division 2 API call fails or times out, THE Counselling_Orchestrator SHALL return HTTP 503 with error message "Evidence retrieval service unavailable"
10. THE Counselling_Orchestrator SHALL log all evidence retrieval requests and responses for debugging and analytics

### Requirement 4: LLM Response Generation with Evidence Grounding

**User Story:** As the Counselling Orchestrator, I want to generate LLM responses that explicitly reference verified evidence, so that families receive trustworthy, data-backed guidance instead of fabricated information.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL use Groq API with llama-3.1-8b-instant model for response generation
2. THE Counselling_Orchestrator SHALL construct a prompt containing: speaker-aware system prompt, conversation history (last 5 turns), current user message, concern classification result, retrieved evidence array formatted as structured text
3. THE Counselling_Orchestrator SHALL include evidence formatting in prompt: "Based on the following verified MSDE outcome data: [Evidence 1: Trade X, District Y, Placement Rate Z%, Earnings ₹A-₹B, Source: MSDE Dataset 2024-25]"
4. THE Counselling_Orchestrator SHALL instruct the LLM to cite evidence explicitly in responses (e.g., "According to MSDE data for Solar Technician in Nashik...")
5. WHEN reality_check data is available, THE Counselling_Orchestrator SHALL include it in the prompt: "Physical demands: [physical_demand]. Typical day: [typical_day]. Trainee experience: [trainee_quote]"
6. WHEN gender context data is available for gender_family concerns, THE Counselling_Orchestrator SHALL include it in the prompt: "Female enrollment: [female_enrollment_pct]. Safety infrastructure: [safety_infrastructure]"
7. THE Counselling_Orchestrator SHALL set LLM parameters: temperature=0.7, max_tokens=300, top_p=0.9
8. THE Counselling_Orchestrator SHALL validate that the LLM response length is between 50 and 400 words
9. WHEN the LLM response exceeds 400 words, THE Counselling_Orchestrator SHALL truncate at the last complete sentence within 400 words
10. WHEN the LLM API fails or times out after 3 retries with exponential backoff, THE Counselling_Orchestrator SHALL return HTTP 503 with error message "LLM response generation failed"

### Requirement 5: Multi-Turn Conversation State Management

**User Story:** As the Counselling Orchestrator, I want to track conversation history and concern evolution across multiple turns, so that I can provide contextually aware responses and avoid repetition.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL retrieve session context from Division 1 before processing each message (family_context, messages, concern_state, evidence_shown)
2. THE Counselling_Orchestrator SHALL include the last 5 conversation turns in the LLM prompt for context continuity
3. THE Counselling_Orchestrator SHALL store each user message in Division 1 messages table with speaker, text_original, text_english (if translated), language, timestamp
4. THE Counselling_Orchestrator SHALL store each assistant response in Division 1 messages table with speaker=NULL, message_type='assistant', text_original, language, timestamp
5. THE Counselling_Orchestrator SHALL track which evidence has already been shown by querying Division 1 evidence_shown history
6. WHEN the same evidence_id has been shown in the current session, THE Counselling_Orchestrator SHALL exclude it from the current response and request additional evidence from Division 2
7. THE Counselling_Orchestrator SHALL detect concern repetition: when the same (category, intent) pair is classified 3+ times without resolution, flag for escalation evaluation
8. THE Counselling_Orchestrator SHALL maintain a turn counter per concern intent, incrementing each time that intent is detected as 'open' in a new message
9. THE Counselling_Orchestrator SHALL reset the turn counter for a concern intent when its status is updated to 'resolved'

### Requirement 6: Hierarchical Concern State Update Logic

**User Story:** As the Counselling Orchestrator, I want to update concern resolution status at both intent and category levels, so that the system accurately tracks which concerns have been addressed.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL store each detected concern in Division 1 concerns table with: message_id, category, intent, confidence, raw_text, status='open', detected_at
2. AFTER generating an LLM response with evidence, THE Counselling_Orchestrator SHALL evaluate if the concern intent has been adequately addressed
3. THE Counselling_Orchestrator SHALL use heuristic rules for resolution evaluation: (a) Evidence was retrieved AND shown, (b) LLM response length > 100 words, (c) Evidence matches concern intent, (d) Confidence score >= 0.7
4. WHEN all heuristic conditions are met, THE Counselling_Orchestrator SHALL update the concern intent status to 'resolved' in Division 1 concerns table and set resolved_at timestamp
5. WHEN some but not all conditions are met, THE Counselling_Orchestrator SHALL update the concern intent status to 'partially_resolved'
6. WHEN the user asks a follow-up question about the same concern intent, THE Counselling_Orchestrator SHALL revert the concern intent status from 'resolved' to 'open'
7. THE Counselling_Orchestrator SHALL compute category-level status from intent-level statuses: (a) If any intent is 'open' → category is 'open', (b) If no intents are 'open' but at least one is 'partially_resolved' → category is 'partially_resolved', (c) If all intents are 'resolved' → category is 'resolved'
8. THE Counselling_Orchestrator SHALL update concern_state in real-time after each message processing cycle
9. THE Counselling_Orchestrator SHALL include updated concern_state in the API response to POST /api/counselling/message

### Requirement 7: Deterministic Escalation Rules Engine

**User Story:** As the Counselling Orchestrator, I want to evaluate 5 deterministic escalation rules, so that cases requiring human counsellor intervention are identified and escalated automatically.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL evaluate escalation rules in the following order after each response generation: Rule 1 (explicit request), Rule 2 (evidence unavailable), Rule 3 (safety concern + insufficient evidence), Rule 4 (turn limit exceeded), Rule 5 (low confidence threshold)
2. **Rule 1 - Explicit Request**: WHEN the user message contains phrases like "talk to a counsellor", "human counsellor", "speak to someone", "real person", THE Counselling_Orchestrator SHALL trigger escalation with reason "explicit_human_counsellor_request"
3. **Rule 2 - Evidence Unavailable**: WHEN Division 2 returns empty evidence array AND concern_category is 'employment' with intent 'placement_probability' OR concern_category is 'safety', THE Counselling_Orchestrator SHALL trigger escalation with reason "required_evidence_unavailable"
4. **Rule 3 - Safety Concern + Insufficient Evidence**: WHEN concern_category is 'safety' AND evidence array contains fewer than 2 items, THE Counselling_Orchestrator SHALL trigger escalation with reason "safety_concern_insufficient_evidence"
5. **Rule 4 - Turn Limit Exceeded**: WHEN a concern intent has been detected in 5+ messages AND its status is still 'open' or 'partially_resolved', THE Counselling_Orchestrator SHALL trigger escalation with reason "concern_unresolved_after_turn_limit"
6. **Rule 5 - Low Confidence Threshold**: WHEN concern classification confidence is below 0.5 AND the user message indicates frustration or dissatisfaction (phrases like "not helpful", "don't understand", "this isn't working"), THE Counselling_Orchestrator SHALL trigger escalation with reason "low_confidence_with_user_dissatisfaction"
7. WHEN any escalation rule triggers, THE Counselling_Orchestrator SHALL proceed to counsellor brief generation (Requirement 8)
8. WHEN no escalation rules trigger, THE Counselling_Orchestrator SHALL return the response with escalated=false, escalation_id=null, counsellor_brief=null
9. THE Counselling_Orchestrator SHALL log which escalation rule triggered for analytics and rule optimization

### Requirement 8: Counsellor Brief Generation

**User Story:** As the Counselling Orchestrator, I want to generate structured counsellor briefs when escalation occurs, so that human counsellors receive complete context to assist families effectively.

#### Acceptance Criteria

1. WHEN an escalation is triggered, THE Counselling_Orchestrator SHALL call Division 1 internal API POST /api/internal/session/{session_id}/escalations to create an escalation record
2. THE Counselling_Orchestrator SHALL identify the primary concern as the most recent concern with status 'open' or the concern that triggered escalation
3. THE Counselling_Orchestrator SHALL identify the secondary concern as the second most recent unresolved concern, if one exists
4. THE Counselling_Orchestrator SHALL compile information_already_provided as a list of evidence types shown: ['placement_rate', 'earnings_range', 'nsqf_level', 'career_progression', 'reality_check', 'gender_context']
5. THE Counselling_Orchestrator SHALL generate escalation_reason as a human-readable explanation of why escalation occurred, referencing the triggering rule and context
6. THE Counselling_Orchestrator SHALL generate recommended_action as a specific suggestion for the counsellor (e.g., "Discuss local Solar Technician employers in Nashik district and arrange site visit if possible")
7. THE counsellor brief SHALL include: learner_education, district, state, trade_interest (from family_context), primary_concern_category, primary_concern_intent, secondary_concern_category (optional), secondary_concern_intent (optional), data_already_shown, concern_status ('open'/'partially_resolved'), escalation_reason, recommended_action
8. THE Counselling_Orchestrator SHALL update the parent session's escalated field to TRUE and set escalation_id
9. THE Counselling_Orchestrator SHALL return the response with escalated=true, escalation_id, and counsellor_brief populated
10. THE Counselling_Orchestrator SHALL log the escalation event for Division 5 analytics tracking

### Requirement 9: Echo Chamber Detection Using Division 5 Analytics

**User Story:** As the Counselling Orchestrator, I want to detect when family concerns are driven by village/peer pressure rather than individual reasoning, so that I can tailor responses to address social dynamics and flag cases for counsellor intervention.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL call Division 5 internal API GET /api/internal/analytics/cross-session?district={district}&trade={trade}&concern_category={category} to retrieve cross-session analytics
2. THE Counselling_Orchestrator SHALL request analytics for: same district, same trade, same concern category as the current session
3. THE Counselling_Orchestrator SHALL receive analytics data from Division 5 containing: district, trade, total_sessions, concern_category, concern_frequency, dominant_percentage (e.g., "District: Nashik, Trade: Wireman, Sessions: 100, Concern: social_perception, Percentage: 72%")
4. WHEN Division 5 analytics show that the configured echo chamber threshold (default 70%) is exceeded for the current concern in the same district+trade combination, THE Counselling_Orchestrator SHALL flag this as a potential echo chamber pattern (Division 3 owns the decision logic, Division 5 provides the data)
5. WHEN an echo chamber pattern is detected AND the concern is 'social_perception' with any intent, THE Counselling_Orchestrator SHALL include echo chamber context in the LLM prompt: "Note: This concern is common among families in [district] considering [trade]. Many families express similar social perception concerns due to local community views. Focus on factual outcome data to address misconceptions."
6. WHEN an echo chamber pattern is detected AND the concern persists after 3 turns, THE Counselling_Orchestrator SHALL trigger escalation with reason "echo_chamber_pattern_requires_community_intervention"
7. THE Counselling_Orchestrator SHALL include echo chamber detection results in counsellor brief recommended_action: "Consider arranging a community information session in [district] to address widespread [concern_category] concerns about [trade]"
8. WHEN Division 5 analytics are unavailable (API failure), THE Counselling_Orchestrator SHALL proceed without echo chamber detection and log the failure
9. THE Counselling_Orchestrator SHALL NOT escalate solely based on echo chamber detection without also meeting turn limit or other escalation criteria
10. THE Counselling_Orchestrator SHALL log the echo chamber detection decision (threshold comparison, pattern detected true/false) for debugging and threshold tuning

### Requirement 10: Guardian Veto Detection from Speaker Analysis

**User Story:** As the Counselling Orchestrator, I want to detect guardian veto situations where a guardian is blocking vocational training despite learner interest, so that I can recommend human counsellor mediation for family alignment.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL analyze speaker patterns across conversation turns to detect guardian veto situations
2. WHEN speakers_present includes 'guardian' AND 'learner', THE Counselling_Orchestrator SHALL track which speaker raises which concerns
3. THE Counselling_Orchestrator SHALL detect guardian veto pattern when: (a) Guardian speaker raises 3+ concerns across categories, (b) Learner speaker has not raised objections or has expressed interest, (c) Concerns are primarily 'social_perception', 'income', or 'employment' raised by guardian
4. WHEN a guardian veto pattern is detected, THE Counselling_Orchestrator SHALL flag this in session metadata with pattern_type='guardian_veto'
5. WHEN a guardian veto pattern is detected AND concerns remain unresolved after 4 turns, THE Counselling_Orchestrator SHALL trigger escalation with reason "guardian_veto_requires_counsellor_mediation"
6. THE Counselling_Orchestrator SHALL include guardian veto context in counsellor brief recommended_action: "Guardian is expressing unresolved concerns while the learner shows interest. Recommend individual conversations with learner and guardian separately to understand underlying objections and build alignment."
7. THE Counselling_Orchestrator SHALL adjust LLM prompts when guardian veto is detected to use more respectful, evidence-first framing: "Your concerns for the learner's future are valid. Let's review the verified government data together."
8. THE Counselling_Orchestrator SHALL NOT detect guardian veto if learner is also raising similar concerns (indicating genuine shared concern vs. veto situation)

### Requirement 11: Third-Party Mentor Pattern and Session Summary Generation

**User Story:** As the Counselling Orchestrator, I want to detect third-party mentor involvement and generate session summaries, so that teachers, relatives, or mentors guiding families receive structured information to support decision-making.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL detect third-party mentor pattern when: (a) User message mentions "my teacher said", "uncle suggested", "counsellor recommended", "someone told me", (b) speaker is 'learner' or 'parent' but message references external guidance
2. WHEN a third-party mentor pattern is detected 2+ times in a session, THE Counselling_Orchestrator SHALL flag this in session metadata with pattern_type='third_party_mentor'
3. WHEN a third-party mentor pattern is detected AND user explicitly requests a summary ("can you summarize this for my teacher?", "I need to share this with my uncle"), THE Counselling_Orchestrator SHALL generate a session summary
4. THE session summary SHALL include: session_id, district, trades_discussed (list), concerns_raised (list of category+intent pairs), concerns_resolved (list of resolved category+intent pairs), key_evidence (summary of top 3 evidence items shown), recommendation (1-2 sentence guidance based on conversation), escalated (boolean), generated_at (timestamp)
5. THE Counselling_Orchestrator SHALL store the generated summary internally and make it available for Division 1 to persist if needed
6. THE Counselling_Orchestrator SHALL NOT create a conflicting public endpoint for session summaries (Division 4 handles GET /api/session/{session_id}/summary for the Share Summary feature)
7. THE Counselling_Orchestrator SHALL use LLM to generate the recommendation field based on conversation history, framing it as decision support: "Based on the discussion, [trade] in [district] shows [placement_rate]% placement and earnings of ₹[range]. Would you like to compare this with other options using local placement, earnings, and work-profile data?"
8. THE Counselling_Orchestrator SHALL log third-party mentor pattern detection for Division 5 analytics to track mentor influence rates

### Requirement 12: Reality Check Presentation for Fascination vs Reality Gap

**User Story:** As the Counselling Orchestrator, I want to present reality check data from Division 2, so that under-18 learners receive authentic trainee experiences and understand physical demands, not just idealized career descriptions.

#### Acceptance Criteria

1. WHEN the speaker is 'learner' AND learner_education indicates under-18 status (e.g., "Class 10", "Class 12"), THE Counselling_Orchestrator SHALL prioritize retrieving evidence with non-null reality_check fields
2. WHEN evidence contains reality_check data (physical_demand, typical_day, trainee_quote), THE Counselling_Orchestrator SHALL include all three fields in the LLM prompt
3. THE Counselling_Orchestrator SHALL instruct the LLM to present reality check data conversationally: "Here's what a typical day looks like: [typical_day]. One recent trainee shared: '[trainee_quote]'. The physical demands include: [physical_demand]."
4. THE Counselling_Orchestrator SHALL include reality_check data in responses to information_gap concerns with intents: 'course_content', 'duration', 'eligibility'
5. WHEN evidence does not contain reality_check data, THE Counselling_Orchestrator SHALL NOT fabricate trainee quotes or workday descriptions
6. THE Counselling_Orchestrator SHALL validate that trainee_quote_source is present before using trainee_quote (per Division 2 provenance requirements)
7. THE Counselling_Orchestrator SHALL log when reality_check data is included in responses for data quality monitoring

### Requirement 13: Gender Context Handling for Gender Isolation Fears

**User Story:** As the Counselling Orchestrator, I want to surface gender context data for gender_family concerns, so that families worried about girls in male-dominated trades receive evidence on female enrollment and safety infrastructure.

#### Acceptance Criteria

1. WHEN concern_category is 'gender_family', THE Counselling_Orchestrator SHALL request evidence from Division 2 with prioritization for non-null female_enrollment_pct and safety_infrastructure fields
2. WHEN evidence contains female_enrollment_pct, THE Counselling_Orchestrator SHALL include it in the LLM response: "Currently, [female_enrollment_pct] of trainees in this program are female."
3. WHEN evidence contains safety_infrastructure, THE Counselling_Orchestrator SHALL include it in the LLM response: "The training center provides: [safety_infrastructure]."
4. THE Counselling_Orchestrator SHALL adjust prompts for gender_family concerns to acknowledge parental protection concerns: "Your concerns about safety and suitability are important. Here's the verified data on female participation and safety measures."
5. WHEN concern_intent is 'suitability_for_daughter' AND female_enrollment_pct is below 20%, THE Counselling_Orchestrator SHALL acknowledge the low enrollment transparently: "Female enrollment is currently [pct], which reflects that this trade has historically had fewer women. However, verified placement data shows..."
6. WHEN concern_intent is 'suitability_for_daughter' AND female_enrollment_pct is 20% or above, THE Counselling_Orchestrator SHALL frame this positively: "Female enrollment is [pct], and the program has demonstrated successful outcomes for women trainees."
7. WHEN evidence does not contain gender context data for gender_family concerns, THE Counselling_Orchestrator SHALL evaluate escalation: if this is the 2nd turn without gender data, trigger escalation with reason "gender_context_data_unavailable"

### Requirement 14: Translation Integration with Division 4

**User Story:** As the Counselling Orchestrator, I want to translate user messages to English and assistant responses to the user's preferred language, so that the platform supports Hindi and Marathi speaking families.

#### Acceptance Criteria

1. WHEN a user message has language != 'en', THE Counselling_Orchestrator SHALL call Division 4 internal API POST /api/internal/language/translate with text=message, source_lang=language, target_lang='en'
2. THE Counselling_Orchestrator SHALL store both text_original (user's language) and text_english (translated) in Division 1 messages table
3. WHEN Division 4 translation fails, THE Counselling_Orchestrator SHALL proceed with text_original and log a warning, but continue processing (graceful degradation)
4. AFTER generating an LLM response in English, THE Counselling_Orchestrator SHALL call Division 4 internal API POST /api/internal/language/translate with text=response, source_lang='en', target_lang=preferred_language
5. THE Counselling_Orchestrator SHALL return both response (English) and response_translated (user's preferred language) in the API response
6. WHEN Division 4 translation of the response fails, THE Counselling_Orchestrator SHALL return response in English only and set response_translated=null with a logged warning
7. THE Counselling_Orchestrator SHALL NOT escalate solely due to translation service failures

### Requirement 15: Error Handling and Graceful Degradation

**User Story:** As the Counselling Orchestrator, I want to handle service failures gracefully, so that temporary outages of LLM, RAG, or translation services don't completely block counselling sessions.

#### Acceptance Criteria

1. WHEN Groq API fails after 3 retries with exponential backoff (1s, 2s, 4s), THE Counselling_Orchestrator SHALL attempt fallback to Ollama local LLM if configured
2. WHEN both Groq API and Ollama fail, THE Counselling_Orchestrator SHALL return HTTP 503 with error message "LLM service unavailable. Please try again in a few minutes."
3. WHEN Division 2 RAG service is unavailable, THE Counselling_Orchestrator SHALL generate a response acknowledging the limitation: "I'm currently unable to retrieve specific outcome data for [trade] in [district]. Would you like me to escalate this to a human counsellor who can help?"
4. WHEN Division 4 translation service is unavailable, THE Counselling_Orchestrator SHALL proceed with English-only responses and log a warning
5. WHEN Division 5 analytics service is unavailable, THE Counselling_Orchestrator SHALL skip echo chamber detection and proceed with standard response generation
6. WHEN Division 1 database operations fail, THE Counselling_Orchestrator SHALL return HTTP 500 with error message "Internal server error. Please contact support."
7. THE Counselling_Orchestrator SHALL log all service failures with error details, stack traces, and request context for debugging
8. THE Counselling_Orchestrator SHALL implement circuit breaker pattern for external API calls: after 5 consecutive failures, open circuit for 60 seconds before retrying

### Requirement 16: Performance and Concurrency Requirements

**User Story:** As the Counselling Orchestrator, I want to process messages efficiently and handle concurrent requests, so that the platform can serve multiple families simultaneously during peak usage.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL complete end-to-end message processing (classification + retrieval + generation + storage) within 5 seconds for 95% of requests
2. THE Counselling_Orchestrator SHALL use async/await pattern for all I/O operations (API calls, database queries)
3. THE Counselling_Orchestrator SHALL make parallel API calls where possible: (a) Concern classification completes before evidence retrieval, (b) Evidence retrieval and conversation history retrieval happen in parallel, (c) Translation of user message and Division 2 evidence retrieval happen in parallel
4. THE Counselling_Orchestrator SHALL support at least 50 concurrent counselling sessions without performance degradation
5. THE Counselling_Orchestrator SHALL implement request timeout of 15 seconds (return HTTP 408 if exceeded)
6. THE Counselling_Orchestrator SHALL use connection pooling for all external API clients (Groq, Division 1, Division 2, Division 4, Division 5)
7. THE Counselling_Orchestrator SHALL log performance metrics for each request: classification_time, retrieval_time, generation_time, total_time
8. WHEN total processing time exceeds 5 seconds, THE Counselling_Orchestrator SHALL log a performance warning with detailed timing breakdown

### Requirement 17: API Response Schema Compliance

**User Story:** As the frontend application, I want counselling responses to match the API contract exactly, so that I can reliably parse and display responses to families.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL return HTTP 200 with response schema: message_id, response (string), response_translated (string or null), concern (object), evidence (array), concern_state (object), escalated (boolean), escalation_id (string or null), counsellor_brief (object or null)
2. THE concern object SHALL contain: category (string), intent (string), confidence (float), raw_text (string)
3. THE evidence array SHALL contain 0-3 Evidence objects matching the Evidence schema from API contract Section 3.5
4. THE concern_state object SHALL contain all 7 categories with status and intents dictionary matching ConcernState schema from API contract Section 3.4
5. WHEN escalated is true, THE counsellor_brief object SHALL contain all fields: learner_education, district, state, trade_interest, primary_concern_category, primary_concern_intent, secondary_concern_category, secondary_concern_intent, data_already_shown, concern_status, escalation_reason, recommended_action
6. THE Counselling_Orchestrator SHALL validate all responses against Pydantic v2 schemas before returning
7. WHEN validation fails, THE Counselling_Orchestrator SHALL log the validation error and return HTTP 500 with error message "Response validation failed"
8. THE Counselling_Orchestrator SHALL return HTTP 404 when session_id does not exist
9. THE Counselling_Orchestrator SHALL return HTTP 422 when request body fails validation (missing required fields, invalid types)

### Requirement 18: Logging and Observability

**User Story:** As a backend developer, I want comprehensive logging and observability, so that I can debug issues, optimize performance, and monitor system health in production.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL log at INFO level: request received (session_id, speaker, language), concern classification (category, intent, confidence), evidence retrieval (query params, result count), escalation triggered (rule, reason), response returned (message_id, response_length)
2. THE Counselling_Orchestrator SHALL log at WARNING level: low confidence classification (< 0.5), evidence unavailable for critical concern, translation service failure, Division 5 analytics unavailable
3. THE Counselling_Orchestrator SHALL log at ERROR level: LLM API failure, Division 2 API failure, Division 1 database error, response validation failure, unexpected exceptions with stack traces
4. THE Counselling_Orchestrator SHALL include structured logging fields: timestamp, log_level, session_id, message_id, concern_category, concern_intent, speaker, district, trade, service_name="division-3"
5. THE Counselling_Orchestrator SHALL log performance metrics for each request: classification_time_ms, retrieval_time_ms, generation_time_ms, translation_time_ms, total_time_ms
6. THE Counselling_Orchestrator SHALL NOT log sensitive user data (full message content, family names) at INFO level; use DEBUG level only
7. THE Counselling_Orchestrator SHALL log all API request/response payloads at DEBUG level for development/staging environments only

### Requirement 19: Configuration Management

**User Story:** As a deployment engineer, I want configurable parameters for escalation thresholds and API endpoints, so that I can tune the system without code changes.

#### Acceptance Criteria

1. THE Counselling_Orchestrator SHALL load configuration from environment variables: GROQ_API_KEY, GROQ_MODEL_NAME (default: llama-3.1-8b-instant), CONFIDENCE_THRESHOLD (default: 0.7), TURN_LIMIT (default: 5), DIVISION_1_BASE_URL, DIVISION_2_BASE_URL, DIVISION_4_BASE_URL, DIVISION_5_BASE_URL, ENABLE_ECHO_CHAMBER_DETECTION (default: true), ENABLE_GUARDIAN_VETO_DETECTION (default: true)
2. THE Counselling_Orchestrator SHALL validate that required environment variables are set at startup and exit with error message if missing
3. THE Counselling_Orchestrator SHALL support Ollama fallback configuration: OLLAMA_BASE_URL (optional), OLLAMA_MODEL_NAME (default: llama3.1:8b)
4. THE Counselling_Orchestrator SHALL use configurable timeout values: GROQ_API_TIMEOUT (default: 10s), DIVISION_2_TIMEOUT (default: 5s), DIVISION_4_TIMEOUT (default: 3s)
5. THE Counselling_Orchestrator SHALL reload escalation rule thresholds without restart when configuration file changes (optional feature for production tuning)

## Special Requirements Guidance: Parsers and Serializers

**LLM Output Parsing Requirements**:
- The Counselling Orchestrator parses structured outputs from LLM APIs (concern classification, response generation)
- LLM outputs are semi-structured text that must be parsed into JSON-compatible objects
- Round-trip testing is NOT applicable (LLM responses are non-deterministic)
- Instead, use property-based testing for parser robustness with malformed/edge-case LLM outputs

**Example Parser Requirements**:
- Requirement 1 covers LLM classification output parsing (category, intent, confidence)
- Parsing logic should handle: missing fields, malformed JSON, extra whitespace, unexpected formats
- Property-based test: Generate random LLM-like strings, verify parser doesn't crash and returns valid or error state

## Special Requirements Guidance: Property-Based Testing

**Where Property-Based Testing Applies in Division 3**:

1. **Concern Classification Parser** (Requirement 1):
   - Property: Parser should handle malformed LLM outputs gracefully (no crashes)
   - Test: Generate random classification strings with missing/extra fields, verify parser returns valid ClassificationResult or raises expected error
   - Edge cases: Empty strings, non-JSON formats, Unicode characters, extremely long strings

2. **Hierarchical Concern State Calculation** (Requirement 6):
   - Property: Category status should always be derivable from intent statuses
   - Metamorphic property: Adding a resolved intent shouldn't change category from 'open' to 'resolved' if other intents are still 'open'
   - Test: Generate random concern sets with various status combinations, verify category calculation follows hierarchical rules

3. **Escalation Rules Evaluation** (Requirement 7):
   - Property: Escalation rules should be mutually exclusive (only one rule triggers per evaluation)
   - Property: Rule 1 (explicit request) should always take precedence over other rules
   - Test: Generate random session states with various escalation conditions, verify correct rule triggers and precedence

4. **Speaker-Aware Prompt Selection** (Requirement 2):
   - Property: Prompt template selection should be deterministic given speaker type
   - Test: Generate random speaker combinations, verify most conservative template is selected

5. **Evidence Filtering and Deduplication** (Requirement 5):
   - Property: Evidence shown in previous turns should not appear in current turn results
   - Test: Generate random evidence_shown histories, verify deduplication logic

**Where Integration Tests Apply**:

1. **LLM API Integration** (Requirements 1, 4): Use 2-3 example messages, verify classification and response generation
2. **Division 2 Evidence Retrieval** (Requirement 3): Use sample filter params, verify API call format and response handling
3. **Division 1 Database Operations** (Requirements 5, 6): Use sample sessions, verify message/concern/evidence storage
4. **Division 4 Translation** (Requirement 14): Use sample Hindi/Marathi messages, verify translation flow
5. **Division 5 Analytics** (Requirement 9): Use sample cross-session data, verify echo chamber detection
6. **Escalation Flow End-to-End** (Requirements 7, 8): Use scenarios triggering each of the 5 escalation rules, verify counsellor brief generation

**What NOT to use property-based testing for**:
- External API calls (LLM, Division 1-5) - use integration tests with mocks
- Database CRUD operations - use integration tests
- Translation service - use integration tests with sample phrases
- End-to-end counselling flow - use scenario-based integration tests

## Division Responsibilities and Boundaries

**Division 3 Core Responsibility:**
Division 3 is the **Counselling Orchestration and Intelligence Layer**. Its responsibility is to:
1. Classify concerns using LLM-based zero-shot classification
2. Orchestrate evidence retrieval from Division 2
3. Generate speaker-aware, evidence-grounded responses using LLM
4. Track multi-turn conversation state and concern resolution
5. Evaluate deterministic escalation rules and generate counsellor briefs
6. Detect edge-case patterns: echo chambers, guardian vetos, third-party mentors
7. Coordinate with Division 1 (session state), Division 2 (evidence), Division 4 (translation), Division 5 (analytics)

**What Division 3 Provides (Intelligence Layer):**
- Concern classification with confidence scoring
- Evidence-grounded LLM responses tailored to speaker type
- Real-time concern state updates
- Escalation decision-making with counsellor briefs
- Echo chamber detection using Division 5 analytics
- Guardian veto detection from speaker analysis
- Third-party mentor pattern detection and session summary generation
- Reality check presentation for under-18 learners
- Gender context handling for gender_family concerns

**What Division 3 Does NOT Do (Data and Services Layer):**
- **Evidence Storage/Retrieval** → Division 2 responsibility
- **Session State Persistence** → Division 1 responsibility
- **Translation Execution** → Division 4 responsibility
- **Cross-Session Analytics Calculation** → Division 5 responsibility
- **Counsellor Queue Management** → Division 1 responsibility

**Division Integration Pattern:**
```
User Message (Frontend)
      ↓
Division 3: Receive message → Translate (D4) → Classify concern (LLM)
      ↓
Division 3: Retrieve evidence (D2) + conversation history (D1) + analytics (D5)
      ↓
Division 3: Generate evidence-grounded response (LLM) + Evaluate escalation rules
      ↓
Division 3: Update concern state (D1) + Store message/concern/evidence (D1)
      ↓
If escalated: Division 3: Generate counsellor brief → Store escalation (D1)
      ↓
Division 3: Translate response (D4) → Return API response (Frontend)
```

**Key Principle:**
Division 3 is the **orchestrator and decision-maker**, not a data store or service provider. It coordinates all divisions to deliver the core counselling experience, implementing the business logic for concern resolution, escalation, and edge-case detection. Data persistence belongs to Division 1, evidence retrieval to Division 2, language handling to Division 4, and analytics to Division 5. Division 3 focuses on intelligence: classification, reasoning, decision-making, and response generation.
