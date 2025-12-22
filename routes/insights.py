from fastapi import APIRouter, HTTPException
from services.llm_insights import generate_llm_insights

router = APIRouter()

@router.post("/llm-insights")
def llm_insights(profile: dict):
    try:
        return generate_llm_insights(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
