#!/bin/bash
source base.sh

# This script is used to run everything using compose
set -e

change_dir_to_root

install_pip_requirements
install_not_gitmodules
retrieve_env_vars # downloading .env

# packing statics for nginx.
if [ -d ./nginx/staticfiles/ ]; then
    echo "Static files already packed."
else
    python manage.py collectstatic
fi

# docker_compose_up_detached
docker_compose_up_build