import sys
import json
import uuid
from pathlib import Path
from typing import Optional, List
import urllib.request

# Ensure the root directory is in python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.config import CORS_ORIGINS, EXPORT_DIR, OLLAMA_TAGS_URL, DEFAULT_MODEL
from backend.schemas import TransformRequest, TransformResponse

# ====================================================================
# Safe Imports with Fallbacks (keeps server alive if teammates are working)
# ====================================================================

# 1. Member 4 Parser Fallback
try:
    from backend.parsers.doc_parser import extract_text_from_file
except ImportError:
    def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
        return file_bytes.decode("utf-8", errors="ignore")

# 2. Member 3 Orchestrator Fallback
try:
    from backend.prompts.orchestrator import transform_content
except ImportError:
    def transform_content(req: TransformRequest) -> TransformResponse:
        return TransformResponse(
            project_title=f"Transformed: {req.raw_text[:40]}...",
            linkedin_post={
                "hook": "🚨 Critical Operational Briefing",
                "body_paragraphs": [f"Analysis conducted with tone: {req.tone} for audience: {req.target_audience}."],
                "bullet_points": ["Point 1: Key finding", "Point 2: Recommended measure", "Point 3: Next steps"],
                "call_to_action": "How is your team addressing this? Let us know below.",
                "hashtags": ["#GenAI", "#Transformation", "#Intelligence"]
            },
            twitter_thread={
                "thread_hook": "🚨 Key Takeaways from the latest advisory:",
                "tweets": [
                    {"tweet_num": 1, "text": "1/3 Here is a concise breakdown of the recent briefing..."},
                    {"tweet_num": 2, "text": "2/3 Core impact identified across primary systems."},
                    {"tweet_num": 3, "text": "3/3 Recommended action: apply patches and review policy."}
                ]
            },
            advisory={
                "advisory_id": "ADV-2026-001",
                "severity_level": "HIGH",
                "date_issued": "2026-09-04",
                "target_audience_or_systems": req.target_audience,
                "threat_or_context_summary": req.raw_text[:200] if len(req.raw_text) > 200 else req.raw_text,
                "impact_analysis": "Potential exposure if mitigations are delayed.",
                "immediate_actions": ["Review network logs", "Isolate affected nodes"],
                "long_term_recommendations": ["Conduct comprehensive audit", "Train personnel"]
            }
        )

# 3. Member 4 PowerPoint Exporter Fallback
try:
    from backend.exporters.pptx_exporter import generate_pptx_file
except ImportError:
    def generate_pptx_file(deck, filepath: str) -> str:
        # Placeholder empty file if exporter not yet finished
        with open(filepath, "w") as f:
            f.write("PPTX placeholder")
        return filepath

# 4. Member 4 Database Fallback
try:
    from backend.database.db import save_transformation, fetch_history
except ImportError:
    _mock_db = []
    def save_transformation(record_id, title, raw_text, settings, result):
        _mock_db.append({"id": record_id, "title": title, "result": result})
    def fetch_history(limit=10):
        return _mock_db[-limit:]

# ====================================================================
# FastAPI App Initialization
# ====================================================================

