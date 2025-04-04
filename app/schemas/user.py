from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    class Roles(str, Enum):
        DOCTOR = "Doctor"
        PATIENT = "Patient"

    name: str
    email: EmailStr
    roles: Roles = Field(..., description="Roles (patient, doctor")
    password: str
