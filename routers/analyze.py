from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag import get_relevant_techniques
from services.groq_client import analyze_incident

router = APIRouter(tags=["analyze"])

class IncidentRequest(BaseModel):
    incident_text: str

@router.post("/analyze")
def post_analyze(req: IncidentRequest):
    if not req.incident_text.strip():
        raise HTTPException(status_code=400, detail="incident_text cannot be empty")
    context = get_relevant_techniques(req.incident_text)
    result = analyze_incident(req.incident_text, context)
    return result