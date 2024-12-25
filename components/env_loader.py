from dotenv import load_dotenv
import os
from utils.file_encryptor import FileEncryptor
from utils.file_manager import BinaryFileManager
from utils.hashicorp_loader import HashiCorpLoader


def decrypt_and_load_env(env_path) -> None:
    """Loads the environment vars from .env and .env.enc"""
    encryptor = FileEncryptor(files_to_encode=(env_path,), binary_file_manager=BinaryFileManager())

    if not (os.path.exists(env_path + '.enc') or os.path.exists(env_path)):
        raise FileNotFoundError(f"File {env_path} not found.")

    # from .env.enc
    if os.path.exists(os.path.join(env_path + '.enc')):
        encryptor.decrypt()

    load_dotenv(dotenv_path=env_path)
    encryptor.encrypt()




class EnvironmentLoader:
    @classmethod
    def load(cls, env_path: str) -> None:
        """
        Loads env variables and remote secrets to environ
        """
        if not cls._are_secrets_loaded():
            decrypt_and_load_env(env_path)
            print('.env was loaded')

            HashiCorpLoader().load()
            print('Remote secrets were successfully loaded')

            cls._mark_secrets_as_loaded()

    @staticmethod
    def _are_secrets_loaded():
        """
        As Django opens threads, each of them use the settings.py file we need to control loading process to avoid
        reloadings and resource wastes, as Envloader is called from settings.py.
        """
        return os.environ.get('secrets_loaded') == '1'

    @staticmethod
    def _mark_secrets_as_loaded():
        os.environ['secrets_loaded'] = '1'
