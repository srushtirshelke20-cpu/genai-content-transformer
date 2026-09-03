
---

### 3. `prompts/advisory_prompts.py`
**Deliverables:** 🛡️ **Formal Advisory** & 📑 **Executive Summary**  
**Key Features:** Formal header (Advisory ID, Date, Severity Level), Context, Impact, 3-stage Action Plan, plus **BLUF (Bottom Line Up Front)**, 3–5 bulleted takeaways, and **Strategic Decision Matrix**.

```python
"""
Advisory and Executive Summary Prompts Module.
Generates prompts for:
1. Formal Advisories (Compliance, Cyber Threat, Policy) with document headers, severity classification, and actionable runbooks.
2. Executive Summaries with BLUF (Bottom Line Up Front), key takeaways, decision matrix, and risk assessments.
"""

from typing import Optional, Dict, Any
from .base_prompt import BasePromptBuilder, TransformationParameters


class FormalAdvisoryPromptBuilder:
    """Builder for Formal Advisory Prompts."""

    TASK_DESCRIPTION = """You are tasked with transforming the provided source content into a Formal Official Advisory suitable for enterprise security, compliance, legal, or policy dissemination.

Your generation must strictly follow this formal advisory structure:
1. Formal Document Header:
   - Advisory Identifier: A standardized unique reference (e.g., ADV-2026-XXXX or SEC-ADV-[CVE/REF]).
   - Release Date & Revision Version (e.g., September 02, 2026 | Rev 1.0).
   - Severity / Priority Level: CRITICAL (CVSS 9.0+), HIGH (7.0-8.9), MEDIUM (4.0-6.9), or INFORMATIONAL.
   - Classification & Handling: (e.g., TLP:CLEAR / PUBLIC / INTERNAL RESTRICTED).
2. Executive Overview & BLUF:
   - A concise 2-3 sentence statement explaining the essence of the advisory.
3. Context & Background:
   - Detailed description of the event, vulnerability, regulatory update, or incident origin.
4. Impact & Blast Radius Analysis:
   - Clear breakdown of potential harm: operational downtime, financial exposure, compliance penalties, or data loss.
5. Affected Systems, Assets, or Target Audiences:
   - Explicit list of software versions, hardware models, departments, or customer segments impacted.
6. Recommended Action Plan (Structured Multi-Stage Runbook):
   - Immediate Mitigations (Workarounds, firewall drops, urgent halts to be executed within hours).
   - Long-Term Remediation (Permanent patching, architectural refactoring, policy implementation).
   - Audit & Verification Steps (Specific commands, queries, or logs to inspect to verify safety).
7. References & Authority Contacts:
   - Official CVE, vendor advisory, regulatory references, and response team contact info."""

    JSON_SCHEMA_INSTRUCTION = """Provide your response as a strictly valid JSON object matching this schema:
```json
{
  "document_header": {
    "advisory_id": "string",
    "release_date": "string",
    "revision": "1.0",
    "severity_level": "CRITICAL | HIGH | MEDIUM | INFORMATIONAL",
    "cvss_score": "optional string e.g. 9.8",
    "classification": "TLP:CLEAR"
  },
  "title": "string",
  "executive_bluf": "string",
  "background_and_context": "string",
  "impact_analysis": {
    "summary": "string",
    "business_risk": "string",
    "technical_blast_radius": "string"
  },
  "affected_scope": {
    "systems_or_assets": ["string"],
    "target_audiences": ["string"]
  },
  "action_plan": {
    "immediate_mitigations": [
      {
        "step_number": 1,
        "action": "string",
        "command_or_config": "optional string",
        "timeframe": "Immediate (< 2 hours)"
      }
    ],
    "long_term_remediation": [
      {
        "step_number": 1,
        "action": "string",
        "milestone": "string"
      }
    ],
    "audit_and_verification": [
      {
        "verification_check": "string",
        "expected_result": "string"
      }
    ]
  },
  "references": ["string"]
}
