
---

### 4. `prompts/infographic_prompts.py`
**Deliverable:** 📊 **Infographic Blueprint**  
**Key Features:** Hero statistic callout banner, 3 comparison/pillar columns, designer icon recommendations (FontAwesome), and **executable Mermaid.js flowchart syntax** (`graph LR`/`TD`).

```python
"""
Infographic Blueprint Prompt Module.
Generates prompts for structural visual layouts:
- Hero statistics
- 3 Comparison / Pillar columns
- Workflow diagram instructions formatted in valid Mermaid.js flowchart syntax and SVG
- Key metric callout badges
- Icon suggestions for human graphic designers
"""

from typing import Optional, Dict, Any
from .base_prompt import BasePromptBuilder, TransformationParameters


class InfographicPromptBuilder:
    """Builder for Infographic Blueprint Prompts."""

    TASK_DESCRIPTION = """You are tasked with transforming the provided source content into an Infographic Blueprint & Visual Wireframe.

This blueprint serves dual purposes:
1. It provides a visual design blueprint for UI graphic designers.
2. It generates valid, executable diagram code (Mermaid.js flowchart / SVG) that can be automatically rendered inline in web browsers.

Your generation must include the following structural components:
1. Infographic Header:
   - Primary Headline & Explanatory Subtitle.
   - Recommended Visual Color Palette (Primary, Secondary, Accent, Background HEX codes).
2. Hero Statistic Banner:
   - The single most jaw-dropping, critical statistic, percentage, or metric from the source content (e.g., '45 MIN' or '68% DROP').
   - Descriptive sub-label explaining the significance of the hero metric.
3. Three-Column Pillar Grid (Comparison or Progression):
   - Column 1: Problem / Threat / Baseline / Legacy State.
   - Column 2: Mechanism / Architecture / Active Vector.
   - Column 3: Solution / Remediation / Future State.
   Each column must include a title, key takeaway, and suggested icon name.
4. Workflow Diagram in Valid Mermaid.js Syntax (KEY DIFFERENTIATOR):
   - You MUST write a clean, syntactically valid Mermaid.js flowchart (`graph TD` or `graph LR`).
   - Use standard Mermaid nodes: `A[Label] --> B(Process) --> C{Decision}`.
   - Do NOT include syntax errors, unquoted parentheses inside brackets, or complex styling that breaks the Mermaid parser.
5. Key Metrics Callout Bar:
   - 3 to 4 secondary micro-metrics with icons (e.g., CVSS Score, Memory Bandwidth, SLA hours).
6. Designer Icon & Asset Guide:
   - Explicit FontAwesome or Lucide icon names for each section (e.g., 'fa-shield-halved', 'fa-bolt', 'fa-server') to guide visual artists."""

    JSON_SCHEMA_INSTRUCTION = """Provide your response as a strictly valid JSON object matching this schema:
```json
{
  "infographic_title": "string",
  "subtitle": "string",
  "visual_theme": {
    "recommended_palette": {
      "primary_color": "#2563eb",
      "accent_color": "#ef4444",
      "background_color": "#0f172a",
      "text_color": "#ffffff"
    },
    "mood": "string"
  },
  "hero_statistic": {
    "metric_value": "string (e.g. 45 MIN)",
    "label": "string",
    "context": "string"
  },
  "three_column_grid": {
    "column_1": {
      "header": "string",
      "bullet_points": ["string"],
      "suggested_icon": "string"
    },
    "column_2": {
      "header": "string",
      "bullet_points": ["string"],
      "suggested_icon": "string"
    },
    "column_3": {
      "header": "string",
      "bullet_points": ["string"],
      "suggested_icon": "string"
    }
  },
  "mermaid_diagram": {
    "diagram_type": "flowchart",
    "mermaid_syntax": "graph LR\\n  A[Source / Ingress] --> B(Analysis / API)\\n  B --> C{Decision / Filter}\\n  C -->|Alert| D[Immediate Action]"
  },
  "secondary_metrics": [
    {
      "value": "string",
      "label": "string",
      "icon": "string"
    }
  ],
  "designer_notes": [
    "string"
  ]
}
