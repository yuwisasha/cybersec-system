from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.user import User
    from app.models.event_category import EventCategory
    from app.models.severity_level import SeverityLevel
    from app.models.event_source import EventSource


class EventLog(Base):
    """Журнал событий."""
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"), nullable=False
    )
    user_login: Mapped[str] = mapped_column(
        ForeignKey("users.login"), nullable=True,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("event_categories.id"), nullable=False
    )
    severity_id: Mapped[int] = mapped_column(
        ForeignKey("severity_levels.id"), nullable=False
    )
    source_ip: Mapped[str] = mapped_column(
        ForeignKey("event_sources.ip_address"), nullable=False
    )
    message: Mapped[str | None] = mapped_column(nullable=True)

    event: Mapped[list["Event"]] = relationship("Event", back_populates="logs")
    user: Mapped[list["User"]] = relationship("User", back_populates="events")
    category: Mapped[list["EventCategory"]] = relationship(
        "EventCategory", back_populates="logs"
    )
    severity: Mapped[list["SeverityLevel"]] = relationship(
        "SeverityLevel", back_populates="logs"
    )
    source: Mapped[list["EventSource"]] = relationship(
        "EventSource", back_populates="logs"
    )

    def __str__(self):
        return f"#{self.id} {self.user_login} {self.message}"
