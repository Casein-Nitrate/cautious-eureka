# Requirements Document: Division 4 - Complete Edge Case UI and Conversation Flow Implementation

## Introduction

This document specifies requirements for Division 4 of the PS 26241 AI-Enabled Career Counselling Platform. Division 4 implements the **complete UI layer and conversational flow** needed to surface all backend capabilities to families, addressing **all 10 real-world edge cases** identified in the audit.

**Context:** The audit revealed that while Divisions 1 (Session Service), 2 (RAG Evidence), and 3 (Counselling Orchestrator design) provide rich backend capabilities, Division 4 currently only implements translation/TTS infrastructure without the conversational AI orchestrator and UI components needed to make edge case solutions accessible to families.

**Goal:** Create a comprehensive React + Vite frontend with full conversational AI orchestrator integration that transforms backend data into family-friendly, mobile-first, regional-language interactions addressing all 10 edge cases.

## Glossary

- **Conversational_AI_Orchestrator**: The backend service (Division 3) that processes messages, classifies concerns, retrieves evidence, and generates speaker-aware responses using LLM
- **Edge_Case_UI_Component**: Specialized UI components designed to present evidence and reality checks for specific edge cases (reality cards, comparison matrices, decision summaries)
- **Speaker_Aware_Interface**: UI that adapts prompts, tone, and visual elements based on whether the current speaker is learner, parent, or guardian
- **Reality_Check_Card**: UI component presenting physical_demand, typical_day, and trainee_quote data to address viral fascination and herd mentality
- **Comparison_Matrix**: UI component enabling side-by-side trade comparisons across placement, earnings, progression, and work conditions
- **Family_Decision_Summary**: Shareable document summarizing trades discussed, concerns addressed, evidence shown, and discussion prompts for family conversation
- **Evidence_Card**: Visual component displaying verified MSDE data with source citations, placement rates, earnings ranges, and career progression paths
- **Multi_Turn_Chat_Interface**: Conversational UI maintaining conversation history, concern status indicators, and contextual follow-up suggestions
- **Mobile_First_Design**: UI optimized for touch interactions, low-literacy users, and regional language display on mobile devices
- **Regional_Language_Support**: Integration with Sarvam AI translation and TTS for Hindi (hi) and Marathi (mr) language support
- **Concern_Status_Indicator**: Visual badge showing real-time status of concerns (open/partially_resolved/resolved) during conversation
- **Escalation_Banner**: UI notification indicating when a case has been escalated to human counsellor with case ID and next steps
- **Alternative_Pathway_Suggester**: UI component recommending 2-3 alternative trades with rationale when herd mentality or proxy choice is detected
- **Investment_ROI_Calculator**: UI component showing training costs, payback timeline, and earnings progression to address investment panic
- **Gender_Context_Presenter**: UI component highlighting female enrollment percentages, safety infrastructure, and success stories for gender concerns
- **NSQF_Ladder_Visualizer**: UI component displaying NSQF levels, lateral entry points, and pathways to higher education

## Requirements

### Requirement 1: Conversational AI Orchestrator Integration

**User Story:** As a family member, I want to have natural multi-turn conversations about vocational education, so that I can get my specific concerns addressed with relevant evidence.

#### Acceptance Criteria

1. THE Chat_Interface SHALL call POST /api/counselling/message endpoint for each user message
2. THE Chat_Interface SHALL pass session_id, speaker (learner/parent/guardian), message text, and preferred language to the orchestrator
3. WHEN the orchestrator returns a response, THE Chat_Interface SHALL display the response_translated text in a message bubble
4. THE Chat_Interface SHALL display concern classification results (category, intent, confidence) in a status indicator
5. WHEN evidence is returned, THE Chat_Interface SHALL render Evidence_Card components inline with AI responses
6. THE Chat_Interface SHALL maintain conversation history displaying last 20 turns with speaker labels and timestamps
7. THE Chat_Interface SHALL auto-scroll to the most recent message when new responses arrive
8. THE Chat_Interface SHALL update Concern_Status_Indicator badges in real-time based on concern_state from API response
9. WHEN escalated flag is true, THE Chat_Interface SHALL display Escalation_Banner with escalation_id and counsellor_brief summary
10. THE Chat_Interface SHALL persist conversation state across page reloads by calling GET /api/session/{session_id} on mount

### Requirement 2: Speaker-Aware Interface with Role Selection

**User Story:** As a family member, I want the system to adapt its tone and questions to my role (learner/parent/guardian), so that conversations feel appropriate and respectful.

#### Acceptance Criteria

1. THE Speaker_Selector SHALL provide radio buttons for "I am the Learner", "I am the Parent/Guardian" based on speakers_present from session context
2. THE Speaker_Selector SHALL persist the selected speaker role across messages within a conversation
3. THE Speaker_Selector SHALL display different avatar colors for each role: learner (blue), parent (green), guardian (purple)
4. WHEN speaker is 'learner', THE Input_Field_Placeholder SHALL display empowering prompts (e.g., "What would you like to know about this career?")
5. WHEN speaker is 'parent', THE Input_Field_Placeholder SHALL display practical prompts (e.g., "Ask about placement rates, earnings, or job security")
6. WHEN speaker is 'guardian', THE Input_Field_Placeholder SHALL display respectful prompts (e.g., "I would like to understand the verified outcomes")
7. THE Message_Bubble SHALL display speaker role label above each user message (e.g., "You as Parent", "You as Learner")
8. THE Chat_Interface SHALL track which speaker raised which concerns in the conversation history sidebar
9. WHEN multiple speakers are present in a session, THE Speaker_Selector SHALL allow switching between roles during the conversation
10. THE Chat_Interface SHALL send the selected speaker value to the orchestrator with each POST /api/counselling/message request

