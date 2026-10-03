# Beginner's Guide to the SIH Project: Cautious Eureka

Welcome to the team! This document will help you understand the project from the ground up: the problem we're solving, the solution we're building, the architecture, and the current state of completion.

## 1. Problem Statement
**Problem Statement ID: 26241 - AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education**

In India, vocational education (like ITI programs) often faces social stigma and information gaps. Students and their families struggle to make informed decisions due to:
- **Social Stigma (Log Kya Kahenge):** Parents preferring traditional degrees over vocational skills.
- **Information Vacuum:** Lack of clarity on course fees, duration, and job prospects.
- **Herd Mentality / Proxy Choices:** Choosing a trade just because friends did, or relying on biased advice from a single person.
- **Viral Fascination:** Misunderstanding the physical realities of a job (e.g., CNC machining) based on social media reels.

We need a system that can address these concerns empathetically, using verified data to guide the family to the right decision.

## 2. Our Solution
We are building a multi-turn, multi-speaker conversational AI platform that counsels both the learner and their parents/guardians.

### Why RAG (Retrieval-Augmented Generation)?
We cannot let the AI hallucinate job placement rates, salaries, or safety infrastructure. By using a RAG approach, the AI retrieves **verified, factual outcome data** (like MSDE placement records) and grounds its responses in reality. If data isn't available, the system escalates to a human counsellor instead of making things up.

### Why LLMs (Large Language Models)?
We need the system to understand nuanced, emotional, and context-heavy concerns. An LLM can reframe a parental concern (e.g., "Vocational jobs have no dignity") respectfully, adapt its tone depending on who it's speaking to (learner vs. parent), and handle edge cases like detecting an "echo chamber" or a "guardian veto".

## 3. Architecture & Data Flow
The system is divided into several backend microservices (Divisions):

- **Division 1: Session Service & State Management**
  Tracks the conversation history, who is speaking, what evidence has already been shown, and handles human counsellor escalation queues.
  
- **Division 2: Evidence Repository & RAG Engine**
  The "brain's factual memory". It takes verified data (like a CSV of MSDE outcomes containing placement rates, earnings ranges, physical demands, and female enrollment percentages) and indexes it using `sentence-transformers` and FAISS for semantic search.
  
- **Division 3: Counselling Orchestrator (Intelligence Layer)**
  The core AI logic. It classifies the user's intent, fetches evidence from Division 2, and uses an LLM (Groq / Gemini) to generate a speaker-aware response. It also detects edge cases and triggers escalations based on hardcoded deterministic rules.
  
- **Division 4: Language Service**
  Handles translations and text-to-speech (TTS) using Sarvam AI to ensure the counselling can happen in regional languages (like Hindi and Marathi) respectfully and formally.
  
- **Division 5: Analytics Service**
  Provides cross-session analytics to detect trends (e.g., if a specific region has a sudden surge in a particular concern).

## 4. Current State of Completion

- **Division 1 (Session & State):** Basic schemas and database models are implemented.
- **Division 2 (Evidence & RAG):** **Completed.** The CSV ingestion, FAISS indexing, embedding service, retrieval endpoints, and strict data validation (provenance checking) are fully functional.
- **Division 3 (Orchestrator):** **Not Started / Work in Progress.** This is the current phase of development. We need to implement the LLM-based concern classifier, speaker-aware prompt manager, and the deterministic escalation engine.
- **Division 4 (Language):** Implemented with translation and TTS capabilities.
- **Frontend:** Not yet implemented. Currently, there are only handoff documents and mock JSON files.

## Next Steps
We are currently focusing on **Division 3**. Our immediate tasks involve building the orchestrator using Groq and Gemini (avoiding Ollama) to classify concerns, retrieve evidence, and generate grounded, empathetic responses.
