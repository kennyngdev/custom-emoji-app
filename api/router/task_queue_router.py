import requests

from celery.result import AsyncResult
from fastapi import APIRouter

task_queue_router = APIRouter(
    prefix='/task-queue',
    tags=['task_queue']
)

FLOWER_API_URL = "http://task-queue-dashboard:5555/api/tasks"


@task_queue_router.get("/status")
def get_task_status(task_id: str):
    """
    ## Get Task Status by ID

    ### Parameters

    - **task_id** (query parameter): ID of the task.

    ### Response

    - **200 OK** - A dictionary with the task ID and status (`PENDING`, `STARTED`, `RETRY`, `FAILURE`, `SUCCESS`).
    """
    task_result = AsyncResult(id=task_id)
    res = {
        "id": task_id,
        "status": task_result.status
    }
    return res


@task_queue_router.get("/tasks")
def list_all_tasks():
    """
    ## List All Tasks

    ### Description
    List all tasks in the task queue.

    ### Response
    - **200 OK** - A list of all tasks and their statuses in the queue.
    """

    response = requests.get(FLOWER_API_URL)
    response.raise_for_status()
    return response.json()
