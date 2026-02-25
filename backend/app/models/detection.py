from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.database import Base

class Detection(Base):
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_path = Column(String, nullable=False)
    disease_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    top_3_predictions = Column(JSON, nullable=False)
    recommendations = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
