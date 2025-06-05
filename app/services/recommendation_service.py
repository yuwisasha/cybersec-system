from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import IncidentRecommendation


def update_recommendation_status(
    recommendation_id: int, new_status: str, db: Session
) -> None:
    rec = (
        db.query(IncidentRecommendation)
        .filter_by(id=recommendation_id)
        .first()
    )
    if not rec:
        raise HTTPException(status_code=404, detail="Рекомендация не найдена")

    rec.status = new_status
    db.commit()
