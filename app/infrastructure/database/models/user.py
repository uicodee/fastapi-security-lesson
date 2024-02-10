from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models import BaseModel


class User(BaseModel):

    __tablename__ = "user"

    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    limit: Mapped[int] = mapped_column(Integer)
    api_key: Mapped[str] = mapped_column(String)
