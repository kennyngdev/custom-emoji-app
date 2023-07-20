# Custom Emoji App

Welcome. This is an API application which allows users to create custom emojis for communication apps by creating small thumbnail images. Leveraging a long-running task queue, this application handles the functionalities of accepting image files, creating thumbnails, and making them retrievable once the processing is complete.

## Technology Stack
- **Language:** Python
- **Frameworks:** FastAPI, Celery
- **Database:** Redis
- **Message Queue:** RabbitMQ
- **Software Tools:** Kompose, Kind
- **Testing Libraries:** pytest, unittest

## Discussion
### Tech Stack
I chose Python as the development language because:
- Python is a popular server-side language which is easy to use and easy to read.
- In an AI company, there are many data scientists, and they usually know python well. This makes easier knowledge sharing between groups and make cooperation possible.
- it has a vibrant ecosystem of third-party packages for data processing(numpy, panda, etc.) and server-side operations (like FastAPI and celery used here)

FastAPI is used because it is one of the most performant API frameworks across languages due to its asynchronous nature. It also supports automatic API documentation with Swagger UI, which allows efficient developing.

Celery is used because it is a robust and reliable task queue distributed system to process messages and tasks. 
Its asynchronous job queue provides good support and efficient management system (along with flower) for long-running tasks, which is one of the keys of this application.

RabbitMQ is used as the message broker because it is one of the most battle-tested broker, and it is flexible to configure also.

