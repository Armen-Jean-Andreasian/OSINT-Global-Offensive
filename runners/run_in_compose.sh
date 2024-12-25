#!/bin/bash

set -e

cd ..

docker-compose build # --no-cache
docker-compose up --build

sleep 10

# docker-compose logs -f # check logs
