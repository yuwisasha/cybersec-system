from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ingest import EventIngestRequest
from app.services import process_event
from app.deps import get_db

router = APIRouter(prefix="/ingest", tags=["Ingest"])


@router.post("/event/api/v2/alerts")   # Требование к пути loki-alertmanager
def ingest_event(payload: EventIngestRequest, db: Session = Depends(get_db)):
    event_id = process_event(payload, db)
    return {"status": "ok", "event_id": event_id}
