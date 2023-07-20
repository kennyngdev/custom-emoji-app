from unittest.mock import Mock, patch

import pytest

from custom_emoji_app.entities.emoji import Emoji
from custom_emoji_app.use_cases.create_emoji.Irepo import ICreateEmojiRepository
from custom_emoji_app.use_cases.create_emoji.input_dto import CreateEmojiInputDto
from custom_emoji_app.use_cases.create_emoji.use_case import CreateEmoji


class TestCreateEmoji:
    @pytest.mark.use_cases
    def test_call(self):
        # Mock the repository
        mock_repository = Mock(spec=ICreateEmojiRepository)

        # Create an instance of CreateEmoji with the mock repository
        create_emoji = CreateEmoji(repository=mock_repository)
        # Example input data for testing
        image_data = 'abc'
        input_dto = CreateEmojiInputDto(name='smiley', image_data=image_data)

        def mock_transform(self):
            self.image_data = 'transformed_image_data'

        # Patch the necessary methods
        with patch.object(Emoji,
                          'transform_to_thumbnail_gif',
                          new=mock_transform):
            # Call the method being tested
            result = create_emoji(input_dto)
            # Assert that the repository's save_emoji method was called with the expected arguments
            mock_repository.save_emoji.assert_called_once_with(name='smiley', image_data='transformed_image_data')

        # Assert that the result is 'success'
        assert result == 'success'