### Requirement 3: Edge Case 1 - Herd Mentality Detection and Alternative Pathway UI

**User Story:** As a learner choosing a trade because friends chose it, I want to explore whether the work actually matches my interests and see alternative pathways, so that I make an informed decision aligned with my aptitudes.

#### Acceptance Criteria

1. WHEN the orchestrator detects herd mentality pattern (peer_comparison intent with high confidence), THE Chat_Interface SHALL display a Reality_Check_Card showing physical_demand, typical_day, and trainee_quote for the chosen trade
2. THE Reality_Check_Card SHALL present work conditions with visual icons (🏗️ for physical demand, ⏰ for typical schedule, 💬 for trainee experience)
3. THE Alternative_Pathway_Suggester SHALL display 2-3 related alternative trades retrieved from the orchestrator
4. THE Alternative_Pathway_Suggester SHALL show brief rationales for each alternative (e.g., "Similar electrical work but with renewable energy focus")
5. THE Alternative_Pathway_Suggester SHALL provide "Compare Trades" buttons launching Comparison_Matrix component
6. THE Comparison_Matrix SHALL display side-by-side comparison of chosen trade vs alternatives across: placement rate, earnings range, training duration, physical demand, career progression
7. THE Chat_Interface SHALL include reflection prompts after Reality_Check_Card: "Does this daily work match what you enjoy doing?"
8. THE Family_Decision_Summary SHALL include a "Why This Trade?" section documenting whether the choice was based on peer influence, personal interest, or aptitude alignment
9. THE Family_Decision_Summary SHALL list alternatives explored and comparison results
10. THE Chat_Interface SHALL allow users to switch their trade of interest after reviewing alternatives, updating session context via backend

### Requirement 4: Edge Case 2 - Viral Fascination Reality Check UI

**User Story:** As a learner attracted to a trade through social media, I want to see unvarnished daily work realities before enrollment, so that I understand what the job actually involves.

#### Acceptance Criteria

1. WHEN the orchestrator detects information_gap intent for course_content, THE Chat_Interface SHALL prioritize displaying Reality_Check_Card with typical_day timeline
2. THE Reality_Check_Card SHALL format typical_day as an hour-by-hour visual timeline with icons
3. THE Reality_Check_Card SHALL highlight physical_demand with color coding: green (low), yellow (moderate), red (high)
4. THE Reality_Check_Card SHALL display trainee_quote prominently with verified source citation below
5. THE Expectation_vs_Reality_Component SHALL present a two-column layout: "What You Might Think" vs "What It's Really Like"
6. THE Expectation_vs_Reality_Component SHALL populate the "Reality" column from evidence physical_demand and typical_day fields
7. THE Expectation_vs_Reality_Component SHALL use conversational language avoiding technical jargon (e.g., "Standing for most of the 8-hour shift" instead of "Stationary work posture")
8. THE Chat_Interface SHALL ask follow-up question after Reality_Check_Card: "After seeing the actual work conditions, does this still interest you?"
9. THE Reality_Check_Card SHALL be displayed BEFORE any enrollment recommendation in the conversation flow
10. THE Family_Decision_Summary SHALL include Reality_Check_Card content in a "What The Work Involves" section for family discussion

### Requirement 5: Edge Case 3 - Income Illusion Earnings Progression UI

**User Story:** As a parent, I want to see verified entry-level wages and realistic progression timelines, so that I don't have inflated salary expectations.

#### Acceptance Criteria

1. WHEN the orchestrator detects income concern (starting_salary or long_term_earning intent), THE Chat_Interface SHALL display Earnings_Progression_Chart component
2. THE Earnings_Progression_Chart SHALL visualize earnings_min and earnings_max as a range bar (not a single inflated figure)
3. THE Earnings_Progression_Chart SHALL display progression_path stages as a vertical timeline with estimated salary ranges for each stage if available
4. THE Earnings_Progression_Chart SHALL show geographic salary variations when evidence from multiple districts is available (e.g., "Nashik: ₹18k-₹26k, Pune: ₹22k-₹35k")
5. THE Earnings_Progression_Chart SHALL include data_source and data_period citations below each salary figure
6. THE Context_Explainer SHALL display factors affecting earnings: "Starting salaries depend on: location, employer type, certification, experience"
7. THE Earnings_Progression_Chart SHALL use ₹ INR currency formatting with thousand separators (e.g., ₹18,000 not 18000)
8. THE Chat_Interface SHALL contrast "Entry-Level (0-2 years)" vs "Experienced (5+ years)" earnings explicitly
9. WHEN user asks about high salaries ("₹50,000/month"), THE Chat_Interface SHALL respond with verified range and progression timeline: "Verified MSDE data shows ₹18k-₹26k entry level, progressing to ₹35k-₹45k with 5+ years experience"
10. THE Earnings_Progression_Chart SHALL include a note: "These are verified government outcome figures, not anecdotal estimates"

### Requirement 6: Edge Case 4 - Information Vacuum Family-Friendly Explainers

**User Story:** As a parent unfamiliar with a trade, I want simple explanations of what the training involves and who hires graduates, so that I can understand and support my child's decision.

#### Acceptance Criteria

