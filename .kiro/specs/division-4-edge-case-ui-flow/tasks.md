# Implementation Plan: Division 4 - Complete Edge Case UI and Conversation Flow Implementation

## Overview

This plan implements Division 4 of the PS 26241 AI-Enabled Career Counselling Platform. Division 4 delivers the **complete frontend UI layer and conversational flow** that transforms backend capabilities from Divisions 1, 2, and 3 into accessible, mobile-first, regional-language interactions addressing **all 10 real-world edge cases**.

**Technology Stack:**
- **Framework**: React 18.2+ with TypeScript 5.0+
- **Build Tool**: Vite 5.0+ for fast development and optimized builds
- **Routing**: React Router DOM 6.20+ for multi-view navigation
- **HTTP Client**: Axios 1.6+ with interceptors for error handling
- **Charts**: Recharts 2.10+ for earnings visualizations
- **Icons**: Lucide React 0.290+ for consistent icons
- **Styling**: CSS Modules for component-scoped styles
- **Browser APIs**: Web Speech API (voice input), SpeechSynthesis API (TTS)
- **State Management**: React Context API + useReducer for session and conversation state
- **Storage**: LocalStorage for conversation caching and offline resilience

**Key Features:**
- Multi-turn conversational chat interface with speaker role management
- 11 specialized edge case UI components (Reality Check Cards, Comparison Matrix, Alternative Pathways, Earnings Charts, Gender Context, NSQF Ladder, etc.)
- Regional language support (Hindi/Marathi) via Sarvam AI integration
- Voice input and text-to-speech for low-literacy users
- Mobile-first responsive design with 48px touch targets
- Offline resilience with LocalStorage caching
- WCAG 2.1 Level AA accessibility compliance
- Family Decision Summary export for offline discussion
- Escalation handling with counsellor handoff UI

**Core Responsibilities:**
- **Multi-Turn Chat**: Conversational UI with history, concern tracking, speaker awareness
- **Edge Case UI Components**: Specialized components for all 10 edge cases
- **API Integration**: Complete integration with Division 3 Counselling Orchestrator
- **Mobile Optimization**: Touch-optimized, single-column layouts, lazy loading
- **Regional Language**: Translation and TTS integration
- **Accessibility**: Screen reader support, keyboard navigation, semantic HTML

## Tasks

- [ ] 1. Project setup and infrastructure
  - [ ] 1.1 Initialize React + Vite + TypeScript project
    - Create project: `npm create vite@latest frontend -- --template react-ts`
    - Install dependencies: react, react-dom, react-router-dom, axios, recharts, lucide-react
    - Configure Vite for development and production builds
    - Set up absolute imports with `@/` path alias
    - _Requirements: 17.1_

  - [ ] 1.2 Configure Axios API client with interceptors
    - Create `src/services/api.ts` with Axios instance
    - Base URL from environment variable: `VITE_API_BASE_URL`
    - Request interceptor: Add session_id to headers if available
    - Response interceptor: Handle 404, 422, 503, 500, timeout errors
    - Retry logic: 3 attempts for network errors with exponential backoff
    - Timeout: 30 seconds for POST /api/counselling/message
    - _Requirements: 19.1, 19.2, 19.6, 19.7_

  - [ ] 1.3 Create TypeScript interfaces for all data models
    - Create `src/types/index.ts` with interfaces: SessionContext, FamilyContext, Message, Concern, ConcernState, Evidence, RealityCheck, GenderContext, EscalationData, CounsellorBrief, CounsellingResponse
    - Match API contract schemas exactly
    - Export all interfaces for reuse across components
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 1.4 Configure React Router with route definitions
    - Create routes: / (Landing), /setup (Family Context), /chat/:sessionId (Counselling Chat), /counsellor (Counsellor Dashboard), /admin (Admin Analytics)
    - Set up protected routes for counsellor and admin dashboards
    - Configure 404 fallback route
    - _Requirements: 1.1_

  - [ ] 1.5 Set up LocalStorage caching utilities
    - Create `src/utils/cache.ts` with functions: cacheConversation, loadCachedConversation, cacheUnsent Message, getCachedUnsentMessage
    - Cache expiry: 24 hours
    - Handle LocalStorage quota exceeded errors gracefully
    - _Requirements: 19.4, 19.8_

- [ ] 2. Session creation and family context setup
  - [ ] 2.1 Create Landing Page with language selector
    - Component: `src/pages/LandingPage.tsx`
    - Display platform title and brief description
    - Language selector: English, Hindi (हिंदी), Marathi (मराठी)
    - "Start Counselling" button navigating to /setup
    - _Requirements: 18.1_

  - [ ] 2.2 Create Family Context Setup form
    - Component: `src/pages/FamilyContextSetup.tsx`
    - Form fields: district (select), state (select), learner_education (select), income_bracket (select), trades_of_interest (multi-select checkboxes), speakers_present (checkboxes: learner/parent/guardian), preferred_language (auto-set from landing)
    - Validation: All fields required except speakers_present (at least 1 required)
    - On submit: Call POST /api/session, navigate to /chat/:sessionId
    - _Requirements: 1.1, 1.2_

  - [ ]* 2.3 Write unit test for session creation flow
    - Test form validation: Ensure required fields are enforced
    - Test API integration: Mock POST /api/session response
    - Test navigation: Verify redirect to /chat/:sessionId on success

