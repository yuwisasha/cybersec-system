from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.schemas import (
    IncidentDetailsResponse,
    IncidentStatusUpdateRequest,
    IncidentListItem,
)
from app.services import (
    get_incident_detail,
    update_incident_status,
    get_incident_list,
    generate_incident_report,
)
from app.deps import get_db
from app.core.auth import require_admin

router = APIRouter(prefix="/incident", tags=["Incident"])


@router.get(
    "/{incident_id}",
    response_model=IncidentDetailsResponse,
    dependencies=[Depends(require_admin)],
)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    return get_incident_detail(incident_id, db)


@router.patch("/{incident_id}", dependencies=[Depends(require_admin)])
def patch_incident_status(
    incident_id: int,
    payload: IncidentStatusUpdateRequest,
    db: Session = Depends(get_db),
):
    update_incident_status(incident_id, payload.status, db)
    return {
        "status": "updated",
        "incident_id": incident_id,
        "new_status": payload.status,
    }


@router.get(
    "/",
    response_model=list[IncidentListItem],
    dependencies=[Depends(require_admin)],
)
def list_incidents(
    db: Session = Depends(get_db),
    status: str | None = Query(None),
    search: str | None = Query(None),
    from_date: Annotated[date | None, Query(alias="from")] = None,
    to_date: Annotated[date | None, Query(alias="to")] = None,
):
    return get_incident_list(
        db=db,
        status=status,
        search=search,
        from_date=from_date,
        to_date=to_date,
    )


@router.get(
    "/export",
    response_class=StreamingResponse,
    dependencies=[Depends(require_admin)],
)
def export_incidents(db: Session = Depends(get_db)):
    file = generate_incident_report(db)
    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=incident_report.xlsx"
        },
    )
