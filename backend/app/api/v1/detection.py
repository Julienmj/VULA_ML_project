from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.schemas.detection import DetectionResponse, DetectionHistory
from app.services.ml_service import ml_service
from app.services.detection_service import DetectionService
from app.core.rate_limiter import limiter
from PIL import Image
import io
import os
import uuid

router = APIRouter(prefix="/detect", tags=["Detection"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]
MAX_FILE_SIZE = 5 * 1024 * 1024

@router.post("", response_model=DetectionResponse)
@limiter.limit("10/minute")
async def detect_disease(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.content_type or file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG and PNG allowed")
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB")
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file")
    
    try:
        prediction = await ml_service.predict(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Model prediction failed")
    
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        image.save(filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save image")
    
    try:
        detection = DetectionService.create_detection(
            db=db,
            user_id=current_user.id,
            image_path=filepath,
            disease_class=prediction["disease_class"],
            confidence=prediction["confidence"],
            top_3_predictions=prediction["top_3_predictions"],
            recommendations=prediction["recommendations"]
        )
        return detection
    except Exception as e:
        db.rollback()
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail="Failed to save detection")

@router.get("/history", response_model=DetectionHistory)
def get_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    
    detections = DetectionService.get_user_detections(db, current_user.id, skip, limit)
    total = DetectionService.count_user_detections(db, current_user.id)
    return {"detections": detections, "total": total}

@router.get("/{detection_id}", response_model=DetectionResponse)
def get_detection(
    detection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if detection_id < 1:
        raise HTTPException(status_code=400, detail="Invalid detection ID")
    
    detection = DetectionService.get_detection_by_id(db, detection_id, current_user.id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection
