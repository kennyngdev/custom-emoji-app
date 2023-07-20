import base64

from fastapi import APIRouter, UploadFile, HTTPException, File
from starlette.responses import Response

from api.responses.get_all_emojis import GetAllEmojisResponse
from custom_emoji_app.repositories.redis.repo import RedisRepository
from custom_emoji_app.use_cases.get_emojis.input_dto import GetEmojiByNameInputDto
from custom_emoji_app.use_cases.get_emojis.use_case import GetEmojis
from worker.tasks import upload_emoji

custom_emoji_router = APIRouter(
    prefix='/custom-emoji',
    tags=['custom_emoji']
)


@custom_emoji_router.get('/emojis')
async def get_all_emojis() -> GetAllEmojisResponse:
    """
    ## Retrieves a list of all emojis, including their name and image data, which is encoded as base64 strings.

    ### Description
    Get all emojis available.

    ### Response
    - **200 OK** - A list of all emojis, including their name and base64 string.
    """
    repo = RedisRepository()
    use_case = GetEmojis(repository=repo)
    result = use_case.get_all_emojis()
    return GetAllEmojisResponse(data=result)


@custom_emoji_router.get('/emojis/{name}')
async def get_emoji_by_name(name: str):
    """
    ## Get Emoji Thumbnail by Name

    ### Parameters

    - **name** (query parameter): Name of the desired emoji.

    ### Response

    - **200 OK** - A GIF thumbnail image with size 100x100.
    - **400 ERR** - Error when no emoji with the inputted name is found.
    """
    input_dto = GetEmojiByNameInputDto(name=name)
    repo = RedisRepository()
    use_case = GetEmojis(repository=repo)
    try:
        image_bytes = use_case.get_emoji_by_name(input_dto)
        return Response(content=image_bytes, media_type='image/gif')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@custom_emoji_router.post('/emojis')
async def create_emoji(name: str, file: UploadFile = File(None)):
    """
    ## Upload Emoji

    ### Parameters

    - **name** (query parameter): Name of the emoji. Existing names cannot be used twice.
    - **file** (form field): An image file of an emoji with the type JPEG, PNG, or GIF.

    ### Response

    - **200 OK** - A Task ID which can be used to track the processing status of the task.
    - **400 ERR** - Error when there is an issue with the name or file.
    """
    repo = RedisRepository()
    # Name check:
    # Throw error if no name is defined
    if not name:
        raise HTTPException(status_code=400, detail="No name for emoji specified.")
    # Throw error if name already exists
    if repo.name_already_exists(name):
        raise HTTPException(status_code=400, detail="Emoji with the same name already exists")

    # File check:
    # Throw error if no file is uploaded
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

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
