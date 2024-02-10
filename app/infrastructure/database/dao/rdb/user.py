from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user(
            self,
            full_name: str,
            email: str,
            password: str,
            limit: int,
            api_key: str
    ) -> dto.User:
        result = await self.session.execute(
            insert(User).values(
                full_name=full_name,
                email=email,
                password=password,
                limit=limit,
                api_key=api_key
            ).returning(
                User
            )
        )
        await self.session.commit()
        return dto.User.from_orm(result.scalar())

    async def get_user(
            self,
            email: str,
            with_password: bool = False
    ) -> dto.User | dto.UserWithPassword:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar()
        if user is not None:
            if with_password:
                return dto.UserWithPassword.from_orm(user)
            else:
                return dto.User.from_orm(user)

    async def get_user_by_api_key(self, api_key: str) -> dto.User:
        result = await self.session.execute(
            select(User).where(User.api_key == api_key)
        )
        user = result.scalar()
        if user is not None:
            return dto.User.from_orm(user)

    async def decrease_limit(self, user_id: int, limit: int) -> dto.User:
        result = await self.session.execute(
            update(User).where(User.id == user_id).values(
                limit=limit
            ).returning(User)
        )
        await self.session.commit()
        return dto.User.from_orm(result.scalar())
