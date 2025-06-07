from datetime import date

from fastapi import HTTPException

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    Incident,
    EventLog,
    Event,
    EventCategory,
    SeverityLevel,
    Recommendation,
    IncidentRecommendation,
    IncidentDetail,
)
from app.schemas import (
    IncidentDetailsResponse,
    EventLogView,
    RecommendationView,
    IncidentListItem,
)


def get_incident_detail(
    incident_id: int, db: Session
) -> IncidentDetailsResponse:
    incident = db.query(Incident).filter_by(id=incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")

    logs = (
        db.query(EventLog, Event, EventCategory, SeverityLevel)
        .join(Event, Event.id == EventLog.event_id)
        .join(IncidentDetail, IncidentDetail.event_id == Event.id)
        .join(EventCategory, EventCategory.id == EventLog.category_id)
        .join(SeverityLevel, SeverityLevel.id == EventLog.severity_id)
        .filter(IncidentDetail.incident_id == incident_id)
        .all()
    )

    events = [
        EventLogView(
            event_id=event.id,
            timestamp=event.created_at,
            message=log.message,
            source_ip=log.source_ip,
            user_login=log.user_login,
            category=category.name,
            severity=severity.name,
        )
        for log, event, category, severity in logs
    ]

    recs = (
        db.query(IncidentRecommendation, Recommendation)
        .join(
            Recommendation,
            Recommendation.id == IncidentRecommendation.recommendation_id,
        )
        .filter(IncidentRecommendation.incident_id == incident_id)
        .all()
    )

    recommendations = [
        RecommendationView(
            id=rec.recommendation.id,
            content=rec.recommendation.content,
            status=rec.status,
        )
        for rec, _ in recs
    ]

    return IncidentDetailsResponse(
        id=incident.id,
        created_at=incident.created_at,
        description=incident.description,
        status=incident.status,
        events=events,
        recommendations=recommendations,
    )


def update_incident_status(
    incident_id: int, new_status: str, db: Session
) -> None:
    incident = db.query(Incident).filter_by(id=incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")

    incident.status = new_status
    db.commit()


def get_incident_list(
    db: Session,
    status: str | None = None,
    search: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> list[IncidentListItem]:
    query = (
        db.query(
            Incident.id,
            Incident.created_at,
            Incident.description,
            Incident.status,
            func.count(IncidentDetail.id).label("event_count"),
            func.count(IncidentRecommendation.id).label(
                "recommendation_count"
            ),
        )
        .outerjoin(IncidentDetail, Incident.id == IncidentDetail.incident_id)
        .outerjoin(
            IncidentRecommendation,
            Incident.id == IncidentRecommendation.incident_id,
        )
        .group_by(Incident.id)
    )

    if status:
        query = query.filter(Incident.status.ilike(status))
    if search:
        query = query.filter(Incident.description.ilike(f"%{search}%"))
    if from_date:
        query = query.filter(Incident.created_at >= from_date)
    if to_date:
        query = query.filter(Incident.created_at <= to_date)

    rows = query.order_by(Incident.created_at.desc()).all()

    return [IncidentListItem.model_validate(row) for row in rows]
