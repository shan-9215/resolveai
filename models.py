from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="open")
    priority: Mapped[str] = mapped_column(nullable=False, default="medium")
    category: Mapped[str | None] = mapped_column(nullable=True)
    impact: Mapped[str | None] = mapped_column(nullable=True)
    urgency: Mapped[str | None] = mapped_column(nullable=True)
    ai_summary: Mapped[str | None] = mapped_column(nullable=True)
    ai_confidence: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())
