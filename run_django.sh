#!/bin/bash

set -e

pip install -r requirements.txt
not_gitmodules -y notgitmodules.yaml -d utils
python manage.py runserver 8080
