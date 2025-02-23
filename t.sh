source test.sh

# as we work dumb compose, we blank these variables for it to not fail
# init_container will overwrite these values
export ENCRYPTION_KEY="YourKeyHere"
export REDIS_PORT="6379"
export REDIS_PASSWORD="myredispassword"


#docker_compose init_project init_container/tests/test-docker-compose.yml "up --build --no-cache"
docker_compose logger_proj docker-compose.yml "up --build --no-cache"
