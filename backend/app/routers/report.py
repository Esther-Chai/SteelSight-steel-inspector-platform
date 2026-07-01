from fastapi import APIRouter, Depends
from app.services.groq_service import generate_report
from app.models.schemas import ReportRequest, ReportResponse
from app.routers.predict import get_current_user

router = APIRouter(prefix="/report", tags=["report"])

@router.post("", response_model=ReportResponse)
def report(
    body: ReportRequest,
    current_user: str = Depends(get_current_user)
):
    return generate_report(body.detections)