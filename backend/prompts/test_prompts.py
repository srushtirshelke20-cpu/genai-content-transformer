"""
Standalone test script for backend/prompts pipeline.
Loads data/samples/sample_1_cyber_threat.txt and tests generation for at least 2 formats
(e.g., Twitter Thread and Executive Summary) against local running Ollama instance.
"""

import sys
import io
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Ensure repository root is on sys.path
CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.schemas import TransformRequest, TransformResponse
from backend.prompts.orchestrator import transform_content


def load_sample_content() -> str:
    """Finds and loads sample_1_cyber_threat.txt."""
    candidate_paths = [
        REPO_ROOT / "data" / "samples" / "sample_1_cyber_threat.txt",
        REPO_ROOT.parent / "data" / "samples" / "sample_1_cyber_threat.txt",
        Path("data/samples/sample_1_cyber_threat.txt").resolve(),
    ]

    for p in candidate_paths:
        if p.exists() and p.stat().st_size > 0:
            return p.read_text(encoding="utf-8")

    # Fallback embedded sample if file not found
    return (
        "CRITICAL SECURITY ADVISORY: CVE-2026-8891 RANSOMWARE EXPLOIT\n"
        "Date: September 2, 2026\n"
        "Threat Actor: ApexShadow Group\n"
        "Target Systems: Enterprise Identity and Access Management (IAM) Gateways\n"
        "OVERVIEW: Zero-day RCE vulnerability (CVSS 9.8) in Apex IAM Gateway v4.2-v5.1.\n"
        "Attackers exploit TLS memory corruption to deploy ransomware within 18 minutes.\n"
        "RECOMMENDED MITIGATION: Isolate port 8443 and apply Emergency Patch v5.1.4."
    )


def test_ollama_pipeline():
    print("=" * 75)
    print("🚀 TESTING BACKEND/PROMPTS PIPELINE WITH LOCAL OLLAMA")
    print("=" * 75)

    sample_text = load_sample_content()
    print(f"Loaded sample content ({len(sample_text)} characters).\n")

    # Construct request testing at least 2 formats: Twitter thread and Executive Summary
    test_formats = ["twitter", "executive_summary"]
    print(f"Requesting transformation for formats: {test_formats}")

    request = TransformRequest(
        raw_text=sample_text,
        target_audience="C-Suite & Security Operations",
        tone="Urgent",
        objective="Alert",
        detail_level="Standard",
        selected_formats=test_formats,
    )

    print("Sending request to transform_content() via Ollama (llama3.1)...")
    response: TransformResponse = transform_content(request)

    print("\n" + "=" * 75)
    print(f"🎉 TRANSFORM RESPONSE RECEIVED: '{response.project_title}'")
    print("=" * 75)

    # Validate Twitter Thread
    if response.twitter_thread:
        print("\n✅ FORMAT 1: Twitter Thread Generated Successfully:")
        print(f"   Hook: {response.twitter_thread.thread_hook}")
        print(f"   Total Tweets: {len(response.twitter_thread.tweets)}")
        for tweet in response.twitter_thread.tweets:
            print(f"   - Tweet #{tweet.tweet_num} ({len(tweet.text)} chars): {tweet.text}")
    else:
        print("\n❌ FORMAT 1: Twitter Thread generation failed or returned None")

    # Validate Executive Summary
    if response.executive_summary:
        print("\n✅ FORMAT 2: Executive Summary Generated Successfully:")
        print(f"   BLUF: {response.executive_summary.bluf}")
        print("   Key Findings:")
        for finding in response.executive_summary.key_findings:
            print(f"   • {finding}")
        print(f"   Strategic Implications: {response.executive_summary.strategic_implications}")
        print(f"   Recommended Decision: {response.executive_summary.recommended_decision}")
    else:
        print("\n❌ FORMAT 2: Executive Summary generation failed or returned None")

    assert response.twitter_thread is not None, "Expected valid TwitterThread deliverable"
    assert response.executive_summary is not None, "Expected valid ExecutiveSummary deliverable"
    print("\n" + "=" * 75)
    print("ALL TESTS PASSED: Ollama pipeline produces strictly valid Pydantic models!")
    print("=" * 75)


if __name__ == "__main__":
    test_ollama_pipeline()