1. WHEN the orchestrator detects information_gap concern (course_content, duration, eligibility intent), THE Chat_Interface SHALL generate Family_Friendly_Explainer component
2. THE Family_Friendly_Explainer SHALL present curriculum in everyday language avoiding technical terms (e.g., "You'll learn to read electrical diagrams and install home wiring systems" instead of "Circuit schematic interpretation and residential conduit installation")
3. THE Family_Friendly_Explainer SHALL include a "Who Hires?" section listing employer types (e.g., "Construction companies, housing projects, electrical contractors, solar installation firms")
4. THE Family_Friendly_Explainer SHALL display training duration prominently with visual icon (📅 6 months ITI, 📅 1 year apprenticeship)
5. THE Family_Friendly_Explainer SHALL list eligibility requirements clearly (e.g., ✅ Class 10 pass, ✅ 15-40 years age, ✅ No entrance exam for ITI)
6. THE Evidence_Card SHALL include a "Share This Info" button generating a shareable Family_Decision_Summary document
7. THE Family_Decision_Summary SHALL be formatted as a mobile-friendly PDF or image with key facts: trade name, training duration, eligibility, placement rate, earnings range, who hires, source citation
8. THE Family_Decision_Summary SHALL include discussion prompts for parents: "Questions to discuss as a family: 1. Does the training duration fit our timeline? 2. Are jobs available in our district? 3. Does the earning potential meet our needs?"
9. THE Chat_Interface SHALL proactively answer anticipated parent questions from information_gap taxonomy before they are asked: fees, duration, eligibility, course content
10. THE Regional_Language_Support SHALL translate Family_Friendly_Explainer to preferred language (Hindi/Marathi) using Sarvam AI integration

### Requirement 7: Edge Case 5 - Proxy Choice Multi-Pathway Comparison UI

**User Story:** As a learner relying on a single mentor's advice, I want to see multiple relevant trade options with neutral comparisons, so that I can make an independent informed decision.

#### Acceptance Criteria

1. WHEN the orchestrator detects third-party mentor pattern or single trade fixation, THE Chat_Interface SHALL trigger Alternative_Pathway_Suggester with 2-3 related trades
2. THE Alternative_Pathway_Suggester SHALL retrieve alternatives from orchestrator based on trade similarity (same NSQF level, same sector, complementary skills)
3. THE Comparison_Matrix SHALL display neutral side-by-side comparison across standardized metrics: placement rate, earnings range, training duration, NSQF level, physical demand, career progression
4. THE Comparison_Matrix SHALL use color-coded indicators for relative comparison (green = higher placement, yellow = average, no red/negative framing to avoid bias)
5. THE Comparison_Matrix SHALL include data_source citations for each metric to establish credibility over personal advice
6. THE Evidence_Card SHALL display "Source: MSDE Outcome Dataset 2024-25" prominently below each trade's data
7. THE Chat_Interface SHALL present comparisons with neutral framing: "Here are verified outcomes for three related trades in your district" (not "Your uncle is wrong")
8. THE Comparison_Matrix SHALL be exportable as Family_Decision_Summary for learner to discuss with mentor
9. THE Chat_Interface SHALL allow users to request additional alternatives: "Show me more related trades"
10. THE Comparison_Matrix SHALL highlight objective differentiators (e.g., "Solar Technician has 12% higher placement rate than Electrician in Pune district based on MSDE data")

### Requirement 8: Edge Case 6 - "Log Kya Kahenge" Social Stigma Reframing UI

**User Story:** As a parent worried about social perception of vocational work, I want to see evidence of professional careers, modern technology, and economic dignity, so that I can feel confident in this path.

#### Acceptance Criteria

1. WHEN the orchestrator detects social_perception concern (status_of_trade, family_acceptance intent), THE Chat_Interface SHALL display Career_Dignity_Reframing component
2. THE Career_Dignity_Reframing SHALL present progression_path as an upward career ladder visualization showing advancement to supervisory/technical specialist roles
3. THE Career_Dignity_Reframing SHALL include titles that convey professionalism (e.g., "Solar Installation Specialist" → "Renewable Energy Supervisor" → "Site Project Manager")
4. THE Career_Dignity_Reframing SHALL display NSQF level equivalence: "NSQF Level 4 ITI = equivalent to Class 12 academic qualification"
5. THE Career_Dignity_Reframing SHALL show modern technology adoption: "Uses CAD software, digital measurement tools, automation systems" (trade-specific)
6. THE Career_Dignity_Reframing SHALL include verified earnings comparison: "ITI Solar Technician earns ₹18k-₹28k entry level vs BA graduate ₹12k-₹18k entry level" (if comparison data available)
7. THE Chat_Interface SHALL use respectful framing acknowledging parental concerns: "Your concerns about your child's future are completely valid. Let's look at verified career outcomes."
8. THE Career_Dignity_Reframing SHALL avoid shaming or dismissing social concerns, focusing on evidence over argumentation
9. THE Career_Dignity_Reframing SHALL include trainee success stories with quotes from trainee_quote field showing career satisfaction
10. THE Regional_Language_Support SHALL translate reframing content with culturally appropriate terminology (formal Hindi/Marathi for guardian conversations)

### Requirement 9: Edge Case 7 - Single-Shot Investment Panic ROI UI

**User Story:** As a parent worried about training costs, I want to see training investment breakdown and earnings payback timeline, so that I understand the financial return.

#### Acceptance Criteria

