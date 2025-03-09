import os.path

from .secrets import ApiTokenRetriever, SecretsRetriever, SecretsKeeper
from .utils.custom_dotenv import load_dotenv
from .utils.custom_logger import Logger


def load_from_file(env_path):
    if os.path.exists(env_path):
        print(f".env file found, loading from it: {env_path}")
        load_dotenv(env_path)
        return True
    else:
        return False


def prepare_system(
    dot_env_path: str,
    dot_vault_path: str,
    log_output_dir: str

):
    secrets_logger = Logger(module_name="secrets", log_output_dir=log_output_dir)

    if load_from_file(env_path=dot_env_path):
        secrets_logger.clear_logs()
        exit(1)

    try:
        load_dotenv(dot_vault_path)

        token_retriever = ApiTokenRetriever(logger=secrets_logger, dot_vault_fp=dot_vault_path)
        token_retriever.retrieve_api_token()

        secrets_retriever = SecretsRetriever(logger=secrets_logger)
        secrets = secrets_retriever.retrieve_secrets()

        secrets_keeper = SecretsKeeper(logger=secrets_logger, dot_env_fp=dot_env_path)
        secrets_keeper.save_to_file(secrets=secrets)

    except Exception as e:
        secrets_logger.error(message=str(e))
    finally:
        secrets_logger.clear_logs()
