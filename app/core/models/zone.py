from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import Base, pk, created_at, updated_at


class ServiceZone(Base):
    __tablename__ = "service_zones"

    id: Mapped[pk]
    name: Mapped[str]
    base_price: Mapped[float] = mapped_column(DECIMAL(10, 2), default=50)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class DriverZoneMap(Base):
    __tablename__ = "driver_zone_maps"
    id: Mapped[pk]
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    zone_id: Mapped[int] = mapped_column(ForeignKey("service_zones.id"))
