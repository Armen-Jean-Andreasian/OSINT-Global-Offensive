FROM nginx:latest

# arg only for build time to obtain the env var (orchestrator should provide)
ARG DJANGO_PORT

RUN test -n "$DJANGO_PORT" || (echo "Error: DJANGO_PORT is not set!" >&2; exit 1)

# Copy config
COPY nginx.conf /etc/nginx/nginx.template.conf

# Replace DJANGO_PORT in the container (8000 is the default)
RUN sh -c "envsubst '\${DJANGO_PORT}' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf"

COPY staticfiles /nginx/staticfiles