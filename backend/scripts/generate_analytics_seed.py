import random
from datetime import datetime, timedelta

def generate_analytics_seed():
    random.seed(42)  # Deterministic generation

    trades = [
        "Solar Technician", "Electrician", "Plumber", "Welder", "CNC Operator",
        "Beauty & Wellness", "Healthcare Assistant", "Draughtsman Civil",
        "Refrigeration & AC Technician", "Food Processing Technician"
    ]

    districts_by_state = {
        "Maharashtra": ["Nashik", "Pune", "Aurangabad", "Nagpur", "Kolhapur", "Thane", "Solapur", "Amravati"],
        "Rajasthan": ["Jaipur", "Jodhpur"],
        "Karnataka": ["Bengaluru", "Mysuru"]
    }

    # Concern category weights: income & employment ~40% combined
    concern_catalog = {
        "income": ["starting_salary", "wage_growth", "long_term_earning", "overtime_pay"],
        "employment": ["placement_probability", "job_guarantee", "local_vs_migration", "industry_demand"],
        "gender_family": ["suitability_for_daughter", "parental_acceptance", "marriage_prospects", "workplace_environment"],
        "safety": ["gender_safety", "workplace_hazards", "late_hours_safety", "protective_equipment"],
        "social_perception": ["status_of_trade", "dignity_of_labour", "peer_pressure", "white_collar_comparison"],
        "information_gap": ["fees", "admission_process", "duration", "eligibility"],
        "education_progression": ["nsqf_levels", "higher_education_lateral_entry", "apprenticeship_pathway"]
    }

    categories = list(concern_catalog.keys())
    # Weights for category selection
    cat_weights = [0.22, 0.20, 0.14, 0.14, 0.10, 0.10, 0.10]

    events = []
    current_ae_idx = 1

    # 1. First cover the 5 Demo Sessions
    demo_sessions_info = [
        ("S_DEMO_01", "Solar Technician", "Nashik", "Maharashtra", datetime(2026, 10, 1, 9, 0, 0), False,
         [("employment", "placement_probability"), ("income", "starting_salary")]),
        ("S_DEMO_02", "Plumber", "Aurangabad", "Maharashtra", datetime(2026, 10, 1, 10, 15, 0), False,
         [("social_perception", "status_of_trade"), ("income", "starting_salary")]),
        ("S_DEMO_03", "Beauty & Wellness", "Nagpur", "Maharashtra", datetime(2026, 10, 1, 11, 30, 0), True,
         [("gender_family", "suitability_for_daughter"), ("safety", "gender_safety"), ("employment", "placement_probability")]),
        ("S_DEMO_04", "Electrician", "Jaipur", "Rajasthan", datetime(2026, 10, 1, 14, 0, 0), False,
         [("information_gap", "fees"), ("education_progression", "nsqf_levels")]),
        ("S_DEMO_05", "CNC Operator", "Bengaluru", "Karnataka", datetime(2026, 10, 1, 15, 45, 0), False,
         [("income", "long_term_earning")]),
    ]

    for sid, trade, dist, state, base_time, is_esc, c_list in demo_sessions_info:
        # session_started
        events.append((
            f"AE_{current_ae_idx:03d}", sid, "session_started", None, None,
            trade, dist, state, base_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        current_ae_idx += 1

        t_offset = 30
        for cat, intent in c_list:
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "concern_detected", cat, intent,
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
            t_offset += 30

        # evidence_shown
        ev_time = base_time + timedelta(seconds=t_offset)
        events.append((
            f"AE_{current_ae_idx:03d}", sid, "evidence_shown", c_list[0][0], c_list[0][1],
            trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        current_ae_idx += 1
        t_offset += 30

        # concern_resolved (if not open)
        if not is_esc:
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "concern_resolved", c_list[0][0], c_list[0][1],
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
            t_offset += 30
        else:
            # escalated
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "escalated", c_list[0][0], c_list[0][1],
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
            t_offset += 30

    # 2. Synthetic Sessions: S_SYN_001 to S_SYN_050
    start_date = datetime(2026, 9, 15, 8, 30, 0)
    end_date = datetime(2026, 10, 3, 17, 30, 0)
    total_seconds = int((end_date - start_date).total_seconds())

    synthetic_sessions = []
    for i in range(1, 51):
        sid = f"S_SYN_{i:03d}"
        trade = trades[(i - 1) % len(trades)]
        
        # Pick state & district
        state_r = random.random()
        if state_r < 0.60:
            state = "Maharashtra"
        elif state_r < 0.80:
            state = "Rajasthan"
        else:
            state = "Karnataka"
        dist = random.choice(districts_by_state[state])

        # Pick random timestamp
        rand_sec = random.randint(0, total_seconds)
        base_time = start_date + timedelta(seconds=rand_sec)

        # Roughly 20% escalation rate overall
        # Higher escalation rate for gender_family / safety trades
        if trade in ["Beauty & Wellness", "Healthcare Assistant"]:
            is_escalated = random.random() < 0.35
        elif trade in ["Welder", "Plumber"]:
            is_escalated = random.random() < 0.25
        else:
            is_escalated = random.random() < 0.15

        # 1-3 concerns
        num_concerns = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
        c_list = []
        for _ in range(num_concerns):
            cat = random.choices(categories, weights=cat_weights)[0]
            intent = random.choice(concern_catalog[cat])
            if (cat, intent) not in c_list:
                c_list.append((cat, intent))
        if not c_list:
            c_list.append(("income", "starting_salary"))

        synthetic_sessions.append((sid, trade, dist, state, base_time, is_escalated, c_list))

    # Generate events for synthetic sessions until we reach 200 total events
    for sid, trade, dist, state, base_time, is_esc, c_list in synthetic_sessions:
        if current_ae_idx > 200:
            break

        # 1. session_started
        events.append((
            f"AE_{current_ae_idx:03d}", sid, "session_started", None, None,
            trade, dist, state, base_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        current_ae_idx += 1

        t_offset = 20
        # 2. concern_detected (1 to len(c_list))
        for cat, intent in c_list:
            if current_ae_idx > 200:
                break
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "concern_detected", cat, intent,
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
            t_offset += 25

        # 3. evidence_shown
        if current_ae_idx <= 200:
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "evidence_shown", c_list[0][0], c_list[0][1],
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
            t_offset += 20

        # 4. concern_resolved or escalated
        if is_esc and current_ae_idx <= 200:
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "escalated", c_list[0][0], c_list[0][1],
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1
        elif not is_esc and random.random() < 0.75 and current_ae_idx <= 200:
            ev_time = base_time + timedelta(seconds=t_offset)
            events.append((
                f"AE_{current_ae_idx:03d}", sid, "concern_resolved", c_list[0][0], c_list[0][1],
                trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            current_ae_idx += 1

    # If still below 200, fill up to exactly 200
    while current_ae_idx <= 200:
        syn = random.choice(synthetic_sessions)
        sid, trade, dist, state, base_time, is_esc, c_list = syn
        ev_type = random.choice(["concern_detected", "evidence_shown", "concern_resolved"])
        cat, intent = random.choice(c_list)
        ev_time = base_time + timedelta(seconds=random.randint(60, 300))
        events.append((
            f"AE_{current_ae_idx:03d}", sid, ev_type, cat, intent,
            trade, dist, state, ev_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        current_ae_idx += 1

    # Sort events chronologically or by ID
    sql = []
    sql.append("-- ============================================================================")
    sql.append("-- ANALYTICS SEED SCRIPT (200 Telemetry Events)")
    sql.append("-- Populates analytics_events table across 5 demo sessions + 50 synthetic sessions")
    sql.append("-- ============================================================================\n")
    sql.append("-- Table: analytics_events")
    sql.append("-- Columns: event_id, session_id, event_type, concern_category, concern_intent, trade, district, state, timestamp\n")

    for ev in events[:200]:
        eid, sid, etype, ccat, cint, trade, dist, state, ts = ev
        ccat_val = f"'{ccat}'" if ccat else "NULL"
        cint_val = f"'{cint}'" if cint else "NULL"
        trade_val = f"'{trade}'" if trade else "NULL"
        dist_val = f"'{dist}'" if dist else "NULL"
        state_val = f"'{state}'" if state else "NULL"

        sql.append(
            f"INSERT OR REPLACE INTO analytics_events (event_id, session_id, event_type, concern_category, concern_intent, trade, district, state, timestamp) "
            f"VALUES ('{eid}', '{sid}', '{etype}', {ccat_val}, {cint_val}, {trade_val}, {dist_val}, {state_val}, '{ts}');"
        )

    full_sql = "\n".join(sql)
    with open(r's:\SEM_7\SIUUHH\SIH241\backend\scripts\analytics_seed.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)

    print(f"Successfully generated {len(events[:200])} analytics events in backend/scripts/analytics_seed.sql")

if __name__ == "__main__":
    generate_analytics_seed()
