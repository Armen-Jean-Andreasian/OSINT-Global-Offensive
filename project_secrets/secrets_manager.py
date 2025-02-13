import os


class SecretsManager:
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
