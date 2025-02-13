** As it was mentioned, for this project, some original tools and modules were created. Including `not_gitmodules`  ([What's not_gitmodules?](https://github.com/Armen-Jean-Andreasian/not_gitmodules)).*

---

Secrets are kept on HashiCorp vault.

In our project we have `.vault.enc` file, which access secrets of HashiCorp, such as:

- `HCP_CLIENT_ID`
- `HCP_CLIENT_SECRET`
- `HCP_API_TOKEN_URL`
- `HCP_SECRETS_URL`

The process is following:

1. Decrypt `.vault.enc` file using password, that user enters in CLI
   *(by the time may be substituted by Github/Docker/Kubernetes/Host secrets)*
2. Sends a request to `https://api.hashicorp.cloud`, attaching `HCP_CLIENT_ID`  and `HCP_CLIENT_SECRET`  to obtain the API token, which is stateless and not being recorded at all.
3. After obtaining the API token, it requests `HCP_SECRETS_URL` with it, getting secrets and extract data from it.

All of this process does **HashiCorp Loader module. [Link](https://github.com/not-gitmodules/notgitmodules-hashicorp-loader)**

---

### **HashiCorp Loader module**

The HashiCorp module depends on two other modules.

- **Python file manager module.** [Link](https://github.com/not-gitmodules/notgitmodules-file-manager-py)
- **Python file encryptor module.** [Link](https://github.com/not-gitmodules/notgitmodules-file-encryptor-py)

---

## Module managment

For these purposes `not_gitmodules` are created. Which is the alt of gitmodules, but simpler and faster. [Link](https://github.com/Armen-Jean-Andreasian/not_gitmodules)

*Btw: *It’s important to keep all modules in `utils` folder in this project.*

The `notgitmodules.yaml` config section responsible for secrets is:

```yaml
utils:
  file_manager : https://github.com/not-gitmodules/notgitmodules-file-manager-py
  file_encryptor : https://github.com/not-gitmodules/notgitmodules-file-encryptor-py
  hashicorp_loader: https://github.com/not-gitmodules/notgitmodules-hashicorp-loader
```

Where `utils` is the folder name to download, and mentioned names are the renamed modules.

---

## The interface on modules: `EnvironmentLoader`

On top of those three modules, we also have `project_secrets` folder, which is the integration of those three modules with some Django-specific features into one interface: `EnvironmentLoader`

`EnvironmentLoader` operates with three classes: `SecretsFetcher`, `SecretsLoader` and `SecretsManager.`

- `SecretsManager`
    - Responsible for the state of secrets.
    - Provides `are_secrets_loaded` and `mark_secrets_as_loaded` methods, both of them work with "`secrets_loaded`" env variable.
    - Important to synchronize Django threads to retrieve secrets only once.
- `SecretsFetcher`
    - Interface built on `HashiCorpLoader` module.
    - Provides:
        - `fetch` method: initializes `HashiCorpLoader` assigns the instance of it to an instance variable.
          The point is that whenever `HashiCorpLoader` is initialized, it automatically fetches the secrets based on the given params, and keeps them in its state. The params in our case are:
            - `dump_env_to_file=True` : means remote secrets will also be dumped to `.env.dump` file.
            - `folder_to_save_env_dump=self.folder_to_save_env_dump` : the folder where `.env.dump` will be outputted. In our case the `config` folder.
        - `load` method : Calls the `.load` method of `HashiCorpLoader`, which loads secrets to environment variables.
          **It doesn’t use `.env.dump` file but loads from the state of* `HashiCorpLoader`’s instance*.*
- `SecretsLoader`
    - Responsible on loading loading secrets whether:
        - From `SecretsFetcher` which keeps the instance of `HashiCorpLoader`
        - From `.vault.enc` file which has encrypted HashiCorp access data, then loads
        - From `env.dump` file which contains the ready to use remote secrets.
    - For these purposes it provides:
        - `load_from_dump` method:
            - Loads secrets using `dotenv.load_dotenv` from `env.dump` file which contains the ready to use remote secrets.
            - Then marks secrets as loaded using `SecretsManager`'s `.mark_secrets_as_loaded` method.
        - `load_from_vault` method:
            - Fetches remote secrets
            - Uploads to environment remote secrets using `SecretsFetcher` class which runs on `HashiCorpLoader` module.
            - Then marks secrets as loaded using `SecretsManager`'s `.mark_secrets_as_loaded` method.
        - `decrypt_and_load_from_vault` method:
            - Decrypts `.vault.enc`file using user password
            - Calls `load_from_vault` method of `SecretsLoader`

---

The flow

1. Check for `env.dump` → load from it to env, mark as loaded
2. Check for `.vault` → fetch from vault, load to env, mark as loaded
3. Check for `.vault.enc` → decrypt, fetch from vault, load to env, mark as loaded