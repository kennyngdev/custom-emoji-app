from typing import Any

from fastapi import APIRouter

from custom_emoji_app.repositories.redis.repo import RedisRepo

redis_router = APIRouter(
    prefix='/redis',
    tags=['redis']
)


@redis_router.get('/data')
async def get_data_by_key(key: str):
    repo = RedisRepo()
    return await repo.get_data_by_key(key)


@redis_router.get('/all_data')
async def get_all_data():
    repo = RedisRepo()
    return await repo.get_all_data()


@redis_router.post('/data')
async def set_data(key: str, value: Any):
    repo = RedisRepo()
    await repo.set_data(key, value)
    return 'success'


@redis_router.delete('/data')
async def delete_data_by_key(key: str):
    repo = RedisRepo()
    await repo.delete_data_by_key()
    return 'success'
