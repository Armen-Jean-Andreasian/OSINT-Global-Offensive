#!/bin/bash

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

# Implementations

# Docker compose build --no-cache
# Using separate functions, bc we need to define COMPOSE_PROJECT_NAME
function build() {
  prepare_system
  sleep 5
  echo "Building Docker images..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} build --no-cache
}

# Only starts the containers using the latest built images.
function up() {
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} up --remove-orphans
}

function down() {
  echo "Stopping and removing Docker containers..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} down
}

# Usage
#build
#up

down