- [ ] 3. Core chat interface foundation
  - [ ] 3.1 Create Chat Interface orchestrator component
    - Component: `src/pages/CounsellingChatPage.tsx`
    - Load session on mount: Call GET /api/session/:id
    - Fallback to LocalStorage if API fails (offline mode)
    - Initialize conversation state: messages, concernState, escalated, currentSpeaker
    - Use useReducer for state management with chatReducer
    - _Requirements: 1.10, 13.1, 13.2, 19.4_

  - [ ] 3.2 Create SessionProvider context for global session state
    - Context: `src/contexts/SessionContext.tsx`
    - Provide: sessionId, familyContext, updateFamilyContext
    - Use throughout app for accessing session data
    - _Requirements: 1.1, 1.2_

  - [ ] 3.3 Create Chat Header component
    - Component: `src/components/chat/ChatHeader.tsx`
    - Display family context summary: district, trades, speakers present
    - Connection status indicator: 🟢 Connected, 🟡 Slow, 🔴 Offline
    - Update connection status based on API response times and errors
    - _Requirements: 19.5_

  - [ ] 3.4 Create Chat Window with message history rendering
    - Component: `src/components/chat/ChatWindow.tsx`
    - Display last 20 messages with auto-scroll to bottom
    - Lazy load messages: Only render visible messages + 5 above/below scroll position
    - Message bubbles: User (right-aligned) vs Assistant (left-aligned)
    - Display loading spinner during API calls
    - Display error message with retry button on API failure
    - _Requirements: 1.6, 1.7, 13.3, 19.1, 19.2_

  - [ ] 3.5 Create Message Bubble component
    - Component: `src/components/chat/MessageBubble.tsx`
    - Props: message (Message object), showSpeakerLabel (boolean)
    - Display speaker role label: "You as Parent", "You as Learner"
    - Display timestamp in relative format: "2 minutes ago"
    - Display message text with word wrap
    - Style differentiation: User (blue background), Assistant (grey background)
    - _Requirements: 2.7, 2.8_

  - [ ]* 3.6 Write unit test for Chat Interface state management
    - Test message appending: User sends message → optimistic UI update → API response adds assistant message
    - Test LocalStorage caching: Verify conversation cached after each API response
    - Test offline mode: Verify cached conversation loads when API fails

- [ ] 4. Checkpoint - Verify core chat foundation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Message sending and API integration
  - [ ] 5.1 Create Chat Input Area component
    - Component: `src/components/chat/ChatInputArea.tsx`
    - Auto-expanding textarea: Min height 60px, max 200px
    - Character counter: Show when approaching reasonable limit (500 chars)
    - Send button: Disabled when textarea empty or loading
    - On Enter key: Send message (Shift+Enter for newline)
    - _Requirements: 1.1, 17.7_

  - [ ] 5.2 Implement sendMessage function with optimistic UI
    - In ChatInterface component
    - Optimistic update: Display user message immediately
    - Cache unsent message in LocalStorage before API call
    - Call POST /api/counselling/message with session_id, speaker, message, language
    - On success: Add assistant message, update concern_state, clear unsent cache
    - On error: Display error message, preserve unsent message in input field
    - _Requirements: 1.1, 1.2, 1.3, 19.2, 19.3, 19.8, 19.10_

  - [ ] 5.3 Create counselling service module
    - Service: `src/services/counsellingService.ts`
    - Function: sendMessage(sessionId, speaker, message, language): Promise<CounsellingResponse>
    - Function: getSession(sessionId): Promise<SessionContext>
    - Function: getConcernState(sessionId): Promise<{concernState: ConcernState}>
    - Function: getEvidenceHistory(sessionId): Promise<{evidence: Evidence[]}>
    - Handle API errors and transform responses to TypeScript interfaces
    - _Requirements: 1.1, 1.2, 1.10_

  - [ ]* 5.4 Write integration test for message sending flow
    - Mock POST /api/counselling/message response
    - Send message → verify optimistic UI → verify API called with correct payload → verify assistant message rendered

- [ ] 6. Speaker role selection and awareness
  - [ ] 6.1 Create Speaker Selector component
    - Component: `src/components/chat/SpeakerSelector.tsx`
    - Radio buttons: "I am the Learner", "I am the Parent/Guardian"
    - Only show options matching speakers_present from family context
    - Display avatar icons with color coding: learner (blue 🎓), parent (green 👨‍👩‍👧), guardian (purple 👴)
    - Persist selected speaker across messages
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 6.2 Implement speaker-aware input placeholders
    - In ChatInputArea component
    - Learner placeholder: "What would you like to know about this career?"
    - Parent placeholder: "Ask about placement rates, earnings, or job security"
    - Guardian placeholder: "I would like to understand the verified outcomes"
    - Update placeholder dynamically when speaker changes
    - _Requirements: 2.4, 2.5, 2.6_

  - [ ] 6.3 Add speaker role display to message bubbles
    - In MessageBubble component
    - Display speaker label above user messages: "You as Parent"
    - Use color-coded label background matching speaker avatar color
    - _Requirements: 2.7_

  - [ ]* 6.4 Write unit test for speaker role consistency
    - **Property 3: Speaker Role Consistency**
    - **Validates: Requirements 2.1, 2.8, 2.9, 2.10**
    - Test: Select speaker='parent' → send 3 messages → verify all API calls have speaker='parent'
    - Test: Change speaker to 'learner' → send message → verify API call has speaker='learner'

