This part is desingned to be executed before uping docker compose.
It will fetch the secrets from the secrets manager and save them in the .env file.

Particularly, all of secrets-fetching stuff will remain "behind the scenes" (behind docker-compose).

So docker-compose will take the .env file and just use it.

I kept it in Python, not shell, because of automation. In both scenarios we need packages,  for shell we need jq for parsing json which is os-dependent. With python we are os-independent. 

---
## Pros

Imo, it's the best possible solution for this case, when:
- The secrets are stored in the remote manager, and the docker-compose needs them "right now" to start the services.
- Usage of other orchestration tools, such as Docker Swarm or Nomad is not desired and may take time to implement and substitute the current solution. Especially taking into account that this project is development focused and not focused on DevOps and orchestration.
- Usage of some tool like Redis to as a message broker for one container to fetch secrets then put into Redis, is absolute overhead and has lots of bottlenecks. Nevertheless, having a separate container for fetching secrets and turns off, may seem secure, but it's a total overhead and overengineering.


So keeping everything this simple, is also a good solution in terms of further maintainability.


## Cons

Minuses:
- Instead of secrets here we get another secure file: `.vault` or `.vault.key` which we need to keep secure. From the point of minimalism, we have no benefit in fact, but from the point of scalability and organization - it's a good boost.
- In controversy with the approach with a container that fetches secrets and turns off disappearing with the dependencies of it, in this case we need to install dependencies of this module on the system.

---
So this script should be added to CI/CD pipeline before the docker compose up command.

