from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt


from models.user import Users


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(Users).where(Users.username == username))
    return result.scalar_one_or_none()


async def get_user_by_username_and_email(
    db: AsyncSession,
    username: str,
    email: str,
):
    result = await db.execute(
        select(Users).where(Users.username == username or Users.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: str, password: str):
    h_password = bcrypt.hash(password)
    new_user = Users(username=username, email=email, password=h_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
