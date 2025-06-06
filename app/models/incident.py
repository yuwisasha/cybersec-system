from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident_detail import IncidentDetail
    from app.models.incident_recommendation import IncidentRecommendation


class Incident(Base):
    """Инцидент."""
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()

    breakdowns: Mapped[list["IncidentDetail"]] = relationship(
        back_populates="incident"
    )
    recommendations: Mapped[list["IncidentRecommendation"]] = relationship(
        back_populates="incident"
    )

    def __str__(self):
        return f"{self.created_at} {self.description} {self.status}"
