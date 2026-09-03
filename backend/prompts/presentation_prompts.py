
---

### 5. `prompts/presentation_prompts.py`
**Deliverable:** 📽️ **Presentation Deck**  
**Key Features:** 5–7 slide structure: Slide Title (<8 words), concise bullets (<15 words each), visual recommendations, and **complete conversational Speaker Notes** ready for `.pptx` generation with `python-pptx`.

```python
"""
Presentation Deck Prompts Module.
Generates prompts for 5–7 slide presentation decks structured for:
1. High-impact visual presentations (concise bullets, visual recommendations).
2. Complete, conversational Speaker Notes for the presenter.
3. Direct automated compilation into native Microsoft PowerPoint (.pptx) files via python-pptx.
"""

from typing import Optional, Dict, Any
from .base_prompt import BasePromptBuilder, TransformationParameters


class PresentationDeckPromptBuilder:
    """Builder for Presentation Deck Prompts."""

    TASK_DESCRIPTION = """You are tasked with transforming the provided source content into an executive 5 to 7 slide Presentation Deck.

CRITICAL SLIDE DESIGN CONSTRAINTS (FOR POWERPOINT COMPILATION):
1. Slide Deck Structure (typically 5 to 7 sequential slides):
   - Slide 1: Title Slide (Executive presentation title, descriptive subtitle, presenter/audience tag).
   - Slide 2: Problem Statement / Context / The Current State.
   - Slide 3: Deep Dive / Core Findings / Technical or Strategic Mechanism.
   - Slide 4: Data & Impact Analysis (Metrics, benchmark comparisons, financial/operational risk).
   - Slide 5: Strategic Action Plan / Remediation Roadmap (Phase 1, Phase 2, Timeline).
   - Slide 6: Summary / Business Outcomes / Leadership Decision.
   - Optional Slide 7: Next Steps / Governance & Q&A.

2. Slide Content Constraints (MAXIMUM BREVITY):
   - Slide Title: Action-oriented, executive headline (< 8 words).
   - Bullet Points: Exactly 3 to 4 concise bullet points per slide.
   - Word Count Constraint: STRICT MAXIMUM of 15 words per bullet point. Slides must never contain walls of text.

3. Visual / Chart Recommendation:
   - Provide explicit instructions for the graphic designer or charting engine (e.g., 'Two-bar comparison chart showing 68% memory reduction', 'Architecture block diagram with firewall filter callout', 'Gantt timeline spanning 30 days').

4. Complete Conversational Speaker Notes (KEY DIFFERENTIATOR):
   - Provide complete, natural spoken narration for the presenter (approx. 60–100 words per slide).
   - Written in first-person spoken cadence (e.g., 'Good morning. On this slide, we are looking at...').
   - Includes conversational transitions to the next slide."""

    JSON_SCHEMA_INSTRUCTION = """Provide your response as a strictly valid JSON object matching this schema (engineered for python-pptx ingestion):
```json
{
  "deck_title": "string",
  "subtitle": "string",
  "total_slides": 6,
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "title_slide",
      "title": "string",
      "subtitle": "string",
      "bullet_points": [],
      "visual_recommendation": "Full-bleed dark background with corporate crest",
      "speaker_notes": "string (verbatim spoken script for presenter)"
    },
    {
      "slide_number": 2,
      "slide_type": "content_slide",
      "title": "string (<8 words)",
      "bullet_points": [
        "string (<15 words per bullet)",
        "string (<15 words per bullet)",
        "string (<15 words per bullet)"
      ],
      "visual_recommendation": "string (description of chart/diagram)",
      "speaker_notes": "string (verbatim spoken script for presenter)"
    }
  ],
  "presentation_metadata": {
    "target_aspect_ratio": "16:9",
    "theme_palette": {
      "accent_color": "#2563eb",
      "slide_bg": "#0f172a"
    }
  }
}