app = FastAPI(
    title="GenAI Platform for Automated Content Transformation",
    description="Transforms raw documents/reports into 7 cross-platform communication artefacts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================================================
# Endpoints
# ====================================================================

@app.get("/api/health")
def health_check():
    """Check API status and verify local Ollama connectivity."""
    ollama_status = "offline"
    available_models = []
    
    try:
      from fastapi import Request

@app.post("/api/transform", response_model=TransformResponse)
async def transform_endpoint(request: Request):
    """
    Main transformation gateway.
    Seamlessly accepts direct JSON payloads OR multipart file uploads (PDF/DOCX/TXT).
    """
    content_type = request.headers.get("content-type", "")
    final_text = ""
    target_audience = "General Public"
    tone = "Professional"
    objective = "Inform"
    detail_level = "Standard"
    formats_list = ["linkedin", "twitter", "advisory", "executive_summary", "presentation", "video_package", "infographic"]

    # 1. Handle JSON Request (from test_e2e.py or API clients)
    if "application/json" in content_type:
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format.")
            
        final_text = body.get("raw_text", "")
        target_audience = body.get("target_audience", "General Public")
        tone = body.get("tone", "Professional")
        objective = body.get("objective", "Inform")
        detail_level = body.get("detail_level", "Standard")
        formats_list = body.get("selected_formats", formats_list)

    # 2. Handle Multipart Form Upload (file upload from Frontend)
    elif "multipart/form-data" in content_type:
        form = await request.form()
        file = form.get("file")
        raw_text = form.get("raw_text", "")
        target_audience = form.get("target_audience", "General Public")
        tone = form.get("tone", "Professional")
        objective = form.get("objective", "Inform")
        detail_level = form.get("detail_level", "Standard")
        selected_formats = form.get("selected_formats")

        if file and hasattr(file, "read"):
            file_bytes = await file.read()
            final_text = extract_text_from_file(file_bytes, file.filename)
        elif raw_text:
            final_text = str(raw_text)

        if selected_formats:
            try:
                formats_list = json.loads(selected_formats)
            except Exception:
                formats_list = [f.strip() for f in str(selected_formats).split(",") if f.strip()]
    else:
        raise HTTPException(status_code=400, detail="Unsupported Content-Type. Send JSON or multipart/form-data.")

    if not final_text.strip():
        raise HTTPException(status_code=400, detail="No source content provided. Provide raw_text or upload a file.")

    # 3. Build structured request object
    structured_request = TransformRequest(
        raw_text=final_text,
        target_audience=target_audience,
        tone=tone,
        objective=objective,
        detail_level=detail_level,
        selected_formats=formats_list
    )

    # 4. Execute Transformation via Orchestrator
    try:
        response_data: TransformResponse = transform_content(structured_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation error: {str(e)}")

    # 5. If Presentation was requested and generated, build PPTX
    if "presentation" in formats_list and response_data.presentation_deck:
        record_id = str(uuid.uuid4())[:8]
        filename = f"presentation_{record_id}.pptx"
        output_path = str(EXPORT_DIR / filename)
        generate_pptx_file(response_data.presentation_deck, output_path)

    # 6. Save run into History Database
    run_id = str(uuid.uuid4())
    save_transformation(
        record_id=run_id,
        title=response_data.project_title,
        raw_text=final_text[:500],
        settings={"tone": tone, "audience": target_audience, "formats": formats_list},
        result=response_data.model_dump()
    )

    return response_data
    elif raw_text:
        final_text = raw_text
        if selected_formats:
            try:
                formats_list = json.loads(selected_formats)
            except Exception:
                formats_list = [f.strip() for f in selected_formats.split(",") if f.strip()]
    else:
        raise HTTPException(status_code=400, detail="No source content provided. Provide raw_text or upload a file.")

    if not final_text.strip():
        raise HTTPException(status_code=400, detail="Provided document or text is empty.")

    # 2. Build structured request object
    structured_request = TransformRequest(
        raw_text=final_text,
        target_audience=target_audience,
        tone=tone,
        objective=objective,
        detail_level=detail_level,
        selected_formats=formats_list
    )

    # 3. Execute Transformation via Orchestrator
    try:
        response_data: TransformResponse = transform_content(structured_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation error: {str(e)}")

    # 4. If Presentation was requested and generated, build real PPTX
    if "presentation" in formats_list and response_data.presentation_deck:
        record_id = str(uuid.uuid4())[:8]
        filename = f"presentation_{record_id}.pptx"
        output_path = str(EXPORT_DIR / filename)
        generate_pptx_file(response_data.presentation_deck, output_path)

    # 5. Save run into History Database
    run_id = str(uuid.uuid4())
    save_transformation(
        record_id=run_id,
        title=response_data.project_title,
        raw_text=final_text[:500],
        settings={"tone": tone, "audience": target_audience, "formats": formats_list},
        result=response_data.model_dump()
    )

    return response_data


@app.get("/api/download/pptx/{filename}")
def download_pptx(filename: str):
    """Download a generated PowerPoint file."""
    file_path = EXPORT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Requested presentation file not found.")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


@app.get("/api/history")
def get_history():
    """Retrieve past transformation runs."""
    return {"history": fetch_history(limit=10)}
