FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /init_container

# install system dependencies (including git for not_gitmodules), clean up
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# copy only the requirements file install python dependencies first for better caching
COPY config/requirements.txt config/
RUN pip install --no-cache-dir -r config/requirements.txt

# copy the rest of config and run not_gitmodules
COPY config/ config/
RUN not_gitmodules -y config/notgitmodules.yaml

# copy the script last to avoid re-building the image when the script changes
COPY main.py .

# let docker-compose handle execution
CMD ["sleep", "infinity"]
