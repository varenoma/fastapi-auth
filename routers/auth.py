from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt

from auth.dependencies import get_current_user
from auth.jwt import create_access_token
from core.db_session import get_db
from cruds.auth import create_user, get_user_by_username, get_user_by_username_and_email
from schemas.user import UserCreateResponseSchemas, UserCreateSchemas

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserCreateResponseSchemas)
async def register(user_data: UserCreateSchemas, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username_and_email(
        db, username=user_data.username, email=user_data.email
    )

    if user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )
    return await create_user(
        db,
        user_data.username,
        user_data.email,
        user_data.password,
    )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_by_username(db, form_data.username)
    if not user or not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me")
async def read_user_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username}
