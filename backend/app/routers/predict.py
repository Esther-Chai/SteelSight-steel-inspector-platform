from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from app.services.yolo_service import run_inference
from app.services.gradcam_service import run_gradcam
from app.models.schemas import PredictResponse
from app.core.security import decode_token

router = APIRouter(prefix="/predict", tags=["predict"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]

@router.post("", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.35),
    current_user: str = Depends(get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG accepted")
    if not 0.1 <= conf_threshold <= 0.9:
        raise HTTPException(status_code=400, detail="Threshold must be between 0.1 and 0.9")

    image_bytes = await file.read()
    inference   = run_inference(image_bytes, conf_threshold)
    gradcam_b64 = run_gradcam(image_bytes)

    return PredictResponse(
        detections=inference["detections"],
        annotated_image=inference["annotated_image"],
        gradcam_image=gradcam_b64,
        inference_time_ms=inference["inference_time_ms"],
    )