from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident import Incident
    from app.models.recommendation import Recommendation


class IncidentRecommendation(Base):
    """Назначение рекомендации."""
    __tablename__ = "incident_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"), nullable=False
    )
    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey("recommendations.id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column()
    status: Mapped[str] = mapped_column()

    incident: Mapped[list["Incident"]] = relationship(
        "Incident", back_populates="recommendations"
    )
    recommendation: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="assignments"
    )
