from utils.hashicorp_loader import HashiCorpLoader


class SecretsFetcher:
    def __init__(self, folder_to_save_env_dump: str):
        self.folder_to_save_env_dump = folder_to_save_env_dump
        self.hashicorp_loader = None

    def fetch(self) -> None:
        """ Fetches the secrets from HashiCorp vault, loads HashiCorp secrets to environment variables. """
        self.hashicorp_loader = HashiCorpLoader(
            dump_env_to_file=True,
            folder_to_save_env_dump=self.folder_to_save_env_dump
        )

    def load(self) -> None:
        self.hashicorp_loader.load()
