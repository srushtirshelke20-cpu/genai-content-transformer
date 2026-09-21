"""
Video Package Prompts Module.
Generates VideoPackage artefacts with scene breakdown, timings, visual descriptions,
narration script, on-screen text, and AI image generator prompts.
Strictly validates against backend.schemas.VideoPackage.
"""

from typing import Dict, Any, Optional
from backend.schemas import VideoPackage
from .base_prompt import call_ollama_json


VIDEO_SYSTEM_PROMPT = """You are a video creative director and AI multimedia production specialist.
Transform the provided source content into a high-impact Video Package script (60-90 seconds total).
Tone: {tone}
Target Audience: {target_audience}
Objective: {objective}
Detail Level: {detail_level}

CRITICAL RULES:
1. title: Compelling video production title.
2. target_duration: Target duration string (e.g. "60 seconds").
3. background_music_vibe: Soundtrack mood and tempo (e.g., "Tense electronic synthwave, 120 BPM, building suspense").
4. scenes: Ordered list of 3 to 6 VideoScene objects.
5. Each VideoScene MUST have:
   - scene_num: integer starting from 1.
   - duration_seconds: integer seconds for the scene (e.g., 10, 15).
   - visual_description: detailed camera, lighting, and visual environment descriptions.
   - narration_script: exact spoken voiceover text calibrated for spoken pacing.
   - on_screen_text: bold graphical overlay text or key metric callouts.
   - ai_image_prompt: production-ready text prompt for AI image/video generators (Midjourney v6/Runway Gen-3) including style and --ar 16:9.

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "title": "string",
  "target_duration": "60 seconds",
  "background_music_vibe": "string",
  "scenes": [
    {{
      "scene_num": 1,
      "duration_seconds": 15,
      "visual_description": "string",
      "narration_script": "string",
      "on_screen_text": "string",
      "ai_image_prompt": "string"
    }}
  ]
}}"""

VIDEO_FEW_SHOT_EXAMPLE = """
Example Output Structure:
{
  "title": "Emergency Threat Flash: Apex IAM Zero-Day",
  "target_duration": "60 seconds",
  "background_music_vibe": "Tense cinematic pulse with electronic bassline, urgent tempo",
  "scenes": [
    {
      "scene_num": 1,
      "duration_seconds": 15,
      "visual_description": "Slow camera zoom into a dark enterprise server room. Pulsing crimson warning lights flash over gateway router racks.",
      "narration_script": "In under 18 minutes, a single zero-day vulnerability can compromise your entire enterprise identity backbone.",
      "on_screen_text": "CRITICAL ZERO-DAY: CVE-2026-8891",
      "ai_image_prompt": "Cinematic shot of enterprise datacenter server racks, red emergency holographic alert pulse, moody cyber thriller lighting, photorealistic 8k --ar 16:9"
    },
    {
      "scene_num": 2,
      "duration_seconds": 20,
      "visual_description": "Dynamic digital graphics trace an unauthenticated TLS handshake attack across port 8443 into an active directory core.",
      "narration_script": "Attackers exploit memory corruption in Apex IAM Gateways, bypassing authentication to deploy AES-256 ransomware across 14,000 corporate servers.",
      "on_screen_text": "14,000+ IDENTITY SERVERS EXPOSED",
      "ai_image_prompt": "Abstract 3D cyber network visualization showing compromised glowing nodes, dark digital matrix aesthetic, volumetric lighting, photorealistic --ar 16:9"
    },
    {
      "scene_num": 3,
      "duration_seconds": 25,
      "visual_description": "Split screen showing firewall port 8443 being locked down with emergency patch v5.1.4 verified by SecOps engineers.",
      "narration_script": "Immediate action is required. Block external ingress on port 8443 and deploy emergency patch 5.1.4 today. Protect your perimeter now.",
      "on_screen_text": "ACTION: BLOCK PORT 8443 | APPLY PATCH v5.1.4",
      "ai_image_prompt": "Modern cybersecurity operations center with analysts looking at large monitoring wall displaying green firewall containment shield, sleek cinematic lighting --ar 16:9"
    }
  ]
}
"""


def generate_video_package(
    raw_text: str,
    tone: str = "Professional",
    target_audience: str = "General Public",
    objective: str = "Inform",
    detail_level: str = "Standard",
    model: str = "llama3.1"
) -> VideoPackage:
    """Generates a VideoPackage model validated against backend.schemas.VideoPackage."""
    system_prompt = VIDEO_SYSTEM_PROMPT.format(
        tone=tone,
        target_audience=target_audience,
        objective=objective,
        detail_level=detail_level
    )

    user_prompt = f"""Transform the following source content into a Video Package script with scene breakdowns and AI image prompts.

{VIDEO_FEW_SHOT_EXAMPLE}

SOURCE CONTENT:
{raw_text}

Respond ONLY with the JSON object."""

    json_dict = call_ollama_json(system_prompt=system_prompt, user_prompt=user_prompt, model=model)
    return VideoPackage.model_validate(json_dict)
