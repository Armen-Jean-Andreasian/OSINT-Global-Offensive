FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN not_gitmodules -y ./notgitmodules.yaml


EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

# docker build -t djangologger .
# docker run -it -p 8080:8080 djangologger
#
# in production:
# python manage.py collectstatic
