FROM python:3.11-slim

RUN echo "Building from django_project/Dockerfile"

#== Enviroment variables ===============================================================================================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DEBUG="TBD"
ENV DJANGO_SECRET_KEY="TBD"
ENV REDIS_PORT="TBD"
ENV REDIS_PASSWORD="TBD"
ENV REDIS_CACHE_TTL="TBD"
ENV DOMAIN_FOR_FAKE_URL="TBD"



# Layers ===============================================================================================================

WORKDIR /django_project

COPY config/requirements.txt config/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r config/requirements.txt

COPY . .
# experimenting
#COPY manage.py .

# Deleting tests
RUN --rm-rf ./tests/

# Generate static
RUN python manage.py collectstatic --noinput
