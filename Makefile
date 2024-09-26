# Variables
PYTHON = python3
FLASK = flask
PYTEST = pytest
DOCKER_COMPOSE = docker-compose
SERVICE_NAME = api 

# Default target
all: build up

# Build the Docker image
build:
	$(DOCKER_COMPOSE) build

# Rebuild the Docker image without using cache
rebuild:
	$(DOCKER_COMPOSE) build --no-cache

# Start the application
up:
	$(DOCKER_COMPOSE) up
	docker ps

# Stop the application
down:
	$(DOCKER_COMPOSE) down

# Run the Flask application (if needed to override the default command)
run:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python run.py

# Run all tests
test:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) pytest tests/

# Run tests with verbose output
test-verbose:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) pytest -v tests/

# Clean up cache files
clean:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) find . -type d -name "__pycache__" -exec rm -rf {} +
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) find . -type f -name "*.pyc" -delete

# Install dependencies (if needed)
install:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) pip install -r requirements.txt

# View logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Restart the service
restart:
	$(DOCKER_COMPOSE) restart

# Help command to display available targets
help:
	@echo "Available targets:"
	@echo "  build          : Build the Docker image"
	@echo "  rebuild        : Rebuild the Docker image without using cache"
	@echo "  up             : Start the application"
	@echo "  down           : Stop the application"
	@echo "  run            : Run the Flask application (if needed)"
	@echo "  test           : Run all tests"
	@echo "  test-verbose   : Run all tests with verbose output"
	@echo "  clean          : Remove Python cache files"
	@echo "  install        : Install project dependencies"
	@echo "  logs           : View container logs"
	@echo "  restart        : Restart the service"
	@echo "  help           : Display this help message"

.PHONY: all build rebuild up down run test test-verbose clean install logs restart help
