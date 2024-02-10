from pydantic import Field

from app.dto import Base


class User(Base):

    full_name: str = Field(alias="fullName")
    email: str
    limit: int
    api_key: str = Field(alias="apiKey")


class UserWithPassword(User):

    password: str
