from datetime import datetime
from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from app.core.models.base import Base, pk, created_at


class OrderStatus(PyEnum):
    new = "new"
    assigned = "assigned"
    accepted = "accepted"
    canceled = "canceled"
    completed = "completed"


class Order(Base):
    id: Mapped[pk]
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    zone_id: Mapped[int] = mapped_column(ForeignKey(""))
    status: Mapped[OrderStatus]
    pickup_address: Mapped[str]
    created_at: Mapped[created_at]
    assigned_at: Mapped[datetime] = mapped_column(nullable=True)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
