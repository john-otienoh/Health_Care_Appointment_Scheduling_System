from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_session
from schemas.user import RegisterUserRequest
from responses.user import UserResponse

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    data: RegisterUserRequest, session: Session = Depends(get_session)
):
    pass
