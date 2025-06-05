from sqlalchemy.orm import Session

from app.models import Event, EventLog
from app.schemas.ingest import EventIngestRequest
from app.services.reaction_engine import apply_reaction


def process_event(data: EventIngestRequest, db: Session) -> int:
    event = Event(created_at=data.timestamp, description=data.message)
    db.add(event)
    db.flush()  # Получаем ID события

    log = EventLog(
        event_id=event.id,
        user_login=data.user_login,
        category_id=data.category_id,
        severity_id=data.severity_id,
        source_ip=data.source_ip,
        message=data.message,
    )
    db.add(log)
    db.flush()

    apply_reaction(log, db)
    db.commit()

    return event.id
