from abc import ABC, abstractmethod
from typing import Any


class ICreateEmojiRepository(ABC):
    @abstractmethod
    def check_if_name_already_exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def save_emoji(self, name: str, image_data: str):
        pass
