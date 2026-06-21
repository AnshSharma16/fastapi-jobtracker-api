from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserResponse
)
from app.services import user_service
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(
        user,
        db
    )

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return user_service.login_user(
        form_data,
        db
    )

@router.get("/me")
def get_me(
    current_user: UserModel = Depends(
        get_current_user
    )
):
    return current_user

