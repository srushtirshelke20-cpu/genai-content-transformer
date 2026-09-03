"""
Video Package Prompt Module.
Generates prompts for full scene-by-scene video scripts, visual cues, voiceovers,
subtitles, pacing, and AI image/video generation prompts (Midjourney, Runway, HeyGen).
"""

from typing import Optional, Dict, Any
from .base_prompt import BasePromptBuilder, TransformationParameters


class VideoPromptBuilder:
    """Builder for Video Package Prompts."""

    TASK_DESCRIPTION = """You are tasked with transforming the provided source content into a high-impact, professional Video Production Package (approx. 60–90 seconds total duration).

Your generation must include:
1. Video Title & Production Overview (Logline, Target Duration, Pacing Strategy, Target Aspect Ratio e.g. 16:9 widescreen or 9:16 vertical).
2. Sequential Scene-by-Scene Breakdown (typically 4 to 6 concise scenes):
   - Scene Number & Timecode (e.g., Scene 1: 0:00 - 0:15)
   - Scene Mood & Pacing (e.g., Urgent / Revealing / Action-oriented / Deliberate)
   - Visual Cue Description: Highly descriptive instructions for the camera, lighting, environment, transitions, and character actions.
   - Voiceover Narration (VO): The verbatim words spoken by the narrator, calibrated for spoken cadence.
   - On-Screen Text / Subtitles: Punchy graphical text overlays highlighting critical facts or statistics.
   - AI Image/Video Generation Prompt (KEY DIFFERENTIATOR): A production-ready text prompt engineered specifically for cutting-edge AI image and video generators (Midjourney v6, Runway Gen-3, HeyGen, or DALL-E 3). Include art style (e.g., photorealistic, cinematic lighting, 8k, bokeh, volumetric fog, color grading) and aspect ratio parameters (e.g., `--ar 16:9`).
3. Sound Design & BGM Recommendations: Background music tempo, mood, and sound effects (SFX) cues.
4. Closing Call to Action (CTA): Final frame visual and verbal sign-off."""

    JSON_SCHEMA_INSTRUCTION = """Provide your response as a strictly valid JSON object matching this schema:
```json
{
  "video_title": "string",
  "logline": "string",
  "target_duration_seconds": 60,
  "aspect_ratio": "16:9",
  "bgm_recommendation": {
    "mood": "string",
    "tempo_bpm": "string",
    "sound_effects": ["string"]
  },
  "scenes": [
    {
      "scene_number": 1,
      "timecode": "0:00 - 0:15",
      "pacing": "string",
      "visual_cue": "string",
      "voiceover": "string",
      "on_screen_text": "string",
      "ai_image_prompt": "string (optimized for Midjourney/Runway/HeyGen with style and --ar 16:9)",
      "sfx_cue": "string"
    }
  ],
  "call_to_action": {
    "visual": "string",
    "voiceover": "string",
    "on_screen_text": "string"
  }
}