- [ ] 7. Concern status tracking and display
  - [ ] 7.1 Create Concern Status Indicator component
    - Component: `src/components/chat/ConcernStatusIndicator.tsx`
    - Props: category (string), status ('not_raised' | 'open' | 'partially_resolved' | 'resolved')
    - Color coding: ⚪ Not Raised (grey), 🔴 Open (red), 🟡 Partially Resolved (yellow), 🟢 Resolved (green)
    - Display category name in English or translated based on preferred language
    - ARIA label: "Employment concern: resolved"
    - _Requirements: 1.8, 13.2, 13.3, 18.6, 20.4_

  - [ ] 7.2 Create Concern Status Panel component
    - Component: `src/components/chat/ConcernStatusPanel.tsx`
    - Display 7 concern categories: income, employment, safety, social_perception, education_progression, gender_family, information_gap
    - Render ConcernStatusIndicator for each category
    - Update status based on concern_state from API responses
    - Animate status changes (brief highlight on transition)
    - _Requirements: 13.2, 13.4, 13.7_

  - [ ] 7.3 Implement concern state update logic
    - In ChatInterface component
    - Update concernState in reducer on each POST /api/counselling/message response
    - Trigger animation on status change: open → partially_resolved → resolved
    - _Requirements: 1.8, 13.4, 13.7_

  - [ ]* 7.4 Write unit test for concern status display
    - **Property 4: Concern Status Monotonic Progress**
    - **Validates: Requirements 13.4, 13.7**
    - Test progression: not_raised → open → partially_resolved → resolved
    - Test UI colors match status at each stage
    - Test status does not regress (resolved → open) without new user question

- [ ] 8. Evidence Card component (core data display)
  - [ ] 8.1 Create Evidence Card component
    - Component: `src/components/chat/EvidenceCard.tsx`
    - Props: evidence (Evidence object), compact (boolean for mobile)
    - Display sections: Trade & Location, Placement Rate, Monthly Earnings, NSQF Level, Career Progression
    - Format currency: ₹18,000 - ₹26,000 (Indian rupee with thousand separators)
    - Display progression_path as ordered list with visual styling
    - Display data_source and data_period citation prominently in footer
    - _Requirements: 1.5, 4.7, 4.8, 4.9, 17.5, 20.5_

  - [ ] 8.2 Add reality check section to Evidence Card
    - Display reality_check data if available: physical_demand, typical_day, trainee_quote
    - Use icons: 🏗️ Physical Demand, ⏰ Typical Day, 💬 Trainee Quote
    - Display trainee_quote as stylized blockquote with verified source citation
    - Only show in full mode (not compact)
    - _Requirements: 3.1, 3.2, 3.3, 4.4_

  - [ ] 8.3 Add gender context section to Evidence Card
    - Display gender_context data if available: female_enrollment_pct, safety_infrastructure
    - Format: "Female Enrollment: 28%" and "Safety: Separate washrooms, female instructors"
    - Only show in full mode (not compact)
    - _Requirements: 11.2, 11.3_

  - [ ]* 8.4 Write unit test for Evidence Card completeness
    - **Property 2: Evidence Display Completeness**
    - **Validates: Requirements 1.5, 4.7, 4.8**
    - Test: Given evidence array with N items → render N Evidence Cards
    - Test: Each Evidence Card displays ALL required fields (trade, district, placement_rate, earnings, data_source, data_period)

  - [ ]* 8.5 Write unit test for evidence provenance display
    - **Property 6: Evidence Card Data Provenance**
    - **Validates: Requirements 1.5, 4.9**
    - Test: Every Evidence Card displays data_source and data_period
    - Test: Evidence without data_source is not rendered (defensive)

- [ ] 9. Edge Case 1 & 2: Reality Check Card component
  - [ ] 9.1 Create Reality Check Card component
    - Component: `src/components/chat/RealityCheckCard.tsx`
    - Props: evidence (Evidence), edgeCase ('herd_mentality' | 'viral_fascination'), onReflectionPrompt (callback)
    - Display physical_demand with color coding: green (low), yellow (moderate), red (high)
    - Parse typical_day into timeline entries with time and activity
    - Display trainee_quote as blockquote with verified source
    - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3_

  - [ ] 9.2 Add reflection prompts to Reality Check Card
    - For herd_mentality: "After seeing what the actual work involves, does this match what you enjoy doing?"
    - Include "I want to explore other options" button triggering onReflectionPrompt callback
    - For viral_fascination: Display note: "Social media often shows the exciting parts. This is the full picture of daily work."
    - _Requirements: 3.7, 4.8_

  - [ ] 9.3 Integrate Reality Check Card into conversation flow
    - In ChatWindow component
    - Display Reality Check Card when evidence includes reality_check data AND concern category is social_perception or information_gap
    - Position card inline with AI response message
    - _Requirements: 3.1, 4.1_

  - [ ]* 9.4 Write unit test for Reality Check Card rendering
    - Test typical_day timeline parsing: "8:30 AM tool inventory..." → { time: "8:30 AM", activity: "tool inventory..." }
    - Test physical_demand color coding: "High" → red, "Moderate" → yellow, "Low" → green
    - Test reflection prompt display for herd_mentality edge case

- [ ] 10. Edge Case 1 & 5: Alternative Pathway Suggester component
  - [ ] 10.1 Create Alternative Pathway Suggester component
    - Component: `src/components/chat/AlternativePathwaySuggester.tsx`
    - Props: currentTrade (string), alternatives (array of { trade, rationale, evidence }), onCompareClick (callback), onSelectAlternative (callback)
    - Display 2-3 alternative trade cards with: trade name, rationale, quick stats (placement rate, earnings)
    - "Learn More" button for each alternative calling onSelectAlternative
    - "Compare All Trades Side-by-Side" button calling onCompareClick
    - _Requirements: 3.3, 3.4, 3.5, 7.1, 7.2, 7.3_

  - [ ] 10.2 Integrate Alternative Pathway Suggester into conversation flow
    - In ChatWindow component
    - Display when AI response includes alternatives data (from orchestrator)
    - Position after Reality Check Card if both present
    - _Requirements: 3.1, 7.1_

  - [ ]* 10.3 Write unit test for alternative pathways uniqueness
    - **Property 9: Alternative Pathways Uniqueness**
    - **Validates: Requirements 3.3, 7.2**
    - Test: Suggested trades SHALL NOT include currentTrade
    - Test: No duplicate trade names in alternatives list
    - Test: Set(alternatives).length === alternatives.length

