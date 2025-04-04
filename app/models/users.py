from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    func,
    ForeignKey,
    Enum as SQLEnum,
)
from config.database import Base
from sqlalchemy.orm import mapped_column, relationship


class User(Base):
    class Roles(str, Enum):
        DOCTOR = "Doctor"
        PATIENT = "Patient"

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    roles = Column(SQLEnum(Roles))
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
