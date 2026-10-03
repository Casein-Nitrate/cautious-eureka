import json

def generate_demo_sessions_sql():
    sql = []
    sql.append("-- ============================================================================")
    sql.append("-- SEED DEMO SESSIONS SCRIPT")
    sql.append("-- Populates 5 realistic demo counselling sessions with messages, concerns,")
    sql.append("-- evidence shown, and escalation records.")
    sql.append("-- ============================================================================\n")

    # 1. Sessions
    sessions = [
        ("S_DEMO_01", "2026-10-01 09:00:00", "Nashik", "Maharashtra", "Class 12", "10k-20k", json.dumps(["Solar Technician"]), json.dumps(["learner", "parent"]), "mr", 0, None),
        ("S_DEMO_02", "2026-10-01 10:15:00", "Aurangabad", "Maharashtra", "Class 10", "5k-10k", json.dumps(["Plumber"]), json.dumps(["parent"]), "hi", 0, None),
        ("S_DEMO_03", "2026-10-01 11:30:00", "Nagpur", "Maharashtra", "Class 12", "10k-20k", json.dumps(["Beauty & Wellness"]), json.dumps(["learner", "parent"]), "mr", 1, "ESC_DEMO_01"),
        ("S_DEMO_04", "2026-10-01 14:00:00", "Jaipur", "Rajasthan", "Class 10", "5k-10k", json.dumps(["Electrician"]), json.dumps(["guardian", "learner"]), "hi", 0, None),
        ("S_DEMO_05", "2026-10-01 15:45:00", "Bengaluru", "Karnataka", "Class 12", "20k-30k", json.dumps(["CNC Operator"]), json.dumps(["parent"]), "en", 0, None),
    ]

    sql.append("-- 1. INSERT SESSIONS")
    for s in sessions:
        esc_val = f"'{s[10]}'" if s[10] else "NULL"
        trades_json = s[6].replace("'", "''")
        speakers_json = s[7].replace("'", "''")
        sql.append(
            f"INSERT OR REPLACE INTO sessions (session_id, created_at, district, state, learner_education, income_bracket, trades_of_interest, speakers_present, preferred_language, escalated, escalation_id) "
            f"VALUES ('{s[0]}', '{s[1]}', '{s[2]}', '{s[3]}', '{s[4]}', '{s[5]}', '{trades_json}', '{speakers_json}', '{s[8]}', {s[9]}, {esc_val});"
        )
    sql.append("")

    # 2. Messages
    messages = [
        # Session 1 (Nashik, Solar Technician, mr)
        ("M_D01_001", "S_DEMO_01", "learner", "user", "मला सोलर टेक्निशियन कोर्सबद्दल माहिती हवी आहे. यामध्ये नोकरीच्या काय संधी आहेत?", "I want information about the Solar Technician course. What are the job opportunities in this?", "mr", "2026-10-01 09:00:30"),
        ("M_D01_002", "S_DEMO_01", None, "assistant", "सोलर टेक्निशियन हा खूप चांगला पर्याय आहे. नाशिक आणि महाराष्ट्रात सोलर सेक्टरमध्ये ८४% पेक्षा जास्त प्लेसमेंट आहे.", "Solar Technician is a very good choice. In Nashik and Maharashtra, placement rate in solar sector is over 84%.", "mr", "2026-10-01 09:01:00"),
        ("M_D01_003", "S_DEMO_01", "parent", "user", "सुरुवातीला पगार किती मिळेल आणि पुढे वाढ होईल का?", "What will be the starting salary and will there be growth?", "mr", "2026-10-01 09:01:30"),
        ("M_D01_004", "S_DEMO_01", None, "assistant", "सुरुवातीचा पगार साधारण ₹१८,००० ते ₹२८,००० प्रति महिना असतो, आणि अनुभवानंतर सुपरवायझर म्हणून ₹३५,०००+ मिळू शकतो.", "Starting salary is around ₹18,000 to ₹28,000 per month, and after experience one can earn ₹35,000+ as supervisor.", "mr", "2026-10-01 09:02:00"),
        ("M_D01_005", "S_DEMO_01", "learner", "user", "प्रशिक्षणासाठी नाशिकमध्ये सरकारी आयटीआय उपलब्ध आहे का?", "Is a government ITI available in Nashik for training?", "mr", "2026-10-01 09:02:30"),
        ("M_D01_006", "S_DEMO_01", None, "assistant", "होय, नाशिक शासकीय आयटीआयमध्ये अत्याधुनिक सोलर लॅब आणि रूफटॉप ट्रेनिंग सुविधा उपलब्ध आहे.", "Yes, Nashik Government ITI has modern solar lab and rooftop training facilities.", "mr", "2026-10-01 09:03:00"),

        # Session 2 (Aurangabad, Plumber, hi)
        ("M_D02_001", "S_DEMO_02", "parent", "user", "प्लंबर का काम क्या समाज में इज्जतदार माना जाता है? लोग क्या कहेंगे?", "Is plumbing considered a respectable job in society? What will people say?", "hi", "2026-10-01 10:15:30"),
        ("M_D02_002", "S_DEMO_02", None, "assistant", "आधुनिक प्लंबिंग एक उच्च तकनीकी और सम्मानजनक पेशा है। आज बड़े कमर्शियल और आवासीय प्रोजेक्ट्स में सर्टिफाइड प्लंबर की भारी मांग है।", "Modern plumbing is a high-tech and respectable profession. Today certified plumbers are in high demand for commercial and residential projects.", "hi", "2026-10-01 10:16:00"),
        ("M_D02_003", "S_DEMO_02", "parent", "user", "शुरुआती कमाई कितनी होगी? क्या परिवार का खर्च चल पाएगा?", "How much will be the starting income? Can it support family expenses?", "hi", "2026-10-01 10:16:30"),
        ("M_D02_004", "S_DEMO_02", None, "assistant", "औरंगाबाद में शुरुआती मासिक वेतन ₹१४,००० से ₹२४,००० तक है, और स्वतंत्र कांट्रैक्टिंग से कमाई और बढ़ सकती है।", "In Aurangabad starting salary is ₹14,000 to ₹24,000, and independent contracting can increase earnings further.", "hi", "2026-10-01 10:17:00"),
        ("M_D02_005", "S_DEMO_02", "parent", "user", "धन्यवाद, अब मैं इस कोर्स के बारे में गंभीरता से विचार करूंगा।", "Thank you, now I will seriously consider this course.", "hi", "2026-10-01 10:17:30"),

        # Session 3 (Nagpur, Beauty & Wellness, mr)
        ("M_D03_001", "S_DEMO_03", "learner", "user", "मला ब्युटी अँड वेलनेस क्षेत्रात करिअर करायचे आहे.", "I want to make a career in Beauty & Wellness.", "mr", "2026-10-01 11:30:30"),
        ("M_D03_002", "S_DEMO_03", None, "assistant", "ब्युटी अँड वेलनेस क्षेत्रात नागपूर आणि पुण्यात उत्तम संधी आहेत. यामध्ये ८४% हून अधिक रोजगार दर आहे.", "There are great opportunities in Nagpur and Pune in Beauty & Wellness with over 84% placement rate.", "mr", "2026-10-01 11:31:00"),
        ("M_D03_003", "S_DEMO_03", "parent", "user", "पण मुलीसाठी हे काम योग्य आहे का? समाजात आणि नातेवाईकांत गैरसमज होतात.", "But is this work suitable for a girl? Relatives and society have misconceptions.", "mr", "2026-10-01 11:31:30"),
        ("M_D03_004", "S_DEMO_03", None, "assistant", "या क्षेत्रात ८०-९०% महिला कार्यरत आहेत आणि हे पूर्णपणे व्यावसायिक व सन्मानजनक क्षेत्र आहे.", "80-90% workforce in this trade are women and it is completely professional and dignified.", "mr", "2026-10-01 11:32:00"),
        ("M_D03_005", "S_DEMO_03", "parent", "user", "संध्याकाळी उशिरापर्यंत काम करावे लागले तर सुरक्षिततेचे काय?", "What about safety if she has to work late in the evening?", "mr", "2026-10-01 11:32:30"),
        ("M_D03_006", "S_DEMO_03", None, "assistant", "प्रशिक्षण संस्थांमध्ये सीसीटीव्ही, सुरक्षित हॉस्टेल आणि सुरक्षित वाहतूक भागीदारी उपलब्ध असते.", "Training institutes provide CCTV, secure hostels, and safe transport partnerships.", "mr", "2026-10-01 11:33:00"),
        ("M_D03_007", "S_DEMO_03", "parent", "user", "तरीही आम्हाला अजून शंका आहेत, आम्ही प्रत्यक्ष तज्ज्ञांशी बोलू इच्छितो.", "Still we have doubts, we want to talk to an expert directly.", "mr", "2026-10-01 11:33:30"),
        ("M_D03_008", "S_DEMO_03", None, "assistant", "मी आपल्यासाठी वरिष्ठ समुपदेशकांशी प्रत्यक्ष चर्चेची व्यवस्था करत आहे. ते लवकरच आपल्याशी संपर्क साधतील.", "I am arranging a direct discussion with a senior human counsellor. They will contact you shortly.", "mr", "2026-10-01 11:34:00"),

        # Session 4 (Jaipur, Electrician, hi)
        ("M_D04_001", "S_DEMO_04", "guardian", "user", "इलेक्ट्रीशियन कोर्स की सरकारी फीस कितनी है? क्या कोई वजीफा मिलता है?", "What are the government fees for the Electrician course? Is any stipend available?", "hi", "2026-10-01 14:00:30"),
        ("M_D04_002", "S_DEMO_04", None, "assistant", "सरकारी आईटीआई में फीस अत्यंत नाममात्र (₹१०००-₹२००० प्रति वर्ष) होती है और सभी पात्र छात्रों को सरकारी छात्रवृत्ति मिलती है।", "Government ITI fees are nominal (₹1000-₹2000/yr) and eligible candidates receive state scholarships.", "hi", "2026-10-01 14:01:00"),
        ("M_D04_003", "S_DEMO_04", "learner", "user", "क्या इस कोर्स के बाद पॉलिटेक्निक डिप्लोमा में सीधे प्रवेश मिल सकता है?", "Can I get direct admission into Polytechnic Diploma after this course?", "hi", "2026-10-01 14:01:30"),
        ("M_D04_004", "S_DEMO_04", None, "assistant", "हाँ, एनएसक्यूएफ लेवल ४ प्रमाणन के बाद आप पॉलिटेक्निक के द्वितीय वर्ष में लेटरल एंट्री के लिए पात्र होते हैं।", "Yes, with NSQF Level 4 certification you are eligible for lateral entry into the second year of Polytechnic.", "hi", "2026-10-01 14:02:00"),
        ("M_D04_005", "S_DEMO_04", "guardian", "user", "यह बहुत अच्छी जानकारी है। हम जयपुर आईटीआई में आवेदन करेंगे।", "This is great information. We will apply at Jaipur ITI.", "hi", "2026-10-01 14:02:30"),

        # Session 5 (Bengaluru, CNC Operator, en)
        ("M_D05_001", "S_DEMO_05", "parent", "user", "What is the long-term career growth and salary potential for a CNC Operator in Bengaluru?", "What is the long-term career growth and salary potential for a CNC Operator in Bengaluru?", "en", "2026-10-01 15:45:30"),
        ("M_D05_002", "S_DEMO_05", None, "assistant", "In Bengaluru, starting salaries range from ₹25,000 to ₹42,000 per month with aerospace and precision tooling firms, progressing to ₹60,000+ as a CNC Programmer or Production Lead.", "In Bengaluru, starting salaries range from ₹25,000 to ₹42,000 per month with aerospace and precision tooling firms, progressing to ₹60,000+ as a CNC Programmer or Production Lead.", "en", "2026-10-01 15:46:00"),
        ("M_D05_003", "S_DEMO_05", "parent", "user", "Is there sufficient industry demand considering automation?", "Is there sufficient industry demand considering automation?", "en", "2026-10-01 15:46:30"),
        ("M_D05_004", "S_DEMO_05", None, "assistant", "Yes, advanced manufacturing and aerospace sectors in Bengaluru report a 94% placement rate for certified Level 5 CNC technicians.", "Yes, advanced manufacturing and aerospace sectors in Bengaluru report a 94% placement rate for certified Level 5 CNC technicians.", "en", "2026-10-01 15:47:00"),
    ]

    sql.append("-- 2. INSERT MESSAGES")
    for m in messages:
        spk_val = f"'{m[2]}'" if m[2] else "NULL"
        orig_text = m[4].replace("'", "''")
        if m[5]:
            safe_eng = m[5].replace("'", "''")
            eng_text = f"'{safe_eng}'"
        else:
            eng_text = "NULL"
        sql.append(
            f"INSERT OR REPLACE INTO messages (message_id, session_id, speaker, message_type, text_original, text_english, language, timestamp) "
            f"VALUES ('{m[0]}', '{m[1]}', {spk_val}, '{m[3]}', '{orig_text}', {eng_text}, '{m[6]}', '{m[7]}');"
        )
    sql.append("")

    # 3. Concerns
    concerns = [
        # Session 1
        ("S_DEMO_01", "M_D01_001", "employment", "placement_probability", 0.95, "नोकरीच्या काय संधी आहेत?", "resolved", "2026-10-01 09:00:30", "2026-10-01 09:01:00"),
        ("S_DEMO_01", "M_D01_003", "income", "starting_salary", 0.92, "सुरुवातीला पगार किती मिळेल आणि पुढे वाढ होईल का?", "resolved", "2026-10-01 09:01:30", "2026-10-01 09:02:00"),

        # Session 2
        ("S_DEMO_02", "M_D02_001", "social_perception", "status_of_trade", 0.94, "प्लंबर का काम क्या समाज में इज्जतदार माना जाता है? लोग क्या कहेंगे?", "resolved", "2026-10-01 10:15:30", "2026-10-01 10:16:00"),
        ("S_DEMO_02", "M_D02_003", "income", "starting_salary", 0.88, "शुरुआती कमाई कितनी होगी? क्या परिवार का खर्च चल पाएगा?", "partially_resolved", "2026-10-01 10:16:30", None),

        # Session 3
        ("S_DEMO_03", "M_D03_001", "employment", "placement_probability", 0.91, "मला ब्युटी अँड वेलनेस क्षेत्रात करिअर करायचे आहे.", "resolved", "2026-10-01 11:30:30", "2026-10-01 11:31:00"),
        ("S_DEMO_03", "M_D03_003", "gender_family", "suitability_for_daughter", 0.96, "पण मुलीसाठी हे काम योग्य आहे का? समाजात आणि नातेवाईकांत गैरसमज होतात.", "open", "2026-10-01 11:31:30", None),
        ("S_DEMO_03", "M_D03_005", "safety", "gender_safety", 0.93, "संध्याकाळी उशिरापर्यंत काम करावे लागले तर सुरक्षिततेचे काय?", "open", "2026-10-01 11:32:30", None),

        # Session 4
        ("S_DEMO_04", "M_D04_001", "information_gap", "fees", 0.95, "इलेक्ट्रीशियन कोर्स की सरकारी फीस कितनी है? क्या कोई वजीफा मिलता है?", "resolved", "2026-10-01 14:00:30", "2026-10-01 14:01:00"),
        ("S_DEMO_04", "M_D04_003", "education_progression", "nsqf_levels", 0.90, "क्या इस कोर्स के बाद पॉलिटेक्निक डिप्लोमा में सीधे प्रवेश मिल सकता है?", "resolved", "2026-10-01 14:01:30", "2026-10-01 14:02:00"),

        # Session 5
        ("S_DEMO_05", "M_D05_001", "income", "long_term_earning", 0.94, "What is the long-term career growth and salary potential for a CNC Operator in Bengaluru?", "resolved", "2026-10-01 15:45:30", "2026-10-01 15:46:00"),
    ]

    sql.append("-- 3. INSERT CONCERNS")
    for c in concerns:
        res_at = f"'{c[8]}'" if c[8] else "NULL"
        raw_txt = c[5].replace("'", "''")
        sql.append(
            f"INSERT INTO concerns (session_id, message_id, category, intent, confidence, raw_text, status, detected_at, resolved_at) "
            f"VALUES ('{c[0]}', '{c[1]}', '{c[2]}', '{c[3]}', {c[4]}, '{raw_txt}', '{c[6]}', '{c[7]}', {res_at});"
        )
    sql.append("")

    # 4. Evidence Shown
    evidence = [
        # Session 1
        ("S_DEMO_01", "M_D01_002", "EV001", "Solar Technician", "Nashik", "Maharashtra", "84%", 18000, 28000, "INR", "MSDE National Outcome Report", "2024-25", "Level 4", json.dumps(["Assistant Solar Installer", "Solar Technician", "Plant Supervisor", "Solar Project Manager"]), "2026-10-01 09:01:00"),
        ("S_DEMO_01", "M_D01_004", "EV002", "Solar Technician", "Pune", "Maharashtra", "89%", 21000, 35000, "INR", "State Skill Development Mission Tracer Study", "2024-25", "Level 4", json.dumps(["Solar PV Installer", "Service Engineer", "Project Lead", "Operations Head"]), "2026-10-01 09:02:00"),

        # Session 2
        ("S_DEMO_02", "M_D02_002", "EV013", "Plumber", "Aurangabad", "Maharashtra", "76%", 14000, 24000, "INR", "MSDE National Outcome Report", "2024-25", "Level 4", json.dumps(["Plumber Helper", "Certified Plumber", "Plumbing Foreman", "Sanitary Contractor"]), "2026-10-01 10:16:00"),

        # Session 3
        ("S_DEMO_03", "M_D03_002", "EV032", "Beauty & Wellness", "Nagpur", "Maharashtra", "84%", 16000, 28000, "INR", "State Skill Development Mission Tracer Study", "2024-25", "Level 4", json.dumps(["Skin Care Specialist", "Hair Stylist & Colorist", "Bridal Makeup Artist", "Salon Manager"]), "2026-10-01 11:31:00"),
        ("S_DEMO_03", "M_D03_004", "EV031", "Beauty & Wellness", "Pune", "Maharashtra", "89%", 18000, 34000, "INR", "MSDE National Outcome Report", "2024-25", "Level 4", json.dumps(["Beauty Therapist", "Senior Aesthetician", "Salon Supervisor", "Wellness Studio Franchisee"]), "2026-10-01 11:32:00"),

        # Session 4
        ("S_DEMO_04", "M_D04_002", "EV010", "Electrician", "Jaipur", "Rajasthan", "85%", 18000, 30000, "INR", "NCVT Alumni Survey 2024-25", "2024-25", "Level 4", json.dumps(["Apprentice", "Industrial Wireman", "Substation Operator", "Chief Electrician"]), "2026-10-01 14:01:00"),

        # Session 5
        ("S_DEMO_05", "M_D05_002", "EV029", "CNC Operator", "Bengaluru", "Karnataka", "94%", 25000, 42000, "INR", "State Skill Development Mission Tracer Study", "2024-25", "Level 5", json.dumps(["Precision CNC Machinist", "Multi-Axis VMC Operator", "CNC CAM Programmer", "Shop Floor Manager"]), "2026-10-01 15:46:00"),
    ]

    sql.append("-- 4. INSERT EVIDENCE SHOWN")
    for e in evidence:
        prog_json = e[13].replace("'", "''")
        sql.append(
            f"INSERT INTO evidence_shown (session_id, message_id, evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path, shown_at) "
            f"VALUES ('{e[0]}', '{e[1]}', '{e[2]}', '{e[3]}', '{e[4]}', '{e[5]}', '{e[6]}', {e[7]}, {e[8]}, '{e[9]}', '{e[10]}', '{e[11]}', '{e[12]}', '{prog_json}', '{e[14]}');"
        )
    sql.append("")

    # 5. Escalations
    escalations = [
        ("ESC_DEMO_01", "S_DEMO_03", "2026-10-01 11:34:00", "family_cultural_objection_requires_human_mediation",
         "gender_family", "suitability_for_daughter", "safety", "gender_safety",
         json.dumps(["Female enrollment 84%", "Nagpur ITI placement 84%", "CCTV and transport security"]),
         "open", "Persistent family cultural objections and safety concerns regarding daughter's vocational training",
         "Discuss female enrollment 84% and safety infrastructure at Nagpur Beauty & Wellness ITI",
         "pending", None, None)
    ]

    sql.append("-- 5. INSERT ESCALATIONS")
    for esc in escalations:
        sec_cat = f"'{esc[6]}'" if esc[6] else "NULL"
        sec_int = f"'{esc[7]}'" if esc[7] else "NULL"
        info_json = esc[8].replace("'", "''")
        esc_reason = esc[10].replace("'", "''")
        rec_action = esc[11].replace("'", "''")
        if esc[13]:
            safe_notes = esc[13].replace("'", "''")
            notes = f"'{safe_notes}'"
        else:
            notes = "NULL"
        sql.append(
            f"INSERT OR REPLACE INTO escalations (escalation_id, session_id, triggered_at, trigger_reason, primary_concern_category, primary_concern_intent, secondary_concern_category, secondary_concern_intent, information_already_provided, concern_status, escalation_reason, recommended_action, counsellor_status, resolved_at, counsellor_notes) "
            f"VALUES ('{esc[0]}', '{esc[1]}', '{esc[2]}', '{esc[3]}', '{esc[4]}', '{esc[5]}', {sec_cat}, {sec_int}, '{info_json}', '{esc[9]}', '{esc_reason}', '{rec_action}', '{esc[12]}', NULL, {notes});"
        )
    sql.append("")

    full_sql = "\n".join(sql)
    with open(r's:\SEM_7\SIUUHH\SIH241\backend\scripts\seed_demo_sessions.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)

    print("Successfully wrote seed_demo_sessions.sql")

if __name__ == "__main__":
    generate_demo_sessions_sql()
