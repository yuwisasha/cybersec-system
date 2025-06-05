from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services import (
    get_event_list,
    get_event_detail,
)
from app.schemas import (
    EventLogShort,
    EventLogDetails,
)
from app.deps import get_db
from app.core.auth import require_admin

router = APIRouter(prefix="/events", tags=["Events"])


@router.get(
    "/",
    response_model=list[EventLogShort],
    dependencies=[Depends(require_admin)],
)
def list_events(
    db: Session = Depends(get_db),
    category_id: int | None = Query(None),
    severity_id: int | None = Query(None),
    user_login: str | None = Query(None),
    source_ip: str | None = Query(None),
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
):
    return get_event_list(
        db=db,
        category_id=category_id,
        severity_id=severity_id,
        user_login=user_login,
        source_ip=source_ip,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/{event_id}", response_model=EventLogDetails)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return get_event_detail(event_id, db)
