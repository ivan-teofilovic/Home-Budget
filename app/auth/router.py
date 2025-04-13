from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
from fastapi import APIRouter, Form, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

from app.auth.config import auth_settings
from app.dependencies import HashDep, SessionDep
from app.auth.models import User, UserCreate, TokenResponse
from app.auth.service import get_user, register_user

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    hash_service: HashDep,
):
    existing_user = await get_user(form_data.username, session)
    if not existing_user or not hash_service.verify(
        form_data.password, existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data_to_encode = {
        "sub": existing_user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=auth_settings.JWT_EXPIRE),
    }
    encoded_jwt = jwt.encode(
        data_to_encode, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALGORITHM
    )
    return TokenResponse(access_token=encoded_jwt, token_type="bearer")


@router.post("/register")
async def register(
    user: Annotated[UserCreate, Form()], session: SessionDep, hash_service: HashDep
):
    existing_user = await get_user(user.username, session)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = hash_service.hash(user.password)
    user = User(**user.model_dump(), hashed_password=hashed_password)
    await register_user(user, session)

    return Response(status_code=201)
