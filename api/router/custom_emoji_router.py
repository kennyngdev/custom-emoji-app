import base64

from fastapi import APIRouter, UploadFile, HTTPException, File

custom_emoji_router = APIRouter(
    prefix='/custom-emoji',
    tags=['custom_emoji']
)


# TODO
@custom_emoji_router.get('/emojis')
async def get_all_emojis():
    pass

@custom_emoji_router.post('/emojis')
async def create_emoji(file: UploadFile = File(None)):
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


    pass
