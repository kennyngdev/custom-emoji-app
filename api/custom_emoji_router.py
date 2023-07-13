from fastapi import APIRouter

custom_emoji_router = APIRouter(
    prefix='/custom-emoji',
    tags=['custom_emoji']
)


# TODO
@custom_emoji_router.get('/emojis')
def get_all_emojis():
    pass


# TODO
@custom_emoji_router.post('/emojis')
def create_emoji():
    pass
