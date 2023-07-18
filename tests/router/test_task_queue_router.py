import pytest
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch, Mock


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_task():
    return Mock(id='1', status='PENDING', state='PENDING', get=Mock(return_value='mocked result'))


def test_get_task_status(mock_task, client):
    with patch('celery.result.AsyncResult', return_value=mock_task):
        response = client.get('/task-queue/status?task_id=1')
        assert response.status_code == 200
        assert response.json() == {'id': '1', 'status': 'PENDING', 'state': 'PENDING'}


def test_get_result(mock_task, client):
    with patch('celery.result.AsyncResult', return_value=mock_task):
        response = client.get('/task-queue/result?task_id=1')
        assert response.status_code == 200
        assert response.json() == {'id': '1', 'task_result': 'mocked result'}


def test_list_all_tasks(client):
    mock_response = Mock()
    mock_response.json.return_value = {'tasks': []}
    with patch('requests.get', return_value=mock_response):
        response = client.get('/task-queue/tasks')
        assert response.status_code == 200
        assert response.json() == {'tasks': []}


def test_run_task(mock_task, client):
    mock_example_task = Mock(delay=Mock(return_value=mock_task))
    with patch('worker.tasks.example_task', new=mock_example_task):
        response = client.post('/task-queue/example_task', json={'message': 'test'})
        assert response.status_code == 200
        assert response.json() == {'task_id': '1'}
