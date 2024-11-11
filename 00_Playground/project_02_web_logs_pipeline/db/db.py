"""Database configuration."""

from __future__ import annotations

from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///logs_data.db", echo=False)
