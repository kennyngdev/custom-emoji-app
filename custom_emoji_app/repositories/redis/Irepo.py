from abc import ABC, abstractmethod
from typing import Any


class IRedisRepo(ABC):
    @abstractmethod
    async def get_data_by_key(self, key: str):
        pass

    @abstractmethod
    async def get_all_data(self):
        pass

    @abstractmethod
    async def set_data(self, key: str, value: Any):
        pass

    @abstractmethod
    async def delete_data_by_key(self, key: str):
        pass
