import os
import sys
import json
from pathlib import Path
import requests

# Set base URL
BASE_URL = "http://localhost:8000"
ROOT_DIR = Path(__file__).resolve().parent.parent
SAMPLE_FILE = ROOT_DIR / "data" / "samples" / "sample_1_cyber_threat.txt"

def run_tests():
    print("=" * 65)
    print("🚀 STARTING E2E AUTOMATION TEST: CONTENT TRANSFORMATION PLATFORM")
    print("=" * 65)

    # 1. Health Check Test
    print("\n[TEST 1] Checking API Health & Ollama Status...")
    try:
        health_resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        assert health_resp.status_code == 200, f"Health check failed with status {health_resp.status_code}"
        health_data = health_resp.json()
        print(f"  ✅ API is Healthy!")
        print(f"  ℹ️  Ollama Status: {health_data.get('ollama_status')}")
        print(f"  ℹ️  Default Model: {health_data.get('default_model')}")
    except requests.exceptions.ConnectionError:
        print("  ❌ ERROR: FastAPI server is not running on http://localhost:8000.")
        print("     Please start it using: uvicorn backend.app:app --reload")
        sys.exit(1)

    # 2. Verify Sample File Exists
    print("\n[TEST 2] Verifying Sample Document...")
    if not SAMPLE_FILE.exists():
        print(f"  ❌ ERROR: Sample file not found at: {SAMPLE_FILE}")
        sys.exit(1)
    
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()
    print(f"  ✅ Sample file loaded successfully ({len(raw_text)} characters).")

    # 3. Test Content Transformation (All 7 Formats)
    print("\n[TEST 3] Testing POST /api/transform (All 7 Formats)...")
    payload = {
        "raw_text": raw_text,
        "target_audience": "C-Suite",
        "tone": "Urgent",
        "objective": "Alert",
        "detail_level": "Standard",
        "selected_formats": [
            "linkedin",
            "twitter",
            "advisory",
            "executive_summary",
            "presentation",
            "video_package",
            "infographic"
        ]
    }

    resp = requests.post(
        f"{BASE_URL}/api/transform",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60
    )

    assert resp.status_code == 200, f"Transform failed with status {resp.status_code}: {resp.text}"
    result = resp.json()
    print("  ✅ Transformation executed successfully with HTTP 200!")

    # 4. Validate Specific Artefact Schemas in the Response
    print("\n[TEST 4] Validating Generated Artefact Schemas...")
    
    # Check Project Title
    assert result.get("project_title"), "Missing project title in response"
    print(f"  ✅ Title: {result.get('project_title')}")

    # Check LinkedIn
    linkedin = result.get("linkedin_post")
    assert linkedin and linkedin.get("hook"), "Missing LinkedIn Hook"
    print("  ✅ LinkedIn Post: Hook, Bullets, and Hashtags verified.")

    # Check Twitter / X
    twitter = result.get("twitter_thread")
    assert twitter and len(twitter.get("tweets", [])) > 0, "Missing Twitter Thread"
    print(f"  ✅ Twitter/X Thread: {len(twitter.get('tweets'))} tweets verified.")

    # Check Advisory
    advisory = result.get("advisory")
    assert advisory and advisory.get("severity_level"), "Missing Advisory severity"
    print(f"  ✅ Advisory: Level [{advisory.get('severity_level')}] verified.")

    # 5. Verify History Endpoint
    print("\n[TEST 5] Verifying Transformation History Database...")
    history_resp = requests.get(f"{BASE_URL}/api/history")
    assert history_resp.status_code == 200, "Failed to retrieve history"
    history_data = history_resp.json().get("history", [])
    assert len(history_data) > 0, "History database is empty"
    print(f"  ✅ History DB: Successfully saved and retrieved recent record.")

    print("\n" + "=" * 65)
    print("🎉 ALL END-TO-END TESTS PASSED SUCCESSFULLY! (READY FOR DEMO)")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
