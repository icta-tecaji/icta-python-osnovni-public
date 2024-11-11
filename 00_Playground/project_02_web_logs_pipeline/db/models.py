"""Database models for the web logs pipeline."""

from __future__ import annotations

from db.db import engine
from sqlalchemy import Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for database models."""


class IpMetadataModel(Base):
    """Model for IP metadata."""

    __tablename__ = "ip_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String(), index=True, unique=True)
    country: Mapped[str] = mapped_column(String(), nullable=True)
    country_code: Mapped[str] = mapped_column(String(), nullable=True)
    region: Mapped[str] = mapped_column(String(), nullable=True)
    region_name: Mapped[str] = mapped_column(String(), nullable=True)
    city: Mapped[str] = mapped_column(String(), nullable=True)
    zip: Mapped[str] = mapped_column(String(), nullable=True)
    lat: Mapped[float] = mapped_column(Float(), nullable=True)
    lon: Mapped[float] = mapped_column(Float(), nullable=True)
    isp: Mapped[str] = mapped_column(String(), nullable=True)
    organization: Mapped[str] = mapped_column(String(), nullable=True)
    autonomous_system: Mapped[str] = mapped_column(String(), nullable=True)


Base.metadata.create_all(engine)
