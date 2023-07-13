from abc import ABC, abstractmethod


class IRedisRepo(ABC):
    @abstractmethod
    async def get_cache(self, key: str):
        pass

    @abstractmethod
    async def get_all_cache(self):
        pass

    @abstractmethod
    async def set_cache(self):
        pass

    @abstractmethod
    async def delete_cache_with_key(self, key):
        pass
