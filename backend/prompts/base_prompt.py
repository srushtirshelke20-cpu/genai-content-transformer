"""
Base Prompt & Ollama Client Module.
Initializes OpenAI client targeting local Ollama (http://localhost:11434/v1).
Provides call_ollama_json utility with strict JSON mode, robust error handling,
and markdown fence stripping.
"""

import os
import json
import re
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

# Ollama Endpoint Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Initialize OpenAI Client pointing to Ollama
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OLLAMA_API_KEY,
)


def clean_json_string(raw: str) -> str:
    """
    Cleans and extracts valid JSON substring from LLM response.
    Strips markdown code blocks, backticks, and any leading/trailing chatter.
    """
    cleaned = raw.strip()

    # Strip markdown ```json ... ``` or ``` ... ```
    if "```" in cleaned:
        # Match content inside ```json ... ``` or ``` ... ```
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
        else:
            # Fallback: remove all backtick fences
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    # Extract substring between first { and last }
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace : last_brace + 1]

    return cleaned


def call_ollama_json(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Calls Ollama via OpenAI client enforcing JSON mode.
    Handles markdown stripping and JSON parsing.

    Args:
        system_prompt: Role and schema guidance for the LLM.
        user_prompt: Source content and task prompt.
        model: Ollama model name (default: llama3.1).
        temperature: Sampling temperature (default 0.2 for consistency).

    Returns:
        Parsed dictionary from the LLM's JSON response.

    Raises:
        RuntimeError: If LLM call fails or returns unparseable JSON.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        raw_content = response.choices[0].message.content or "{}"
    except Exception as e:
        logger.error(f"Error communicating with Ollama endpoint ({OLLAMA_BASE_URL}): {e}")
        raise RuntimeError(f"Ollama API request failed: {e}") from e

    cleaned_json_str = clean_json_string(raw_content)

    try:
        return json.loads(cleaned_json_str)
    except json.JSONDecodeError as err:
        logger.error(f"Failed to decode JSON from Ollama. Raw content:\n{raw_content}")
        raise RuntimeError(f"Ollama returned invalid JSON: {err}\nContent was: {raw_content[:200]}...") from err


def get_client() -> OpenAI:
    """Returns the configured OpenAI client."""
    return client


def invoke_ollama(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """
    Invokes Ollama returning the raw string response.
    Provided for backward compatibility.
    """
    target_model = model or DEFAULT_MODEL
    default_system = (
        "You are an expert AI Content Transformation Engine. "
        "Analyze the provided source information and transform it into the requested "
        "communication artefact. Respond strictly with a valid JSON object."
    )
    messages = [
        {"role": "system", "content": system_prompt or default_system},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=target_model,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content or "{}"


def format_parameters(parameters: Optional[Dict[str, Any]] = None) -> str:
    """Formats configurable parameters into prompt text."""
    if not parameters:
        return "Target Audience: Executive / Professional\nTone: Authoritative & Objective\nLanguage: English"
    lines = [f"{k.replace('_', ' ').title()}: {v}" for k, v in parameters.items()]
    return "\n".join(lines)
