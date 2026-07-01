from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ── Auth ──────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ── Prediction ────────────────────────────────────────────────────────────────
class DetectionResult(BaseModel):
    defect: str
    confidence: float
    bbox: List[float]
    area_percent: float
    location: str

class PredictResponse(BaseModel):
    detections: List[DetectionResult]
    annotated_image: str
    gradcam_image: str
    inference_time_ms: float

# ── Report ────────────────────────────────────────────────────────────────────
class ReportRequest(BaseModel):
    detections: List[DetectionResult]

class ReportResponse(BaseModel):
    summary: str
    severity: str
    recommendations: List[str]