"""
Database session management.
Creates the SQLAlchemy engine, session factory, and declarative Base.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# ── Engine ───────────────────────────────────────────────────────
# connect_args only needed for SQLite (single-threaded by default)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# ── Session Factory ──────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Declarative Base ─────────────────────────────────────────────
Base = declarative_base()
