import os
from typing import Union, Optional, Dict, Any

try:
    from backend.schemas import TransformResponse
except ImportError:
    from schemas import TransformResponse


def export_dossier_markdown(
    data: Union[TransformResponse, Dict[str, Any]],
    output_filename: Optional[str] = None
) -> str:
    """
    Generates a clean, comprehensive Markdown (.md) report containing
    all generated transformation artefacts from the intelligence dossier.
    Optionally saves it to disk if output_filename is provided.
    """
    d = (
        data.model_dump()
        if hasattr(data, "model_dump")
        else (data.dict() if hasattr(data, "dict") else data)
    )

    lines = []
    title = d.get("project_title", "Intelligence Dossier")
    lines.append(f"# {title}\n")
    lines.append("> *Generated automatically by GenAI Content Transformer*\n")
    lines.append("---\n")

    # 1. Executive Summary
    exec_sum = d.get("executive_summary")
    if exec_sum:
        lines.append("## 📋 Executive Summary\n")
        lines.append(f"**Bottom Line Up Front (BLUF):**\n{exec_sum.get('bluf', '')}\n")
        lines.append("### Key Findings")
        for item in exec_sum.get("key_findings", []):
            lines.append(f"- {item}")
        lines.append(f"\n**Strategic Implications:**\n{exec_sum.get('strategic_implications', '')}\n")
        lines.append(f"**Recommended Decision:**\n{exec_sum.get('recommended_decision', '')}\n")
        lines.append("---\n")

    # 2. Structured Advisory
    advisory = d.get("advisory")
    if advisory:
        lines.append(f"## ⚠️ Advisory: {advisory.get('advisory_id', 'ALERT')}\n")
        lines.append(f"- **Severity Level:** `{advisory.get('severity_level', 'HIGH')}`")
        lines.append(f"- **Date Issued:** {advisory.get('date_issued', 'N/A')}")
        lines.append(f"- **Target Systems / Audience:** {advisory.get('target_audience_or_systems', 'N/A')}\n")
        lines.append(f"### Threat Summary\n{advisory.get('threat_or_context_summary', '')}\n")
        lines.append(f"### Impact Analysis\n{advisory.get('impact_analysis', '')}\n")
        lines.append("### Immediate Actions")
        for action in advisory.get("immediate_actions", []):
            lines.append(f"1. {action}")
        lines.append("\n### Long-Term Recommendations")
        for rec in advisory.get("long_term_recommendations", []):
            lines.append(f"- {rec}")
        lines.append("\n---\n")

    # 3. LinkedIn Post
    li = d.get("linkedin_post")
    if li:
        lines.append("## 💼 LinkedIn Announcement\n")
        lines.append(f"**Hook:**\n*{li.get('hook', '')}*\n")
        for p in li.get("body_paragraphs", []):
            lines.append(f"{p}\n")
        if li.get("bullet_points"):
            for bp in li.get("bullet_points", []):
                lines.append(f"• {bp}")
            lines.append("")
        lines.append(f"👉 **Call To Action:** {li.get('call_to_action', '')}\n")
        hashtags = " ".join([h if h.startswith("#") else f"#{h}" for h in li.get("hashtags", [])])
        lines.append(f"**Tags:** {hashtags}\n")
        lines.append("---\n")

    # 4. Twitter / X Thread
    tw = d.get("twitter_thread")
    if tw:
        lines.append("## 🐦 Twitter / X Thread\n")
        lines.append(f"**Hook:** {tw.get('thread_hook', '')}\n")
        for tweet in tw.get("tweets", []):
            lines.append(f"> **[{tweet.get('tweet_num')}]** {tweet.get('text')}\n")
        lines.append("---\n")

    # 5. Infographic Blueprint
    info = d.get("infographic_plan")
    if info:
        lines.append("## 📊 Infographic Blueprint\n")
        lines.append(f"**Title:** {info.get('main_title')}")
        lines.append(f"**Hero Stat:** `{info.get('hero_statistic')}` | **Layout:** {info.get('layout_style')}\n")
        lines.append("| Metric / Icon | Heading | Details |")
        lines.append("|---|---|---|")
        for s in info.get("sections", []):
            lines.append(f"| {s.get('stat_or_icon')} | {s.get('heading')} | {s.get('description')} |")
        lines.append(f"\n*Color Palette:* {', '.join(info.get('color_palette_recommendation', []))}\n")
        lines.append("---\n")

    # 6. Video Package
    vid = d.get("video_package")
    if vid:
        lines.append("## 🎬 Video Package Script\n")
        lines.append(f"**Title:** {vid.get('title')} ({vid.get('target_duration')})")
        lines.append(f"**Vibe / Music:** *{vid.get('background_music_vibe')}*\n")
        for scene in vid.get("scenes", []):
            lines.append(f"### Scene {scene.get('scene_num')} ({scene.get('duration_seconds')}s)")
            lines.append(f"- **Visuals:** {scene.get('visual_description')}")
            lines.append(f"- **Narration:** \"{scene.get('narration_script')}\"")
            lines.append(f"- **On-Screen:** `{scene.get('on_screen_text')}`\n")

    # 7. Presentation Deck Outline
    deck = d.get("presentation_deck")
    if deck:
        lines.append("## 📽️ Presentation Deck Outline\n")
        lines.append(f"**Deck Title:** {deck.get('deck_title')}")
        lines.append(f"**Audience:** {deck.get('target_audience')}\n")
        for slide in deck.get("slides", []):
            lines.append(f"### Slide {slide.get('slide_num')}: {slide.get('title')}")
            for bp in slide.get("bullet_points", []):
                lines.append(f"- {bp}")
            if slide.get("visual_diagram_concept"):
                lines.append(f"*Visual Concept:* {slide.get('visual_diagram_concept')}")
            if slide.get("speaker_notes"):
                lines.append(f"*Speaker Notes:* {slide.get('speaker_notes')}")
            lines.append("")

    full_markdown = "\n".join(lines)

    if output_filename:
        out_dir = os.path.dirname(os.path.abspath(output_filename))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(full_markdown)

    return full_markdown