1. WHEN the orchestrator detects income concern with return_on_training intent, THE Chat_Interface SHALL display Investment_ROI_Calculator component
2. THE Investment_ROI_Calculator SHALL show training cost breakdown if available in evidence: tuition fees, exam fees, kit costs, hostel costs (if stored in backend)
3. THE Investment_ROI_Calculator SHALL display earnings_min monthly salary multiplied by 12 months for first-year earnings
4. THE Investment_ROI_Calculator SHALL calculate payback timeline: "If training costs ₹25,000 and starting salary is ₹20,000/month, investment recovered in 2 months" (if cost data available)
5. WHEN training cost data is NOT available in evidence, THE Investment_ROI_Calculator SHALL display generic guidance: "ITI training typically costs ₹10,000-₹30,000 for government institutes. With starting salary of ₹18,000/month, payback is typically 1-3 months."
6. THE Investment_ROI_Calculator SHALL compare training investment to degree costs: "ITI 6 months + ₹15k vs BA 3 years + ₹1.5 lakh" (if comparison data available)
7. THE Investment_ROI_Calculator SHALL visualize payback with a simple bar chart: Training Cost vs First Year Earnings
8. THE Chat_Interface SHALL proactively address investment panic: "Many parents worry about training costs. Here's the financial breakdown:"
9. THE Investment_ROI_Calculator SHALL include financial assistance information if available: "Government ITI: ₹0-₹5000/year tuition, scholarships available for SC/ST/OBC students"
10. THE Investment_ROI_Calculator SHALL emphasize fast payback: "Unlike 4-year degrees, vocational training pays back quickly - you start earning within 6-12 months"

### Requirement 10: Edge Case 8 - Desk-Job Security Fair Trade Comparison UI

**User Story:** As a parent, I want to see fair comparisons between technical trades and office jobs, so that I don't assume desk jobs are always better or more secure.

#### Acceptance Criteria

1. WHEN the orchestrator detects employment concern with job_security intent or social_perception with salary_comparison, THE Chat_Interface SHALL display Trade_vs_Desk_Comparison component
2. THE Trade_vs_Desk_Comparison SHALL compare vocational trade outcomes to general academic degree outcomes on: starting salary, placement rate, job availability, career progression (if comparison data available in backend)
3. THE Trade_vs_Desk_Comparison SHALL present trade advantages fairly: "Technical trades often have higher entry-level placement rates (78% vs 54% for BA/BCom) due to employer demand"
4. THE Trade_vs_Desk_Comparison SHALL acknowledge trade-offs without bias: "Technical work is more physical but has faster earning progression; desk jobs may have different growth paths"
5. THE Trade_vs_Desk_Comparison SHALL display career progression for both paths: "CNC Operator → Programmer → Production Supervisor" vs "Office Assistant → Executive → Manager"
6. THE Trade_vs_Desk_Comparison SHALL include job security context: "Manufacturing sector hiring is strong in Maharashtra - verified MSDE data shows 74-88% placement for technical trades"
7. WHEN parent expresses bias toward desk jobs ("I want my child in AC office, not workshop"), THE Chat_Interface SHALL respond with non-judgmental reframing: "Both paths have value. Here's verified outcome data to help you compare:"
8. THE Trade_vs_Desk_Comparison SHALL avoid portraying either path as superior, focusing on evidence-based differences
9. THE Trade_vs_Desk_Comparison SHALL highlight that technical trades can lead to desk-job-like roles: "CNC Programmer works at computer terminals; Draughtsman Civil does CAD design in office"
10. THE Trade_vs_Desk_Comparison SHALL use progression_path data from evidence to show upward mobility in technical careers

### Requirement 11: Edge Case 9 - Safety-Distance Lock Gender Context UI

**User Story:** As a parent concerned about my daughter's safety in male-dominated trades, I want to see female enrollment data, safety infrastructure, and success stories, so that I feel confident she will be safe and supported.

#### Acceptance Criteria

1. WHEN the orchestrator detects gender_family concern (suitability_for_daughter intent), THE Chat_Interface SHALL display Gender_Context_Presenter component
2. THE Gender_Context_Presenter SHALL prominently display female_enrollment_pct from evidence: "Currently 28% of trainees in this program are women"
3. THE Gender_Context_Presenter SHALL display safety_infrastructure from evidence: "Training center provides: separate women's washrooms, female instructors, hostel accommodation, safety protocols"
4. WHEN female_enrollment_pct is below 20%, THE Gender_Context_Presenter SHALL acknowledge honestly: "Female enrollment is currently lower (15%), which means this trade has historically had fewer women. However, verified placement data shows women graduates have 82% placement rate."
5. WHEN female_enrollment_pct is 20% or above, THE Gender_Context_Presenter SHALL frame positively: "Good female participation (28%) with demonstrated successful outcomes for women trainees"
6. THE Gender_Context_Presenter SHALL include female trainee success stories from trainee_quote field if trainee is female
7. THE Gender_Context_Presenter SHALL display workplace safety data if available: "85% of placement partners have women's safety committees and harassment prevention policies"
8. THE Chat_Interface SHALL use respectful tone acknowledging parental protection concerns: "Your daughter's safety is paramount. Here's what the data shows:"
9. THE Distance_Calculator SHALL display institute location and approximate distance from session district (if GPS/distance data becomes available in backend)
10. THE Gender_Context_Presenter SHALL include "Success Stories" section with verified outcomes of female graduates in the trade

### Requirement 12: Edge Case 10 - Academic Horizon Block NSQF Ladder UI

**User Story:** As a learner, I want to understand how vocational training connects to higher education, so that I don't think ITI is a dead-end blocking college degrees.

#### Acceptance Criteria

