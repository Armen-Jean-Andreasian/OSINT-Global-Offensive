from dotenv import load_dotenv
from pathlib import Path
import os
from utils import FileEncryptor


def decrypt_and_load_env(env_file='.env') -> None:
    """Loads the environment vars from .env and .env.enc"""
    base_dir = Path(__file__).resolve().parent.parent.parent  # nevertheless, keep in this stack to not mess up

    encryptor = FileEncryptor(files_to_encode=(env_file,))

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
