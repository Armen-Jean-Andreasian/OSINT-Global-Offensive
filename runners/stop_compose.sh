#!/bin/bash

VERSION="v1" # update version
prefix="djangologger"

container_name="${prefix}-container-${VERSION}"

# beautiful Docker Compose needs env file to shut down the containers. wow
docker compose --env-file ../config/.env.dump down
docker stop "${container_name}"