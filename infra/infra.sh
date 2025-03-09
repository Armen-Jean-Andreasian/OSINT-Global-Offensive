#!/bin/bash

#=======================================================================================================================

# About
#
# This is the shell version.
# This script should be run from the project root.

# Usage
#
#| sh infra/infra.sh up
#| sh infra/infra.sh down
#| sh infra/infra.sh test
#| sh infra/infra.sh reload


#== Constants ==========================================================================================================


# Loads vars from infra.ini.
load_config() {
  if [[ -f "infra/infra.ini" ]]; then
    eval $(awk -F '=' '/^[^#]/ { gsub(/\r/,""); if ($1 ~ /^\[/) next; print $1 "=" $2 }' infra/infra.ini)
  else
    echo "Config file infra/infra.ini not found!"
    exit 1
  fi
}

#== Functions ==========================================================================================================

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
  echo "Secrets are retrieved."
}

# Docker compose build --no-cache
function build() {
  prepare_system
  sleep 5
  echo "Building Docker images..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} build --no-cache
}

# Starts the containers using the latest built images.
# Rebuilds only the outdated/modified containers and removes orphaned ones.
function up() {
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} up --remove-orphans
}

# Stops and removes all running containers, networks, and volumes associated with the infrastructure.
function down() {
  echo "Stopping and removing Docker containers..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose --env-file ${ENV_FILE} -f ${COMPOSE_YAML_FILE} down
}

# Run Django tests inside the container
function run_tests() {
  echo "Running Django tests..."
  COMPOSE_PROJECT_NAME=${PROJECT_NAME} docker compose exec ${DJANGO_SERVICE_NAME} python manage.py test
}


#== Interface ==========================================================================================================

# Run the infrastructure (build + up)
function run() {
  load_config
  build
  up
}

# Stop the infrastructure
function stop() {
  load_config
  down
}

# Restarts the infrastructure
function reload() {
  down
  load_config
  up
}


# Runs the infrastructure, runs tests
function test() {
  load_config
  build
  up
  sleep 5
  run_tests
}


#== Main script logic ==================================================================================================

if [[ "$1" == "run" ]]; then
  run
elif [[ "$1" == "stop" ]]; then
  stop
elif [[ "$1" == "test" ]]; then
  test
elif [[ "$1" == "reload" ]]; then
  reload
else
  echo "Usage: $0 {run|stop|test|reload}"
  exit 1
fi
