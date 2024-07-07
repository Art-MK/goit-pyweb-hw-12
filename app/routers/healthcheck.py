from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, check_db_connection
from app.schemas import HealthCheckResponse

router = APIRouter()

@router.get("/healthcheck", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    try:
        check_db_connection()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "unhealthy", "details": str(e)}
