import httpx
import json

def run_tests():
    s_resp = httpx.post('http://127.0.0.1:8000/api/session', json={
        'district': 'Jaipur',
        'state': 'Rajasthan',
        'learner_education': 'Class 12',
        'income_bracket': '10k-20k',
        'trades_of_interest': ['Electrician'],
        'speakers_present': ['parent'],
        'preferred_language': 'en'
    })
    session_id = s_resp.json()['session_id']
    print(f"=== TEST SESSION CREATED: {session_id} ===")

    questions = [
        ("A", "Will my son get a job after this course?"),
        ("B", "How much can he earn?"),
        ("C", "Is this career safe for my daughter?"),
        ("D", "What does an electrician actually do?"),
        ("E", "Can he study further after ITI?"),
        ("F", "People in my family don't respect ITI.")
    ]

    results = []
    for label, q in questions:
        print(f"\nSending [{label}]: {q}")
        r = httpx.post('http://127.0.0.1:8000/api/counselling/message', json={
            'session_id': session_id,
            'speaker': 'parent',
            'message': q,
            'language': 'en'
        }, timeout=45.0)
        
        if r.status_code != 200:
            print(f"ERROR {r.status_code}: {r.text}")
            continue
            
        data = r.json()
        e_ids = [e['evidence_id'] for e in data.get('evidence', [])]
        cat = data.get('concern', {}).get('category')
        intent = data.get('concern', {}).get('intent')
        escalated = data.get('escalated')
        resp = data.get('response', '')
        
        print(f"-> Category: {cat} | Intent: {intent}")
        print(f"-> Evidence IDs: {e_ids}")
        print(f"-> Escalated: {escalated}")
        print(f"-> Response:\n{resp}\n")
        
        results.append({
            'label': label,
            'question': q,
            'category': cat,
            'intent': intent,
            'evidence_ids': e_ids,
            'escalated': escalated,
            'response': resp
        })

    with open('test_run_output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nAll 6 tests completed successfully and saved to test_run_output.json.")

if __name__ == '__main__':
    run_tests()
