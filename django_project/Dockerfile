FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django_project

# RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/* # for postgres

COPY config/requirements.txt config/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r config/requirements.txt
# not_gitmodules removed to init_container, as well as  python-dotenv, requests, cryptography

COPY . .
COPY manage.py .




