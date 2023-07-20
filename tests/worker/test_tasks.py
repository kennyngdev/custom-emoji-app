import pytest
from unittest.mock import patch, Mock
from celery import states
from custom_emoji_app.repositories.redis.repo import RedisRepository
from custom_emoji_app.use_cases.create_emoji.input_dto import CreateEmojiInputDto
from custom_emoji_app.use_cases.create_emoji.use_case import CreateEmoji
from worker.tasks import upload_emoji


class TestTasks:
    @pytest.mark.tasks
    @patch.object(RedisRepository, "__init__", return_value=None)  # Mock RedisRepository init to do nothing
    @patch.object(CreateEmoji, "__call__")  # Mock CreateEmoji's __call__ method
    def test_upload_emoji_success(self, mock_create_emoji, mock_redis_repo):
        name, image_data = 'emoji_name', 'image_data'
        expected_emoji = CreateEmojiInputDto(name=name, image_data=image_data)
        mock_create_emoji.return_value = 'success'

        # Act
        result = upload_emoji(name, image_data)

        # Assert
        mock_create_emoji.assert_called_once_with(expected_emoji)
        assert result == 'success'