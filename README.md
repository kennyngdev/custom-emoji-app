# Cogent Labs Assignment

## Tech Stack
Language: Python
Framework: FastAPI, Celery
Database: Redis
Software Tool: RabbitMQ, Kompose

## Usage
Swagger URL: http://localhost:8000/docs

## TODO LIST
1. make some endpoints to check redis usability DONE
2. make upload image endpoint that:
   - allows uploading image
   - transform image to 100*100 thumbnails through celery worker
   - allow task status to be checked through Job ID ("processing", "succeeded", "failed")
   - task should save thumbnail into DB
3. make endpoint to fetch thumbnail from DB (by key and fetch all)
4. make endpoint to list all tasks
5. write tests

## Introduction
This is an API application that allows user to create custom emojis for communication apps, which allows them to create small thumbnail images.
Utilizing a log-running task queue, it can fulfill the functionalities of accepting image files, 
creating thumbnails and allowing them to be fetched when done processing.


## Spec
1. A user should be able to submit an image to an API endpoint. The API should save the image somewhere and initiate a long-running
job to generate a thumbnail of the image with a fixed size of 100x100. The user should receive a job ID that they can use to check the
status of the job later.
2. A user should be able to check the status of a job by submitting its ID to the API. The API should return the current status of the job (e.g.
"processing", "succeeded", "failed").
3. A user should be able to fetch the thumbnail image via API once the Job has succeeded processing.
4. A user should be able to list all the submitted jobs via API in case they forgot one of their Job ID.

* You do NOT need to support multiple user accounts or authorization. Instead, you can assume that anyone with access to the API is allowed
to perform any API operation (viewing processed thumbnails, etc.).
* MUST be packaged into Docker Containers
* MUST be packaged via Helm so they can be deployed into a kubernetes cluster
* MUST provide basic unit/integration tests that are easily runnable
* No UI Needed

## Setup and Installation
### Using Docker 
1. To host the project, start by building the Docker images for Celery and the API, using the commands below:

    ```
    # Build the Celery and the api image
    docker build . -f worker.Dockerfile -t worker
    docker build . -f api.Dockerfile -t api 
    ```

2. Next, to spin up the Celery, FastAPI, RabbitMQ, and Redis containers together, use the following command:

    ```
    # Host the containers
    docker-compose up -d --build
    ```
   
3. After initializing the Docker containers, access the Swagger UI at http://localhost:8000/docs or interact with the API directly.

## How to Use
This API offers three main endpoints:

- `POST run_task`: Triggers a task that takes approximately 10 seconds to complete. Upon initiating this task, a unique task ID is generated for tracking progress and retrieving results.

- `GET status`: Allows users to track the status of a specific task using its ID.

- `GET result`: Retrieves the result of a completed task using its ID.

