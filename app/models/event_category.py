from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event_log import EventLog


class EventCategory(Base):
    """Категория события."""
    __tablename__ = "event_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(nullable=True)

    logs: Mapped[list["EventLog"]] = relationship(back_populates="category")

    def __str__(self):
        return f"{self.name}"
