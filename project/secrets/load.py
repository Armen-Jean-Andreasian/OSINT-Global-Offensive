from .hashicorp_loader import HashiCorp
from .dotenv_loader import load_env_vars


def load_secrets():
    """This will load all secrets securely and load to env automatically"""
    load_env_vars()
    return HashiCorp().load()
