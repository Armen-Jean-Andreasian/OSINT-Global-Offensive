from dotenv import load_dotenv
from pathlib import Path
import os
from utils.file_encryptor import FileEncryptor
from utils.file_manager import BinaryFileManager
from utils.hashicorp_loader import HashiCorpLoader


def decrypt_and_load_env(env_file='.env') -> None:
    """Loads the environment vars from .env and .env.enc"""
    base_dir = Path(__file__).resolve().parent.parent  # nevertheless, keep in this stack to not mess up

    encryptor = FileEncryptor(files_to_encode=(env_file,), binary_file_manager=BinaryFileManager())

    if os.path.exists(os.path.join(base_dir, env_file + '.enc')):
        encryptor.decrypt()
        load_dotenv()
        encryptor.encrypt()

    elif os.path.exists(os.path.join(base_dir, env_file)):
        # trying to find .env (maybe someone messed up)
        load_dotenv()
        encryptor.encrypt()
    else:
        raise FileNotFoundError(".env file (nor encrypted or decrypted) weren't found in ", base_dir)


class EnvironmentLoader:
    @classmethod
    def load(cls):
        """
        Loads env variables and remote secrets to environ
        """
        if not cls._are_secrets_loaded():
            decrypt_and_load_env()
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
