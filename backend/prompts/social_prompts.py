
---

### 2. `prompts/social_prompts.py`
**Deliverables:** 💼 **LinkedIn Post** & 🐦 **Twitter / X Thread**  
**Key Features:** LinkedIn hook before fold, bullet points with emojis, CTA, **Readability Score optimization (Grade 7–9)**, and Twitter thread with **strict `< 280 characters` limit validation**.

```python
"""
Social Media Prompts Module (LinkedIn & Twitter / X).
Generates prompts for:
1. Algorithm-optimized LinkedIn Posts with Readability Index scoring.
2. Twitter / X Threads with strict character-limit compliance (<280 chars per tweet).
"""

from typing import Optional, Dict, Any
from .base_prompt import BasePromptBuilder, TransformationParameters


class LinkedInPromptBuilder:
    """Builder for LinkedIn Post Prompts."""

    TASK_DESCRIPTION = """You are tasked with transforming the provided source content into a high-engagement, executive LinkedIn post.

Your generation must adhere to the following professional LinkedIn content architecture:
1. Attention-Grabbing Hook: The first 1-2 lines MUST be high-voltage and provoke curiosity before the desktop/mobile "...see more" fold. Avoid generic clichés.
2. Spacing & Visual Cadence: Use short paragraphs (1-2 sentences maximum) and white space to maximize readability on mobile feeds.
3. Core Value Body: Distill the primary findings, statistics, or threat intelligence into clean, scannable bullet points using strategic emojis (e.g., 🚨, 💡, 📊, ⚡, 🔍).
4. Critical Takeaway / Bold Callout: A 1-sentence synthesis emphasizing business or operational impact.
5. Engaging Closing Question & CTA: An open-ended, thought-provoking question that prompts comments, peer debate, and organic algorithm distribution.
6. Industry Hashtags: 4–6 highly targeted, active industry hashtags (e.g., #CyberSecurity #TechLeadership #Innovation #DevSecOps).
7. Readability Index Optimization (KEY DIFFERENTIATOR): Craft the prose to hit an optimal readability score (target: Flesch-Kincaid Grade 7–9 or reading ease 65-75). Provide an estimated Readability Score and Read Time estimate."""

    JSON_SCHEMA_INSTRUCTION = """Provide your response as a strictly valid JSON object matching this schema:
```json
{
  "hook": "string (the first 1-2 lines designed to appear before the 'see more' fold)",
  "body_paragraphs": ["string"],
  "bullet_points": [
    {
      "emoji": "string",
      "bold_header": "string",
      "text": "string"
    }
  ],
  "bold_takeaway": "string",
  "closing_cta_question": "string",
  "hashtags": ["string"],
  "full_formatted_text": "string (the complete, copy-paste ready LinkedIn post)",
  "analytics_optimization": {
    "estimated_reading_time_seconds": 45,
    "flesch_reading_ease_score": 72,
    "readability_grade_level": "Grade 8 (High Engagement)",
    "algorithm_hooks_used": ["High-contrast opening", "Scannable bullets", "Comment-inducing closing question"]
  }
}
