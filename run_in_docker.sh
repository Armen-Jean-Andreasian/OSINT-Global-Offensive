#!/bin/bash

set -e

docker build -t djangologger . # --no-cache
docker run -it -p 8080:8080 djangologger # important -it flag to enter the password for encrypted .env file

