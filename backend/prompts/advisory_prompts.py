"""
Structured Advisory Prompts Module.
Enforces severe/formal tone, threat context, and structured mitigation steps.
Strictly validates against backend.schemas.Advisory.
"""

from typing import Dict, Any, Optional
from backend.schemas import Advisory
from .base_prompt import call_ollama_json


ADVISORY_SYSTEM_PROMPT = """You are an elite Cyber Threat Intelligence and Enterprise Compliance Officer.
Transform the provided source content into an official, severe, and structured Advisory.
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. advisory_id: Standard reference identifier (e.g., ADV-2026-XXXX or SEC-ADV-[CVE]).
2. severity_level: MUST STRICTLY BE ONE OF: "LOW", "MEDIUM", "HIGH", or "CRITICAL".
3. date_issued: Today's date or date from source (e.g. "September 3, 2026").
4. target_audience_or_systems: Explicit list or description of vulnerable hardware, software, or organizations.
5. threat_or_context_summary: Concise explanation of the exploit vector, flaw mechanism, or incident context.
6. impact_analysis: Rigorous breakdown of technical blast radius, data loss risk, and financial/business exposure.
7. immediate_actions: List of 2 to 4 urgent actions to be executed within 0-4 hours (firewall rules, patches, port isolation).
8. long_term_recommendations: List of 2 to 4 strategic recommendations (zero trust, MFA, architectural upgrades).

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "advisory_id": "string",
  "severity_level": "CRITICAL",
  "date_issued": "string",
  "target_audience_or_systems": "string",
  "threat_or_context_summary": "string",
  "impact_analysis": "string",
  "immediate_actions": ["string"],
  "long_term_recommendations": ["string"]
}}"""

ADVISORY_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "advisory_id": "ADV-2026-8891",
  "severity_level": "CRITICAL",
  "date_issued": "September 3, 2026",
  "target_audience_or_systems": "Enterprise Identity and Access Management (IAM) Gateways v4.2 - v5.1; SecOps & Infrastructure Teams",
  "threat_or_context_summary": "A critical CVSS 9.8 remote code execution flaw in Apex IAM Gateway allows unauthenticated remote adversaries to abuse TLS handshake memory corruption and inject ransomware payloads.",
  "impact_analysis": "Active weaponization exposes over 14,000 corporate identity servers globally. Lateral movement to full domain controller takeover occurs within 18 minutes, resulting in unauthorized customer data exfiltration and AES-256 database volume encryption.",
  "immediate_actions": [
    "Immediately isolate external WAN access to port 8443 on border firewalls.",
    "Deploy vendor Emergency Patch v5.1.4 released today across all IAM clusters.",
    "Inspect reverse proxy logs for anomalous POST requests containing binary strings in Authorization headers."
  ],
  "long_term_recommendations": [
    "Implement zero-trust certificate pinning across all edge routing infrastructure.",
    "Enforce hardware-backed FIDO2 / MFA authentication keys enterprise-wide.",
    "Conduct a comprehensive lateral threat hunt across internal subnets for residual adversary presence."
  ]
}
"""


def generate_advisory(
    raw_text: str,
    tone: str = "Urgent",
    target_audience: str = "Technical",
    objective: str = "Alert",
    detail_level: str = "Comprehensive",
    model: str = "llama3.1"
) -> Advisory:
    """Generates an Advisory model validated against backend.schemas.Advisory."""
    system_prompt = ADVISORY_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into a Formal Advisory.

{ADVISORY_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return Advisory.model_validate(json_dict)
