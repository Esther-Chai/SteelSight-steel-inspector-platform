import time
import base64
import numpy as np
import cv2
from ultralytics import YOLO
from app.core.config import settings
from app.models.schemas import DetectionResult

# Lazy load — model loads on first request, not at startup
_model = None

def get_model():
    global _model
    if _model is None:
        _model = YOLO(settings.MODEL_PATH)
    return _model

LOCATION_MAP = {
    (0, 0): "Upper-left",   (1, 0): "Upper-centre",  (2, 0): "Upper-right",
    (0, 1): "Middle-left",  (1, 1): "Centre",         (2, 1): "Middle-right",
    (0, 2): "Lower-left",   (1, 2): "Lower-centre",   (2, 2): "Lower-right",
}

def get_location(cx: float, cy: float) -> str:
    col = min(int(cx * 3), 2)
    row = min(int(cy * 3), 2)
    return LOCATION_MAP.get((col, row), "Centre")

def encode_image(img_bgr: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', img_bgr)
    return base64.b64encode(buffer).decode('utf-8')

def run_inference(image_bytes: bytes, conf_threshold: float = 0.35) -> dict:
    model     = get_model()
    img_array = np.frombuffer(image_bytes, np.uint8)
    img_bgr   = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w      = img_bgr.shape[:2]

    start   = time.time()
    results = model.predict(img_bgr, conf=conf_threshold, iou=0.45, verbose=False)
    elapsed = (time.time() - start) * 1000

    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf     = float(box.conf[0])
            cls_id   = int(box.cls[0])
            cls_name = model.names[cls_id]

            nx1, ny1 = x1 / w, y1 / h
            nx2, ny2 = x2 / w, y2 / h
            cx = (nx1 + nx2) / 2
            cy = (ny1 + ny2) / 2
            area_pct = round((nx2 - nx1) * (ny2 - ny1) * 100, 2)

            detections.append(DetectionResult(
                defect=cls_name,
                confidence=round(conf, 4),
                bbox=[round(nx1, 4), round(ny1, 4), round(nx2, 4), round(ny2, 4)],
                area_percent=area_pct,
                location=get_location(cx, cy),
            ))

    annotated_b64 = encode_image(results[0].plot())

    return {
        "detections":        detections,
        "annotated_image":   annotated_b64,
        "inference_time_ms": round(elapsed, 2),
    }