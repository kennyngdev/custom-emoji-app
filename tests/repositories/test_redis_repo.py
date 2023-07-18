import os
from unittest.mock import MagicMock

import pytest
import redis
from dotenv import load_dotenv

from custom_emoji_app.repositories.redis.repo import RedisRepository

load_dotenv()


@pytest.fixture
def redis_repository():
    return RedisRepository()


class TestRedisRepository:
    def test_name_already_exists_existing(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = b'{"key": "value"}'

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        result = redis_repository.name_already_exists("key")

        # Assert that the Redis client's get method was called with the correct key
        redis_client_mock.get.assert_called_once_with("key")

        # Assert that the result is True
        assert result is True

    def test_name_already_exists_not_found(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = None

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        result = redis_repository.name_already_exists("key")

        # Assert that the Redis client's get method was called with the correct key
        redis_client_mock.get.assert_called_once_with("key")

        # Assert that the result is False
        assert result is False

    def test_save_emoji(self, redis_repository):
        # Mock the Redis client and its set method
        redis_client_mock = MagicMock(spec=redis.Redis)

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        redis_repository.save_emoji("name", "image_data")

        # Assert that the Redis client's set method was called with the correct arguments
        redis_client_mock.set.assert_called_once_with("name", "image_data")

    def test_get_all_emojis(self, redis_repository):
        # Mock the Redis client and its scan_iter and get methods
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.scan_iter.return_value = [b"key1", b"key2"]
        redis_client_mock.get.side_effect = [b'value1', b'value2']

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        result = redis_repository.get_all_emojis()

        # Assert that the Redis client's scan_iter and get methods were called
        redis_client_mock.scan_iter.assert_called_once()
        redis_client_mock.get.assert_has_calls([mock.call(b'key1'), mock.call(b'key2')])

        # Assert that the returned result matches the expected value
        assert result == {'key1': 'value1', 'key2': 'value2'}

    def test_get_emoji_by_name_existing(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = b'{"name": "smiley", "image_data": "data"}'

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        result = redis_repository.get_emoji_by_name("smiley")

        # Assert that the Redis client's get method was called with the correct name
        redis_client_mock.get.assert_called_once_with("smiley")

        # Assert that the result matches the expected value
        assert result == '{"name": "smiley", "image_data": "data"}'

    def test_get_emoji_by_name_not_found(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = None

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        with pytest.raises(ValueError) as exc_info:
            redis_repository.get_emoji_by_name("smiley")

        # Assert that the Redis client's get method was called with the correct name
        redis_client_mock.get.assert_called_once_with("smiley")

        # Assert that a ValueError exception was raised
        assert str(exc_info.value) == "No value found by the name smiley"