1. WHEN the orchestrator detects education_progression concern (nsqf_levels, further_education, degree_equivalence intent), THE Chat_Interface SHALL display NSQF_Ladder_Visualizer component
2. THE NSQF_Ladder_Visualizer SHALL display NSQF levels as a vertical ladder: Level 4 ITI → Level 5 Advanced ITI → Level 6 Diploma → Level 7 B.Voc → Level 8 Master's
3. THE NSQF_Ladder_Visualizer SHALL highlight the current trade's NSQF level from evidence nsqf_level field
4. THE NSQF_Ladder_Visualizer SHALL show lateral entry points: "After Level 4 ITI, you can enter Polytechnic Diploma (Level 6) directly"
5. THE NSQF_Ladder_Visualizer SHALL explain NSQF equivalence: "NSQF Level 4 ITI = Class 12 academic qualification for employment and further study"
6. THE NSQF_Ladder_Visualizer SHALL include progression_path from evidence showing on-the-job advancement alongside academic advancement
7. THE Chat_Interface SHALL explicitly address "dead-end" misconception: "ITI is not a dead-end. Verified pathways exist to Diploma, B.Voc, and university degrees through NSQF framework."
8. THE NSQF_Ladder_Visualizer SHALL show specific bridge programs if available: "Electrician ITI → Electrical Engineering Diploma → B.Tech Electrical Engineering"
9. THE NSQF_Ladder_Visualizer SHALL include both full-time and part-time study options: "You can work as a technician while pursuing evening Diploma classes"
10. THE Chat_Interface SHALL present progression as an opportunity: "Vocational training gives you two growth paths: career advancement at work AND higher education if you choose"

### Requirement 13: Multi-Turn Conversation State Management UI

**User Story:** As a family member, I want the chat interface to track conversation history and concern resolution progress, so that I don't have to repeat questions and can see what's been addressed.

#### Acceptance Criteria

1. THE Chat_Interface SHALL display last 20 conversation turns with speaker labels, message text, and timestamps
2. THE Chat_Interface SHALL display Concern_Status_Indicator badges for all 7 concern categories: income, employment, safety, social_perception, education_progression, gender_family, information_gap
3. THE Concern_Status_Indicator SHALL use color coding: 🔴 Open, 🟡 Partially Resolved, 🟢 Resolved, ⚪ Not Raised
4. THE Concern_Status_Indicator SHALL update in real-time after each AI response based on concern_state from POST /api/counselling/message response
5. THE Conversation_History_Sidebar SHALL list all concerns raised with their current status, clickable to scroll to relevant message
6. THE Chat_Interface SHALL display conversation turn count: "Turn 3 of session" for user awareness
7. WHEN a concern status changes from Open to Resolved, THE Chat_Interface SHALL briefly highlight the status change with animation
8. THE Chat_Interface SHALL persist conversation state across browser refreshes by calling GET /api/session/{session_id} on page load
9. THE Chat_Interface SHALL display "Continue your conversation" prompt when returning to an existing session
10. THE Chat_Interface SHALL include "Start New Session" button to create fresh session if user wants to explore different trades

### Requirement 14: Voice Input and Text-to-Speech for Low-Literacy Users

**User Story:** As a family member with limited reading ability, I want to speak my questions and hear responses read aloud, so that I can fully participate in counselling without literacy barriers.

#### Acceptance Criteria

1. THE Voice_Input_Button SHALL activate browser Web Speech API for voice recording
2. THE Voice_Input_Button SHALL display pulsing animation while recording is active
3. THE Voice_Input_Button SHALL automatically detect language from session preferred_language (mr-IN for Marathi, hi-IN for Hindi, en-IN for English)
4. WHEN voice transcription completes, THE Chat_Interface SHALL populate text input field with transcript and allow user to review before sending
5. THE Voice_Input_Button SHALL display error message if browser does not support Web Speech API: "Voice input not supported. Please type your message."
6. THE Text_to_Speech_Button SHALL appear next to each AI response message bubble
7. WHEN Text_to_Speech_Button is clicked, THE Chat_Interface SHALL use browser SpeechSynthesis API to read response_translated aloud
8. THE Text_to_Speech_Button SHALL display play/pause controls during audio playback
9. THE Text_to_Speech_Button SHALL use appropriate voice language based on session preferred_language
10. THE Chat_Interface SHALL provide audio playback speed control: 0.8x (slower), 1x (normal), 1.2x (faster) for user preference

### Requirement 15: Escalation Banner and Human Counsellor Handoff UI

**User Story:** As a family member, I want clear notification when my case is escalated to a human counsellor, so that I know what to expect next.

#### Acceptance Criteria

1. WHEN POST /api/counselling/message returns escalated=true, THE Chat_Interface SHALL display Escalation_Banner component prominently
2. THE Escalation_Banner SHALL display escalation_id prominently: "Case ID: ESC001"
3. THE Escalation_Banner SHALL display escalation reason in family-friendly language: "A human counsellor will help because: [reason]"
4. THE Escalation_Banner SHALL map technical trigger reasons to user-friendly explanations:
   - "required_evidence_unavailable" → "We need more specific local information to answer your question"
   - "concern_unresolved_after_turn_limit" → "Your concern needs personalized attention from an expert"
   - "explicit_human_counsellor_request" → "You requested to speak with a counsellor"
   - "safety_concern_insufficient_evidence" → "Safety questions deserve detailed personalized guidance"
5. THE Escalation_Banner SHALL display next steps: "A counsellor will review your case and contact you within 24-48 hours"
6. THE Escalation_Banner SHALL include counsellor_brief summary in simple language: "The counsellor will focus on: [primary_concern_category] - [primary_concern_intent]"
7. THE Escalation_Banner SHALL display what information has already been provided: "You've already received data on: placement rates, earnings, career progression"
8. THE Escalation_Banner SHALL include "Request Human Counsellor" button allowing users to manually escalate at any time
9. WHEN user clicks "Request Human Counsellor" button, THE Chat_Interface SHALL send message with explicit escalation trigger phrase to orchestrator
10. THE Escalation_Banner SHALL remain visible at top of chat after escalation, not disappearing on scroll

