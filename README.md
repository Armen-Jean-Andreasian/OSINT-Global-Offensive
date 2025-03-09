# Stack
<p align="center">
<img src="https://e7.pngegg.com/pngimages/10/113/png-clipart-django-web-development-web-framework-python-software-framework-django-text-trademark-thumbnail.png" alt="Python" width="48" height="48" />
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFRo0Y8B-K-skRKINQNGB_LQz029Cf9VEcsw&s" alt="Go" width="48" height="48" />
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_Jxyptf2jPCbEozdlBsQhJBzws8ek2CoeZg&s" alt="Go" width="48" height="48" />
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-4q2h8RjVBQY75dIRbZI3A4V3G_UGGVutUB72egCcWuKt2VZA2MvSsb5CgLT9l5fXELg&usqp=CAU" alt="Go" width="48" height="48" />
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsbQP2DoSO32lDEtfRfMDsrpAhn-qUxh-9YMvFqDuYuH5NgkfrBlj1l3mjDGca0z4z7Fg&usqp=CAU" alt="Go" width="48" height="48" />
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLXdPtfBobUsKl5vwAxC34rwz9EsqOF2Tj9w&s" alt="" width="48" height="48" />
</p>


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
- In `.env` are kept HashiCorpLoader-related secrets
- The `.env` file is encrypted.
  - By default it's the `master-key` that you'll be asked to enter
  - Optionally you can encrypt using a random generated salt, which will be saved as a file called `salt`, which is also supported.

So the order is:
1. Decrypt the `.env` file
2. Retrieve Hashicorp data outta it
3. Request Hashicorp and obtain Django secrets.

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
