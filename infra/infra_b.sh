#!/bin/bash

#=======================================================================================================================
# About
#
# This is the reserve bash version.
# This script should be run from the project root.

# Usage
#
#| sh infra/infra_b.sh run
#| sh infra/infra_b.sh stop
#| sh infra/infra_b.sh test
#| sh infra/infra_b.sh reload


#== Load Configuration =================================================================================================

load_config() {
  if [[ -f "infra/infra.ini" ]]; then
    eval $(awk -F '=' '/^[^#]/ { gsub(/\r/,""); if ($1 ~ /^\[/) next; print $1 "=" $2 }' infra/infra.ini)
  else
    echo "Config file infra/infra.ini not found!"
    exit 1
  fi
}

load_config

#== Functions ==========================================================================================================

prepare_system() {
  python -c "from system import prepare_system; prepare_system(
    dot_env_path='system/config/.env',
    dot_vault_path='system/config/.vault_credentials',
    log_output_dir='system/logs'
  )"
  echo "Secrets are retrieved."
}

build() {
  prepare_system
  sleep 5
  echo "Building Docker images..."
  COMPOSE_PROJECT_NAME=$PROJECT_NAME docker compose --env-file $ENV_FILE -f $COMPOSE_YAML_FILE build --no-cache
}

up() {
  COMPOSE_PROJECT_NAME=$PROJECT_NAME docker compose --env-file $ENV_FILE -f $COMPOSE_YAML_FILE up --remove-orphans
}

down() {
  echo "Stopping and removing Docker containers..."
  COMPOSE_PROJECT_NAME=$PROJECT_NAME docker compose --env-file $ENV_FILE -f $COMPOSE_YAML_FILE down
}

run_tests() {
  echo "Running Django tests..."
  COMPOSE_PROJECT_NAME=$PROJECT_NAME docker compose exec $DJANGO_SERVICE_NAME python manage.py test
}


#== Interface ==========================================================================================================

run() {
  build
  up
}

reload() {
  down
  up
}

stop() {
  down
}

test() {
  run
  sleep 5
  run_tests
}


#== Main script logic ==================================================================================================

case "$1" in
  run) run ;;
  stop) stop ;;
  reload) reload ;;
  test) test ;;
  *) echo "Usage: $0 {run|stop|reload|test}" && exit 1 ;;
esac
