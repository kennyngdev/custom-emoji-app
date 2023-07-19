import os
from typing import Any

import jsonpickle
import redis
from dotenv import load_dotenv

from custom_emoji_app.entities.emoji import Emoji
from custom_emoji_app.use_cases.create_emoji.Irepo import ICreateEmojiRepository
from custom_emoji_app.use_cases.get_emojis.Irepo import IGetEmojisRepository

load_dotenv()


class RedisRepository(ICreateEmojiRepository, IGetEmojisRepository):
    def __init__(self):
        # read redis configuration parameter from env
        self.connection_parameter = {
            "host": os.getenv('REDIS_HOST'),
            "port": os.getenv('REDIS_PORT'),
            "db": os.getenv('REDIS_DB')}
        self.client = redis.Redis(**self.connection_parameter)

    def name_already_exists(self, name: str) -> bool:
        result = self.client.get(name)
        if result:
            return True
        return False

    def save_emoji(self, name: str, image_data: str):
        self.client.set(name, image_data)

    def get_all_emojis(self) -> list[Emoji]:
        res = list()
        for key in self.client.scan_iter():
            decoded_key = key.decode("utf-8")
            val = self.client.get(key)
            val = val.decode("utf-8")
            res.append(Emoji(name=decoded_key, image_data=val))
        return res

    def get_emoji_by_name(self, name) -> Emoji:
        res = self.client.get(name)
        if res:
            return Emoji(name=name, image_data=res.decode('utf-8'))
        raise ValueError(f'No emoji found by the name {name}')
