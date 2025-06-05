from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import RecommendationStatusUpdateRequest
from app.services import update_recommendation_status
from app.deps import get_db
from app.core.auth import require_admin

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.patch("/{recommendation_id}", dependencies=[Depends(require_admin)])
def patch_recommendation_status(
    recommendation_id: int,
    payload: RecommendationStatusUpdateRequest,
    db: Session = Depends(get_db),
):
    update_recommendation_status(recommendation_id, payload.status, db)
    return {
        "status": "updated",
        "recommendation_id": recommendation_id,
        "new_status": payload.status,
    }
