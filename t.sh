#!/bin/bash

pip install -r secrets/requirements.txt

python secrets/retrieve.py


# docker_compose logger_proj docker-compose.yml "up --build --no-cache"
