from pydantic import BaseModel


class CreateEmojiInputDto(BaseModel):
    name: str  # name of emoji
    image_data: str  # image data as a base64 string
