# Avoiding hardcoding ports into `nginx.conf`

For both approaches we use `proxy_pass http://django:$DJANGO_PORT;` in `nginx.conf`

Both approaches use envsubst, which is built in default nginx Docker image


> Way 1: Hardcoding into container's `nginx.conf` during build-time
> - Cons: if the port changes, container needs to be rebuilt
>
> ```dockerfile
> FROM nginx:latest
> 
> # arg for build time to obtain the env var (orchestrator should provide)
> ARG DJANGO_PORT
> ENV DJANGO_PORT=${DJANGO_PORT}
> 
> # Copy config
> COPY nginx.conf /etc/nginx/nginx.template.conf
> 
> # Replace env vars in config and move it into place
> # If DJANGO_PORT is not found in environ 8000 is the default
> RUN sh -c "envsubst '\${DJANGO_PORT:-8000}' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf"
> 
> COPY staticfiles /nginx/staticfiles
> ```
>

> Way 2: Substituting during runtime
> - New `entrypoint.sh` file:
> ```shell
> #!/bin/sh
> 
> # Replace env vars in config and move it into place
> envsubst '\${DJANGO_PORT}' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf
> 
> # Start Nginx
> exec "$@"
> ```
> And in Dockerfile we run the script:

```dockerfile
FROM nginx:latest

# Copy config
COPY nginx.conf /etc/nginx/nginx.template.conf

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY staticfiles /nginx/staticfiles

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

---

### **Key Differences Between the Two Approaches:**

| Approach                            | When Substitution Happens | Pros                                                                                                           | Cons                                                                   |
|-------------------------------------|---------------------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Way 1 (Build-Time Substitution)** | During `docker build`     | - No need for an extra script. <br> - Simpler container startup.                                               | - **Requires rebuild** if `DJANGO_PORT` changes. <br> - Less flexible. |
| **Way 2 (Runtime Substitution)**    | When the container starts | - **More flexible** (just restart the container if the port changes). <br> - Works well with `docker-compose`. | - Adds an `entrypoint.sh` script.                                      |


---

I chose first way, as the port is not gonna change, and to keep everything simple.