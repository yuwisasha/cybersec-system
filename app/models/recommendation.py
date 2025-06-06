from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident_recommendation import IncidentRecommendation
    from app.models.reaction_rule import ReactionRule


class Recommendation(Base):
    """Рекомендация."""
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    assignments: Mapped[list["IncidentRecommendation"]] = relationship(
        back_populates="recommendation"
    )
    rules: Mapped[list["ReactionRule"]] = relationship(
        back_populates="recommendation"
    )

    def __str__(self):
        return f"{self.created_at} {self.content}"
