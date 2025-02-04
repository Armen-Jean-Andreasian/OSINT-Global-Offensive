#!/bin/bash
source base_runner.sh
source scripts.sh

prepare
docker_compose_up_detached
