from typing import Any

from fastapi import APIRouter

from custom_emoji_app.repositories.redis.repo import RedisRepository

redis_router = APIRouter(
    prefix='/redis',
    tags=['redis']
)


@redis_router.get('/data')
async def get_data_by_key(key: str):
    repo = RedisRepository()
    return repo.get_data_by_key(key)


@redis_router.get('/all_data')
async def get_all_data():
    repo = RedisRepository()
    return repo.get_all_data()


@redis_router.post('/data')
async def set_data(key: str, value: Any):
    repo = RedisRepository()
    repo.set_data(key, value)
    return 'success'


@redis_router.delete('/data')
async def delete_data_by_key(key: str):
    repo = RedisRepository()
    repo.delete_data_by_key(key)
    return 'success'
