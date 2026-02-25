from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class PredictionResult(BaseModel):
    disease_class: str
    confidence: float

class DetectionResponse(BaseModel):
    id: int
    disease_class: str
    confidence: float
    top_3_predictions: List[Dict[str, float]]
    recommendations: str
    created_at: datetime
    image_path: str
    
    class Config:
        from_attributes = True

class DetectionHistory(BaseModel):
    detections: List[DetectionResponse]
    total: int
