from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.detection import Detection

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/stats")
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total_detections = db.query(Detection).filter(Detection.user_id == current_user.id).count()
    
    healthy_count = db.query(Detection).filter(
        Detection.user_id == current_user.id,
        Detection.disease_class.like("%healthy%")
    ).count()
    
    diseased_count = total_detections - healthy_count
    
    avg_confidence = db.query(func.avg(Detection.confidence)).filter(
        Detection.user_id == current_user.id
    ).scalar() or 0
    
    return {
        "total_detections": total_detections,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "healthy_percentage": round((healthy_count / total_detections * 100) if total_detections > 0 else 0, 2),
        "diseased_percentage": round((diseased_count / total_detections * 100) if total_detections > 0 else 0, 2),
        "avg_confidence": round(float(avg_confidence), 2)
    }

@router.get("/disease-distribution")
def get_disease_distribution(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    results = db.query(
        Detection.disease_class,
        func.count(Detection.id).label("count")
    ).filter(
        Detection.user_id == current_user.id
    ).group_by(Detection.disease_class).all()
    
    return [{"disease": r.disease_class, "count": r.count} for r in results]
