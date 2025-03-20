# Usage


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

For users who prefer convenience (like running scripts directly from an IDE by right-clicking), there are [quick_run.sh](../quick_run.sh) and [quick_stop.sh](../quick_stop.sh) scripts available.


### Quick Start Tests and Quick Stop Tests

For the same users, there are [quick_tests_run.sh](../quick_tests_run.sh) and [quick_tests_stop.sh](../quick_tests_stop.sh) scripts available.