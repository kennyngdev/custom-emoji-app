from fastapi import FastAPI

from api.custom_emoji_router import custom_emoji_router
from api.redis_router import redis_router
from api.task_queue_router import task_queue_router

app = FastAPI()
app.include_router(custom_emoji_router)
app.include_router(task_queue_router)
app.include_router(redis_router)

