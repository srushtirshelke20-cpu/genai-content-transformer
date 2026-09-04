"""
Executive Summary Prompts Module.
Generates ultra-dense C-Suite executive briefings with BLUF, key findings,
strategic implications, and recommended decisions.
Strictly validates against backend.schemas.ExecutiveSummary.
"""

from typing import Dict, Any, Optional
from backend.schemas import ExecutiveSummary
from .base_prompt import call_ollama_json


SUMMARY_SYSTEM_PROMPT = """You are an executive chief of staff and corporate intelligence strategist.
Transform the provided source content into an ultra-dense, C-Suite ready Executive Summary.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. bluf: Bottom Line Up Front - exactly 1 to 2 crisp, high-impact sentences stating the core issue and required leadership decision.
2. key_findings: List of 3 to 5 high-density, quantified takeaways with metrics, exposure numbers, or timelines.
3. strategic_implications: 2 to 3 sentences analyzing business, compliance, brand, or operational consequences.
4. recommended_decision: Unambiguous, actionable directive for leadership (e.g. authorize emergency downtime, approve patch deployment).

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "bluf": "string (1-2 punchy sentences)",
  "key_findings": ["string"],
  "strategic_implications": "string",
  "recommended_decision": "string"
}}"""

SUMMARY_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "bluf": "An active zero-day RCE flaw in Apex IAM Gateways requires authorizing an immediate 15-minute emergency maintenance window tonight to deploy Emergency Patch v5.1.4 and avoid critical ransomware compromise.",
  "key_findings": [
    "Vulnerability CVE-2026-8891 carries a maximum CVSS 9.8 critical severity rating.",
    "Over 14,000 corporate identity servers are exposed with active in-the-wild exploitation.",
    "Average lateral movement from initial perimeter breach to domain controller takeover is 18 minutes.",
    "Emergency patch v5.1.4 is available and successfully tested for fleet-wide rollout."
  ],
  "strategic_implications": "Unpatched exposure risks complete enterprise data exfiltration, database ransomware encryption, and severe regulatory reporting penalties under cybersecurity incident disclosure mandates.",
  "recommended_decision": "Authorize SecOps to enforce immediate external firewall drops on port 8443 and execute fleet-wide deployment of Emergency Patch v5.1.4 during tonight's 23:30 maintenance window."
}
"""


def generate_executive_summary(
    raw_text: str,
    tone: str = "Authoritative",
    target_audience: str = "C-Suite",
    objective: str = "Alert",
    detail_level: str = "Brief",
    model: str = "llama3.1"
) -> ExecutiveSummary:
    """Generates an ExecutiveSummary model validated against backend.schemas.ExecutiveSummary."""
    system_prompt = SUMMARY_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into an Executive Summary.

{SUMMARY_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return ExecutiveSummary.model_validate(json_dict)
