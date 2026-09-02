# backend/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

# ==========================================
# 1. INPUT REQUEST PAYLOAD
# ==========================================
class TransformRequest(BaseModel):
    raw_text: str = Field(..., description="Extracted text from uploaded doc or input box")
    target_audience: str = Field("General Public", description="e.g., C-Suite, Technical, General Public")
    tone: str = Field("Professional", description="e.g., Urgent, Authoritative, Conversational, Technical")
    objective: str = Field("Inform", description="e.g., Inform, Alert, Educate, Sell")
    detail_level: str = Field("Standard", description="Brief, Standard, or Comprehensive")
    selected_formats: List[str] = Field(
        default=["linkedin", "twitter", "advisory", "executive_summary", "presentation", "video_package", "infographic"],
        description="List of artefacts requested by the operator"
    )

# ==========================================
# 2. OUTPUT ARTEFACT SCHEMAS
# ==========================================

# 2.1 Video Package
class VideoScene(BaseModel):
    scene_num: int
    duration_seconds: int
    visual_description: str
    narration_script: str
    on_screen_text: str
    ai_image_prompt: str

class VideoPackage(BaseModel):
    title: str
    target_duration: str
    background_music_vibe: str
    scenes: List[VideoScene]

# 2.2 LinkedIn Post
class LinkedInPost(BaseModel):
    hook: str
    body_paragraphs: List[str]
    bullet_points: List[str]
    call_to_action: str
    hashtags: List[str]

# 2.3 Twitter / X Thread
class Tweet(BaseModel):
    tweet_num: int
    text: str = Field(..., max_length=280)
    suggested_media_type: Optional[str] = "None"

class TwitterThread(BaseModel):
    thread_hook: str
    tweets: List[Tweet]

# 2.4 Structured Advisory
class Advisory(BaseModel):
    advisory_id: str
    severity_level: str = Field(..., description="LOW, MEDIUM, HIGH, or CRITICAL")
    date_issued: str
    target_audience_or_systems: str
    threat_or_context_summary: str
    impact_analysis: str
    immediate_actions: List[str]
    long_term_recommendations: List[str]

# 2.5 Infographic Blueprint
class InfographicItem(BaseModel):
    stat_or_icon: str
    heading: str
    description: str

class InfographicPlan(BaseModel):
    main_title: str
    hero_statistic: str
    layout_style: str = Field(..., description="e.g., 3-Column Comparison, Timeline, Hierarchy")
    sections: List[InfographicItem]
    color_palette_recommendation: List[str]

# 2.6 Executive Summary
class ExecutiveSummary(BaseModel):
    bluf: str = Field(..., description="Bottom Line Up Front")
    key_findings: List[str]
    strategic_implications: str
    recommended_decision: str

# 2.7 Presentation Slides
class Slide(BaseModel):
    slide_num: int
    title: str
    bullet_points: List[str]
    visual_diagram_concept: str
    speaker_notes: str

class PresentationDeck(BaseModel):
    deck_title: str
    target_audience: str
    slides: List[Slide]

# ==========================================
# 3. COMPLETE AGGREGATED RESPONSE
# ==========================================
class TransformResponse(BaseModel):
    project_title: str
    video_package: Optional[VideoPackage] = None
    linkedin_post: Optional[LinkedInPost] = None
    twitter_thread: Optional[TwitterThread] = None
    advisory: Optional[Advisory] = None
    infographic_plan: Optional[InfographicPlan] = None
    executive_summary: Optional[ExecutiveSummary] = None
    presentation_deck: Optional[PresentationDeck] = None
