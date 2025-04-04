from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config.settings import get_settings
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()


def get_db_url():
    return f"postgresql://{urllib.parse.quote_plus(os.getenv('DB_USER'))}:{urllib.parse.quote_plus(os.getenv('DB_PASS'))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# SQLALCHEMY_DATABASE_URL = f'postgresql://{config("DB_USER")}:{config("DB_PASS")}@{config("DB_HOST")}:{config("DB_PORT")}/{config("DB_NAME")}'
SQLALCHEMY_DATABASE_URL = get_db_url()

settings = get_settings()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
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