- [ ] 11. Edge Case 1, 5, 7, 8: Comparison Matrix component
  - [ ] 11.1 Create Comparison Matrix component
    - Component: `src/components/chat/ComparisonMatrix.tsx`
    - Props: trades (Evidence[]), highlightTrade (string), onTradeSelect (callback)
    - Table columns: Trade, Location, Placement Rate, Earnings, Training Duration, NSQF Level, Physical Demand
    - Comparative indicators: green (higher than average), yellow (average), no red to avoid negative framing
    - Calculate relative rankings: placement rates, avg earnings
    - _Requirements: 3.6, 5.3, 5.4, 5.5, 5.6, 7.3, 7.4, 8.8, 10.3, 10.4_

  - [ ] 11.2 Add responsive behavior for mobile Comparison Matrix
    - Horizontal scrolling on mobile (<768px width)
    - Sticky first column (trade names) during scroll
    - Compress column widths for mobile readability
    - _Requirements: 17.6_

  - [ ] 11.3 Add data provenance to Comparison Matrix
    - Display "Source: {data_source} ({data_period})" below table
    - All trades in comparison should cite same data source for credibility
    - _Requirements: 5.6, 7.6_

  - [ ] 11.4 Integrate Comparison Matrix into conversation flow
    - In ChatWindow component
    - Display when "Compare All" button clicked from Alternative Pathway Suggester
    - Or display when AI response includes comparison_data (from orchestrator)
    - _Requirements: 3.6, 7.3, 10.3_

  - [ ]* 11.5 Write integration test for Comparison Matrix responsive behavior
    - Test horizontal scrolling on mobile viewport (375px width)
    - Test sticky first column remains visible during scroll
    - Test touch target sizes for table rows >= 48px height

- [ ] 12. Checkpoint - Verify edge case components rendering
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Edge Case 3 & 7: Earnings Progression Chart component
  - [ ] 13.1 Create Earnings Progression Chart component with Recharts
    - Component: `src/components/chat/EarningsProgressionChart.tsx`
    - Props: evidence (Evidence), showROI (boolean), trainingCost (number | undefined)
    - Use Recharts BarChart to visualize earnings progression
    - Data points: Entry Level (0-2 years), Intermediate stages from progression_path, Experienced (5+ years)
    - Estimate intermediate earnings: entry * (1 + stage_index * 0.3)
    - Format Y-axis: ₹18k format for thousands
    - _Requirements: 5.1, 5.2, 5.3, 9.1, 9.2_

  - [ ] 13.2 Add earnings breakdown list to chart component
    - Display earnings range for each progression stage
    - Format: "Entry Level (0-2 years): ₹18,000 - ₹26,000 per month"
    - Include disclaimer: "These are verified entry-level figures. Earnings growth is estimated based on typical career progression."
    - _Requirements: 5.1, 5.8, 5.9, 5.10_

  - [ ] 13.3 Add Investment ROI Calculator section
    - Display if showROI=true and trainingCost available
    - Calculate payback period: Math.ceil(trainingCost / earnings_min) months
    - Display: Training Cost, First Year Earnings (earnings_min * 12), Payback Period
    - Highlight payback period prominently
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.7, 9.10_

  - [ ] 13.4 Add geographic salary variations if multiple districts available
    - If evidence array includes multiple districts, show comparison
    - Format: "Nashik: ₹18k-₹26k, Pune: ₹22k-₹35k"
    - _Requirements: 5.4_

  - [ ] 13.5 Integrate Earnings Progression Chart into conversation flow
    - In ChatWindow component
    - Display when concern category is 'income' (starting_salary, long_term_earning, return_on_training intent)
    - Position inline with AI response
    - _Requirements: 5.1, 9.1_

  - [ ]* 13.6 Write unit test for earnings progression data construction
    - Test: Given evidence with earnings_min=18000, earnings_max=26000, progression_path=["Helper", "Technician", "Senior"]
    - Verify chart data points include: Entry Level, Technician, Senior, Experienced
    - Verify earnings increase monotonically across stages

- [ ] 14. Edge Case 4: Family-Friendly Explainer component
  - [ ] 14.1 Create Family-Friendly Explainer component
    - Component: `src/components/chat/FamilyFriendlyExplainer.tsx`
    - Props: evidence (Evidence), concernIntent (string)
    - Translate technical curriculum to everyday language
    - Display "Who Hires?" section: List employer types
    - Display training duration with calendar icon: 📅 6 months ITI
    - Display eligibility requirements: ✅ Class 10 pass, ✅ 15-40 years age
    - _Requirements: 6.2, 6.3, 6.4, 6.5_

  - [ ] 14.2 Add discussion prompts for families
    - Display "Questions to discuss as a family:" section
    - Generate prompts based on concern intent detected
    - Example prompts: "Does the training duration fit our timeline?", "Are jobs available in our district?", "Does the earning potential meet our needs?"
    - _Requirements: 6.8_

  - [ ] 14.3 Add "Share This Info" button to Explainer
    - Button triggers Family Decision Summary generation
    - Call handleDownloadSummary function (to be implemented in later task)
    - _Requirements: 6.6_

  - [ ] 14.4 Integrate Family-Friendly Explainer into conversation flow
    - In ChatWindow component
    - Display when concern category is 'information_gap' (course_content, duration, eligibility intent)
    - _Requirements: 6.1, 6.9_

