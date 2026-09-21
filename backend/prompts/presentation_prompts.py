"""
Presentation Deck Prompts Module.
Generates 5-7 slides with concise bullets and complete speaker notes.
Strictly validates against backend.schemas.PresentationDeck.
"""

from typing import Dict, Any, Optional
from backend.schemas import PresentationDeck
from .base_prompt import call_ollama_json


PRESENTATION_SYSTEM_PROMPT = """You are an executive communications designer and presentation coach.
Transform the provided source content into an executive 5-7 slide Presentation Deck.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. deck_title: High-level executive presentation title.
2. target_audience: Intended viewer persona (e.g., C-Suite, Technical, General Public).
3. slides: Exactly 5 to 7 Slide objects.
4. Each Slide MUST have:
   - slide_num: integer starting from 1.
   - title: concise, action-oriented header (< 8 words).
   - bullet_points: 3 to 4 concise bullets, STRICTLY <= 15 words per bullet point. No walls of text.
   - visual_diagram_concept: description of chart, architecture diagram, or visual metaphor.
   - speaker_notes: complete, natural spoken narrative script for the presenter (50-100 words).

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "deck_title": "string",
  "target_audience": "string",
  "slides": [
    {{
      "slide_num": 1,
      "title": "string",
      "bullet_points": ["string"],
      "visual_diagram_concept": "string",
      "speaker_notes": "string"
    }}
  ]
}}"""

PRESENTATION_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "deck_title": "Emergency Threat Response: Apex IAM Gateway Exploitation",
  "target_audience": "Executive Leadership & SecOps Committee",
  "slides": [
    {
      "slide_num": 1,
      "title": "Executive Threat Overview",
      "bullet_points": [
        "Active zero-day CVE-2026-8891 discovered in IAM Gateways",
        "CVSS 9.8 critical severity rating with active exploitation",
        "Over 14,000 corporate identity servers exposed globally"
      ],
      "visual_diagram_concept": "Global exposure map highlighting affected financial and healthcare identity nodes",
      "speaker_notes": "Good morning. Over the last 24 hours our threat intelligence confirmed active in-the-wild exploitation of CVE-2026-8891 affecting our identity perimeter. We need leadership alignment on immediate containment."
    },
    {
      "slide_num": 2,
      "title": "Adversary Attack Chain",
      "bullet_points": [
        "Unauthenticated TLS handshake memory corruption on port 8443",
        "Adversary achieves domain controller takeover within 18 minutes",
        "Ransomware payload encrypts core databases via AES-256"
      ],
      "visual_diagram_concept": "Three-stage attack progression flowchart showing perimeter breach to DC takeover",
      "speaker_notes": "This diagram illustrates the rapid adversary timeline. Attackers abuse port 8443 and compromise domain controllers in under 18 minutes, deploying AES-256 ransomware unless halted upstream."
    },
    {
      "slide_num": 3,
      "title": "Immediate Containment Roadmap",
      "bullet_points": [
        "Drop all external WAN ingress to port 8443 immediately",
        "Deploy vendor Emergency Patch v5.1.4 across IAM fleet",
        "Execute automated threat hunt across reverse proxy logs"
      ],
      "visual_diagram_concept": "Firewall filter blocking port 8443 with verification checkmarks",
      "speaker_notes": "SecOps has prepared a 15-minute maintenance window tonight to roll out patch 5.1.4. In parallel, our edge firewalls are already dropping external traffic on port 8443."
    }
  ]
}
"""


def generate_presentation_deck(
    raw_text: str,
    tone: str = "Professional",
    target_audience: str = "General Public",
    objective: str = "Inform",
    detail_level: str = "Standard",
    model: str = "llama3.1"
) -> PresentationDeck:
    """Generates a PresentationDeck model validated against backend.schemas.PresentationDeck."""
    system_prompt = PRESENTATION_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into a 5-7 slide Presentation Deck. Ensure bullet points are strictly <= 15 words and full speaker notes are included.

{PRESENTATION_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return PresentationDeck.model_validate(json_dict)
