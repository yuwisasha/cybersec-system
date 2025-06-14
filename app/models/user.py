from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event_log import EventLog


class User(Base):
    """Пользователь."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()

    events: Mapped[list["EventLog"]] = relationship(back_populates="user")

    def __str__(self):
        return (
            f"{self.login} {self.last_name} "
            f"{self.first_name} {self.middle_name}"
        )
