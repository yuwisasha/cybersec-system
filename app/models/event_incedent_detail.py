from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models.base import Base


class EventIncidentDetail(Base):
    """Событие_разбор."""

    __tablename__ = "event_incedent_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"), nullable=False
    )
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
