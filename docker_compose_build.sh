#!/bin/bash

# Detect the host OS
HOST_OS="$(uname -s)"

# Set the default Docker Compose file (Linux with GPU) 
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Check if the host OS is macOS and set the Compose file accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
  DOCKER_COMPOSE_FILE="docker-compose-macos.yml"
fi

# Run Docker Compose with the selected configuration file
docker-compose -f "$DOCKER_COMPOSE_FILE" build