def _create_simple_pdf(text_content: str, pdf_path: str) -> None:
    """
    Lightweight pure-Python PDF-1.4 writer.
    Converts plain text into a valid PDF file with pagination
    without requiring external C-libraries or extra dependencies.
    """
    lines = text_content.split("\n")
    # Wrap text roughly to 85 characters per line
    wrapped_lines = []
    for line in lines:
        if not line:
            wrapped_lines.append("")
        else:
            while len(line) > 85:
                wrapped_lines.append(line[:85])
                line = line[85:]
            wrapped_lines.append(line)

    lines_per_page = 45
    pages = [wrapped_lines[i:i + lines_per_page] for i in range(0, len(wrapped_lines), lines_per_page)]
    if not pages:
        pages = [["[Empty Document]"]]

    objects = []

    def add_object(content: str) -> int:
        objects.append(content)
        return len(objects)

    # 1. Catalog & Pages objects (placeholders)
    add_object("<< /Type /Catalog /Pages 2 0 R >>")

    page_obj_ids = []
    # 2. Pages object will be at index 1 (resolved later)
    # Reserve space for Pages object
    objects.append("")

    # Add Font object
    font_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    # Add each Page
    for page_num, page_lines in enumerate(pages, 1):
        # Escape parenthesis and backslashes for PDF string syntax
        stream_parts = ["BT", f"/F1 11 Tf", "50 750 Td", "14 TL"]
        for pline in page_lines:
            safe_text = pline.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            # Basic styling: bold titles
            if pline.startswith("#"):
                stream_parts.append(f"({safe_text}) Tj T*")
            else:
                stream_parts.append(f"({safe_text}) Tj T*")

        stream_parts.append("ET")
        stream_content = "\n".join(stream_parts)

        content_id = add_object(
            f"<< /Length {len(stream_content.encode('latin-1', 'replace'))} >>\nstream\n{stream_content}\nendstream"
        )
        page_id = add_object(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {content_id} 0 R /Resources << /Font << /F1 {font_id} 0 R >> >> >>"
        )
        page_obj_ids.append(page_id)

    # Now define the Pages root object at index 1 (ID 2)
    kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
    objects[1] = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>"

    # Assemble the final PDF file buffer
    pdf_buf = bytearray(b"%PDF-1.4\n")
    offsets = [0]

    for idx, obj in enumerate(objects, 1):
        offsets.append(len(pdf_buf))
        pdf_buf.extend(f"{idx} 0 obj\n{obj}\nendobj\n".encode("latin-1", "replace"))

    xref_offset = len(pdf_buf)
    pdf_buf.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        pdf_buf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf_buf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )

    out_dir = os.path.dirname(os.path.abspath(pdf_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(pdf_path, "wb") as f:
        f.write(pdf_buf)


def export_dossier_pdf(
    data: Union[TransformResponse, Dict[str, Any]],
    output_filename: str
) -> str:
    """
    Generates both:
    1. A clean Markdown (.md) dossier file.
    2. A valid binary PDF (.pdf) file.
    Returns the path to the generated PDF.
    """
    base_name = os.path.splitext(output_filename)[0]
    md_path = f"{base_name}.md"
    pdf_path = f"{base_name}.pdf"

    # Generate full Markdown text and save the .md file
    md_content = export_dossier_markdown(data, output_filename=md_path)

    # Generate the actual .pdf file
    _create_simple_pdf(md_content, pdf_path)

    return pdf_path
