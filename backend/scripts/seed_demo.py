"""
Seed script for Division 1 - Session Service.
Pre-populates the SQLite database with realistic demo data across 3 distinct sessions.
Run with:
    python scripts/seed_demo.py
"""

import sys
import os
import asyncio
from datetime import datetime
from pathlib import Path

# Adjust python path to locate 'app' module
current_file = Path(__file__).resolve()
backend_dir = current_file.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.database import AsyncSessionLocal, init_db
from app.models.session import Session, Message, Concern, EvidenceShown, Escalation


async def seed_data():
    """Seed demo data into database."""
    # Ensure tables are created
    await init_db()

    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()

        # ==========================================
        # SESSION 1: Nashik, Solar Technician (Resolved)
        # ==========================================
        s1_id = "SNASHIK01"
        s1 = Session(
            session_id=s1_id,
            district="Nashik",
            state="Maharashtra",
            learner_education="10th Standard",
            income_bracket="₹15,000 - ₹25,000/month",
            trades_of_interest=["Solar Technician"],
            speakers_present=["parent", "learner"],
            preferred_language="mr",
            escalated=False,
            escalation_id=None,
            created_at=now
        )
        db.add(s1)

        s1_messages = [
            Message(
                message_id="M101",
                session_id=s1_id,
                speaker="parent",
                message_type="user",
                text_original="माझ्या मुलाला सोलर टेक्निशियनचा कोर्स केल्यावर नाशिकमध्ये नोकरी मिळेल का?",
                text_english="Will my child get a job in Nashik after doing the Solar Technician course?",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M102",
                session_id=s1_id,
                speaker=None,
                message_type="assistant",
                text_original="होय, नाशिक आणि महाराष्ट्रात सोलर क्षेत्रात चांगली मागणी आहे. प्लेसमेंट दर सुमारे ७८% आहे.",
                text_english="Yes, there is strong demand in the solar sector in Nashik and Maharashtra. Placement rate is around 78%.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M103",
                session_id=s1_id,
                speaker="learner",
                message_type="user",
                text_original="सुरुवातीला पगार किती मिळू शकेल आणि पुढे वाढ कशी होईल?",
                text_english="What kind of salary can I expect initially and how will it grow?",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M104",
                session_id=s1_id,
                speaker=None,
                message_type="assistant",
                text_original="सुरुवातीचा पगार साधारणपणे ₹१८,००० ते ₹२६,००० प्रति महिना असतो आणि अनुभवासह सुपरवायझर पदापर्यंत प्रगती होते.",
                text_english="Starting salary is typically ₹18,000 to ₹26,000 per month, with career progression up to Supervisor.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M105",
                session_id=s1_id,
                speaker="parent",
                message_type="user",
                text_original="प्रवेशासाठी लागणारी फी आणि पात्रता काय आहे?",
                text_english="What are the admission fees and eligibility criteria?",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M106",
                session_id=s1_id,
                speaker=None,
                message_type="assistant",
                text_original="१०वी उत्तीर्ण विद्यार्थी शासकीय आयटीआय किंवा एनएसडीसी केंद्रात माफक शुल्कात प्रवेश घेऊ शकतात.",
                text_english="10th pass students can enroll in government ITIs or NSDC centres with subsidized fees.",
                language="mr",
                timestamp=now
            )
        ]
        db.add_all(s1_messages)

        s1_concerns = [
            Concern(
                session_id=s1_id,
                message_id="M101",
                category="employment",
                intent="placement_probability",
                confidence=0.92,
                raw_text="माझ्या मुलाला सोलर टेक्निशियनचा कोर्स केल्यावर नाशिकमध्ये नोकरी मिळेल का?",
                status="resolved",
                detected_at=now,
                resolved_at=now
            ),
            Concern(
                session_id=s1_id,
                message_id="M103",
                category="income",
                intent="starting_salary",
                confidence=0.89,
                raw_text="सुरुवातीला पगार किती मिळू शकेल आणि पुढे वाढ कशी होईल?",
                status="resolved",
                detected_at=now,
                resolved_at=now
            )
        ]
        db.add_all(s1_concerns)

        s1_evidence = EvidenceShown(
            session_id=s1_id,
            message_id="M102",
            evidence_id="EV001",
            trade="Solar Technician",
            district="Nashik",
            state="Maharashtra",
            placement_rate="78%",
            earnings_min=18000,
            earnings_max=26000,
            currency="INR",
            data_source="MSDE Outcome Dataset",
            data_period="2024-25",
            nsqf_level="Level 4",
            progression_path=["Helper", "Technician", "Senior Technician", "Supervisor"],
            shown_at=now
        )
        db.add(s1_evidence)

        # ==========================================
        # SESSION 2: Aurangabad, Plumber (In Progress)
        # ==========================================
        s2_id = "SAURANG02"
        s2 = Session(
            session_id=s2_id,
            district="Aurangabad",
            state="Maharashtra",
            learner_education="12th Standard",
            income_bracket="₹10,000 - ₹20,000/month",
            trades_of_interest=["Plumber"],
            speakers_present=["parent"],
            preferred_language="hi",
            escalated=False,
            escalation_id=None,
            created_at=now
        )
        db.add(s2)

        s2_messages = [
            Message(
                message_id="M201",
                session_id=s2_id,
                speaker="parent",
                message_type="user",
                text_original="प्लम्बर का काम समाज में कैसा माना जाता है? क्या इसमें सम्मानजनक काम मिलेगा?",
                text_english="How is plumbing work viewed socially? Will there be respectable work?",
                language="hi",
                timestamp=now
            ),
            Message(
                message_id="M202",
                session_id=s2_id,
                speaker=None,
                message_type="assistant",
                text_original="प्लम्बिंग आज एक आधुनिक और उच्च तकनीक वाला पेशा है। बड़े हाउसिंग प्रोजेक्ट्स और कमर्शियल साइट्स पर सर्टिफाइड प्लम्बर की बहुत मांग है।",
                text_english="Plumbing today is a modern, high-tech profession. Certified plumbers are in high demand in commercial projects.",
                language="hi",
                timestamp=now
            ),
            Message(
                message_id="M203",
                session_id=s2_id,
                speaker="parent",
                message_type="user",
                text_original="आगे चलकर कमाई में कितनी बढ़ोतरी हो सकती है?",
                text_english="How much growth can happen in earnings later on?",
                language="hi",
                timestamp=now
            ),
            Message(
                message_id="M204",
                session_id=s2_id,
                speaker=None,
                message_type="assistant",
                text_original="औरंगाबाद में शुरुआती वेतन ₹१५,००० से ₹२४,००० है और स्वतंत्र कांट्रैक्टर बनने पर मासिक कमाई ₹४०,००० से अधिक हो सकती है।",
                text_english="Starting salary in Aurangabad is ₹15,000 to ₹24,000, and independent contractors earn ₹40,000+ per month.",
                language="hi",
                timestamp=now
            )
        ]
        db.add_all(s2_messages)

        s2_concerns = [
            Concern(
                session_id=s2_id,
                message_id="M201",
                category="social_perception",
                intent="dignity_of_labour",
                confidence=0.91,
                raw_text="प्लम्बर का काम समाज में कैसा माना जाता है?",
                status="open",
                detected_at=now,
                resolved_at=None
            ),
            Concern(
                session_id=s2_id,
                message_id="M203",
                category="income",
                intent="wage_growth",
                confidence=0.86,
                raw_text="आगे चलकर कमाई में कितनी बढ़ोतरी हो सकती है?",
                status="partially_resolved",
                detected_at=now,
                resolved_at=None
            )
        ]
        db.add_all(s2_concerns)

        s2_evidence = EvidenceShown(
            session_id=s2_id,
            message_id="M204",
            evidence_id="EV002",
            trade="Plumber",
            district="Aurangabad",
            state="Maharashtra",
            placement_rate="82%",
            earnings_min=15000,
            earnings_max=24000,
            currency="INR",
            data_source="Maharashtra Skill Development Society",
            data_period="2024-25",
            nsqf_level="Level 4",
            progression_path=["Apprentice", "General Plumber", "Master Plumber", "Plumbing Contractor"],
            shown_at=now
        )
        db.add(s2_evidence)

        # ==========================================
        # SESSION 3: Nagpur, Beauty & Wellness (Escalated)
        # ==========================================
        s3_id = "SNAGPUR03"
        esc_id = "ESCNAG001"
        s3 = Session(
            session_id=s3_id,
            district="Nagpur",
            state="Maharashtra",
            learner_education="10th Standard",
            income_bracket="₹12,000 - ₹20,000/month",
            trades_of_interest=["Beauty & Wellness"],
            speakers_present=["parent", "learner"],
            preferred_language="mr",
            escalated=True,
            escalation_id=esc_id,
            created_at=now
        )
        db.add(s3)

        s3_messages = [
            Message(
                message_id="M301",
                session_id=s3_id,
                speaker="learner",
                message_type="user",
                text_original="मला ब्युटी अँड वेलनेस क्षेत्रात करिअर करायचे आहे.",
                text_english="I want to build a career in Beauty & Wellness.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M302",
                session_id=s3_id,
                speaker=None,
                message_type="assistant",
                text_original="नागपूरमध्ये ब्युटी थेरपिस्ट आणि सलून व्यवसायात चांगल्या संधी आहेत. सरासरी पगार ₹१४,००० ते ₹२२,००० आहे.",
                text_english="In Nagpur, beauty therapist and salon roles offer good opportunities with average earnings of ₹14,000 to ₹22,000.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M303",
                session_id=s3_id,
                speaker="parent",
                message_type="user",
                text_original="पण मुलींसाठी कामाची वेळ आणि कामाच्या ठिकाणी सुरक्षिततेचे काय?",
                text_english="What about work timings and workplace safety for girls?",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M304",
                session_id=s3_id,
                speaker=None,
                message_type="assistant",
                text_original="अनेक नोंदणीकृत सलूनमध्ये डे-शिफ्ट असतात. अधिक अचूक स्थानिक माहितीसाठी ही केस समुपदेशकांकडे पाठवली जात आहे.",
                text_english="Many registered salons have day shifts. For specific verified workplace safety details, this case is being referred to a counsellor.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M305",
                session_id=s3_id,
                speaker="parent",
                message_type="user",
                text_original="आम्हाला स्थानिक सुरक्षित सलून आणि प्रवासाच्या सोयीबद्दल मार्गदर्शन हवे आहे.",
                text_english="We need guidance regarding locally verified safe salons and transport facilities.",
                language="mr",
                timestamp=now
            ),
            Message(
                message_id="M306",
                session_id=s3_id,
                speaker=None,
                message_type="assistant",
                text_original="समुपदेशक लवकरच आपल्याशी संपर्क साधून योग्य सलूनची यादी आणि मार्गदर्शन देतील.",
                text_english="A counsellor will contact you shortly with a list of verified salons and personalized guidance.",
                language="mr",
                timestamp=now
            )
        ]
        db.add_all(s3_messages)

        s3_concerns = [
            Concern(
                session_id=s3_id,
                message_id="M303",
                category="gender_family",
                intent="late_hours_safety",
                confidence=0.94,
                raw_text="पण मुलींसाठी कामाची वेळ आणि कामाच्या ठिकाणी सुरक्षिततेचे काय?",
                status="partially_resolved",
                detected_at=now,
                resolved_at=None
            ),
            Concern(
                session_id=s3_id,
                message_id="M301",
                category="employment",
                intent="salon_vs_freelance",
                confidence=0.82,
                raw_text="मला ब्युटी अँड वेलनेस क्षेत्रात करिअर करायचे आहे.",
                status="open",
                detected_at=now,
                resolved_at=None
            )
        ]
        db.add_all(s3_concerns)

        s3_evidence = EvidenceShown(
            session_id=s3_id,
            message_id="M302",
            evidence_id="EV003",
            trade="Beauty & Wellness",
            district="Nagpur",
            state="Maharashtra",
            placement_rate="74%",
            earnings_min=14000,
            earnings_max=22000,
            currency="INR",
            data_source="MSDE Outcome Dataset",
            data_period="2024-25",
            nsqf_level="Level 3",
            progression_path=["Assistant Beauty Therapist", "Beauty Therapist", "Salon Manager", "Studio Owner"],
            shown_at=now
        )
        db.add(s3_evidence)

        s3_escalation = Escalation(
            escalation_id=esc_id,
            session_id=s3_id,
            triggered_at=now,
            trigger_reason="local_employer_safety_data_unavailable",
            primary_concern_category="gender_family",
            primary_concern_intent="late_hours_safety",
            secondary_concern_category="employment",
            secondary_concern_intent="salon_vs_freelance",
            information_already_provided=["placement_rate", "earnings_range", "nsqf_progression"],
            concern_status="partially_resolved",
            escalation_reason="Parent requires verification of day-shift policies and local commute safety for female candidate in Nagpur",
            recommended_action="Discuss verified salon employers offering fixed day shifts and transport in Nagpur",
            counsellor_status="pending",
            resolved_at=None,
            counsellor_notes=None
        )
        db.add(s3_escalation)

        await db.commit()

    print("Demo data seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_data())
