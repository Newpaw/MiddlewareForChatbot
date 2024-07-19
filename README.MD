# MiddlewareForChatbot

## Overview
MiddlewareForChatbot is a FastAPI-based application designed to process webhooks and integrate with external services like a FastAPI Assistant and Mluvii chatbot. The application leverages asynchronous programming to handle requests efficiently and uses Redis for session management.

## Features
- Asynchronous webhook handling
- Integration with external FastAPI Assistant service
- Integration with Mluvii chatbot
- Redis for session management
- Logging with Loguru
- Health check endpoint

## Requirements
- Python 3.10+
- Redis
- Docker (for containerization)

## Setup

### Environment Variables
Create a `.env` file in the root directory with the following variables:

```sh
PROJECT_NAME=MiddlewareForChatbot
PROJECT_VERSION=1.0.1
LOG_LEVEL=DEBUG
BASE_URL_ASSISTENT=<base_url_assistent>
CHATBOT_ID=<chatbot_id>
BASE_URL_MLUVII=<base_url_mluvii>
CLIENT_ID=<client_id>
CLIENT_SECRET=<client_secret>
REDIS_HOST=<redis_host>
REDIS_PORT=<redis_port>
REDIS_DB=<redis_db>
```

### Installation

1. **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd MiddlewareForChatbot
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    uvicorn main:app --reload --port 8080
    ```

### Docker

1. **Build the Docker image:**
    ```sh
    docker build -t middlewareforchatbot .
    ```

2. **Run the Docker container:**
    ```sh
    docker run --env-file .env -p 8080:8080 middlewareforchatbot
    ```

## Usage

### Health Check
To check if the API is running, access the health check endpoint:

```sh
GET /healthcheck
```


### Webhooks
The application listens for POST requests at the root endpoint `/`. To send a webhook request, use the following structure:
```json
{
    "activity": "Text",
    "timestamp": "<timestamp>",
    "text": "<message>",
    "sessionId": "<session_id>",
    "language": "<language>",
    "source": "<source>"
}
```

#### Example Request

```sh
curl -X POST "http://localhost:8080/" -H "Content-Type: application/json" -d '{
    "activity": "Text",
    "timestamp": "2024-07-19T12:34:56Z",
    "text": "Hello, how can I help you?",
    "sessionId": 12345,
    "language": "en",
    "source": "test"
}'
```

### Logging
Logs are stored in the async_app.log file and also output to stdout, making them accessible via Docker logs.

To view Docker logs:
```sh
docker logs <container_id>
```

### Contributing
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.

### License

This project is licensed under the MIT License - see the LICENSE file for details.


### Explanation:
- **Overview**: Provides a brief introduction to the application.
- **Features**: Highlights key features of the application.
- **Requirements**: Lists the requirements to run the application.
- **Setup**: Provides steps to set up the application locally.
- **Docker**: Provides steps to build and run the application using Docker.
- **Usage**: Explains how to use the application, including endpoints and example requests.
- **Logging**: Explains how to access logs.
- **Contributing**: Provides instructions for contributing to the project.
- **License**: Specifies the licensing information. 

This `README.md` should give users a clear understanding of how to set up, run, and contribute to the application.
