from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ingest import EventIngestRequest
from app.services import process_event
from app.deps import get_db
from app.core.auth import require_admin

router = APIRouter(prefix="/ingest", tags=["Ingest"])


@router.post("/event", dependencies=[Depends(require_admin)])
def ingest_event(payload: EventIngestRequest, db: Session = Depends(get_db)):
    event_id = process_event(payload, db)
    return {"status": "ok", "event_id": event_id}
