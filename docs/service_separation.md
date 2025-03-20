# Service Separation

- All services are split into corresponding folders.
- Each service has its own `Dockerfile`.
- All start commands are centralized in the **orchestrator** service (docker-compose for now).
