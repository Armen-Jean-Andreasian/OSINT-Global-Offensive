#!/bin/bash

# Constants ---
# shellcheck disable=SC2034
version="v1"
prefix="djangologger"
DJANGO_IMAGE_NAME="${prefix}-image-${version}"
DJANGO_CONTAINER_NAME="${prefix}-container-${version}"
EXISTING_CONTAINERS=$(docker ps -a --format "{{.Names}}")
EXISTING_IMAGES=$(docker images --format "{{.Repository}}")

# Generic functions ---
function delete_docker_image() {
  local image=$1 # arg
    echo "Removing image: ${image}"
    docker rmi -f "${image}"
}


# Implemented functions--
function delete_django_images_with_different_version() {
  for image in ${EXISTING_IMAGES}; do
    if [[ "${image}" == ${prefix}* && "${image}" != "${DJANGO_IMAGE_NAME}" ]]; then
      delete_docker_image image
    fi
  done
}


# Switches the directory from runners folder to root
function change_dir_to_root() {
  cd ..
}

# Installs Python dependencies locally
function install_pip_requirements() {
  local path_to_requirements_txt="${1:-config/requirements.txt}"
    pip install -r "${path_to_requirements_txt}"
}

# Installs or updates not-gitmodules based on a YAML configuration file.
function install_not_gitmodules() {
  local not_gitmodules_yaml_path="${1:-config/notgitmodules.yaml}" # default value
    not_gitmodules -y "${not_gitmodules_yaml_path}"
}

function retrieve_env_vars() {
  python project_secrets/entrypoint.py
}

# Runs docker compose
function docker_compose_up_detached() {
    docker compose --env-file config/.env.dump up -d
}

# Builds and runs docker compose. Only rebuilds changed layers
function docker_compose_up_build() {
    docker-compose --env-file config/.env.dump up --build
}

# Builds and runs docker compose. Rebuilds all layers
function docker_compose_up_no_cache() {
  docker-compose --env-file config/.env.dump up --build --no-cache
}

# Starts django from the project
function run_django_locally() {
  local django_internal_port="${1:-8080}"
    python manage.py runserver "${django_internal_port}"
}

# Starts django from container using the service name
function run_django_from_container() {
    docker exec -it django python manage.py runserver 0.0.0.0:8080
}

function stop_docker_compose() {
  docker compose --env-file ../config/.env.dump down
  # docker stop "${DJANGO_CONTAINER_NAME}"
}

