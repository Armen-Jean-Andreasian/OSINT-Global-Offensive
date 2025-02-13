from utils.hashicorp_loader import HashiCorpLoader


class SecretsFetcher:
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
    def __init__(self, folder_to_save_env_dump: str):
        self.folder_to_save_env_dump = folder_to_save_env_dump
        self.hashicorp_loader = None

    def fetch(self) -> None:
        """
        Fetches the secrets from HashiCorp vault, loads HashiCorp secrets to environment variables.
        HashiCorpLoader fetches the secrets at the moment of initialization, and keeps in its state.
        """
        self.hashicorp_loader = HashiCorpLoader(
            dump_env_to_file=True,
            folder_to_save_env_dump=self.folder_to_save_env_dump
        )

    def load(self) -> None:
        """
        Calls the .load method of HashiCorpLoader, which loads secrets to environment variables.
        It doesn’t use .env.dump file loads from the HashiCorpLoader’s instance.
        """
        self.hashicorp_loader.load()
