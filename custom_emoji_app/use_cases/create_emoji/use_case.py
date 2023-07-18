from custom_emoji_app.entities.emoji import Emoji
from custom_emoji_app.use_cases.create_emoji.Irepo import ICreateEmojiRepository
from custom_emoji_app.use_cases.create_emoji.Iuse_case import ICreateEmoji
from custom_emoji_app.use_cases.create_emoji.input_dto import CreateEmojiInputDto


class CreateEmoji(ICreateEmoji):
    def __init__(self, repository: ICreateEmojiRepository):
        self.repository = repository

    def __call__(self, input_dto: CreateEmojiInputDto):
        # create entity
        emoji = Emoji(name=input_dto.name, image_data=input_dto.image_data)
        emoji.transform_to_thumbnail_gif()

        # save to DB
        self.repository.save_emoji(name=emoji.name, image_data=emoji.image_data)

        return 'success'
