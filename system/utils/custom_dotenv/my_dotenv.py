import os


def load_dotenv(path: str) -> None:
    with open(path) as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):  # skipping comments and empty lines
                continue

            key, _, val = line.partition("=")

            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]  # for surrounding quotes if present

            if key:  # avoiding empty keys
                os.environ[key] = val
