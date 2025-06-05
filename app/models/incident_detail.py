from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident import Incident


class IncidentDetail(Base):
    __tablename__ = "incident_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"), nullable=False
    )
    added_at: Mapped[date] = mapped_column()
    comment: Mapped[str | None] = mapped_column(nullable=True)

    incident: Mapped[list["Incident"]] = relationship(
        "Incident", back_populates="breakdowns"
    )
