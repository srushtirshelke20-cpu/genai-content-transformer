"""
backend.prompts Package.
LLM prompt generation and orchestration pipeline for Gen AI Content Transformation Engine.
"""

from .base_prompt import client, call_ollama_json
from .social_prompts import generate_linkedin_post, generate_twitter_thread
from .advisory_prompts import generate_advisory
from .presentation_prompts import generate_presentation_deck
from .video_prompts import generate_video_package
from .infographic_prompts import generate_infographic_plan
from .summary_prompts import generate_executive_summary
from .orchestrator import transform_content, generate_artefacts

__all__ = [
    "client",
    "call_ollama_json",
    "generate_linkedin_post",
    "generate_twitter_thread",
    "generate_advisory",
    "generate_presentation_deck",
    "generate_video_package",
    "generate_infographic_plan",
    "generate_executive_summary",
    "transform_content",
    "generate_artefacts",
]
