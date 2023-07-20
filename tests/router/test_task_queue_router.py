import unittest.mock as mock

import pytest
import requests
from fastapi.testclient import TestClient
from requests import Response

from api.main import app

client = TestClient(app)


class TestTaskQueueRouter:

    @pytest.mark.router
    @mock.patch('api.router.task_queue_router.AsyncResult')
    def test_get_task_status(self, mock_async_result):
        mock_async_result.return_value = mock.Mock(status='PENDING')
        response = client.get("/task-queue/status", params={"task_id": '123'})
        assert response.status_code == 200
        assert response.json() == {'id': '123', 'status': 'PENDING'}

    def mock_get_flower(self):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

            def raise_for_status(self):
                if self.status_code != 200:
                    raise ValueError

        response = MockResponse([{"id": "1", "status": "SUCCESS"}, {"id": "2", "status": "PENDING"}], 200)
        return response

    @pytest.mark.router
    @mock.patch.object(requests, 'get', new=mock_get_flower)
    def test_list_all_tasks(self):
        response = client.get("/task-queue/tasks")

        assert response.status_code == 200
        assert response.json() == [{"id": "1", "status": "SUCCESS"}, {"id": "2", "status": "PENDING"}]
