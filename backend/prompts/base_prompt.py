"""
Base Prompt Module for Gen AI Content Transformation Engine.
Provides core system prompts, hallucination guardrails, and parameter matrix formatting.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TransformationParameters:
    """Configurable parameter matrix governing content transformation."""
    target_audience: str = "Executive / C-Suite"
    tone: str = "Authoritative & Objective"
    level_of_detail: str = "Standard"
    communication_objective: str = "Inform & Synthesize"
    language: str = "English"
    content_style: str = "Professional / Enterprise"
    additional_instructions: Optional[str] = None


class BasePromptBuilder:
    """
    Base Prompt Builder that injects system guardrails, source attribution constraints,
    and parameter matrix dimensions into all deliverable prompts.
    """

    CORE_SYSTEM_INSTRUCTION = (
        "You are an expert Content Transformation AI Engine. Your primary purpose is to analyze "
        "heterogeneous source content (threat intelligence, technical reports, policy updates, "
        "academic papers, incident briefs) and transform it into high-impact, tailored communication "
        "deliverables with absolute precision, factual grounding, and domain-appropriate styling."
    )

    GUARDRAILS = (
        "CRITICAL GROUNDING & ACCURACY CONSTRAINTS:\n"
        "1. STRICT FACTUAL GROUNDING: Rely strictly on the information presented in the SOURCE CONTENT. "
        "Do not invent facts, CVE numbers, dates, statistics, benchmark figures, or quotes.\n"
        "2. UNCERTAINTY HANDLING: If an essential detail is absent from the source, clearly indicate it "
        "as 'Not specified in source' rather than hallucinating.\n"
        "3. ATTRIBUTION: Maintain fidelity to named entities, technical specifications, and severity levels.\n"
        "4. AUDIENCE CALIBRATION: Strictly adapt terminology, density, and register to match the requested "
        "TARGET AUDIENCE and TONE without sacrificing factual accuracy."
    )

    @classmethod
    def format_parameters_block(cls, params: Optional[TransformationParameters] = None) -> str:
        """Formats the parameter matrix into a clear prompt block for the LLM."""
        if params is None:
            params = TransformationParameters()

        block = [
            "### OPERATIONAL PARAMETER MATRIX",
            f"- **Target Audience**: {params.target_audience}",
            f"- **Tone & Register**: {params.tone}",
            f"- **Level of Detail**: {params.level_of_detail}",
            f"- **Communication Objective**: {params.communication_objective}",
            f"- **Target Language**: {params.language}",
            f"- **Style Guide**: {params.content_style}",
        ]

        if params.additional_instructions:
            block.append(f"- **Operator Guidance**: {params.additional_instructions.strip()}")

        return "\n".join(block)

    @classmethod
    def format_source_block(cls, source_content: str, source_metadata: Optional[Dict[str, Any]] = None) -> str:
        """Wraps source content cleanly with source metadata if available."""
        metadata_lines = []
        if source_metadata:
            metadata_lines.append("Source Metadata:")
            for k, v in source_metadata.items():
                metadata_lines.append(f"  - {k.capitalize()}: {v}")
            metadata_str = "\n".join(metadata_lines) + "\n\n"
        else:
            metadata_str = ""

        return (
            "### SOURCE CONTENT TO TRANSFORM\n"
            f"{metadata_str}"
            "```text\n"
            f"{source_content.strip()}\n"
            "```"
        )

    @classmethod
    def assemble_prompt(
        cls,
        task_instruction: str,
        source_content: str,
        params: Optional[TransformationParameters] = None,
        source_metadata: Optional[Dict[str, Any]] = None,
        output_schema_instruction: Optional[str] = None
    ) -> str:
        """Assembles a full prompt containing system instructions, parameters, task, schema, and source."""
        sections = [
            cls.CORE_SYSTEM_INSTRUCTION,
            "",
            cls.GUARDRAILS,
            "",
            cls.format_parameters_block(params),
            "",
            "### TASK INSTRUCTION",
            task_instruction.strip(),
        ]

        if output_schema_instruction:
            sections.extend([
                "",
                "### REQUIRED OUTPUT FORMAT & SCHEMA",
                output_schema_instruction.strip()
            ])

        sections.extend([
            "",
            cls.format_source_block(source_content, source_metadata),
            "",
            "Begin transformation below:"
        ])

        return "\n".join(sections)
