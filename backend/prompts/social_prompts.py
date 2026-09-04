"""
Social Media Prompts Module (LinkedIn Post & Twitter/X Thread).
Strictly validates against schemas in backend.schemas.
"""

from typing import Dict, Any, Optional
from backend.schemas import LinkedInPost, TwitterThread
from .base_prompt import call_ollama_json


# =====================================================================
# LinkedIn Post Generator
# =====================================================================

LINKEDIN_SYSTEM_PROMPT = """You are a senior social media copywriter specializing in viral, high-authority B2B LinkedIn content.
Your goal is to transform raw source text into an impactful LinkedIn post that strictly adheres to the requested JSON schema.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. hook: Must be a compelling 1-2 sentence hook designed to capture attention before the 'see more' fold.
2. body_paragraphs: 2-3 short, punchy paragraphs explaining the context and stakes.
3. bullet_points: 3-5 scannable bullet points highlighting key data or takeaways (use emojis if tone permits).
4. call_to_action: An engaging question or call-to-action that encourages comments.
5. hashtags: 3-6 relevant industry hashtags without punctuation.

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "hook": "string",
  "body_paragraphs": ["string"],
  "bullet_points": ["string"],
  "call_to_action": "string",
  "hashtags": ["#tag1", "#tag2"]
}}"""

LINKEDIN_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "hook": "Over 14,000 corporate identity servers are actively exposed to a critical zero-day exploit right now.",
  "body_paragraphs": [
    "A CVSS 9.8 remote code execution flaw in Apex IAM Gateways is being actively weaponized by the ApexShadow Group.",
    "Once breached, adversaries achieve complete domain administrator control in under 18 minutes."
  ],
  "bullet_points": [
    "🚨 CVSS 9.8 Remote Code Execution in versions 4.2 through 5.1",
    "⏱️ 18-minute window from initial breach to domain controller takeover",
    "🔒 Emergency Patch v5.1.4 released today to neutralize the vector"
  ],
  "call_to_action": "Has your security team verified port 8443 firewall isolation today? Let's discuss your mitigation timeline below.",
  "hashtags": ["#CyberSecurity", "#Ransomware", "#Infosec", "#CISO", "#DevSecOps"]
}
"""


def generate_linkedin_post(
    raw_text: str,
    tone: str = "Professional",
    target_audience: str = "General Public",
    objective: str = "Inform",
    detail_level: str = "Standard",
    model: str = "llama3.1"
) -> LinkedInPost:
    """Generates a LinkedInPost model validated against backend.schemas.LinkedInPost."""
    system_prompt = LINKEDIN_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into a LinkedIn post.

{LINKEDIN_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return LinkedInPost.model_validate(json_dict)


# =====================================================================
# Twitter / X Thread Generator
# =====================================================================

TWITTER_SYSTEM_PROMPT = """You are an expert tech communicator on X / Twitter.
Transform the provided source content into an authoritative, engaging Twitter/X thread.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. thread_hook: A high-impact opening tweet text that establishes urgency and curiosity.
2. tweets: An ordered list of 4 to 7 Tweet objects.
3. Every single tweet's 'text' field MUST STRICTLY be <= 280 characters.
4. Number tweets cleanly inside the text: "1/5 ... 🧵👇", "2/5 ...", etc.
5. suggested_media_type: "None", "Infographic", "Chart", or "Screenshot".

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "thread_hook": "string",
  "tweets": [
    {{
      "tweet_num": 1,
      "text": "string (strictly <= 280 chars)",
      "suggested_media_type": "None"
    }}
  ]
}}"""

TWITTER_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "thread_hook": "🚨 CRITICAL ZERO-DAY: 14,000+ corporate IAM gateways are exposed to remote code execution. Here is what your team needs to know 🧵👇",
  "tweets": [
    {
      "tweet_num": 1,
      "text": "1/5 🚨 A critical CVSS 9.8 RCE flaw (CVE-2026-8891) in Apex IAM Gateways v4.2-5.1 is actively exploited in the wild. Threat actors breach domain controllers in <18 mins. 🧵👇",
      "suggested_media_type": "None"
    },
    {
      "tweet_num": 2,
      "text": "2/5 The attack vector abuses memory corruption during TLS handshakes on port 8443, enabling unauthenticated remote shell injection and AES-256 ransomware deployment.",
      "suggested_media_type": "Chart"
    },
    {
      "tweet_num": 3,
      "text": "3/5 Action item 1: Immediately isolate port 8443 on external firewalls. Do not wait for scheduled maintenance windows.",
      "suggested_media_type": "None"
    },
    {
      "tweet_num": 4,
      "text": "4/5 Action item 2: Deploy emergency vendor patch v5.1.4 released today across all gateway clusters and inspect reverse proxy logs for anomalous POSTs.",
      "suggested_media_type": "None"
    },
    {
      "tweet_num": 5,
      "text": "5/5 Long term: Enforce hardware MFA and zero-trust certificate pinning. Retweet to alert SecOps teams and stay safe. [Link]",
      "suggested_media_type": "None"
    }
  ]
}
"""


def generate_twitter_thread(
    raw_text: str,
    tone: str = "Professional",
    target_audience: str = "General Public",
    objective: str = "Inform",
    detail_level: str = "Standard",
    model: str = "llama3.1"
) -> TwitterThread:
    """Generates a TwitterThread model validated against backend.schemas.TwitterThread."""
    system_prompt = TWITTER_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into a Twitter / X thread. Ensure every single tweet text is strictly under 280 characters.

{TWITTER_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return TwitterThread.model_validate(json_dict)
