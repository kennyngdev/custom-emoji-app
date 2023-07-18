import requests

from celery.result import AsyncResult
from fastapi import APIRouter
from pydantic import BaseModel
from worker.tasks import example_task

task_queue_router = APIRouter(
    prefix='/task-queue',
    tags=['task_queue']
)

FLOWER_API_URL = "http://task-queue-dashboard:5555/api/tasks"


@task_queue_router.get("/status")
def get_task_status(task_id):
    task_result = AsyncResult(id=task_id)
    res = {
        "id": task_id,
        "status": task_result.status,
        "state": task_result.state
    }
    return res


@task_queue_router.get("/result")
def get_result(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "id": task_id,
        "task_result": task_result.get()
    }
    return result


@task_queue_router.get("/tasks")
def list_all_tasks():
    response = requests.get(FLOWER_API_URL)
    response.raise_for_status()
    return response.json()


class ExampleInputModel(BaseModel):
    message: str = ''


@task_queue_router.post("/example_task")
def run_task(input_dto: ExampleInputModel):
    json_body = input_dto.model_dump()
    result = example_task.delay(json_body)
    return {'task_id': result.id}