- [ ] 15. Edge Case 6: Career Dignity Reframing component
  - [ ] 15.1 Create Career Dignity Reframing component
    - Component: `src/components/chat/CareerDignityReframing.tsx`
    - Props: evidence (Evidence)
    - Display progression_path as upward career ladder visualization
    - Use professional titles: "Solar Installation Specialist" → "Renewable Energy Supervisor"
    - Display NSQF level equivalence: "NSQF Level 4 ITI = Class 12 academic qualification"
    - Include modern technology adoption section (trade-specific)
    - _Requirements: 8.2, 8.3, 8.4, 8.5_

  - [ ] 15.2 Add earnings comparison to Career Dignity Reframing
    - If comparison data available: "ITI Solar Technician earns ₹18k-₹28k entry level vs BA graduate ₹12k-₹18k entry level"
    - Use respectful framing: "Your concerns about your child's future are completely valid. Let's look at verified career outcomes."
    - _Requirements: 8.6, 8.7, 8.8_

  - [ ] 15.3 Add trainee success stories section
    - Display trainee_quote from reality_check if available
    - Frame as career satisfaction testimonial
    - _Requirements: 8.9_

  - [ ] 15.4 Integrate Career Dignity Reframing into conversation flow
    - In ChatWindow component
    - Display when concern category is 'social_perception' (status_of_trade, family_acceptance intent)
    - _Requirements: 8.1_

- [ ] 16. Edge Case 8: Trade vs Desk Job Comparison component
  - [ ] 16.1 Create Trade vs Desk Comparison component
    - Component: `src/components/chat/TradeVsDeskComparison.tsx`
    - Props: tradeEvidence (Evidence), deskJobData (if available from backend)
    - Compare: starting salary, placement rate, job availability, career progression
    - Present trade advantages fairly: "Technical trades often have higher entry-level placement rates (78% vs 54% for BA/BCom)"
    - Acknowledge trade-offs without bias: "Technical work is more physical but has faster earning progression"
    - _Requirements: 10.2, 10.3, 10.4_

  - [ ] 16.2 Add career progression comparison visualization
    - Display both paths: "CNC Operator → Programmer → Production Supervisor" vs "Office Assistant → Executive → Manager"
    - Use visual ladder or timeline
    - _Requirements: 10.5, 10.10_

  - [ ] 16.3 Integrate Trade vs Desk Comparison into conversation flow
    - In ChatWindow component
    - Display when concern category is 'employment' (job_security intent) or 'social_perception' (salary_comparison)
    - _Requirements: 10.1_

- [ ] 17. Edge Case 9: Gender Context Presenter component
  - [ ] 17.1 Create Gender Context Presenter component
    - Component: `src/components/chat/GenderContextPresenter.tsx`
    - Props: evidence (Evidence)
    - Display female_enrollment_pct prominently: "Currently 28% of trainees in this program are women"
    - Display safety_infrastructure: "Separate women's washrooms, female instructors, hostel accommodation, safety protocols"
    - _Requirements: 11.2, 11.3_

  - [ ] 17.2 Add contextual framing based on female enrollment percentage
    - If female_enrollment_pct < 20%: "Female enrollment is currently lower (15%), which means this trade has historically had fewer women. However, verified placement data shows women graduates have 82% placement rate."
    - If female_enrollment_pct >= 20%: "Good female participation (28%) with demonstrated successful outcomes for women trainees"
    - Use respectful tone: "Your daughter's safety is paramount. Here's what the data shows:"
    - _Requirements: 11.4, 11.5, 11.8_

  - [ ] 17.3 Add female trainee success stories section
    - Display female trainee quotes from trainee_quote field if available
    - Display "Success Stories" section with verified outcomes
    - _Requirements: 11.6, 11.10_

  - [ ] 17.4 Integrate Gender Context Presenter into conversation flow
    - In ChatWindow component
    - Display when concern category is 'gender_family' (suitability_for_daughter intent)
    - _Requirements: 11.1_

- [ ] 18. Edge Case 10: NSQF Ladder Visualizer component
  - [ ] 18.1 Create NSQF Ladder Visualizer component
    - Component: `src/components/chat/NSQFLadderVisualizer.tsx`
    - Props: evidence (Evidence)
    - Display NSQF levels as vertical ladder: Level 4 ITI → Level 5 Advanced ITI → Level 6 Diploma → Level 7 B.Voc → Level 8 Master's
    - Highlight current trade's NSQF level from evidence.nsqf_level
    - Display lateral entry points: "After Level 4 ITI, you can enter Polytechnic Diploma (Level 6) directly"
    - _Requirements: 12.2, 12.3, 12.4_

  - [ ] 18.2 Add NSQF equivalence explanation
    - Display: "NSQF Level 4 ITI = Class 12 academic qualification for employment and further study"
    - Address "dead-end" misconception: "ITI is not a dead-end. Verified pathways exist to Diploma, B.Voc, and university degrees through NSQF framework."
    - _Requirements: 12.5, 12.7_

  - [ ] 18.3 Add progression_path integration to NSQF Ladder
    - Display on-the-job advancement alongside academic advancement
    - Show both paths: career progression at work AND higher education options
    - Include part-time study options: "You can work as a technician while pursuing evening Diploma classes"
    - _Requirements: 12.6, 12.9, 12.10_

  - [ ] 18.4 Integrate NSQF Ladder Visualizer into conversation flow
    - In ChatWindow component
    - Display when concern category is 'education_progression' (nsqf_levels, further_education, degree_equivalence intent)
    - _Requirements: 12.1_

