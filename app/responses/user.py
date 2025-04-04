from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseResponseModel


class UserResponse(BaseResponseModel):
    class Roles(str, Enum):
        DOCTOR = "Doctor"
        PATIENT = "Patient"

    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime | None
    roles: Roles