### Requirement 16: Family Decision Summary Export and Sharing

**User Story:** As a family, I want to export a summary of our counselling session, so that we can discuss it together offline and share with relatives.

#### Acceptance Criteria

1. THE Chat_Interface SHALL include "Download Summary" button in sidebar menu
2. WHEN "Download Summary" button is clicked, THE Chat_Interface SHALL call GET /api/session/{session_id}/summary endpoint
3. THE Family_Decision_Summary SHALL display: session_id, district, trades_discussed, concerns_raised, concerns_resolved, key_evidence, recommendation, escalated status, generated_at timestamp
4. THE Family_Decision_Summary SHALL include "Trades Explored" section listing all trades mentioned in conversation with brief outcome summaries
5. THE Family_Decision_Summary SHALL include "Concerns Addressed" section with checkmarks for resolved concerns and notes for unresolved concerns
6. THE Family_Decision_Summary SHALL include "Key Evidence" section with top 3 evidence items: trade, placement rate, earnings range, source citation
7. THE Family_Decision_Summary SHALL include "Family Discussion Questions" section with 3-5 prompts based on concerns raised (e.g., "Does the training duration fit our family timeline?" for information_gap concerns)
8. THE Family_Decision_Summary SHALL be formatted as mobile-friendly PDF or shareable image (PNG/JPG)
9. THE Family_Decision_Summary SHALL include platform branding: "Generated by Ministry of Skill Development AI Career Counselling Platform"
10. THE Family_Decision_Summary SHALL be downloadable in preferred language (Hindi/Marathi/English) matching session language

### Requirement 17: Mobile-First Responsive Design for Rural Access

**User Story:** As a family in a rural area accessing counselling on mobile phone, I want large touch targets and readable text on small screens, so that I can use the platform easily.

#### Acceptance Criteria

1. THE Chat_Interface SHALL use mobile-first responsive design with breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)
2. THE Touch_Targets SHALL have minimum size of 48x48 pixels for buttons and interactive elements (WCAG 2.1 compliance)
3. THE Text SHALL use minimum font size of 16px for body text to avoid zoom requirement on mobile browsers
4. THE Chat_Interface SHALL use single-column layout on mobile, collapsing sidebar into bottom sheet or hamburger menu
5. THE Evidence_Card SHALL stack sections vertically on mobile rather than side-by-side layout
6. THE Comparison_Matrix SHALL allow horizontal scrolling on mobile with sticky first column for trade names
7. THE Input_Field SHALL resize height automatically as user types long messages (auto-expand textarea)
8. THE Voice_Input_Button SHALL be positioned prominently on mobile for one-thumb access
9. THE Chat_Interface SHALL use system fonts supporting Devanagari script (Hindi/Marathi) without requiring font downloads
10. THE Chat_Interface SHALL minimize data usage by lazy-loading conversation history and compressing images

### Requirement 18: Regional Language Translation Integration

**User Story:** As a family preferring Hindi or Marathi, I want all UI text and AI responses in my language, so that I can fully understand counselling guidance.

#### Acceptance Criteria

1. THE Chat_Interface SHALL display all static UI text (buttons, labels, placeholders) in user's preferred language from session context
2. THE Chat_Interface SHALL call POST /api/internal/language/translate via backend for AI response translation (not directly calling Sarvam AI)
3. THE Chat_Interface SHALL display response_translated from POST /api/counselling/message response in message bubbles
4. THE Chat_Interface SHALL maintain English as fallback when translation service is unavailable, displaying warning: "Translation temporarily unavailable. Showing English response."
5. THE Evidence_Card SHALL translate category labels and field names: "Placement Rate" → "नियुक्ति दर" (Hindi), "नियुक्ती दर" (Marathi)
6. THE Concern_Status_Indicator SHALL translate category names: "Employment" → "रोजगार" (Hindi/Marathi), "Income" → "आय" (Hindi/Marathi)
7. THE Family_Decision_Summary SHALL be fully translated to preferred language including section headers and discussion prompts
8. THE Chat_Interface SHALL use appropriate text direction (LTR for all supported languages)
9. THE Chat_Interface SHALL avoid machine translation for critical terms, using verified translations from glossary: "NSQF" remains "NSQF", "ITI" remains "ITI" (established acronyms)
10. THE Regional_Language_Support SHALL handle code-mixed input (Hindi/Marathi with English technical terms) without breaking translation

### Requirement 19: Performance and Error Handling for Slow Networks

**User Story:** As a family in an area with slow internet, I want the chat to work reliably even with connection issues, so that I don't lose my conversation.

#### Acceptance Criteria

1. THE Chat_Interface SHALL display loading spinner during POST /api/counselling/message API calls with timeout of 30 seconds
2. WHEN API call times out or network error occurs, THE Chat_Interface SHALL display retry button: "Connection issue. Click to retry sending message."
3. THE Chat_Interface SHALL preserve unsent message text in input field when API call fails, allowing user to retry without retyping
4. THE Chat_Interface SHALL cache conversation history in browser localStorage, restoring on page refresh even without network
5. THE Chat_Interface SHALL display connection status indicator: 🟢 Connected, 🟡 Slow Connection, 🔴 Offline
6. WHEN backend returns 503 Service Unavailable (LLM service down), THE Chat_Interface SHALL display user-friendly error: "AI temporarily unavailable. Please try again in a few minutes or request human counsellor."
7. WHEN backend returns 404 Session Not Found, THE Chat_Interface SHALL redirect user to context setup page with message: "Session expired. Please start new session."
8. THE Chat_Interface SHALL implement optimistic UI updates: display user message immediately, show "Sending..." status until API confirms
9. THE Chat_Interface SHALL batch non-critical API calls (analytics, evidence history) to reduce network requests on slow connections
10. THE Chat_Interface SHALL compress images and lazy-load Evidence_Card components to minimize initial page load time

