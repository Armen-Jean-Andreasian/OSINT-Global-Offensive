#!/bin/bash

# This script is used to run the django from a pc alongside with redis docker image

set -e

cd ..

pip install -r config/requirements.txt
not_gitmodules -y config/notgitmodules.yaml
python components/env_loader.py

docker compose --env-file config/.env.dump up -d

python manage.py runserver 8080