- [ ] 19. Checkpoint - Verify all edge case components integrated
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Escalation handling and counsellor handoff UI
  - [ ] 20.1 Create Escalation Banner component
    - Component: `src/components/chat/EscalationBanner.tsx`
    - Props: escalationId (string), counsellorBrief (CounsellorBrief), triggerReason (string)
    - Display escalation_id prominently: "Case ID: ESC001"
    - Map trigger reasons to user-friendly explanations (see requirements 15.4)
    - Display next steps: "A counsellor will review your case and contact you within 24-48 hours"
    - Display information already provided list
    - _Requirements: 15.2, 15.3, 15.4, 15.5, 15.7_

  - [ ] 20.2 Add sticky positioning to Escalation Banner
    - Banner remains visible at top of chat during scrolling
    - Use CSS position: sticky with z-index to overlay content
    - _Requirements: 15.10_

  - [ ] 20.3 Add "Request Human Counsellor" button
    - Display button prominently in Chat Sidebar
    - On click: Send message with explicit escalation trigger phrase to orchestrator
    - Or call dedicated escalation endpoint if available
    - _Requirements: 15.8, 15.9_

  - [ ] 20.4 Integrate Escalation Banner into Chat Interface
    - In ChatInterface component
    - Display when escalated=true from API response
    - Persist escalation state across page refreshes (from session data)
    - _Requirements: 1.9, 15.1_

  - [ ]* 20.5 Write unit test for Escalation Banner visibility
    - **Property 7: Escalation Banner Visibility**
    - **Validates: Requirements 15.1, 15.10**
    - Test: When escalated=true → banner visible
    - Test: Banner persists after scrolling and sending new messages
    - Test: Banner visible after page refresh (loaded from session)

- [ ] 21. Voice input and text-to-speech for low-literacy users
  - [ ] 21.1 Create Voice Input Button component with Web Speech API
    - Component: `src/components/chat/VoiceInputButton.tsx`
    - Use browser SpeechRecognition API
    - Language detection: Map preferred_language to speech API locale (mr-IN, hi-IN, en-IN)
    - Display pulsing animation while recording
    - On transcript complete: Populate input field for user review before sending
    - Handle browser compatibility: Display error if API not supported
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

  - [ ] 21.2 Integrate Voice Input Button into Chat Input Area
    - Position prominently for mobile one-thumb access
    - Icon: 🎤 microphone
    - Tooltip: "Speak your question"
    - _Requirements: 17.8_

  - [ ] 21.3 Create Text-to-Speech Button component with SpeechSynthesis API
    - Component: `src/components/chat/TextToSpeechButton.tsx`
    - Props: text (string), language (string)
    - Use browser SpeechSynthesis API
    - Display play/pause controls during playback
    - Language selection: Use appropriate voice based on preferred_language
    - Playback speed controls: 0.8x (slower), 1x (normal), 1.2x (faster)
    - _Requirements: 14.6, 14.7, 14.8, 14.9, 14.10_

  - [ ] 21.4 Integrate TTS Button next to each AI response message
    - In MessageBubble component
    - Display button next to assistant messages only
    - Icon: 🔊 speaker
    - Tooltip: "Listen to this response"
    - _Requirements: 14.6_

  - [ ]* 21.5 Write unit test for voice input flow
    - Mock SpeechRecognition API
    - Test: Click voice button → recording starts → transcript received → input field populated
    - Test: Browser compatibility error handling

- [ ] 22. Regional language translation integration
  - [ ] 22.1 Create translation utility functions
    - Utility: `src/utils/translation.ts`
    - Function: translateStaticUI(key: string, language: string): string
    - Maintain translation dictionary for static UI text: buttons, labels, placeholders, category names
    - Fallback to English if translation unavailable
    - _Requirements: 18.1, 18.5, 18.6, 18.9_

  - [ ] 22.2 Apply translations to all static UI text
    - Translate button labels: "Send" → "भेजें" (Hindi), "पाठवा" (Marathi)
    - Translate placeholders (use speaker-aware prompts)
    - Translate concern category names in Concern Status Indicator
    - Translate Evidence Card field labels
    - _Requirements: 18.1, 18.5, 18.6_

  - [ ] 22.3 Display response_translated from API in message bubbles
    - In MessageBubble component
    - Use response_translated field from CounsellingResponse
    - Display English fallback warning if translation fails
    - _Requirements: 18.3, 18.4_

  - [ ] 22.4 Translate Family Decision Summary content
    - Apply translations to section headers, discussion prompts, field labels
    - Use preferred_language from session context
    - _Requirements: 18.7_

  - [ ]* 22.5 Write unit test for translation idempotence
    - **Property 5: Translation Idempotence**
    - **Validates: Requirements 18.3**
    - Test: Display response_translated → re-render 10x → same text displayed
    - Test: No redundant translation API calls on re-render

- [ ] 23. Family Decision Summary export and sharing
  - [ ] 23.1 Create Family Decision Summary component
    - Component: `src/components/chat/FamilyDecisionSummary.tsx`
    - Props: session (SessionContext), concernState (ConcernState), evidenceShown (Evidence[])
    - Display sections: Session Info, Trades Explored, Concerns Addressed, Key Evidence, Discussion Questions
    - Format: Mobile-friendly layout for PDF/image generation
    - _Requirements: 16.3, 16.4, 16.5, 16.6, 16.7_

  - [ ] 23.2 Add "Download Summary" button to Chat Sidebar
    - In ChatSidebar component
    - On click: Generate Family Decision Summary
    - Options: Download as PDF (using jsPDF library) or shareable image (using html2canvas)
    - _Requirements: 16.1, 16.8_

  - [ ] 23.3 Add platform branding to summary
    - Include footer: "Generated by Ministry of Skill Development AI Career Counselling Platform"
    - Include timestamp and session_id for reference
    - _Requirements: 16.9_

  - [ ] 23.4 Apply regional language to summary content
    - Translate all text based on preferred_language
    - Use translation utility from previous task
    - _Requirements: 16.10_

