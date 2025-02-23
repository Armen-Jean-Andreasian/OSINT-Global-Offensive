from utils.hashicorp_loader import HashiCorpLoader
from utils.file_manager import BinaryFileManager
from utils.file_encryptor import FileEncryptor

from dotenv import load_dotenv
import os

__all__ = ["EnvironmentLoader"]


class EnvironmentLoader:
    def __init__(
        self,
        config_folder: str = os.path.join(os.path.dirname(__file__), 'config', ),
        save_dump=True,
    ):
        """
        :param config_folder: str - path to the folder where .vault.enc file is stored
        """
        self.vault_encrypted_fp: str = os.path.join(config_folder, ".vault.enc")
        self.vault_decrypted_fp: str = os.path.join(config_folder, ".vault")
        self.env_dump_fp: str = os.path.join(config_folder, ".env.dump")
        self.config_folder = config_folder
        self.save_dump = save_dump

    def load(self) -> None:
        """
        Loads env variables and remote secrets to environ
        """

        if not SecretsTracker.are_secrets_loaded():
            # Case 1 | If .env.dump exists (is already decrypted and fetched)=> load and early return
            if os.path.exists(self.env_dump_fp):
                return SecretsLoader.load_from_dump(env_dump_fp=self.env_dump_fp)

            # Case 2 | If .vault exists (is already decrypted) => fetch remote secrets, load them and early return
            if os.path.exists(self.vault_decrypted_fp):
                return SecretsLoader.load_from_vault(self.vault_decrypted_fp, self.config_folder, self.save_dump)

            # Case 3 | If .vault.enc exists => decrypt it, load and early return
            if os.path.exists(self.vault_encrypted_fp):
                return SecretsLoader.decrypt_and_load_from_vault(self.vault_decrypted_fp, self.config_folder,
                                                                 self.save_dump)

            # Case 4 | If none of the above => raise error
            raise FileNotFoundError(
                f"None of: {self.env_dump_fp}, {self.vault_decrypted_fp}, or {self.vault_encrypted_fp} were found."
                f"Impossible to load secrets."
            )
        else:
            print("Secrets are already loaded. Skipping...")


class RemoteSecretsFetcher:
    """
    Interface built on HashiCorpLoader module.

    Provides methods:

    - `fetch` method: initializes HashiCorpLoader assigns the instance of it to an instance variable.
    The point is that whenever HashiCorpLoader is initialized,
    it automatically fetches the secrets based on the given params, and keeps them in its state.
    The params in our case are:
        - dump_env_to_file=True : means remote secrets will also be dumped to .env.dump file.
        - folder_to_save_env_dump=self.folder_to_save_env_dump : the folder where .env.dump will be outputted.
        In our case the config folder.

    - load method : Calls the .load method of HashiCorpLoader, which loads secrets to environment variables.
        *It doesn’t use .env.dump file but loads from the HashiCorpLoader’s instance.
    """

    def __init__(self, folder_to_save_env_dump: str, save_dump: bool):
        self.save_dump = save_dump  # for debug
        self.folder_to_save_env_dump = folder_to_save_env_dump
        self.hashicorp_loader = None

    def fetch(self) -> None:
        """
        Fetches the secrets from HashiCorp vault, loads HashiCorp secrets to environment variables.
        HashiCorpLoader fetches the secrets at the moment of initialization, and keeps in its state.
        """
        self.hashicorp_loader = HashiCorpLoader(folder_to_save_dump=self.folder_to_save_env_dump)

    def load(self) -> None:
        """
        Calls the .load method of HashiCorpLoader, which loads secrets to environment variables.
        It doesn’t use .env.dump file loads from the HashiCorpLoader’s instance.
        """
        self.hashicorp_loader.load()


class SecretsLoader:
    @staticmethod
    def load_from_dump(env_dump_fp: str) -> None:
        """
        Loads secrets from env.dump file which contains the ready to use remote secrets.
        Then marks secrets as loaded using SecretsTracker's .mark_secrets_as_loaded method.
        """
        print(f'Remote secrets were found at: {env_dump_fp}. Loading them...')
        load_dotenv(dotenv_path=env_dump_fp)
        SecretsTracker.mark_secrets_as_loaded()
        print(f'Remote secrets were successfully loaded from: {env_dump_fp}.')
        return

    @staticmethod
    def load_from_vault(vault_decrypted_fp: str, folder_to_save_env_dump: str, save_dump: bool) -> None:
        """
        Fetches, uploads to environment remote secrets using RemoteSecretsFetcher class which runs on HashiCorpLoader module.
        Then marks secrets as loaded using SecretsManager's .mark_secrets_as_loaded method.
        """

        print(f'Vault-access secrets were found decrypted at: {vault_decrypted_fp}.')
        load_dotenv(dotenv_path=vault_decrypted_fp)
        fetcher = RemoteSecretsFetcher(folder_to_save_env_dump=folder_to_save_env_dump, save_dump=save_dump)
        fetcher.fetch()
        fetcher.load()
        SecretsTracker.mark_secrets_as_loaded()
        print(f'Remote secrets were successfully loaded from the vault.')
        return

    @classmethod
    def decrypt_and_load_from_vault(cls, encrypted_fp: str, folder_to_save_env_dump: str, save_dump: bool) -> None:
        """
        - Decrypts `.vault.enc`file using user password
        - Calls load_from_vault method
        """

        if encrypted_fp.endswith('.enc'):  # important to pass the name without .enc
            encrypted_fp = encrypted_fp.rsplit('.enc')[0]

        encryptor = FileEncryptor(
            files_to_encode=[encrypted_fp],
            binary_file_manager=BinaryFileManager()
        )
        encryptor.decrypt()
        print(f"{encrypted_fp} was successfully decrypted.")

        load_dotenv(dotenv_path=encrypted_fp)
        print(f"Vault-access secrets were loaded to OS from decrypted .vault file.")

        cls.load_from_vault(encrypted_fp, folder_to_save_env_dump,
                            save_dump)  # call cls method which already marks as loaded
        print(f"Processing with loading remote secrets from the vault.")
        return


class SecretsTracker:
    """
    Responsible for the state of secrets.
    Provides are_secrets_loaded and mark_secrets_as_loaded methods, both of them work with "secrets_loaded" env variable.
    Important to synchronize Django threads to retrieve secrets only once.
    """

    @staticmethod
    def are_secrets_loaded() -> bool:
        """ Checks if secrets are already loaded """
        return os.environ.get('secrets_loaded') == "1"

    @staticmethod
    def mark_secrets_as_loaded() -> None:
        """ Marks secrets as loaded """
        os.environ['secrets_loaded'] = "1"


if __name__ == "__main__":
    env_loader = EnvironmentLoader()
    env_loader.load()
    if SecretsTracker.are_secrets_loaded():
        print("Secrets are loaded.")
    else:
        raise Exception("Secrets are not loaded.")

