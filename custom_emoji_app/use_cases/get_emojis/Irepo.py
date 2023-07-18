from abc import ABC, abstractmethod

from custom_emoji_app.use_cases.get_emojis.input_dto import GetEmojiByNameInputDto


class IGetEmojisRepository(ABC):
    @abstractmethod
    def get_all_emojis(self):
        pass

    @abstractmethod
    def get_emoji_by_name(self, input_dto: GetEmojiByNameInputDto):
        pass