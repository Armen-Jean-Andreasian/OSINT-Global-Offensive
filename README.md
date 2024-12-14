# Logger Django App

The diagram of app: [Google Drive](https://drive.google.com/file/d/1aD0W2nmfU3mZkTCkDyJxTl87X1wKRheW/view?usp=sharing)


# Stack
- Django
- SQLite3 (PostgreSQL)


# Secrets, encryption, etc

- All project-level secrets are kept in HashiCorp Vault
- In `.env` are kept HashiCorp-related secrets
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