- [ ] 24. Mobile-first responsive design implementation
  - [ ] 24.1 Create responsive CSS with mobile-first breakpoints
    - File: `src/styles/responsive.css`
    - Breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)
    - Mobile: Single column layout, collapsible sidebar, bottom sheet for concern status
    - Tablet: Sidebar visible, 2-column evidence cards
    - Desktop: Wide sidebar, multi-column layouts
    - _Requirements: 17.1, 17.4_

  - [ ] 24.2 Implement touch target sizing for mobile
    - All buttons, radio buttons, checkboxes: Minimum 48x48px touch area
    - Include label area in touch target for radio/checkbox inputs
    - Add padding to increase touch area if needed
    - _Requirements: 17.2_

  - [ ] 24.3 Set minimum font sizes and auto-expand textarea
    - Body text: 16px minimum (no zoom requirement)
    - Headings: 18-24px
    - Textarea: Auto-expand from 60px to 200px as user types
    - _Requirements: 17.3, 17.7_

  - [ ] 24.4 Implement lazy loading for conversation history
    - Load only visible messages + 5 above/below scroll position
    - Use IntersectionObserver API for scroll detection
    - Load more messages when scrolling near top of history
    - _Requirements: 17.10_

  - [ ] 24.5 Configure system fonts supporting Devanagari script
    - CSS: font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans Devanagari', sans-serif
    - No font downloads required (use system fonts)
    - _Requirements: 17.9_

  - [ ]* 24.6 Write integration test for mobile touch target sizes
    - **Property 8: Mobile Touch Target Size**
    - **Validates: Requirements 17.2**
    - Test: Set viewport to 375px width → measure all interactive elements → verify >= 48x48px

- [ ] 25. Checkpoint - Verify mobile responsiveness and accessibility
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 26. Performance and error handling for slow networks
  - [ ] 26.1 Implement loading states and timeout handling
    - Display loading spinner during POST /api/counselling/message
    - Timeout: 30 seconds
    - On timeout: Display retry button, preserve unsent message
    - _Requirements: 19.1, 19.2, 19.3_

  - [ ] 26.2 Implement LocalStorage caching for offline resilience
    - Cache conversation after each successful API response
    - Cache expiry: 24 hours
    - On mount: Load cached conversation if API fails
    - Display offline indicator when using cached data
    - _Requirements: 19.4, 19.5_

  - [ ] 26.3 Implement optimistic UI updates
    - Display user message immediately before API call
    - Show "Sending..." status until API confirms
    - Rollback on API failure (or preserve with error indicator)
    - _Requirements: 19.8_

  - [ ] 26.4 Add connection status indicator
    - Component: `src/components/chat/ConnectionStatusIndicator.tsx`
    - States: 🟢 Connected, 🟡 Slow Connection (response > 3s), 🔴 Offline
    - Update based on API response times and errors
    - _Requirements: 19.5_

  - [ ] 26.5 Implement error handling for specific API failures
    - 404 Session Not Found: Redirect to /setup with warning message
    - 503 Service Unavailable: Display "AI temporarily unavailable" + manual escalation button
    - Network error: Display connection issue message with retry
    - _Requirements: 19.6, 19.7_

  - [ ]* 26.6 Write unit test for error recovery message preservation
    - **Property 10: Error Recovery Message Preservation**
    - **Validates: Requirements 19.2, 19.3, 19.10**
    - Test: Type message → API fails → input field still contains message
    - Test: Retry sends same message without retyping

- [ ] 27. Accessibility compliance (WCAG 2.1 Level AA)
  - [ ] 27.1 Implement semantic HTML structure
    - Use `<main>`, `<nav>`, `<section>`, `<article>`, `<header>`, `<footer>`
    - Proper heading hierarchy: h1 (page title), h2 (sections), h3 (subsections)
    - _Requirements: 20.1, 20.5_

  - [ ] 27.2 Add ARIA labels to all interactive elements
    - Buttons: aria-label="Send message button"
    - Inputs: aria-label="Type your message" or associated <label>
    - Status indicators: aria-label="Employment concern: resolved"
    - _Requirements: 20.2, 20.4, 20.7_

  - [ ] 27.3 Implement aria-live region for message announcements
    - Chat message container: aria-live="polite"
    - Screen readers announce new messages automatically
    - _Requirements: 20.3_

  - [ ] 27.4 Add descriptive alt text to images and icons
    - Evidence cards: alt="Career progression ladder showing 5 stages"
    - Icons: Use aria-hidden="true" for decorative icons, aria-label for functional icons
    - _Requirements: 20.6_

  - [ ] 27.5 Implement keyboard navigation
    - Tab order: Header → Chat History → Input Area → Sidebar
    - Enter key: Send message
    - Escape key: Close modals
    - Arrow keys: Navigate concern status indicators
    - _Requirements: 20.8_

  - [ ] 27.6 Ensure color contrast ratios meet WCAG AA
    - Body text: 7:1 contrast (AAA)
    - Headings: 4.5:1 contrast (AA)
    - Status indicators: Include text/icons alongside colors (not color-only)
    - Focus indicators: 2px outline with 3:1 contrast
    - _Requirements: 20.9, 20.10_

  - [ ]* 27.7 Write accessibility audit test checklist
    - Test with screen readers (NVDA, JAWS, VoiceOver)
    - Test keyboard navigation completeness
    - Test color contrast with automated tools (axe, Lighthouse)
    - Test touch target sizes on mobile

