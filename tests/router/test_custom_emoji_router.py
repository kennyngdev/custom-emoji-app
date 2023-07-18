import base64
from fastapi import UploadFile, HTTPException
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import pytest
from unittest.mock import patch, Mock

from api.main import app
from custom_emoji_app.repositories.redis import repo as redis_repo
from custom_emoji_app.use_cases.get_emojis import use_case as emoji_use_case
from worker.tasks import upload_emoji


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_image_content():
    with open("test.png", "rb") as image_file:  # add a test image in your directory
        return base64.b64encode(image_file.read()).decode()


class MockRedisRepository:
    def __init__(self):
        self.emoji_names = []

    def name_already_exists(self, name):
        return name in self.emoji_names


class MockGetEmojis:
    def __init__(self, repository):
        self.repository = repository

    def get_all_emojis(self):
        return ["happy", "sad"]

    def get_emoji_by_name(self, input_dto):
        if input_dto.name not in self.repository.emoji_names:
            raise HTTPException(status_code=404, detail="Emoji not found")
        return {"name": input_dto.name, "image_data": "base64-encoded-string"}


@patch.object(redis_repo, 'RedisRepository', new=MockRedisRepository)
@patch.object(emoji_use_case, 'GetEmojis', new=MockGetEmojis)
def test_get_all_emojis(client):
    response = client.get("/custom-emoji/emojis")
    assert response.status_code == HTTP_200_OK
    assert response.json() == ["happy", "sad"]


@patch.object(redis_repo, 'RedisRepository', new=MockRedisRepository)
@patch.object(emoji_use_case, 'GetEmojis', new=MockGetEmojis)
def test_get_emoji_by_name(client):
    response = client.get("/custom-emoji/emojis/happy")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"name": "happy", "image_data": "base64-encoded-string"}


@patch.object(redis_repo, 'RedisRepository', new=MockRedisRepository)
@patch.object(emoji_use_case, 'GetEmojis', new=MockGetEmojis)
def test_create_emoji(client, test_image_content):
    response = client.post("/custom-emoji/emojis",
                           data={"name": "excited",
                                 "file": UploadFile("test.png", content=test_image_content)})
    assert response.status_code == HTTP_200_OK
    assert 'task_id' in response.json()