Redis is used as the result backend because it is a performant database which allows timely and robust tracking of task status. It is also the most commonly used result backend for celery. (RPC backend has an issue in reporting correct task status and it is still unsolved in celery now : https://github.com/celery/celery/issues/4084)

Redis is also used as the database for storing emojis. This allows fast retrieval and storing of emojis due to Redis being an in-memory database.
While Redis's storage can be more expensive than other databases as it uses memory as the storage; as this application only stores 100x100 sized images, it should not be a big concern. 

This application's specification does not require specific filtering of emojis(like user-specific or channel-specific ones), 
Redis being a key-value store is sufficient to store the images as there are not much metadata needed to be stored together.
But if such feature needs to be added in the future, a SQL database can be considered to better manage the ownership or usage management of emojis. Luckily,
with clean architecture, such change is not difficult to make.

### Architecture
I adopted Clean Architecture, a famous and widely adopted hexagonal architecture created by Robert Martin(aka Uncle Bob).
This architecture allows loosely coupling of application components, and separation of business logic from frameworks, UI, DB or other external agencies.
In this app, all business logics reside in the domain layer (entities and use cases); and through the use of interfaces, 
such logics do not depend on celery, fastAPI nor Redis (the stack used in this app).　Instead, through dependency inversion, external frameworks depend on business logic. (For example, RedisRepository depends on the Emoji entity)
For example, if one wants to use PostgresSQL to store the emojis, they just need to implement the methods according to the interface,
and through some minor adjustments in the controller, it can fit right into the application. This allows an easy change of tech stack and the application can utilize different technologies as needed.

Separating coding components into different layers also allow easier testing (and test writing) of the application. 
Unit test can be written as ease as business logic is separated from repository implementation(like redis access code), 
and mocks and stubs can be easily created to emulate external components' behavior. 

### Tests
I used pytest and unittest to write unit tests for the application. I covered the different components I implemented: 
entities, use cases, repositories, router and worker.

### Tradeoffs
With a normal daytime job and other duties, it is difficult to dedicate time to strike a balance between developing time and test coverage.
If I had more time, I could have written more tests to cover edge cases. However, In my opinion I did cover enough base cases for the application, at least as a PoC. 

Also having an integration test module to actually test out the connectivity of celery, redis, rabbitMQ and fastAPI would be nice,
but that would require a significant amount of time to do so, in which I couldn't with the time limit.

A different database like MySQL could be used, in a use case that we needed to control the usage/availability of emojis. 
However, I think for this application's specification, it might be an overkill, and it would take extra time to develop.
So I stick with Redis since it is more time sufficient, and it also fits well with the required use case.

### Potential Future Features/Changes
**Features**:
- User can change the name of a certain emoji
- User can delete emoji
- User can change the content(image) of an emoji
- For other long-running tasks, an email/Slack notification can be sent once task is finished

**Infrastructure**:
- Redis can be run as a cluster for scalability, if we have many emojis to store. (the cluster needs to be separated from the result backend though, because celery could not use a redis cluster to store results)
- FastAPI can be run using gunicorn instead of unicorn to handle greater load and to utilize multicore CPUs.
- Cloud message services like Amazon MQ might be utilized for its ease of management.
- If there are other demanding jobs in the future, extra celery workers can also be added.

**Tests**:
- More unit tests to cover edge cases
- Integration test module to test out the connectivity with external frameworks

## Installation and Setup
You can set up and run this application using Kubernetes with Helm or Docker Compose. Follow the instructions below based on your choice.

### Kubernetes with Helm Setup
1. **Build Docker images:** For both Celery and the API, use the commands below to build Docker images:
    ```shell
    docker build . -f worker.Dockerfile -t worker:1.0.0
    docker build . -f api.Dockerfile -t api:1.0.0
    ```
2. **Convert Docker compose file to Helm charts(if docker-compose directory doesn't exist yet):** Use Kompose to convert the docker-compose file and generate Helm charts:
    ```shell
    kompose convert -f docker-compose.yml -c
    ```
3. **Create a Kubernetes cluster:** Run `kind create cluster` to create a local Kubernetes cluster.
4. **Load Docker images into the cluster:** Load locally built Docker images into the cluster:
    ```shell
    kind load docker-image worker:1.0.0
    kind load docker-image api:1.0.0
    ```
5. **Install the app onto the cluster:** Run `helm install custom-emoji-app ./docker-compose` to install the application onto the cluster.
6. **Verify the application deployment:** Run `kubectl get all` to check if the application is correctly deployed.
7. **Delete the cluster:** After you're done, run `kind delete cluster` to delete the cluster.


### Docker Setup
1. **Build Docker images:** For both Celery and the API, use the commands below to build Docker images:
    ```shell
    docker build . -f worker.Dockerfile -t worker:1.0.0
    docker build . -f api.Dockerfile -t api:1.0.0
    ```
2. **Host containers:** To launch the Celery, FastAPI, RabbitMQ, and Redis containers together, use the command below:
    ```shell
    docker-compose up -d --build
    ```
3. **Access the application:** After initializing the Docker containers, access the Swagger UI at `http://localhost:8000/docs` or interact with the API directly.

## Usage
### Port Forwarding (for kubernetes with helm only)
If you have built and deployed the application with kubernetes, you need to first forward the ports used in order to access the application. 
```shell
# For API
kubectl port-forward service/custom-emoji-api 8000:8000
# For flower(Task Queue Monitoring Dashboard)
kubectl port-forward service/task-queue-dashboard 5555:5555
```
### API
You can access the API directly from `localhost:8000`, 
or visit the Swagger UI from `localhost:8000/docs` for documentation and testing.
While the full documentation is accessible from the Swagger UI, here is a brief introduction to the endpoints.
- `GET /custom-emoji/emojis` : This retrieves a list of all emojis, including their name and image data, which is encoded as base64 strings.
- `GET /custom-emoji/{name}`: This retrieves an emoji with a certain name in the form of an GIF image.
- `POST /custom-emoji/emojis`: This allows users to upload an image and to create an emoji, which will be processed into a 100x100 sized thumbnail GIF, which is then saved into the database; The processing is done by a task queue and a task ID would be provided to the user to track the status of the processing task.
- `GET /task-queue/status`: This allows users to track the status of a task. (Possible outcomes: `PENDING`, `STARTED`, `RETRY`, `FAILURE`)
- `GET /task-queue/tasks`: This retrieves a list of past and current tasks and their respective details.

### Task Queue
You can visit the flower dashboard from `localhost:5555`, 
which acts as a monitoring tool for task worker and task statuses.

### Debugging
If you have built and deployed the application with kubernetes, you can use the following command to export logs.
```shell
kind export logs
```
Then, you can visit the directory outputted to see the logs of the services.
If you deployed the application with Docker Compose, you can just see the logs directly through Docker Desktop.