import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from users.schemas import UserLoginSchema, UserRegisterSchema
from users.models import UserModel

from typing import Annotated
from core.database import get_db

# sqlalchemy
from sqlalchemy.orm import Session

# Authentication with jwt
from auth.jwt_auth import generate_access_token, generate_refresh_token


router = APIRouter(tags=["users"], prefix="/users")


# Token generator for basic token authentication
# def generate_token(length=32):
#     """Generate a secure random token as a string."""
#     return secrets.token_hex(length)


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    db: Annotated[Session, Depends(get_db)],
):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="username or password Invalid"
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="username or password Invalid"
        )

    # Token Based Authentication
    # token_obj = TokenModel(user_id=user_obj.id, token=generate_token())
    # db.add(token_obj)
    # db.commit()
    # db.refresh(token_obj)
    
    # JWT Authentication
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse({"message": "logged in successfully!", "access_token": access_token, "refresh_token": refresh_token})


@router.post("/register")
async def user_register(
    request: UserRegisterSchema,
    db: Annotated[Session, Depends(get_db)],
):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already exists"
        )
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse({"detail": "user registered successfully"})
