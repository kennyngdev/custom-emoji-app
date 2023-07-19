from custom_emoji_app.entities.emoji import Emoji
from custom_emoji_app.use_cases.get_emojis.Irepo import IGetEmojisRepository
from custom_emoji_app.use_cases.get_emojis.Iuse_case import IGetEmojis
from custom_emoji_app.use_cases.get_emojis.input_dto import GetEmojiByNameInputDto


class GetEmojis(IGetEmojis):
    def __init__(self, repository: IGetEmojisRepository):
        self.repository = repository

    def get_all_emojis(self):
        return self.repository.get_all_emojis()

    def get_emoji_by_name(self, input_dto: GetEmojiByNameInputDto):
        emoji : Emoji = self.repository.get_emoji_by_name(input_dto.name)
        return emoji.get_image_as_bytes()
