from pathlib import Path
import os
import sys

# Dynamically resolve imports based on execution context
if __name__ == '__main__':
    print(str(Path(__file__).resolve().parent.parent))

    # Add the root of your project (LoggerDjango) to the sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from project_secrets.secrets_manager import SecretsManager
    from project_secrets.secrets_loader import SecretsLoader
else:
    from project_secrets.secrets_loader import SecretsLoader


class EnvironmentLoader:
    def __init__(
        self,
        config_folder: str = os.path.join(Path(__file__).resolve().parent.parent, 'config'),
    ):
        """
        :param config_folder: str - path to the folder where .vault.enc file is stored
        """
        self.vault_encrypted_fp: str = os.path.join(config_folder, ".vault.enc")
        self.vault_decrypted_fp: str = os.path.join(config_folder, ".vault")
        self.env_dump_fp: str = os.path.join(config_folder, ".env.dump")
        self.config_folder = config_folder

    def load(self) -> None:
        """
        Loads env variables and remote secrets to environ
        """
        # IT'S LOB PRINCIPLE. DONT GET TRIGGERED BABY

        if not SecretsManager.are_secrets_loaded():
            # Case 1 | If .env.dump exists (is already decrypted and fetched)=> load and early return
            if os.path.exists(self.env_dump_fp):
                return SecretsLoader.load_from_dump(env_dump_fp=self.env_dump_fp)

            # Case 2 | If .vault exists (is already decrypted) => fetch remote secrets, load them and early return
            if os.path.exists(self.vault_decrypted_fp):
                return SecretsLoader.load_from_vault(self.vault_decrypted_fp, self.config_folder)

            # Case 3 | If .vault.enc exists => decrypt it, load and early return
            if os.path.exists(self.vault_encrypted_fp):
                return SecretsLoader.decrypt_and_load_from_vault(self.vault_decrypted_fp, self.config_folder)

            # Case 4 | If none of the above => raise error
            raise FileNotFoundError(
                f"None of: {self.env_dump_fp}, {self.vault_decrypted_fp}, or {self.vault_encrypted_fp} were found."
                f"Impossible to load secrets."
            )
        else:
            print("Secrets are already loaded. Skipping...")


if __name__ == "__main__":
    # to run from shell script
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_folder", help="Path to the environment folder.")
    args = vars(parser.parse_args())  # Convert parsed arguments to a dictionary

    env_loader = EnvironmentLoader(**{k: v for k, v in args.items() if v})
    env_loader.load()
