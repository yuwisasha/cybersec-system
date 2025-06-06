from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event_log import EventLog


class EventSource(Base):
    """Источник события."""
    __tablename__ = "event_sources"

    id: Mapped[str] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    logs: Mapped[list["EventLog"]] = relationship(back_populates="source")

    def __str__(self):
        return f"{self.ip_address} {self.name} {self.type}"