### Requirement 20: Accessibility Compliance for Screen Readers

**User Story:** As a visually impaired user using screen reader, I want all UI elements properly labeled, so that I can navigate the counselling interface.

#### Acceptance Criteria

1. THE Chat_Interface SHALL use semantic HTML: `<main>`, `<nav>`, `<section>`, `<article>` for proper document structure
2. THE Interactive_Elements SHALL have descriptive aria-label attributes: "Send message button", "Select speaker role", "Download summary"
3. THE Chat_Messages SHALL use aria-live="polite" region for screen readers to announce new messages
4. THE Concern_Status_Indicator SHALL use aria-label describing status: "Employment concern: resolved", "Income concern: partially resolved"
5. THE Evidence_Card SHALL use proper heading hierarchy (h1, h2, h3) for card sections
6. THE Images SHALL have descriptive alt text: "Career progression ladder for Solar Technician showing 5 advancement stages"
7. THE Form_Inputs SHALL have associated labels using `<label for="input-id">` or aria-labelledby
8. THE Chat_Interface SHALL support keyboard navigation: Tab to navigate, Enter to send message, Escape to close modals
9. THE Color_Coding SHALL not be sole indicator of status - include text labels and icons alongside colors
10. THE Chat_Interface SHALL maintain focus management: focus input field after sending message, focus first button in modal when opened

## Correctness Properties

### Property 1: Conversation State Consistency (Round-Trip Property)

**Type:** Round-Trip Property (serialization/deserialization)

**Description:** For any conversation state stored in backend via POST /api/counselling/message, retrieving session via GET /api/session/{session_id} SHALL return equivalent conversation history and concern state.

**Test Strategy:**
```
1. Create session with family context
2. Send 5 messages via POST /api/counselling/message
3. Retrieve session via GET /api/session/{session_id}
4. Assert:
   - messages array length = 10 (5 user + 5 assistant)
   - concern_state matches last POST response concern_state
   - speaker values match original inputs
   - message text_original matches sent messages
```

**Why this matters:** Ensures conversation state persists correctly across API calls and page refreshes, preventing data loss.

### Property 2: Evidence Display Completeness (Invariant)

**Type:** Invariant (property preserved after transformation)

**Description:** For any evidence array returned from POST /api/counselling/message, THE Chat_Interface SHALL display ALL required fields: trade, district, placement_rate, earnings_min, earnings_max, data_source, data_period. The count of Evidence_Card components rendered SHALL equal the length of evidence array.

**Test Strategy:**
```
GIVEN evidence array with N items from API response
WHEN Chat_Interface renders Evidence_Card components
THEN:
  - Evidence_Card component count = N
  - Each Evidence_Card displays ALL required fields
  - No evidence item is skipped or duplicated
  - Evidence order matches API response order
```

**Why this matters:** Prevents UI from dropping critical evidence fields or missing evidence items, ensuring families see complete data.

### Property 3: Speaker Role Consistency (Invariant)

**Type:** Invariant (property preserved across interactions)

**Description:** For any speaker role selected in UI, all subsequent POST /api/counselling/message requests SHALL include that speaker value until user explicitly changes it. The speaker value sent to API SHALL match the currently selected radio button.

**Test Strategy:**
```
GIVEN user selects speaker='parent'
WHEN user sends 3 messages without changing speaker
THEN:
  - All 3 POST requests have speaker='parent'
  - Message bubbles display "You as Parent" label
  - Input placeholder shows parent-specific prompt
  
WHEN user changes to speaker='learner'
THEN:
  - Subsequent POST request has speaker='learner'
  - UI updates to learner avatar color and prompts
```

**Why this matters:** Ensures speaker-aware prompts in backend receive correct speaker context for appropriate tone and framing.

### Property 4: Concern Status Monotonic Progress (Metamorphic Property)

**Type:** Metamorphic Property (relationship between states)

**Description:** Concern status changes SHALL follow progression: not_raised → open → partially_resolved → resolved. A concern SHALL NOT regress from resolved to open UNLESS user asks explicit follow-up question about that concern. The status displayed in UI SHALL match concern_state from API response.

**Test Strategy:**
```
GIVEN concern starts as 'not_raised'
WHEN concern is detected: status → 'open'
WHEN evidence shown: status → 'partially_resolved' OR 'resolved'
THEN:
  - Status SHALL NOT jump from 'not_raised' to 'resolved' (must pass through 'open')
  - Status SHALL NOT regress except on explicit user follow-up
  - UI Concern_Status_Indicator color matches status
  
Test case: income concern progression
1. Start: income = not_raised (⚪)
2. User asks "What's the salary?": income = open (🔴)
3. AI shows earnings evidence: income = partially_resolved (🟡)
4. User satisfied: income = resolved (🟢)
5. Assert UI badge colors match at each step
```

**Why this matters:** Ensures concern resolution tracking is logical and UI reflects accurate progress, preventing false "resolved" indicators.

### Property 5: Translation Idempotence (Idempotence Property)

**Type:** Idempotence (operation yields same result when repeated)

**Description:** For any AI response text, displaying response_translated from API SHALL produce same UI output regardless of how many times the component re-renders. Translation SHALL NOT be called multiple times for the same message on re-render.

