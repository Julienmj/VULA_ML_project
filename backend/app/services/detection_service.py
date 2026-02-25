from sqlalchemy.orm import Session
from app.models.detection import Detection
from typing import List
import os
from datetime import datetime

class DetectionService:
    @staticmethod
    def create_detection(db: Session, user_id: int, image_path: str, 
                        disease_class: str, confidence: float, 
                        top_3_predictions: list, recommendations: str) -> Detection:
        detection = Detection(
            user_id=user_id,
            image_path=image_path,
            disease_class=disease_class,
            confidence=confidence,
            top_3_predictions=top_3_predictions,
            recommendations=recommendations
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        return detection
    
    @staticmethod
    def get_user_detections(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Detection]:
        return db.query(Detection).filter(Detection.user_id == user_id).order_by(Detection.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_detection_by_id(db: Session, detection_id: int, user_id: int) -> Detection:
        return db.query(Detection).filter(Detection.id == detection_id, Detection.user_id == user_id).first()
    
    @staticmethod
    def count_user_detections(db: Session, user_id: int) -> int:
        return db.query(Detection).filter(Detection.user_id == user_id).count()
