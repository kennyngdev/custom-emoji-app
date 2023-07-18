from abc import ABC, abstractmethod

from custom_emoji_app.use_cases.create_emoji.input_dto import CreateEmojiInputDto


class ICreateEmoji(ABC):
    @abstractmethod
    def __call__(self, input_dto: CreateEmojiInputDto):
        pass
