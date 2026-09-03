"""
Executive Summary Prompts Module.
Generates ExecutiveSummary artefacts containing BLUF (Bottom Line Up Front),
key takeaways, decision matrix, and strategic impact analysis.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .base_prompt import invoke_ollama, format_parameters


# =====================================================================
# Pydantic v2 Models
# =====================================================================

class DecisionOption(BaseModel):
    """Option in the executive decision matrix."""
    option_name: str = Field(description="Name of the strategic or operational choice")
    cost_or_downtime: str = Field(description="Estimated cost, resource commitment, or service downtime")
    residual_risk: str = Field(description="Level and nature of remaining risk (e.g. 'Low', 'High')")
    recommendation_status: str = Field(description="'Recommended', 'Alternative', or 'Not Advised'")
    rationale: str = Field(description="Brief justification for the leadership evaluation")


class ExecutiveSummary(BaseModel):
    """Structured deliverable for an Executive Summary."""
    document_title: str = Field(description="Executive briefing title")
    bluf: str = Field(description="Bottom Line Up Front: 1-2 punchy sentences stating the situation and core decision")
    key_takeaways: List[str] = Field(description="3 to 5 high-density, quantified executive takeaways")
    decision_matrix: List[DecisionOption] = Field(description="Structured trade-off matrix comparing actionable options")
    strategic_impact: List[str] = Field(description="Implications on organizational reputation, compliance, operations, or revenue")
    risk_assessment: str = Field(description="Overall risk summary (Probability vs. Business Impact)")


# =====================================================================
# Generator Function
# =====================================================================

def generate_executive_summary(
    source_content: str,
    parameters: Optional[Dict[str, Any]] = None,
    model: Optional[str] = None
) -> ExecutiveSummary:
    """
    Transforms source content into an ultra-dense C-Suite Executive Summary.
    Enforces BLUF upfront, quantified takeaways, decision matrix, and strategic impact.
    Parses and validates output using Pydantic's model_validate_json().
    """
    param_text = format_parameters(parameters)

    system_prompt = (
        "You are an executive chief of staff and corporate strategist. "
        "Transform the provided content into an ultra-dense, C-Suite ready Executive Summary. "
        "Strict rule: start with a crisp BLUF (Bottom Line Up Front) in 1-2 sentences. "
        "Provide quantified takeaways, an actionable decision matrix, and strategic business impact. "
        "You MUST respond ONLY with a parseable JSON object matching the requested schema."
    )

    prompt = f"""Generate a C-Suite Executive Summary based on the source content below.

CONFIGURABLE PARAMETERS:
{param_text}

EXECUTIVE REQUIREMENTS:
1. BLUF: Exactly 1-2 sentences at the absolute top stating situation and required leadership decision.
2. 3 to 5 Bulleted Key Takeaways with numbers and impact metrics.
3. Strategic Decision Matrix: Compare 2-3 options with cost/downtime, residual risk, and status.
4. Strategic Impact: High-level organizational and business consequences.
5. Risk Assessment: Overall risk rating and drivers.

SOURCE CONTENT:
{source_content}

Respond ONLY with a JSON object matching this exact schema:
{{
  "document_title": "string",
  "bluf": "string (1-2 sentences stating the core decision or outcome)",
  "key_takeaways": [
    "Quantified key takeaway 1",
    "Quantified key takeaway 2",
    "Quantified key takeaway 3"
  ],
  "decision_matrix": [
    {{
      "option_name": "Option A: Immediate Hotfix Deployment",
      "cost_or_downtime": "15-minute maintenance window",
      "residual_risk": "Near Zero",
      "recommendation_status": "Recommended",
      "rationale": "Neutralizes perimeter RCE vulnerability immediately"
    }},
    {{
      "option_name": "Option B: Upstream Port Isolation Only",
      "cost_or_downtime": "Zero downtime",
      "residual_risk": "High (Internal LAN threat)",
      "recommendation_status": "Alternative",
      "rationale": "Temporary stopgap only until patch can be scheduled"
    }}
  ],
  "strategic_impact": [
    "Prevents regulatory disclosure penalties under cybersecurity incident guidelines",
    "Eliminates lateral movement threat across enterprise subnetworks"
  ],
  "risk_assessment": "CRITICAL (Probability: High, Impact: Catastrophic without emergency mitigation)"
}}"""

    raw_json = invoke_ollama(prompt=prompt, system_prompt=system_prompt, model=model)
    return ExecutiveSummary.model_validate_json(raw_json)
