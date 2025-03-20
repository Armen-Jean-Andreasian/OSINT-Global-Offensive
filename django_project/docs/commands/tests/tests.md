## - Run all tests

### Using Docker Compose
```bash
docker compose exec django pytest
```
This runs `pytest` inside the `django` service container.

### Inside the Docker Container
```bash
pytest
```
If you are already inside the running container, simply execute `pytest`.

---

## - Run tests with coverage
```bash
docker compose exec django pytest --cov=.
```
This runs all tests and generates a coverage report.

---

## - Debugging test failures
Run tests with detailed output:
```bash
docker compose exec django pytest -v -s
```

Run tests with `pdb` for interactive debugging:
```bash
docker compose exec django pytest --pdb
```

---
