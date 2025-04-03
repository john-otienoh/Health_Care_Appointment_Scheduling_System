from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from decouple import config
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

def get_db_url():
    return f"postgresql://{urllib.parse.quote_plus(os.getenv('DB_USER'))}:{urllib.parse.quote_plus(os.getenv('DB_PASS'))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# SQLALCHEMY_DATABASE_URL = f'postgresql://{config("DB_USER")}:{config("DB_PASS")}@{config("DB_HOST")}:{config("DB_PORT")}/{config("DB_NAME")}'
SQLALCHEMY_DATABASE_URL = get_db_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
