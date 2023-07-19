from fastapi import FastAPI

from api.router.custom_emoji_router import custom_emoji_router
from api.router.task_queue_router import task_queue_router

tags_metadata = [
    {
        'name': 'custom_emoji',
        'description': 'Creating and getting emojis.'
    },
    {
        'name': 'task_queue',
        'description': 'Tracking task status and getting results'
    }
]

app = FastAPI(
    title='Custom Emoji App',
    description='This is an API application that allows user to create custom emojis for communication apps, '
                'which allows them to create small thumbnail images.'
                'Utilizing a log-running task queue, it can fulfill the functionalities of accepting image files, '
                'creating thumbnails and allowing them to be fetched when done processing.',
    version='1.0.0',
    openapi_tags=tags_metadata
)
app.include_router(custom_emoji_router)
app.include_router(task_queue_router)
