"""
Orchestration Module for Content Transformation Pipeline.
Implements transform_content(request: TransformRequest) -> TransformResponse
mapping selected_formats to specific generators and validating strictly against backend.schemas.
"""

import logging
import os
from typing import Dict, Any, Optional
from backend.schemas import (
    TransformRequest,
    TransformResponse,
    LinkedInPost,
    TwitterThread,
    Advisory,
    PresentationDeck,
    VideoPackage,
    InfographicPlan,
    ExecutiveSummary,
)
from .social_prompts import generate_linkedin_post, generate_twitter_thread
from .advisory_prompts import generate_advisory
from .presentation_prompts import generate_presentation_deck
from .video_prompts import generate_video_package
from .infographic_prompts import generate_infographic_plan
from .summary_prompts import generate_executive_summary

logger = logging.getLogger(__name__)
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


def _derive_project_title(raw_text: str, response_fields: Dict[str, Any]) -> str:
    """Derives a sensible project title from generated deliverables or raw text header."""
    if "advisory" in response_fields and response_fields["advisory"]:
        return response_fields["advisory"].title
    if "presentation_deck" in response_fields and response_fields["presentation_deck"]:
        return response_fields["presentation_deck"].deck_title
    if "video_package" in response_fields and response_fields["video_package"]:
        return response_fields["video_package"].title
    if "infographic_plan" in response_fields and response_fields["infographic_plan"]:
        return response_fields["infographic_plan"].main_title

    # Fallback to first non-empty line of source text
    for line in raw_text.splitlines():
        line = line.strip().lstrip("#").strip()
        if line and len(line) > 5:
            return line[:80]
    return "Automated Content Transformation"


def transform_content(
    request: TransformRequest,
    model: str = DEFAULT_MODEL
) -> TransformResponse:
    """
    Main orchestration function for multi-artefact content transformation.

    Inspects request.selected_formats, invokes the corresponding generator for each format,
    validates returned JSON against Pydantic models in backend.schemas,
    and returns a consolidated TransformResponse.

    Args:
        request: TransformRequest containing raw_text, parameters, and selected_formats.
        model: Ollama model name (default from env or llama3.1).

    Returns:
        TransformResponse populated with validated deliverables.
    """
    raw_text = request.raw_text
    tone = request.tone
    target_audience = request.target_audience
    objective = request.objective
    detail_level = request.detail_level

    # Normalize format keys
    normalized_formats = {
        fmt.strip().lower().replace(" ", "_").replace("-", "_")
        for fmt in request.selected_formats
    }

    response_dict: Dict[str, Any] = {}

    # 1. Video Package
    if "video" in normalized_formats or "video_package" in normalized_formats:
        try:
            logger.info("Generating Video Package...")
            response_dict["video_package"] = generate_video_package(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Video Package: {e}")

    # 2. LinkedIn Post
    if "linkedin" in normalized_formats or "linkedin_post" in normalized_formats:
        try:
            logger.info("Generating LinkedIn Post...")
            response_dict["linkedin_post"] = generate_linkedin_post(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate LinkedIn Post: {e}")

    # 3. Twitter / X Thread
    if "twitter" in normalized_formats or "twitter_thread" in normalized_formats or "x" in normalized_formats:
        try:
            logger.info("Generating Twitter/X Thread...")
            response_dict["twitter_thread"] = generate_twitter_thread(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Twitter/X Thread: {e}")

    # 4. Formal Advisory
    if "advisory" in normalized_formats or "structured_advisory" in normalized_formats:
        try:
            logger.info("Generating Advisory...")
            response_dict["advisory"] = generate_advisory(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Advisory: {e}")

    # 5. Infographic Plan
    if "infographic" in normalized_formats or "infographic_plan" in normalized_formats or "infographic_blueprint" in normalized_formats:
        try:
            logger.info("Generating Infographic Plan...")
            response_dict["infographic_plan"] = generate_infographic_plan(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Infographic Plan: {e}")

    # 6. Executive Summary
    if "executive_summary" in normalized_formats or "summary" in normalized_formats or "exec_summary" in normalized_formats:
        try:
            logger.info("Generating Executive Summary...")
            response_dict["executive_summary"] = generate_executive_summary(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Executive Summary: {e}")

    # 7. Presentation Deck
    if "presentation" in normalized_formats or "presentation_deck" in normalized_formats or "slides" in normalized_formats:
        try:
            logger.info("Generating Presentation Deck...")
            response_dict["presentation_deck"] = generate_presentation_deck(
                raw_text=raw_text,
                tone=tone,
                target_audience=target_audience,
                objective=objective,
                detail_level=detail_level,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to generate Presentation Deck: {e}")

    # Build and validate consolidated TransformResponse
    project_title = _derive_project_title(raw_text, response_dict)
    response_dict["project_title"] = project_title

    return TransformResponse.model_validate(response_dict)


# Backwards compatibility alias
generate_artefacts = transform_content
