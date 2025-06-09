from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.deps import get_db
from app.services import generate_incident_report

router = APIRouter()


@router.get("/report/reactions")
def export_reaction_report(
    db: Session = Depends(get_db),
    from_: datetime = Query(None, alias="from"),
    to: datetime = Query(None),
):
    results = generate_incident_report(db, from_, to)

    return StreamingResponse(
        results,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # noqa
        headers={"Content-Disposition": "attachment; filename=detailed_reaction_report.xlsx"},  # noqa
    )
