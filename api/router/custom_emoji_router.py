import base64

from fastapi import APIRouter, UploadFile, HTTPException, File

from custom_emoji_app.repositories.redis.repo import RedisRepository
from custom_emoji_app.use_cases.get_emojis.input_dto import GetEmojiByNameInputDto
from custom_emoji_app.use_cases.get_emojis.use_case import GetEmojis
from worker.tasks import upload_emoji

custom_emoji_router = APIRouter(
    prefix='/custom-emoji',
    tags=['custom_emoji']
)


@custom_emoji_router.get('/emojis')
async def get_all_emojis():
    repo = RedisRepository()
    use_case = GetEmojis(repository=repo)
    result = use_case.get_all_emojis()
    return result


@custom_emoji_router.get('/emojis/{name}')
async def get_emoji_by_name(name: str):
    input_dto = GetEmojiByNameInputDto(name=name)
    repo = RedisRepository()
    use_case = GetEmojis(repository=repo)
    result = use_case.get_emoji_by_name(input_dto)
    return result


@custom_emoji_router.post('/emojis')
async def create_emoji(name: str, file: UploadFile = File(None)):
    repo = RedisRepository()
    # Name check:
    # Throw error if no name is defined
    if not name:
        return HTTPException(status_code=400, detail="No name for emoji specified.")
    if repo.name_already_exists(name):
        return HTTPException(status_code=400, detail="Emoji with the same name already exists")

    # File check:
    # Throw error if no file is uploaded
    if not file:
        return HTTPException(status_code=400, detail="No file uploaded.")

    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > 50 * 1024 * 1024:
        # more than 50 MB
        raise HTTPException(status_code=400, detail="File too large")

    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file with the type "
                                                    "jpeg, png or gif.")

    file_content = await file.read()
    encoded_image_data = base64.b64encode(file_content).decode()

    async_result = upload_emoji.delay(name=name, image_data=encoded_image_data)

    return {'task_id': async_result.id}
