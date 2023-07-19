from pydantic import BaseModel

from custom_emoji_app.entities.emoji import Emoji


class GetAllEmojisResponse(BaseModel):
    data: list[Emoji]
