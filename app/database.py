import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


DEFAULT_DATABASE_URL = (
    "postgresql://postgres@localhost/"
    "ai_reliability_platform"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    DEFAULT_DATABASE_URL,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
