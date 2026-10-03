TAXONOMY = {
    "income": ["starting_salary", "long_term_earning", "salary_comparison", "return_on_training"],
    "employment": ["placement_probability", "local_jobs", "employer_availability", "job_security"],
    "safety": ["workplace_safety", "gender_safety", "travel_safety"],
    "social_perception": ["status_of_trade", "peer_comparison", "family_acceptance"],
    "education_progression": ["nsqf_levels", "further_education", "degree_equivalence"],
    "gender_family": ["suitability_for_daughter", "family_approval", "migration_concern"],
    "information_gap": ["course_content", "duration", "fees", "eligibility"]
}

SYSTEM_PROMPT = """You are a concern classifier for a vocational career counselling platform in India.
Classify the following message into exactly one category and one intent.
Respond ONLY with valid JSON. No explanation. No markdown.

Taxonomy: {TAXONOMY}
Speaker: {speaker}
Trades discussed: {trades}
District: {district}, State: {state}

Message: "{message}"

Respond with:
{{"category": "<category>", "intent": "<intent>", "confidence": <0.0-1.0>, "reasoning": "<one line>"}}
"""
