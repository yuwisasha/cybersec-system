from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import (
    SeverityLevel,
    EventCategory,
)
from app.schemas.ingest import EventIngestRequest, AlertItem
from app.services import process_event
from app.deps import get_db

router = APIRouter(prefix="/ingest", tags=["Ingest"])


@router.post("/event/api/v2/alerts")  # Требование к пути loki-alertmanager
def ingest_event(alerts: list[AlertItem], db: Session = Depends(get_db)):
    for alert in alerts:
        event_request = EventIngestRequest(
            source_ip=alert.labels.source_ip,
            message=alert.annotations.summary,
            user_login=alert.labels.user_login,
            category_id=db.query(EventCategory).filter(
                EventCategory.name == alert.labels.category,
            ).first().id,
            severity_id=db.query(SeverityLevel).filter(
                SeverityLevel.name == alert.labels.severity,
            ).first().id,
            timestamp=alert.startsAt,
        )
        print(alert.model_dump_json())
        event_id = process_event(event_request, db)
        return {"status": "ok", "event_id": event_id}
