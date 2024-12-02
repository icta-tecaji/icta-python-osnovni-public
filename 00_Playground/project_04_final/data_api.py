from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import Float, Integer, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for database models."""


class MeritveAltTest(Base):
    """Data model for the message data."""

    __tablename__ = "alt_test"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=True)
    uptime: Mapped[int] = mapped_column(Integer, nullable=True)
    ntc_temp: Mapped[float] = mapped_column(Float, nullable=True)
    bridge_temp: Mapped[float] = mapped_column(Float, nullable=True)
    target_speed_rpm: Mapped[int] = mapped_column(Integer, nullable=True)
    speed_rpm: Mapped[int] = mapped_column(Integer, nullable=True)
    motor_power_w: Mapped[int] = mapped_column(Integer, nullable=True)


app = FastAPI()
engine = create_async_engine("sqlite+aiosqlite:///../../meritve.db", echo=False)


class MeritevSchema(BaseModel):
    """Data model for the message data."""

    timestamp: int | None = None
    uptime: int | None = None
    ntc_temp: float | None = None
    bridge_temp: float | None = None
    target_speed_rpm: int | None = None
    speed_rpm: int | None = None
    motor_power_w: int | None = None


class ReadMeritveSchema(BaseModel):
    """Data model for the message data."""

    status: bool = False
    total_meritve: int = 0
    meritve: list[MeritevSchema] = []


async def get_data_from_db(start_timestamp: int | None, end_timestamp: int | None, limit: int | None) -> list[tuple]:
    """Get all the data from the database."""
    stmt = select(MeritveAltTest)

    if start_timestamp is not None:
        stmt = stmt.where(MeritveAltTest.timestamp >= start_timestamp)

    if end_timestamp is not None:
        stmt = stmt.where(MeritveAltTest.timestamp <= end_timestamp)

    if limit is not None:
        stmt = stmt.limit(limit)

    async with engine.connect() as conn:
        result = await conn.execute(stmt)
        return list(result.fetchall())  # type: ignore  # noqa: PGH003


@app.get("/meritve", response_model=ReadMeritveSchema)
async def get_meritve(
    start_timestamp: Annotated[int | None, Query(description="Start timestamp.")] = None,
    end_timestamp: Annotated[int | None, Query(description="End timestamp.")] = None,
    limit: Annotated[int | None, Query(description="Limit the number of results.")] = 100,
) -> ReadMeritveSchema:
    """Get all the data from the database."""
    data = await get_data_from_db(start_timestamp, end_timestamp, limit)
    return ReadMeritveSchema(
        status=True,
        total_meritve=len(data),
        meritve=[MeritevSchema.model_validate(row, from_attributes=True) for row in data],
    )
