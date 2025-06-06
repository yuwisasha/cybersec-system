from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event_log import EventLog
    from app.models.reaction_rule import ReactionRule


class SeverityLevel(Base):
    """Уровень критичности."""

    __tablename__ = "severity_levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    explanation: Mapped[str | None] = mapped_column(nullable=True)

    logs: Mapped[list["EventLog"]] = relationship(back_populates="severity")
    rules: Mapped[list["ReactionRule"]] = relationship(
        back_populates="severity"
    )

    def __str__(self):
        return f"{self.name} {self.explanation}"
