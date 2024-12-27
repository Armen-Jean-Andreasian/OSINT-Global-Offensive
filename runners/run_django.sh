#!/bin/bash

# This script is used to run the django from a pc alongside with redis docker image

set -e

cd ..

pip install -r config/requirements.txt
not_gitmodules -y config/notgitmodules.yaml

docker compose up -d

python manage.py runserver 8080
