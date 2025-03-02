#!/bin/bash

# Usage: docker_compose -p <project_name> -f <compose_file> [-e <env_file>] [additional_args]
#
# Example with env_file: docker_compose -p my_project -f docker-compose.yml -e .env up -d --build
# Example without env_file: docker_compose -p my_project -f docker-compose.yml up -d --build
docker_compose() {
    local project_name compose_file env_file additional_args

    # Parse flags
    while getopts ":p:f:e:" opt; do
        case $opt in
            p) project_name="$OPTARG" ;;
            f) compose_file="$OPTARG" ;;
            e) env_file="$OPTARG" ;;
            *) echo "Invalid option: -$OPTARG" >&2; return 1 ;;
        esac
    done
    shift $((OPTIND - 1)) # Shift to remove parsed options, leaving additional_args in $@
    additional_args="$@"

    # Default compose file if not provided
    compose_file="${compose_file:-docker-compose.yml}"

    # Check if the compose file exists -> Error if not
    if [[ ! -f "$compose_file" ]]; then
        echo "Error: Docker Compose file '$compose_file' not found."
        return 1
    fi
    echo "Starting Docker Compose with project: $project_name"

    # Check if env_file is provided and exists
    if [[ -n "$env_file" && ! -f "$env_file" ]]; then
        echo "Warning: Environment file '$env_file' not found. Proceeding without it."
        env_file=""
    fi

    # Build the base command
    local base_cmd=("docker" "compose" "-f" "$compose_file")
    if [[ -n "$env_file" ]]; then
        base_cmd+=("--env-file" "$env_file")
    fi

    # Check if --no-cache is in additional_args
    if [[ "$additional_args" == *"--no-cache"* ]]; then
        COMPOSE_PROJECT_NAME="$project_name" "${base_cmd[@]}" build --no-cache
        COMPOSE_PROJECT_NAME="$project_name" "${base_cmd[@]}" up -d
    else
        COMPOSE_PROJECT_NAME="$project_name" "${base_cmd[@]}" $additional_args
    fi
}