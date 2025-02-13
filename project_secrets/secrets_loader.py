from dotenv import load_dotenv
from project_secrets.secrets_fetcher import SecretsFetcher
from utils.file_encryptor import FileEncryptor
from utils.file_manager import BinaryFileManager
from project_secrets.secrets_manager import SecretsManager


class SecretsLoader:
    @staticmethod
    def load_from_dump(env_dump_fp: str) -> None:
        """
        Loads secrets from env.dump file which contains the ready to use remote secrets.
        Then marks secrets as loaded using SecretsManager's .mark_secrets_as_loaded method.
        """
        print(f'Remote secrets were found at: {env_dump_fp}. Loading them...')
        load_dotenv(dotenv_path=env_dump_fp)
        SecretsManager.mark_secrets_as_loaded()
        return

    @staticmethod
    def load_from_vault(vault_decrypted_fp: str, config_folder: str, save_dump: bool) -> None:
        """
        Fetches, uploads to environment remote secrets using SecretsFetcher class which runs on HashiCorpLoader module.
        Then marks secrets as loaded using SecretsManager's .mark_secrets_as_loaded method.
        """

        print(f'Hashicorp secrets were found decrypted at: {vault_decrypted_fp}.')
        load_dotenv(dotenv_path=vault_decrypted_fp)
        fetcher = SecretsFetcher(folder_to_save_env_dump=config_folder, save_dump=save_dump)
        fetcher.fetch()
        fetcher.load()
        SecretsManager.mark_secrets_as_loaded()
        return

    @classmethod
    def decrypt_and_load_from_vault(cls, encrypted_fp: str, config_folder: str, save_dump: bool) -> None:
        """
        - Decrypts `.vault.enc`file using user password
        - Calls load_from_vault method
        """

        if encrypted_fp.endswith('.enc'):   # important to pass the name without .enc
            encrypted_fp = encrypted_fp.rsplit('.enc')[0]

        encryptor = FileEncryptor(
            files_to_encode=[encrypted_fp],
            binary_file_manager=BinaryFileManager()
        )
        encryptor.decrypt()
        load_dotenv(dotenv_path=encrypted_fp)
        cls.load_from_vault(encrypted_fp, config_folder, save_dump)  # call cls method which already marks as loaded
        return
