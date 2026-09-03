"""
Prompts Package - Gen AI Content Transformation Engine.
Role: Member 3 Subsystem.

Exports:
- Base prompt builders & TransformationParameters matrix.
- 🎬 Video Package prompt builders.
- 💼 LinkedIn & 🐦 Twitter/X prompt builders.
- 🛡️ Formal Advisory & 📑 Executive Summary prompt builders.
- 📊 Infographic Blueprint prompt builders.
- 📽️ Presentation Deck prompt builders (.pptx ready).
"""

from .base_prompt import BasePromptBuilder, TransformationParameters
from .video_prompts import VideoPromptBuilder, build_video_package_prompt
from .social_prompts import (
    LinkedInPromptBuilder,
    TwitterThreadPromptBuilder,
    build_linkedin_prompt,
    build_twitter_thread_prompt,
)
from .advisory_prompts import (
    FormalAdvisoryPromptBuilder,
    ExecutiveSummaryPromptBuilder,
    build_formal_advisory_prompt,
    build_executive_summary_prompt,
)
from .infographic_prompts import (
    InfographicPromptBuilder,
    build_infographic_blueprint_prompt,
)
from .presentation_prompts import (
    PresentationDeckPromptBuilder,
    build_presentation_deck_prompt,
)

__all__ = [
    # Parameters & Base
    "TransformationParameters",
    "BasePromptBuilder",
    # Deliverable 1: Video Package
    "VideoPromptBuilder",
    "build_video_package_prompt",
    # Deliverable 2 & 3: Social Media (LinkedIn & Twitter/X)
    "LinkedInPromptBuilder",
    "build_linkedin_prompt",
    "TwitterThreadPromptBuilder",
    "build_twitter_thread_prompt",
    # Deliverable 4 & 6: Advisory & Executive Summary
    "FormalAdvisoryPromptBuilder",
    "build_formal_advisory_prompt",
    "ExecutiveSummaryPromptBuilder",
    "build_executive_summary_prompt",
    # Deliverable 5: Infographic Blueprint
    "InfographicPromptBuilder",
    "build_infographic_blueprint_prompt",
    # Deliverable 7: Presentation Deck
    "PresentationDeckPromptBuilder",
    "build_presentation_deck_prompt",
]
