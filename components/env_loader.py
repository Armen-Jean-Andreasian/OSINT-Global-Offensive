from pathlib import Path
from dotenv import load_dotenv
import os
import sys

# Dynamically resolve imports based on execution context
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from utils.file_encryptor import FileEncryptor
    from utils.file_manager import BinaryFileManager
    from utils.hashicorp_loader import HashiCorpLoader
else:
    from utils.file_encryptor import FileEncryptor
    from utils.file_manager import BinaryFileManager
    from utils.hashicorp_loader import HashiCorpLoader


def are_secrets_loaded():
    """
    As Django opens threads, each of them use the settings.py file we need to control loading process to avoid
    reloadings and resource wastes, as Envloader is called from settings.py.
    """
    return os.environ.get('secrets_loaded') == '1'


def load_local_hashicorp_to_env(hashicorp_env_path: str):
    """
    Loads the environment vars from .env and .env.enc
    :param hashicorp_env_path: path to the .env file keeping the HashiCorp credentials
    """
    encryptor = FileEncryptor(files_to_encode=(hashicorp_env_path,), binary_file_manager=BinaryFileManager())

    if not (os.path.exists(hashicorp_env_path + '.enc') or os.path.exists(hashicorp_env_path)):
        raise FileNotFoundError(f"File {hashicorp_env_path} not found.")

    # from .env.enc
    if os.path.exists(os.path.join(hashicorp_env_path + '.enc')):
        encryptor.decrypt()

    load_dotenv(dotenv_path=hashicorp_env_path)
    # encryptor.encrypt() -> as Docker start doesn't have -it - keep the file decrypted


def fetch_hashicorp_secrets(dump_env_to_file: bool, folder_to_save_env_dump: str):
    """ Fetches the secrets from HashiCorp vault, loads HashiCorp secrets to environment variables. """
    hashicorp_loader = HashiCorpLoader(dump_env_to_file, folder_to_save_env_dump)
    hashicorp_loader.load()


class EnvironmentLoader:
    @staticmethod
    def load(
        env_folder=os.path.join(Path(__file__).resolve().parent.parent, 'config'),
        hashicorp_env_file_name='.env',
        dump_env_to_file=True,
        folder_to_save_env_dump=os.path.join(Path(__file__).resolve().parent.parent, 'config'),
    ) -> None:
        """
        Loads env variables and remote secrets to environ
        """
        if not are_secrets_loaded():
            load_local_hashicorp_to_env(os.path.join(env_folder, hashicorp_env_file_name))
            print('.env was loaded')

            fetch_hashicorp_secrets(dump_env_to_file, folder_to_save_env_dump)
            print('Remote secrets were successfully loaded')

            EnvironmentLoader._mark_secrets_as_loaded()

    @staticmethod
    def _mark_secrets_as_loaded():
        os.environ['secrets_loaded'] = '1'


if __name__ == '__main__':
    EnvironmentLoader.load()
