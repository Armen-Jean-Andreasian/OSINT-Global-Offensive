#!/bin/bash

VERSION="v1" # update version
prefix="djangologger"

container_name="${prefix}-container-${VERSION}"


docker compose down
docker stop "${container_name}"