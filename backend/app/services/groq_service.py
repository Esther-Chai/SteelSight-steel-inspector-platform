from groq import Groq
from app.core.config import settings
from app.models.schemas import DetectionResult, ReportResponse
from typing import List
import json

client = Groq(api_key=settings.GROQ_API_KEY)

SEVERITY_MAP = {
    "crazing":        "Moderate",
    "inclusion":      "High",
    "patches":        "Low",
    "pitted_surface": "Moderate",
    "rolled-in_scale":"High",
    "scratches":      "Low",
}

def generate_report(detections: List[DetectionResult]) -> ReportResponse:
    if not detections:
        return ReportResponse(
            summary="No defects were detected on the inspected surface.",
            severity="None",
            recommendations=["Surface meets quality standards.", "No action required."]
        )

    # Build structured context for the LLM
    detection_text = "\n".join([
        f"- {d.defect} at {d.location} | confidence: {d.confidence*100:.1f}% | area: {d.area_percent}%"
        for d in detections
    ])
    severity = max(
        [SEVERITY_MAP.get(d.defect, "Moderate") for d in detections],
        key=lambda s: {"Low": 0, "Moderate": 1, "High": 2}[s]
    )

    prompt = f"""You are an industrial quality control assistant for steel manufacturing.

The following surface defects were detected on a steel sample:
{detection_text}

Overall severity: {severity}

Write a concise inspection report with:
1. A 2-3 sentence summary describing the defects found
2. The severity level ({severity})
3. Exactly 3 recommended actions as a JSON array

Respond ONLY in this JSON format, no extra text:
{{
  "summary": "...",
  "severity": "{severity}",
  "recommendations": ["action 1", "action 2", "action 3"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)

    return ReportResponse(
        summary=parsed["summary"],
        severity=parsed["severity"],
        recommendations=parsed["recommendations"]
    )