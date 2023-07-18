from fastapi import FastAPI

from api.router.custom_emoji_router import custom_emoji_router
from api.router.redis_router import redis_router
from api.router.task_queue_router import task_queue_router

app = FastAPI()
app.include_router(custom_emoji_router)
app.include_router(task_queue_router)
app.include_router(redis_router)

