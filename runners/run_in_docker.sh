#!/bin/bash

# This script is used to run the django from a docker container alongside with redis docker image
set -e

cd ..

docker compose --env-file config/.env.dump up -d

VERSION="v1" # update version
prefix="djangologger"

image_name="${prefix}-${VERSION}"
container_name="${prefix}-container-${VERSION}"


existing_containers=$(docker ps -a --format "{{.Names}}")
existing_images=$(docker images --format "{{.Repository}}")
container_found=false

for container in ${existing_containers}; do
  if [[ "${container}" == ${prefix}* ]]; then
    # if the container is not the one we want to run, stop and remove it
    if [[ "${container}" != "${container_name}" ]]; then
      echo "Stopping and removing container: ${container}"
      docker stop "${container}"
      docker rm -f "${container}"
    else
        # we found the container we want to run
        container_found=true
    fi
  fi
done

# deleting images with different version
for image in ${existing_images}; do
  if [[ "${image}" == ${prefix}* && "${image}" != "${image_name}" ]]; then
    echo "Removing image: ${image}"
    docker rmi -f "${image}"
  fi
done

# Check if the container is already running
if ${container_found}; then
  echo "${container_name} is already running. Stopping it."
  docker stop "${container_name}"
  docker start "${container_name}"
else
  echo "Building and running the container: ${container_name}"
  docker build -t "${image_name}" .  # --no-cache if necessary
  docker run --name "${container_name}" -it -p 8080:8080 "${image_name}"
fi

docker exec -it "${container_name}" python manage.py runserver 0.0.0.0:8080


