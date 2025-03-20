# Usage

---
## Vault Credentials Setup

1. Create a `.vault_credentials` file in the `system/config/` folder.
2. The file should include the following variables, which can be obtained from the HashiCorp Web App:
    - `HCP_CLIENT_ID`
    - `HCP_CLIENT_SECRET`
    - `HCP_SECRETS_URL`
3. Optionally, you can add the `LOADED` variable.
4. Run the script `run.sh` in the project root.
5. Use the following commands to manage the project:
    - `build` and `up` to start the project.
    - `stop` to turn off the compose environment.

This setup retrieves secrets into the `.env` file and then runs the project using Docker Compose.

---
## Infrastructure Management

### Start Infrastructure

Starts the containers using the latest built images. Rebuilds only the outdated/modified ones and removes orphaned containers.

```bash
sh infra/infra.sh run
```


### Stop Infrastructure

Stops and removes all running containers, networks, and volumes associated with the infrastructure.

```bash
sh infra/infra.sh stop
```

### Quick Start and Stop

For users who prefer convenience (like running scripts directly from an IDE by right-clicking), there are [quick_run.sh](quick_run.sh) and [quick_stop.sh](quick_stop.sh) scripts available.


### Quick Start Tests and Quick Stop Tests

For the same users, there are [quick_tests_run.sh](quick_tests_run.sh) and [quick_tests_stop.sh](quick_tests_stop.sh) scripts available.