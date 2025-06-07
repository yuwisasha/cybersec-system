from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models import (
    ReactionRule,
    EventLog,
    Incident,
    IncidentDetail,
    IncidentRecommendation,
    EventSource,
    SeverityLevel,
    Recommendation,
)
from app.core.telegram import send_telegram_alert


def apply_reaction(event_log: EventLog, db: Session):
    source = (
        db.query(EventSource).filter_by(ip_address=event_log.source_ip).first()
    )
    if not source:
        print(1)
        return

    rule = (
        db.query(ReactionRule)
        .filter_by(
            severity_id=event_log.severity_id,
            category_id=event_log.category_id,
            source_type=source.type,
        )
        .first()
    )

    if not rule:
        print(2)
        return

    # Поиск открытого инцидента по совпадающим параметрам
    recent_threshold = datetime.now() - timedelta(minutes=5)
    existing_incident = (
        db.query(Incident)
        .join(IncidentDetail, Incident.id == IncidentDetail.incident_id)
        .join(EventLog, EventLog.event_id == IncidentDetail.event_id)
        .filter(
            (Incident.status == "открыт") |
            (EventLog.category_id == event_log.category_id) |
            (EventLog.severity_id == event_log.severity_id) |
            (EventLog.source_ip == event_log.source_ip) |
            (Incident.created_at >= recent_threshold),
        )
        .first()
    )

    if existing_incident:
        print(3)
        incident = existing_incident
        logger.info(
            f"Привязываем событие #{event_log.event_id}"
            f"к существующему инциденту #{incident.id}"
        )
    else:
        incident = Incident(
            created_at=datetime.now().date(),
            description=event_log.message,
            status="открыт",
        )
        db.add(incident)
        db.flush()
        logger.info(
            f"Создан новый инцидент #{incident.id}"
            f"под событие #{event_log.event_id}"
        )

        db.add(
            IncidentRecommendation(
                incident_id=incident.id,
                recommendation_id=rule.recommendation_id,
                assigned_at=datetime.now().date(),
                status="новая",
            )
        )

    # Привязываем событие к инциденту
    db.add(
        IncidentDetail(
            incident_id=incident.id,
            event_id=event_log.event_id,
            added_at=datetime.now().date(),
            comment=None,
        )
    )

    # Критический инцидент — уведомление
    severity = (
        db.query(SeverityLevel).filter_by(id=event_log.severity_id).first()
    )
    recomnendation = (
        db.query(Recommendation).filter_by(id=rule.recommendation_id).first()
    )
    if severity and severity.name.lower() == "критический":
        print(4)
        print("====== Telegram sending ======")
        send_telegram_alert(
            f"⚠️ <b>Критический инцидент #{incident.id}</b>\n"
            f"🧾 {event_log.message}\n"
            f"📍 Источник: {event_log.source_ip}\n"
            f"👤 Пользователь: {event_log.user_login}"
            f"⚠️ Рекомендация: {recomnendation.content}"
        )

    db.commit()
