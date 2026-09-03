"""
Artefact Transformation Orchestrator.
Main entrypoint for coordinating multi-deliverable generation:
generate_artefacts(request: TransformRequest) -> TransformResponse
"""

import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from .social_prompts import (
    LinkedInPost,
    TwitterThread,
    generate_linkedin_post,
    generate_twitter_thread,
)
from .advisory_prompts import Advisory, generate_advisory
from .presentation_prompts import PresentationDeck, generate_presentation_deck
from .video_prompts import VideoPackage, generate_video_package
from .infographic_prompts import InfographicPlan, generate_infographic_plan
from .summary_prompts import ExecutiveSummary, generate_executive_summary

logger = logging.getLogger(__name__)


# =====================================================================
# Request / Response Models
# =====================================================================

class TransformRequest(BaseModel):
    """
    Input request for content transformation.
    Specifies source content, selected deliverables, and optional parameter matrix.
    """
    source_content: str = Field(description="Raw source text, document excerpt, or incident notes")
    artefacts: List[str] = Field(
        description=(
            "List of requested artefact identifiers: "
            "['linkedin', 'twitter', 'advisory', 'presentation', 'video', 'infographic', 'summary']"
        )
    )
    parameters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Configurable parameters: target_audience, tone, language, detail_level, objective"
    )
    model: Optional[str] = Field(
        default=None,
        description="Target Ollama model identifier (defaults to llama3.1:latest)"
    )


class TransformResponse(BaseModel):
    """
    Consolidated output containing all requested deliverables parsed via Pydantic v2.
    """
    linkedin_post: Optional[LinkedInPost] = Field(default=None, description="Generated LinkedIn post deliverable")
    twitter_thread: Optional[TwitterThread] = Field(default=None, description="Generated Twitter/X thread deliverable")
    advisory: Optional[Advisory] = Field(default=None, description="Generated Formal Advisory deliverable")
    presentation_deck: Optional[PresentationDeck] = Field(default=None, description="Generated Presentation Deck deliverable")
    video_package: Optional[VideoPackage] = Field(default=None, description="Generated Video Production Package deliverable")
    infographic_plan: Optional[InfographicPlan] = Field(default=None, description="Generated Infographic Blueprint deliverable")
    executive_summary: Optional[ExecutiveSummary] = Field(default=None, description="Generated Executive Summary deliverable")
    errors: Optional[Dict[str, str]] = Field(default=None, description="Per-artefact generation error details if any failed")


# =====================================================================
# Orchestrator Function
# =====================================================================

def generate_artefacts(request: TransformRequest) -> TransformResponse:
    """
    Coordinates multi-deliverable generation:
    1. Inspects request.artefacts list.
    2. Calls the respective generator functions with source content and parameters.
    3. Validates and parses each LLM output using Pydantic's model_validate_json().
    4. Collects results and any errors into a unified TransformResponse.

    Args:
        request: TransformRequest containing source content, requested artefacts, and parameters.

    Returns:
        TransformResponse populated with validated Pydantic model instances.
    """
    response_kwargs: Dict[str, Any] = {}
    errors: Dict[str, str] = {}

    # Normalize requested artefact keys
    requested_set = {a.strip().lower().replace(" ", "_").replace("-", "_") for a in request.artefacts}

    # 1. 💼 LinkedIn Post
    if "linkedin" in requested_set or "linkedin_post" in requested_set:
        try:
            response_kwargs["linkedin_post"] = generate_linkedin_post(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating LinkedIn post: {e}")
            errors["linkedin_post"] = str(e)

    # 2. 🐦 Twitter / X Thread
    if "twitter" in requested_set or "twitter_thread" in requested_set or "x" in requested_set or "x_thread" in requested_set:
        try:
            response_kwargs["twitter_thread"] = generate_twitter_thread(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Twitter thread: {e}")
            errors["twitter_thread"] = str(e)

    # 3. 🛡️ Formal Advisory
    if "advisory" in requested_set or "formal_advisory" in requested_set:
        try:
            response_kwargs["advisory"] = generate_advisory(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Advisory: {e}")
            errors["advisory"] = str(e)

    # 4. 📽️ Presentation Deck
    if "presentation" in requested_set or "presentation_deck" in requested_set or "deck" in requested_set or "slides" in requested_set:
        try:
            response_kwargs["presentation_deck"] = generate_presentation_deck(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Presentation Deck: {e}")
            errors["presentation_deck"] = str(e)

    # 5. 🎬 Video Package
    if "video" in requested_set or "video_package" in requested_set:
        try:
            response_kwargs["video_package"] = generate_video_package(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Video Package: {e}")
            errors["video_package"] = str(e)

    # 6. 📊 Infographic Blueprint
    if "infographic" in requested_set or "infographic_plan" in requested_set or "blueprint" in requested_set:
        try:
            response_kwargs["infographic_plan"] = generate_infographic_plan(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Infographic Plan: {e}")
            errors["infographic_plan"] = str(e)

    # 7. 📑 Executive Summary
    if "summary" in requested_set or "executive_summary" in requested_set or "exec_summary" in requested_set:
        try:
            response_kwargs["executive_summary"] = generate_executive_summary(
                source_content=request.source_content,
                parameters=request.parameters,
                model=request.model,
            )
        except Exception as e:
            logger.error(f"Failed generating Executive Summary: {e}")
            errors["executive_summary"] = str(e)

    if errors:
        response_kwargs["errors"] = errors

    return TransformResponse(**response_kwargs)
