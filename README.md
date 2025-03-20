# OSINT-Global-Offensive

## Project Overview

### Introduction
OSINT-Global-Offensive is an advanced open-source intelligence (OSINT) framework designed to streamline and automate the process of gathering, analyzing, and processing publicly available information. Built for cybersecurity professionals, ethical hackers, and investigative researchers, this project leverages various data sources to provide actionable intelligence.

### Key Features
- **Automated Data Collection** – Extract and process data from multiple sources, including social media, websites, and public databases.
- **Modular Architecture** – Easily extend functionality with new data sources and processing modules.
- **Efficient Search & Filtering** – Query and filter results to extract relevant insights.
- **Data Normalization** – Standardizes extracted data for better analysis and correlation.
- **Extensive API Support** – Integrates with third-party services and APIs for enriched intelligence gathering.
- **Scalability** – Built with Docker to ensure easy deployment and scalability.
- **Enhanced Security** – Leverages HashiCorp Vault for secure storage of secrets and credentials.
- **Custom Git Modules** – Implements `not_gitmodules` to manage dependencies more effectively.

### Use Cases
- **Cybersecurity Investigations** – Identify threats, track malicious actors, and uncover security vulnerabilities.
- **Threat Intelligence** – Monitor potential risks and analyze digital footprints.
- **Law Enforcement & Forensics** – Support investigations by uncovering publicly available evidence.
- **Journalistic Research** – Gather and verify information for investigative journalism.
- **Competitive Intelligence** – Analyze market trends and monitor competitors.

### Technologies Used
<p align="center">
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/python.png" alt="Python" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/go.png" alt="GO" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/bash.png" alt="bash" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/js.png" alt="JS" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/html.png" alt="HTML" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/css.png" alt="CSS" height="48" />
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/django.png" alt="Django" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/fastapi.png" alt="fastapi" height="48" />
</p>


<p align="center">
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/rmq.png" alt="rmq" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/redis.png" alt="redis" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/nginx.png" alt="nginx" width="48" height="48" />

<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/kafka.png" alt="kafka" width="50" height="50" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/logstash.svg" alt="logstash" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/elasticsearch.png" alt="elasticsearch" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/grafana.png" alt="grafana" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/postgresql.png" alt="postgresql" width="48" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/sqlite.png" alt="sqlite" width="48" height="48" />
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/hashicorp.png" alt="hashicorp" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/docker.png" alt="docker" height="48" />
<img src="https://raw.githubusercontent.com/dev-tools-utils/logos/refs/heads/master/docker_compose.png" alt="docker" height="48" />
</p>





- **Python** – Core programming language for automation and data processing.
- **GoLang** – Used for high-performance components.
- **Bash** – Shell scripting for automation and system tasks.
- **HTML/CSS/JavaScript** – For front-end rendering and user interaction.


- **Django** – Provides a robust backend framework.
- **FastAPI** – Included in some microservices to provides high-performance.


- **RabbitMQ** – Handles asynchronous task processing
- **Redis** – Handles caching, also is used as a secondary message broker.
- **Nginx** – Reverse proxy and load balancing.


- **Kafka** – Facilitates real-time data streaming.
- **Logstash** – Enables data collection, transformation, and forwarding.
- **Elasticsearch** – Provides full-text search and analytics capabilities.
- **Grafana** – Visualizes and monitors metrics for system performance.
- **PostgreSQL (previously SQLite3)** – Manages structured data storage.


- **HashiCorp Vault** – Utilized for secure secrets management.
- **Not Git Modules** – Blazingly fast **original** interpretation of Git submodules for dependency management.
- **Docker** – Ensures consistent deployment and environment management.
- **Docker Compose** – Orchestrates multi-container applications.


