#!/bin/bash

### Usage
# sh infra.sh up
# sh infra.sh down


# Constants
PROJECT_NAME="logger_proj"
ENV_FILE="system/config/.env"
COMPOSE_YAML_FILE="docker-compose.yml"

# Fetches remote secrets from HashiCorp and saves to .env file
function prepare_system() {
  python -c "
from system import prepare_system

prepare_system(
    dot_env_path='system/config/.env',
    dot_vault_path='system/config/.vault_credentials',
    log_output_dir='system/logs'
)
"
  echo "Secrets are retrieved to .env"
}

# Docker compose build --no-cache
function build() {
  prepare_system
  sleep 5
  echo "Building Docker images..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} build --no-cache
}

# Starts the containers using the latest built images. Rebuilds only the outdated/modified ones and removes orphaned containers.
function up() {
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} up --remove-orphans
}

# Stops and removes all running containers, networks, and volumes associated with the infrastructure.
function down() {
  echo "Stopping and removing Docker containers..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} down
}

# Run the infrastructure (build + up)
function run() {
  build
  up
}

# Stop the infrastructure
function stop() {
  down
}

# Main script logic
if [[ "$1" == "run" ]]; then
  run
elif [[ "$1" == "stop" ]]; then
  stop
else
  echo "Usage: $0 {run|stop}"
  exit 1
fi