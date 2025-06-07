from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.severity_level import SeverityLevel
    from app.models.recommendation import Recommendation


class ReactionRule(Base):
    """Правило реагирования."""
    __tablename__ = "reaction_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    severity_id: Mapped[int] = mapped_column(ForeignKey("severity_levels.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("event_categories.id"))
    source_type: Mapped[str] = mapped_column()
    recommendation_id: Mapped[int] = mapped_column(
        ForeignKey("recommendations.id")
    )

    severity: Mapped[list["SeverityLevel"]] = relationship(
        "SeverityLevel", back_populates="rules"
    )
    recommendation: Mapped[list["Recommendation"]] = relationship(
        "Recommendation", back_populates="rules"
    )

    def __str__(self):
        return f"Rule #{self.id}"
