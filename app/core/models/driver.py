from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from app.core.models.base import Base, pk, created_at, updated_at


class OrderStatus(PyEnum):
    new = "new"
    assigned = "assigned"
    accepted = "accepted"
    canceled = "canceled"
    completed = "completed"


class Driver(Base):
    id: Mapped[pk]
    balance: Mapped[float] = mapped_column(DECIMAL(10, 2))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
