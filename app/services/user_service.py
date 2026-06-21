from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.schemas.user_schema import (
    UserCreate,
    UserLogin
)

from app.core.security import (
    hash_password,
    verify_password
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

def create_user(
    user_data: UserCreate,
    db: Session
):
    existing_user = db.query(
        UserModel
    ).filter(
        UserModel.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(
    form_data: OAuth2PasswordRequestForm,
    db: Session
):
    user = db.query(
        UserModel
    ).filter(
        UserModel.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    is_valid = verify_password(
        form_data.password,
        user.hashed_password
    )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
    {
        "sub": str(user.id)
    }
)

    return {
    "access_token": token,
    "token_type": "bearer"
}
    