from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.config.settings import get_settings
from sqlalchemy.orm import sessionmaker


settings = get_settings()

engine = create_engine(
    settings.DATABASE_URI,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
