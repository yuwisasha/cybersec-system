from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event_log import EventLog


class Event(Base):
    """Событие."""
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    description: Mapped[str] = mapped_column()

    logs: Mapped[list["EventLog"]] = relationship(back_populates="event")

    def __str__(self):
        return f"{self.created_at} {self.description}"
