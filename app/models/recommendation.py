from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident_recommendation import IncidentRecommendation
    from app.models.reaction_rule import ReactionRule


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    created_at: Mapped[date] = mapped_column()

    assignments: Mapped[list["IncidentRecommendation"]] = relationship(
        back_populates="recommendation"
    )
    rules: Mapped[list["ReactionRule"]] = relationship(
        back_populates="recommendation"
    )
