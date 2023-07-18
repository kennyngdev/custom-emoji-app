from pydantic import BaseModel


class GetEmojiByNameInputDto(BaseModel):
    name: str
