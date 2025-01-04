from dotenv import load_dotenv
from project_secrets.secrets_fetcher import SecretsFetcher
from utils.file_encryptor import FileEncryptor
from utils.file_manager import BinaryFileManager
from project_secrets.secrets_manager import SecretsManager


class SecretsLoader:
    @staticmethod
    def load_from_dump(env_dump_fp: str) -> None:
        print(f'Remote secrets were found at: {env_dump_fp}. Loading them...')
        load_dotenv(dotenv_path=env_dump_fp)
        SecretsManager.mark_secrets_as_loaded()
        return

    @staticmethod
    def load_from_vault(vault_decrypted_fp: str, config_folder: str) -> None:
        print(f'Hashicorp secrets were found decrypted at: {vault_decrypted_fp}.')
        load_dotenv(dotenv_path=vault_decrypted_fp)
        fetcher = SecretsFetcher(folder_to_save_env_dump=config_folder)
        fetcher.fetch()
        fetcher.load()
        SecretsManager.mark_secrets_as_loaded()
        return

    @classmethod
    def decrypt_and_load_from_vault(cls, vault_decrypted_fp: str, config_folder: str) -> None:
        encryptor = FileEncryptor(
            files_to_encode=[vault_decrypted_fp],  # important to pass the name without .enc
            binary_file_manager=BinaryFileManager()
        )
        encryptor.decrypt()
        load_dotenv(dotenv_path=vault_decrypted_fp)
        cls.load_from_vault(vault_decrypted_fp, config_folder)
        return
