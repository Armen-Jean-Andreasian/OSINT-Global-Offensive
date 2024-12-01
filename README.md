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

As Django is MTV not MVC, and I like quality, MTVC will be used:

- View: **(Presentation Layer)** 
  - Handles only GET method
  - delegates to Controller: POST, PUT, PATCH, DELETE methods
  - Returns HTML and receives data from front to send to Controller


- Controller: **(Business Logic Layer)**
- Handles only POST, PUT, PATCH, DELETE methods
- Does the black ops, returns the result to View in ServiceResponse

Full flow. view receives data and transfers to controller, it does the job, returns ServiceResponse to View which according to ServiceResponse's status decided what to render/redirect.