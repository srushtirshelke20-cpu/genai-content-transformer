import os
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from backend.database.db import (
    delete_record,
    purge_all_history,
    fetch_history,
    init_db,
)

app = FastAPI(
    title="GenAI Content Transformer API",
    description="Multi-artefact content synthesis engine with DPDP Act 2023 compliance",
    version="1.0.0"
)

# Enable CORS for frontend integration (Vite, React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Ensure database schema is initialized on server startup."""
    init_db()


@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "GenAI Content Transformer"}


@app.get("/api/history")
def get_history(limit: Optional[int] = 10):
    """Fetch recent transformation history."""
    return fetch_history(limit=limit or 10)


# ====================================================================
# 🛡️ DPDP Act 2023 (Sec 12) Right to Erasure / Purge Endpoints
# ====================================================================
@app.delete("/api/history/{record_id}")
def delete_history_item(record_id: str):
    """
    DPDP Act 2023 (Sec 12) Right to Erasure endpoint.
    Permanently erases a specific transformation record by ID from history.
    """
    success = delete_record(record_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return {
        "status": "success",
        "message": "Record permanently erased per DPDP 2023 Sec 12",
        "record_id": record_id
    }


@app.delete("/api/history")
def purge_history():
    """
    DPDP Act 2023 (Sec 12) Complete History Purge endpoint.
    Permanently deletes all historical records from the database on demand.
    """
    purge_all_history()
    return {
        "status": "success",
        "message": "All records permanently purged per DPDP 2023 Sec 12"
    }
