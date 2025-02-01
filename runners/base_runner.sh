#!/bin/bash
source scripts.sh

# This script is used to run everything using compose
function prepare() {

    set -e
    change_dir_to_root

    install_pip_requirements
    install_not_gitmodules
    retrieve_env_vars # downloading .env
    pack_statics_for_nginx # packing statics for nginx.
}
