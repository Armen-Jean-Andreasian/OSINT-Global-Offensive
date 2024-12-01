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
- It may hurt your solid feelings of an over-engineered amateur developer. 
