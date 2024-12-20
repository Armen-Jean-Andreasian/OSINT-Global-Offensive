#!/bin/bash

set -e

pip install -r requirements.txt
not_gitmodules -y notgitmodules.yaml
python manage.py runserver 8080
