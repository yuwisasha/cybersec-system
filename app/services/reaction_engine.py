from datetime import date

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
)
from app.core.telegram import send_telegram_alert


def apply_reaction(event_log: EventLog, db: Session):
    # Получаем тип источника
    source = (
        db.query(EventSource).filter_by(ip_address=event_log.source_ip).first()
    )
    if not source:
        return

    # Ищем правило
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
        return  # нет подходящего правила

    # Создаём инцидент
    incident = Incident(
        created_at=date.today(),
        description=f"Инцидент по событию #{event_log.event_id}",
        status="открыт",
    )
    db.add(incident)
    db.flush()

    # Привязка события
    db.add(
        IncidentDetail(
            incident_id=incident.id,
            event_id=event_log.event_id,
            added_at=date.today(),
            comment=None,
        )
    )

    # Привязка рекомендации
    db.add(
        IncidentRecommendation(
            incident_id=incident.id,
            recommendation_id=rule.recommendation_id,
            assigned_at=date.today(),
            status="новая",
        )
    )

    logger.info(
        f"Rule #{rule.id} triggered for event #{event_log.event_id}"
        f", incident #{incident.id} created"
    )

    severity = (
        db.query(SeverityLevel).filter_by(id=event_log.severity_id).first()
    )
    if severity and severity.name.lower() == "критический":
        send_telegram_alert(
            f"⚠️ <b>Критический инцидент #{incident.id}</b>\n"
            f"🧾 {event_log.message}\n"
            f"📍 Источник: {event_log.source_ip}\n"
            f"👤 Пользователь: {event_log.user_login}"
        )