- [ ] 28. Conversation Sidebar and History navigation
  - [ ] 28.1 Create Chat Sidebar component
    - Component: `src/components/chat/ChatSidebar.tsx`
    - Sections: Conversation History List, Concern Status Summary, Download Summary Button, Request Counsellor Button
    - Collapsible on mobile: Bottom sheet or hamburger menu
    - _Requirements: 13.5, 16.1, 17.4_

  - [ ] 28.2 Create Conversation History List
    - Display all concerns raised with timestamps
    - Clickable to scroll to relevant message in chat history
    - Show current status for each concern (color-coded badge)
    - _Requirements: 13.5_

  - [ ] 28.3 Add "Start New Session" button
    - Button at top of sidebar
    - On click: Navigate to /setup to create new session
    - Confirm dialog: "Are you sure? Current conversation will be saved but you'll start fresh."
    - _Requirements: 13.10_

- [ ] 29. Counsellor Dashboard (basic view for Division 1 integration)
  - [ ] 29.1 Create Counsellor Dashboard page
    - Page: `src/pages/CounsellorDashboard.tsx`
    - Call GET /api/counsellor/cases to fetch escalated cases
    - Display case queue with tabs: Pending, In Progress, Resolved
    - _Requirements: Division 1 integration_

  - [ ] 29.2 Create Case Card component
    - Component: `src/components/counsellor/CaseCard.tsx`
    - Display: escalation_id, session_id, triggered_at, primary_concern, district, state, status
    - Click to view full case details in modal
    - _Requirements: Division 1 integration_

  - [ ] 29.3 Create Case Detail Modal with conversation transcript
    - Modal: Display full conversation history from GET /api/session/:id
    - Display counsellor_brief with recommended_action
    - Status update form: PATCH /api/counsellor/cases/:id with status dropdown
    - _Requirements: Division 1 integration_

- [ ] 30. Admin Analytics Dashboard (basic view for Division 5 integration)
  - [ ] 30.1 Create Admin Dashboard page
    - Page: `src/pages/AdminDashboard.tsx`
    - Call GET /api/admin/analytics for summary statistics
    - Display summary cards: Total Sessions, Concerns Resolved, Escalation Rate, AI Resolution Rate
    - _Requirements: Division 5 integration_

  - [ ] 30.2 Create analytics visualization components with Recharts
    - Component: `src/components/admin/AnalyticsCharts.tsx`
    - District Heatmap: Bar chart of resistance rate by district
    - Trade Breakdown: Bar chart of top trades by session count
    - Concern Breakdown: Pie chart of concerns by category
    - Resolution Funnel: Funnel chart of concern progression (raised → open → resolved)
    - _Requirements: Division 5 integration_

  - [ ] 30.3 Add filter controls for analytics
    - Component: `src/components/admin/FilterControls.tsx`
    - Filters: Date range, District, Trade, Concern Category
    - Apply filters to analytics API calls with query parameters
    - _Requirements: Division 5 integration_

- [ ] 31. Integration testing and end-to-end scenarios
  - [ ]* 31.1 Write integration test for complete counselling flow
    - Scenario: Create session → Send 3 messages → Receive evidence → Concern resolved
    - Verify: Conversation history persists across page refresh using LocalStorage

  - [ ]* 31.2 Write integration test for escalation flow
    - Scenario: Send message triggering escalation → Verify Escalation Banner displays
    - Verify: escalation_id and counsellor_brief visible
    - Verify: Manual escalation via "Request Human Counsellor" button

  - [ ]* 31.3 Write integration test for herd mentality edge case flow
    - Scenario: Social_perception concern detected → Reality Check Card displays → Click "Explore alternatives" → Alternative Pathway Suggester → Comparison Matrix
    - Verify: All edge case components render correctly inline with conversation

  - [ ]* 31.4 Write integration test for earnings progression edge case flow
    - Scenario: Income concern detected → Earnings Progression Chart displays → ROI Calculator shows payback period
    - Verify: Chart renders with correct data points and currency formatting

  - [ ]* 31.5 Write integration test for gender context edge case flow
    - Scenario: Gender_family concern detected → Gender Context Presenter displays → Female enrollment and safety info visible
    - Verify: Contextual framing based on female enrollment percentage

  - [ ]* 31.6 Write integration test for NSQF ladder edge case flow
    - Scenario: Education_progression concern detected → NSQF Ladder Visualizer displays → Lateral entry points and equivalence shown
    - Verify: Current trade's NSQF level highlighted in ladder

  - [ ]* 31.7 Write integration test for mobile responsive behavior
    - Test viewport widths: 375px, 768px, 1024px
    - Verify: Sidebar collapses on mobile, touch targets >= 48px, horizontal scrolling on Comparison Matrix

  - [ ]* 31.8 Write integration test for offline resilience
    - Scenario: Load session → Go offline (mock network failure) → Send message → Verify cached conversation loads → Verify retry mechanism works

- [ ] 32. Final checkpoint - End-to-end validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional test-related tasks and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- **No property-based tests** are included because the design document has no "Correctness Properties" section defining universal properties suitable for PBT
- Integration tests validate end-to-end edge case flows and API integration
- Unit tests validate component rendering, state management, and user interactions
- The implementation uses TypeScript/React as specified in the design document (not pseudocode)
- Mobile-first design ensures rural accessibility on slow networks and small screens
- Accessibility compliance (WCAG 2.1 AA) ensures screen reader support and keyboard navigation
- LocalStorage caching provides offline resilience for unreliable connectivity
- Voice input and TTS support low-literacy users
- Regional language support (Hindi/Marathi) via Sarvam AI integration
- Family Decision Summary enables offline family discussion
- All 10 edge cases have dedicated UI components integrated into conversational flow
- Escalation handling provides seamless handoff to human counsellors
- Counsellor and Admin dashboards provide basic integration points for Divisions 1 and 5

