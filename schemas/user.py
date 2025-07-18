from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreateSchemas(BaseModel):
    username: str = Field(
        ...,
    )
    email: EmailStr
    password: str


class UserCreateResponseSchemas(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchemas(BaseModel):
    username: str
    password: str
