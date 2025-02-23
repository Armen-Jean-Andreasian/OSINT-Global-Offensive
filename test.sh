#!/bin/bash

# Usage: docker_compose <project_name> <compose_file> <additional_args>
# Example: docker_compose x_project "up -d --build --no-cache"
# Arguments:
#   project_name: The name of the project. This will be used as the prefix for the containers.
#   compose_file: The path to the Docker Compose file.
#   additional_args: Additional arguments to pass to the `docker compose` command. (e.g., "up -d --build")

docker_compose() {
    local project_name="$1"
    local compose_file="${2:-docker-compose.yml}"
    shift 2 # Shift removes the first N arguments, keeping additional ones in $@
    local additional_args="$@"


    # Check if the compose file exists -> Error if not
    if [[ ! -f "$compose_file" ]]; then
        echo "Error: Docker Compose file '$compose_file' not found."
        return 1
    fi
    echo "Starting Docker Compose with project: $project_name"


    # Check if --no-cache is in additional_args
    if [[ "$additional_args" == *"--no-cache"* ]]; then
        COMPOSE_PROJECT_NAME="$project_name" docker compose -f "$compose_file" build --no-cache
        COMPOSE_PROJECT_NAME="$project_name" docker compose -f "$compose_file" up -d
    else
        COMPOSE_PROJECT_NAME="$project_name" docker compose -f "$compose_file" $additional_args
    fi
}
