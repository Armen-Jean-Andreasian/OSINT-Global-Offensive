import os


class SecretsManager:
    @staticmethod
    def are_secrets_loaded() -> bool:
        """ Checks if secrets are already loaded """
        return os.environ.get('secrets_loaded') == "1"

    @staticmethod
    def mark_secrets_as_loaded() -> None:
        """ Marks secrets as loaded """
        os.environ['secrets_loaded'] = "1"