**Test Strategy:**
```
GIVEN AI response with response_translated="यह एक परीक्षण संदेश है"
WHEN Chat_Interface renders message bubble
THEN:
  - Display response_translated directly (no redundant translation call)
  - Re-rendering component 10x displays same text
  - No additional POST /api/internal/language/translate calls
  
Test case: Force re-render by updating parent component state
1. Render message bubble with translated text
2. Trigger 5 parent component re-renders
3. Assert: Translation API called 0 times (uses cached response_translated)
4. Assert: Displayed text is identical across all renders
```

**Why this matters:** Prevents redundant translation API calls, reduces costs, and ensures consistent display across re-renders.

### Property 6: Evidence Card Data Provenance (Invariant)

**Type:** Invariant (required property always present)

**Description:** For every Evidence_Card displayed, data_source and data_period fields SHALL be visible and non-empty. THE Evidence_Card SHALL NOT display evidence without provenance citation.

**Test Strategy:**
```
GIVEN evidence array from API where each item has data_source and data_period
WHEN Evidence_Card components render
THEN:
  - Each Evidence_Card displays "Source: {data_source} ({data_period})"
  - Citation text is visible (not hidden or truncated)
  - If evidence lacks data_source, Evidence_Card SHALL NOT render (defensive)
  
Property-based test:
FORALL evidence in evidence_array:
  IF evidence is displayed in UI
  THEN evidence.data_source IS NOT NULL AND evidence.data_period IS NOT NULL
```

**Why this matters:** Ensures all evidence shown to families has verified provenance, maintaining trust and credibility.

### Property 7: Escalation Banner Visibility (Model-Based Testing)

**Type:** Model-Based Testing (reference implementation vs optimized)

**Description:** THE Escalation_Banner SHALL be visible whenever escalated=true in API response. The banner SHALL remain visible across scrolling and conversation continuation. This matches the reference model: escalated=true ↔ banner visible.

**Test Strategy:**
```
Reference model (simple boolean):
  escalated=true → banner visible
  escalated=false → banner hidden

Optimized UI implementation test:
1. Send message triggering escalation (POST returns escalated=true)
2. Assert Escalation_Banner is rendered in DOM
3. Scroll chat history to bottom
4. Assert Escalation_Banner still visible (sticky positioning)
5. Send 3 more messages after escalation
6. Assert Escalation_Banner still visible at top
7. Refresh page (reload session via GET)
8. Assert Escalation_Banner visible (session.escalated=true persisted)

Test case: escalation_id display
GIVEN escalation_id="ESC001"
THEN banner text contains "Case ID: ESC001"
```

**Why this matters:** Ensures users are always aware when their case is escalated, preventing confusion about conversation status.

### Property 8: Mobile Touch Target Size (Accessibility Invariant)

**Type:** Invariant (WCAG compliance property)

**Description:** ALL interactive elements (buttons, radio buttons, checkboxes, links) SHALL have minimum touch target size of 48x48 pixels on mobile viewport (<768px width). This invariant holds for all edge case UI components.

**Test Strategy:**
```
GIVEN viewport width = 375px (mobile)
WHEN Chat_Interface renders with all UI components
THEN:
  - Send button: width >= 48px AND height >= 48px
  - Speaker radio buttons: touch area >= 48x48px (including label)
  - Voice input button: width >= 48px AND height >= 48px
  - Evidence_Card action buttons: each >= 48x48px
  - Concern_Status_Indicator badges: clickable area >= 48x48px
  
Property-based test:
FORALL interactive_element in UI:
  IF viewport.width < 768px
  THEN element.touchArea >= 48x48px
```

**Why this matters:** Ensures mobile usability for rural families accessing platform on small-screen devices with finger touch input.

### Property 9: Alternative Pathways Uniqueness (Confluence Property)

**Type:** Confluence (order independence)

**Description:** For any Alternative_Pathway_Suggester display, suggested trades SHALL NOT include the currently selected trade AND SHALL contain no duplicates. The order of alternatives SHALL NOT affect comparison results in Comparison_Matrix.

**Test Strategy:**
```
GIVEN user's trade_of_interest = "Electrician"
WHEN Alternative_Pathway_Suggester displays alternatives
THEN:
  - Suggested trades SHALL NOT include "Electrician"
  - No duplicate trade names in suggestions
  - Suggestions are unique: Set(suggestions).length = suggestions.length
  
GIVEN alternatives = ["Solar Technician", "Wireman", "Electronics"]
WHEN Comparison_Matrix displays comparison
THEN:
  - Comparison results SHALL be identical regardless of order:
    - Compare(Electrician, Solar, Wireman) = Compare(Electrician, Wireman, Solar)
    - Placement rate ranking is deterministic
```

**Why this matters:** Prevents confusing UI showing same trade as both selected and alternative, ensures consistent comparison results.

### Property 10: Error Recovery Message Preservation (Invariant)

**Type:** Invariant (data preservation across failure)

**Description:** WHEN POST /api/counselling/message fails (timeout, network error, 503), the user's unsent message text SHALL remain in input field. THE Chat_Interface SHALL NOT clear input on API failure.

**Test Strategy:**
```
GIVEN user types message="What is the placement rate?"
WHEN POST /api/counselling/message returns 503 Service Unavailable
THEN:
  - Input field still contains "What is the placement rate?"
  - Error message displays: "Connection issue. Click to retry."
  - User can click retry without retyping
  
GIVEN user types long message (200 words)
WHEN network timeout occurs after 30 seconds
THEN:
  - Input field preserves full 200-word message
  - Retry button sends same message text
  
Test case: Multiple retry attempts preserve message
1. Type message
2. API fails
3. Edit message (add text)
4. API fails again
5. Assert: Input contains edited message, not original
```

**Why this matters:** Prevents frustration of retyping messages on unreliable networks, critical for rural areas with connectivity issues.