### Architectural Principles
- **Lightweight and Optimized** – Adheres to `LOB` and `YAGNI` principles, avoiding unnecessary complexity.
- **Service-Oriented Design** – CRUD operations are handled at the model level, reducing reliance on controllers.
- **Controllerless Flow** – Views handle data presentation, while models manage CRUD operations.
- **Custom Logging System** – Implements a structured logging mechanism for audit trails and debugging.

### Why This Project?
In a world where information is power, OSINT-Global-Offensive provides the tools needed to harness publicly available data effectively. The framework is built with security, flexibility, and usability in mind, ensuring that professionals can focus on intelligence analysis rather than tedious data collection.

---
This overview serves as a high-level introduction to the project. Further sections will dive into installation, usage, and contribution guidelines.




---
# Usage


**Start infrastructure**: Starts the containers using the latest built images. Rebuilds only the outdated/modified ones and removes orphaned containers.


```bash
sh infra/infra.sh run
```

**Stop infrastructure**: Stops and removes all running containers, networks, and volumes associated with the infrastructure.

```bash
sh infra/infra.sh stop
```


**Additionally**, for users who prefer convenience (like running scripts directly from an IDE by right-clicking), there are `quick_run.sh` and `quick_stop.sh`.  


---
#### [20.12.2024]
New update of the project.

- SQLite3 (PostgreSQL)
- Redis
- Docker
- Nginx
- `not_gitmodules` (original implementation of git modules)
- HashiCorp Vault
- HTML/CSS/JavaScript

Since now all CRUD methods will be moved to Models.
- create (all params needed) => create one based on params
- index (may have params) => show all based on params 
- show (has at least one param) => show one based on params
- update (at least id, new_content) => update one based on params
- destroy (at least id) => delete one based on params

Additionally, some other methods:
- clone (at least id) => clones the object into a new one with different id


No more Controllers. Views will be responsible for handling the data and passing it to Models. Models will be responsible for CRUD operations. Views will be responsible for rendering the data.

---
# Logger Django App

The diagram of app: [Google Drive](https://drive.google.com/file/d/1aD0W2nmfU3mZkTCkDyJxTl87X1wKRheW/view?usp=sharing)


# Stack
- Django
- SQLite3 (PostgreSQL)
- Redis
- Docker
- `not_gitmodules` (original implementation of git modules)
- HashiCorp Vault
- HTML/CSS/JavaScript


# Secrets, encryption, etc

- All project-level secrets are kept in HashiCorpLoader Vault


# Principle

- The project strongly maintains `LOB` principle combined with `YAGNI`. 
- Also, this project violates the PEP on line length with beautiful one-line solutions 
- It may hurt your solid feelings of an over-engineered amateur developer. 


# Segregation

## These are made to not make the project a mess of functions separated by files.

View: **(Presentation Layer)**
- Views are represented as View based classes, so they contain REST methods: `get`, `post`, `put`, `patch`, `delete`
- Each view has only one path it handles.
- Ideally views shouldn't contain business logic and they should return `Controller.call` or files (HTML). However, the scenarios can be complex, and to not summon new layers such as `Transaction`, `Contract`, or `BusinessLogic`, depending on the goal.
- One path may include multiple subpaths, each of them should have their own View based class. `/path` has `PathView` and `/path/data/<id>` has its own `DataView`.
- Views obtain data and pass to templates.
- To handle `get` maybe `dispatch` will be used.

  
Controller: **(Business Logic Layer)**
- Controllers are custom classes, which contain limited CRUD methods: `index`, `show`, `update`, `destroy`. 
- Controllers provide interface to work solely with their own models.
- Controllers answer using `ServiceResponse` custom data structure.

Full flow. view receives data and transfers to controller, it does the job, returns ServiceResponse to View which according to ServiceResponse's status decided what to render/redirect.

---

# Stats of 7.01.2025

- Date of start: Nov 26, 2024
- Lines of code: 26162
- Languages: 
    - Python 42.8%
    - JavaScript 37.9%
    - HTML 9.8%
    - CSS 5.7%
    - Shell 3.2%
    - Dockerfile 0.6%
