import os
from unittest import mock
from unittest.mock import MagicMock

import pytest
import redis
from dotenv import load_dotenv

from custom_emoji_app.entities.emoji import Emoji
from custom_emoji_app.repositories.redis.repo import RedisRepository

load_dotenv()


class TestRedisRepository:
    @pytest.fixture
    def redis_repository(self):
        return RedisRepository()

    @pytest.fixture
    def dummy_keys(self):
        return [b"smiley", b"cry", b"hot", b"cold", b"running"]

    @pytest.fixture
    def dummy_values(self):
        return [b'value1', b'value2', b'value3', b'value4', b'value5']

    @pytest.mark.repositories
    def test_name_already_exists_existing_case(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = b'{"key": "value"}'

        redis_repository.client = redis_client_mock

        result = redis_repository.name_already_exists("hot")

        # Assert that the Redis client's get method was called with the correct key
        redis_client_mock.get.assert_called_once_with("hot")
        assert result is True

    @pytest.mark.repositories
    def test_name_already_exists_non_existing_case(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = None

        redis_repository.client = redis_client_mock

        result = redis_repository.name_already_exists("cold")

        # Assert that the Redis client's get method was called with the correct key
        redis_client_mock.get.assert_called_once_with("cold")
        assert result is False

    @pytest.mark.repositories
    def test_save_emoji(self, redis_repository):
        # Mock the Redis client and its set method
        redis_client_mock = MagicMock(spec=redis.Redis)

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        redis_repository.save_emoji("name", "image_data")

        # Assert that the Redis client's set method was called with the correct arguments
        redis_client_mock.set.assert_called_once_with("name", "image_data")

    @pytest.mark.repositories
    def test_get_all_emojis(self, redis_repository, dummy_keys, dummy_values):
        # Mock the Redis client and its scan_iter and get methods
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.scan_iter.return_value = dummy_keys
        redis_client_mock.get.side_effect = dummy_values

        redis_repository.client = redis_client_mock
        result = redis_repository.get_all_emojis()

        # Assert that the Redis client's scan_iter and get methods were called
        redis_client_mock.scan_iter.assert_called_once()
        redis_client_mock.get.assert_has_calls([mock.call(b'smiley'),
                                                mock.call(b'cry'),
                                                mock.call(b'hot'),
                                                mock.call(b'cold'),
                                                mock.call(b'running')])

        expected_result = list()
        for i in range(len(dummy_keys)):
            expected_result.append(Emoji(name=dummy_keys[i], image_data=dummy_values[i]))

        assert result == expected_result

    @pytest.mark.repositories
    def test_get_emoji_by_name_existing(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = b'data'

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested
        result = redis_repository.get_emoji_by_name("smiley")

        # Assert that the Redis client's get method was called with the correct name
        redis_client_mock.get.assert_called_once_with("smiley")

        # Assert that the result matches the expected value
        assert result == Emoji(name='smiley', image_data='data')

    @pytest.mark.repositories
    def test_get_emoji_by_name_not_found(self, redis_repository):
        # Mock the Redis client and its get method
        redis_client_mock = MagicMock(spec=redis.Redis)
        redis_client_mock.get.return_value = None

        # Set the Redis client mock as the client attribute of the repository
        redis_repository.client = redis_client_mock

        # Call the method being tested and assert that error is raised
        with pytest.raises(ValueError, match="No emoji found by the name smiley"):
            redis_repository.get_emoji_by_name("smiley")

        # Assert that the Redis client's get method was called with the correct name
        redis_client_mock.get.assert_called_once_with("smiley")
