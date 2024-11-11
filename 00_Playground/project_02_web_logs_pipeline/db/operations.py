"""Database operations module."""

from __future__ import annotations

from db.db import engine
from db.models import IpMetadataModel
from sqlalchemy import insert, select


class IpMetadataOperations:
    """Operations for IP metadata."""

    def get_data(self, ip: str) -> dict | None:
        """Get data from the database."""
        with engine.connect() as conn:
            query = select(IpMetadataModel).where(IpMetadataModel.ip == ip)
            result = conn.execute(query)
            if result.rowcount == 0:
                return None
            data = result.fetchone()
            if data:
                return data._asdict()
            return None

    def insert_data(self, data: dict) -> None:
        """Insert data into the database."""
        with engine.connect() as conn:
            conn.execute(insert(IpMetadataModel), data)
            conn.commit()


ip_metadata_operations = IpMetadataOperations()
