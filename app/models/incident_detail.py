from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident import Incident


class IncidentDetail(Base):
    """Разбор инцидента."""
    __tablename__ = "incident_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"), nullable=False
    )
    added_at: Mapped[datetime] = mapped_column(default=datetime.now())
    comment: Mapped[str | None] = mapped_column(nullable=True)

    incident: Mapped[list["Incident"]] = relationship(
        "Incident", back_populates="breakdowns"
    )

    def __str__(self):
        return f"{self.added_at} {self.comment}"
