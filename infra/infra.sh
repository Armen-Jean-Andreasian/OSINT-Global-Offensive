#!/bin/bash

#=======================================================================================================================

# About
#
# This is the shell version.
# This script should be run from the project root.

# Usage
#
#| sh infra/infra.sh run
#| sh infra/infra.sh run debug
#| sh infra/infra.sh stop
#| sh infra/infra.sh test
#| sh infra/infra.sh test debug
#| sh infra/infra.sh reload
#| sh infra/infra.sh stop test

#== Constants ==========================================================================================================

# Loads vars from infra.ini.
load_config() {
  if [[ -f "infra/infra.ini" ]]; then
    echo "Loading config from infra/infra.ini..."
    eval $(awk -F '=' '/^[^#]/ { gsub(/\r/,""); if ($1 ~ /^\[/) next; print $1 "=" $2 }' infra/infra.ini)
  else
    echo "Config file infra/infra.ini not found!"
    exit 1
  fi
}

#== Functions ==========================================================================================================

# Fetches remote secrets from HashiCorp and saves to .env file
function prepare_system() {
  echo "Retrieving .env files"
  python -c "
from system import prepare_system

prepare_system(
    dot_env_path='system/config/.env',
    dot_vault_path='system/config/.vault_credentials',
    log_output_dir='system/logs'
)
"
}

# Docker compose build --no-cache
#
# Params: env_file, compose_yaml_file, project_name (optional) | If not given will be used constants from infra.ini
function build() {
  local env_file=${1:-$ENV_FILE}
  local compose_yaml_file=${2:-$COMPOSE_YAML_FILE}
  local project_name=${3:-$PROJECT_NAME}
  local debug_flag=${4:-false}

  prepare_system
  sleep 5
  echo "Building Docker images..."
  COMPOSE_PROJECT_NAME=${project_name} docker compose \
      --env-file ${env_file} -f ${compose_yaml_file} build --no-cache \
      --build-arg DOCKER_DEBUG=${debug_flag}
}

# Starts the containers using the latest built images.
# Rebuilds only the outdated/modified containers and removes orphaned ones.
#
# Params: env_file, compose_yaml_file, project_name (optional) | If not given will be used constants from infra.ini
function up() {
  local env_file=${1:-$ENV_FILE}
  local compose_yaml_file=${2:-$COMPOSE_YAML_FILE}
  local project_name=${3:-$PROJECT_NAME}

  COMPOSE_PROJECT_NAME=${project_name} docker compose --env-file ${env_file} -f ${compose_yaml_file} up --remove-orphans
}

# Stops and removes all running containers, networks, and volumes associated with the infrastructure.
#
# Params: env_file, compose_yaml_file, project_name (optional) | If not given will be used constants from infra.ini
function down() {
  local env_file=${1:-$ENV_FILE}
  local compose_yaml_file=${2:-$COMPOSE_YAML_FILE}
  local project_name=${3:-$PROJECT_NAME}

  echo "Stopping and removing Docker containers..."
  COMPOSE_PROJECT_NAME=${project_name} docker compose --env-file ${env_file} -f ${compose_yaml_file} down
}

#== Interface ==========================================================================================================

# Run the infrastructure (build + up)
function run() {
  local debug=${1:-false}

  load_config
  build "" "" "" $debug
  up
}

# Stop the infrastructure
function stop() {
  load_config
  down
}

# Stops testing infrastructure
function stop_test() {
  load_config
  down "${ENV_FILE_TEST}" "${COMPOSE_YAML_FILE_TEST}" "${PROJECT_NAME_TEST}"
}

# Restarts the infrastructure
function reload() {
  load_config
  down
  up
}

# Runs the infrastructure in test mode
function test() {
  local debug=${1:-false}

  load_config
  build "${ENV_FILE}" "${COMPOSE_YAML_FILE_TEST}" "${PROJECT_NAME_TEST}" $debug
  up "${ENV_FILE}" "${COMPOSE_YAML_FILE_TEST}" "${PROJECT_NAME_TEST}"
}

#== Main script logic ==================================================================================================

if [[ "$1" == "run" && "$2" == "debug" ]]; then
  run true
elif [[ "$1" == "run" ]]; then
  run
elif [[ "$1" == "stop" && "$2" == "test" ]]; then
  stop_test
elif [[ "$1" == "stop" ]]; then
  stop
elif [[ "$1" == "test" && "$2" == "debug" ]]; then
  test true
elif [[ "$1" == "test" ]]; then
  test
elif [[ "$1" == "reload" ]]; then
  reload
else
  echo "Usage: $0 {run|stop|test|reload|stop test|run debug|test debug}"
  exit 1
fi
