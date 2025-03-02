#!/bin/bash
source new.sh

function up() {
    pip install -r system/config/requirements.txt
    python retrieve_secrets.py
    sleep 5
    #docker_compose -p logger_proj -f docker-compose.yml "up --build --no-cache"
    docker_compose -p logger_proj -f docker-compose.yml -e system/config/.env "up --build --no-cache --remove-orphans"
}

function down() {
    docker compose --env-file system/config/.env -f docker-compose.yml down
}

down