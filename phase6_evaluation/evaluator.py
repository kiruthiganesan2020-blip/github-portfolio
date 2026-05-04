import requests
import time
import json
from typing import List, Dict

TEST_CASES = [
    {"location": "Bellandur", "budget": "high", "cuisine": "any", "min_rating": 4.0},
    {"location": "Marathahalli", "budget": "medium", "cuisine": "North Indian", "min_rating": 3.5},
    {"location": "BTM", "budget": "low", "cuisine": "Fast Food", "min_rating": 3.0},
]

def run_eval():
    print("Starting Evaluation for Zomato AI Recommendation System...")
    report = []
    
    for case in TEST_CASES:
        print(f"Testing: {case['location']} | {case['cuisine']} | {case['budget']}")
        start_time = time.time()
        try:
            response = requests.post("http://localhost:8000/recommend", json={
                **case,
                "top_n": 3
            })
            latency = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                recs = data.get("recommendations", [])
                
                # Basic sanity check
                location_correct = all(case['location'].lower() in r['location'].lower() for r in recs)
                
                report.append({
                    "case": case,
                    "status": "PASS" if location_correct else "FAIL (Location mismatch)",
                    "latency": f"{latency:.2f}s",
                    "recommendations_count": len(recs)
                })
            else:
                report.append({
                    "case": case,
                    "status": f"FAIL (HTTP {response.status_code})",
                    "latency": f"{latency:.2f}s"
                })
        except Exception as e:
            report.append({
                "case": case,
                "status": f"ERROR ({str(e)})",
                "latency": "N/A"
            })

    print("\n--- Evaluation Report ---")
    print(json.dumps(report, indent=2))
    
    with open("phase6_evaluation/report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nReport saved to phase6_evaluation/report.json")

if __name__ == "__main__":
    # Note: Backend must be running
    try:
        run_eval()
    except Exception as e:
        print(f"Evaluation failed. Is the backend running? {e}")
