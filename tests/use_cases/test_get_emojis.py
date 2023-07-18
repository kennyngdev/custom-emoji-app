from unittest.mock import Mock

from custom_emoji_app.use_cases.get_emojis.Irepo import IGetEmojisRepository
from custom_emoji_app.use_cases.get_emojis.input_dto import GetEmojiByNameInputDto
from custom_emoji_app.use_cases.get_emojis.use_case import GetEmojis


class TestGetEmojis:
    def test_get_all_emojis(self):
        # Mock the repository
        mock_repository = Mock(spec=IGetEmojisRepository)

        # Create an instance of GetEmojis with the mock repository
        get_emojis = GetEmojis(repository=mock_repository)

        # Mock the get_all_emojis method of the repository
        mock_repository.get_all_emojis.return_value = ['emoji1', 'emoji2', 'emoji3']

        # Call the method being tested
        result = get_emojis.get_all_emojis()

        # Assert that the repository's get_all_emojis method was called
        mock_repository.get_all_emojis.assert_called_once()

        # Assert that the result matches the expected value
        assert result == ['emoji1', 'emoji2', 'emoji3']

    def test_get_emoji_by_name(self):
        # Mock the repository
        mock_repository = Mock(spec=IGetEmojisRepository)

        # Create an instance of GetEmojis with the mock repository
        get_emojis = GetEmojis(repository=mock_repository)

        # Example input data for testing
        input_dto = GetEmojiByNameInputDto(name='smiley')

        # Mock the get_emoji_by_name method of the repository
        mock_repository.get_emoji_by_name.return_value = {'name': 'smiley', 'image_data': 'base64_encoded_data'}

        # Call the method being tested
        result = get_emojis.get_emoji_by_name(input_dto)

        # Assert that the repository's get_emoji_by_name method was called with the expected arguments
        mock_repository.get_emoji_by_name.assert_called_once_with('smiley')

        # Assert that the result matches the expected value
        assert result == {'name': 'smiley', 'image_data': 'base64_encoded_data'}