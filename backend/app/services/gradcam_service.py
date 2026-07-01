import base64
import numpy as np
import cv2
import torch
import torch.nn as nn
from torchvision import transforms
from pytorch_grad_cam import EigenCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from ultralytics import YOLO
from app.core.config import settings

class YOLOBackboneWrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.backbone = nn.Sequential(*list(model.model.model.children())[:10])

    def forward(self, x):
        return self.backbone(x)

# Lazy load
_wrapper       = None
_target_layers = None

def get_cam_model():
    global _wrapper, _target_layers
    if _wrapper is None:
        yolo           = YOLO(settings.MODEL_PATH)
        _wrapper       = YOLOBackboneWrapper(yolo)
        _wrapper.eval()
        _target_layers = [list(_wrapper.backbone.children())[-1]]
    return _wrapper, _target_layers

_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def run_gradcam(image_bytes: bytes) -> str:
    wrapper, target_layers = get_cam_model()

    img_array = np.frombuffer(image_bytes, np.uint8)
    img_bgr   = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img_rgb   = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_r     = cv2.resize(img_rgb, (640, 640)).astype(np.float32) / 255.0

    tensor = _transform(img_r).unsqueeze(0)
    cam    = EigenCAM(model=wrapper, target_layers=target_layers)
    mask   = cam(input_tensor=tensor)[0]
    mask   = cv2.resize(mask, (640, 640))

    overlay     = show_cam_on_image(img_r, mask, use_rgb=True)
    overlay_bgr = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)

    _, buffer = cv2.imencode('.jpg', overlay_bgr)
    return base64.b64encode(buffer).decode('utf-8')