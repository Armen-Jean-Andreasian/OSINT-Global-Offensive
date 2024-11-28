from .dotenv_loader import decrypt_and_load_env
from .hashicorp_loader import HashiCorp
import os


class EnvLoader:
    @classmethod
    def load(cls):
        """
        Loads env variables and remote secrets to environ
        """
        if not cls._are_secrets_loaded():
            decrypt_and_load_env()
            print('.env was loaded')

            HashiCorp().load()
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
