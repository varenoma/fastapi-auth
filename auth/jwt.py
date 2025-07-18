from datetime import timedelta, datetime
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv

load_dotenv()


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        getenv("MY_SECRET_KEY", "no_secret_key"),
        algorithm=getenv("ALGORITHM", "HS256"),
    )
    return encoded_jwt
