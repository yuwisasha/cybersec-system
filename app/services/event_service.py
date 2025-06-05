from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import (
    EventLog,
    Event,
    EventCategory,
    SeverityLevel,
    IncidentDetail,
)
from app.schemas import (
    EventLogShort,
    EventLogDetails,
)


def get_event_list(
    db: Session,
    category_id: int | None = None,
    severity_id: int | None = None,
    user_login: str | None = None,
    source_ip: str | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
) -> list[EventLogShort]:
    query = (
        db.query(EventLog, Event, EventCategory, SeverityLevel)
        .join(Event, Event.id == EventLog.event_id)
        .join(EventCategory, EventCategory.id == EventLog.category_id)
        .join(SeverityLevel, SeverityLevel.id == EventLog.severity_id)
    )

    if category_id:
        query = query.filter(EventLog.category_id == category_id)
    if severity_id:
        query = query.filter(EventLog.severity_id == severity_id)
    if user_login:
        query = query.filter(EventLog.user_login.ilike(f"%{user_login}%"))
    if source_ip:
        query = query.filter(EventLog.source_ip.ilike(f"%{source_ip}%"))
    if from_date:
        query = query.filter(Event.created_at >= from_date)
    if to_date:
        query = query.filter(Event.created_at <= to_date)

    rows = query.order_by(Event.created_at.desc()).all()

    return [
        EventLogShort(
            event_id=event.id,
            timestamp=event.created_at,
            message=log.message,
            source_ip=log.source_ip,
            user_login=log.user_login,
            category=category.name,
            severity=severity.name
        )
        for log, event, category, severity in rows
    ]


def get_event_detail(event_id: int, db: Session) -> EventLogDetails:
    q = (
        db.query(EventLog, Event, EventCategory, SeverityLevel)
        .join(Event, Event.id == EventLog.event_id)
        .join(EventCategory, EventCategory.id == EventLog.category_id)
        .join(SeverityLevel, SeverityLevel.id == EventLog.severity_id)
        .filter(Event.id == event_id)
        .first()
    )
    if not q:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    log, event, category, severity = q

    incident_link = (
        db.query(IncidentDetail)
        .filter(IncidentDetail.event_id == event_id)
        .first()
    )
    return EventLogDetails(
        event_id=event.id,
        timestamp=event.created_at,
        source_ip=log.source_ip,
        user_login=log.user_login,
        message=log.message,
        category=category.name,
        severity=severity.name,
        incident_id=incident_link.incident_id if incident_link else None
    )
