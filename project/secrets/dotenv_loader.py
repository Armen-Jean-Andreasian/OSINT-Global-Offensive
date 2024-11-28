from dotenv import load_dotenv
from pathlib import Path
import os

ENV_FILE = '.env'


def load_env_vars():
    """Loads the environment vars from .env"""

    base_dir = Path(__file__).resolve().parent.parent.parent  # nevertheless, keep in this stack to not mess up

    dotenv_path = os.path.join(base_dir, ENV_FILE)

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(ENV_FILE, "wasn't found in ", dotenv_path)

    load_dotenv(dotenv_path=dotenv_path)
