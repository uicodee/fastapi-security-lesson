from fastapi import APIRouter, Query, Depends, HTTPException, status

from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/weather")

city_info = [
    {
        "city": "Ferghana",
        "temperature": 10
    },
    {
        "city": "Tashkent",
        "temperature": 11
    }
]


@router.get(
    path="/"
)
async def get_weather(
        api_key: str = Query(alias="apiKey"),
        city: str = Query(),
        dao: HolderDao = Depends(dao_provider)
):
    user = await dao.user.get_user_by_api_key(api_key=api_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with entered api key not found"
        )
    if user.limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The limit has been reached"
        )
    for current_city in city_info:
        if city == current_city.get('city'):
            await dao.user.decrease_limit(user_id=user.id, limit=user.limit - 1)
            return current_city
