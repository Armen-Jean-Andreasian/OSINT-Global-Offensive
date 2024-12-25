FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y gcc libpq-dev git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r config/requirements.txt
RUN not_gitmodules -y config/notgitmodules.yaml

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]


# docker build -t djangologger .
# docker run -it -p 8080:8080 djangologger

# -p 8080:8080 part of the command is mapping the ports: -p [host machine port]:[container port]
