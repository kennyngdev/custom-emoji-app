import os
import traceback

from celery import Celery, states

from custom_emoji_app.repositories.redis.repo import RedisRepository
from custom_emoji_app.use_cases.create_emoji.input_dto import CreateEmojiInputDto
from custom_emoji_app.use_cases.create_emoji.use_case import CreateEmoji


# celery config
class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "json"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]
    task_acks_late = True
    task_track_started = True
    result_persistent = True
    worker_send_task_events = True


# Initializing celery app
app = Celery('tasks',
             backend=f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',
             broker=f'pyamqp://{os.getenv("RABBITMQ_HOST")}:{os.getenv("RABBITMQ_PORT")}')
# Apply Configurations
app.set_default()
app.config_from_object(CeleryConfig)


@app.task(bind=True)
def upload_emoji(self, name: str, image_data: str):
    try:
        input_dto = CreateEmojiInputDto(name=name, image_data=image_data)
        repo = RedisRepository()
        use_case = CreateEmoji(repository=repo)
        return use_case(input_dto)
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n'),
                'custom': 'emoji processing task failed.'
            }
        )
