"""
Infographic Plan Prompts Module.
Generates InfographicPlan artefacts with hero statistics, layout architecture,
and sectional breakdowns with visual icon recommendations.
Strictly validates against backend.schemas.InfographicPlan.
"""

from typing import Dict, Any, Optional
from backend.schemas import InfographicPlan
from .base_prompt import call_ollama_json


INFOGRAPHIC_SYSTEM_PROMPT = """You are an information architect and visual infographics designer.
Transform the provided source content into an Infographic Plan and blueprint.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. main_title: Captivating, bold infographic headline.
2. hero_statistic: The single most impactful statistic or metric callout (e.g. "14,000 EXPOSED" or "18 MINS").
3. layout_style: Must specify structural layout (e.g., "3-Column Comparison", "Sequential Threat Timeline", or "Perimeter Defense Hierarchy").
4. sections: An ordered list of 3 to 5 InfographicItem objects:
   - stat_or_icon: A key micro-metric, percentage, or FontAwesome/Lucide icon string (e.g., "fa-shield-halved", "9.8 CVSS", "Port 8443").
   - heading: Section or pillar title.
   - description: 1-2 concise descriptive sentences.
5. color_palette_recommendation: List of 3 to 5 HEX color codes with brief descriptive names (e.g. ["#EF4444 (Critical Red)", "#1E293B (Dark Slate)", "#3B82F6 (Action Blue)"]).

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "main_title": "string",
  "hero_statistic": "string",
  "layout_style": "3-Column Comparison",
  "sections": [
    {{
      "stat_or_icon": "string",
      "heading": "string",
      "description": "string"
    }}
  ],
  "color_palette_recommendation": ["string"]
}}"""

INFOGRAPHIC_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "main_title": "Anatomy of the Apex IAM Gateway Zero-Day Exploit",
  "hero_statistic": "14,000+ SERVERS EXPOSED",
  "layout_style": "3-Column Comparison",
  "sections": [
    {
      "stat_or_icon": "fa-bug",
      "heading": "1. Ingress Vulnerability",
      "description": "Unauthenticated attackers exploit TLS handshake memory corruption on port 8443 to achieve remote code execution."
    },
    {
      "stat_or_icon": "18 MINS",
      "heading": "2. Blast Radius & Exfiltration",
      "description": "Adversaries escalate to domain controller administrative privileges within 18 minutes, deploying AES-256 ransomware."
    },
    {
      "stat_or_icon": "fa-shield-halved",
      "heading": "3. Immediate Containment",
      "description": "Isolate port 8443 upstream on border firewalls and deploy vendor Emergency Patch v5.1.4 immediately."
    }
  ],
  "color_palette_recommendation": [
    "#EF4444 (Emergency Red)",
    "#0F172A (Midnight Slate Background)",
    "#3B82F6 (Remediation Blue)",
    "#10B981 (Verified Green)"
  ]
}
"""


def generate_infographic_plan(
    raw_text: str,
    tone: str = "Professional",
    target_audience: str = "General Public",
    objective: str = "Inform",
    detail_level: str = "Standard",
    model: str = "llama3.1"
) -> InfographicPlan:
    """Generates an InfographicPlan model validated against backend.schemas.InfographicPlan."""
    system_prompt = INFOGRAPHIC_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into an Infographic Plan.

{INFOGRAPHIC_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return InfographicPlan.model_validate(json_dict)
