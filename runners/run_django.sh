#!/bin/bash

set -e

cd ..

pip install -r config/requirements.txt
not_gitmodules -y config/notgitmodules.yaml
python manage.py runserver 8080
