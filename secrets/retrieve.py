import os
import requests
import traceback
from dotenv import load_dotenv
from app_logs import Logger

DOT_VAULT = "secrets/.vault"
DOT_ENV = ".env"

TOKEN_URL = "https://auth.idp.hashicorp.com/oauth2/token"

logger = Logger(module_name="secrets")

load_dotenv(DOT_VAULT)


def retrieve_api_token():
    """Fetches API token from HashiCorp if not already set."""
    if not os.environ.get("LOADED"):
        raise Exception(f"Vault variables were not loaded to environ. {os.path.abspath(DOT_VAULT)}")

    if os.environ.get("HASHICORP_API_TOKEN"):
        logger.info("API token is already set.")
        return

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": os.environ.get("HCP_CLIENT_ID"),
        "client_secret": os.environ.get("HCP_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "audience": "https://api.hashicorp.cloud"
    }

    logger.info("Requesting API token from HashiCorp...")
    response = requests.post(url=TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        api_token = response.json().get("access_token")
        if api_token:
            os.environ["HASHICORP_API_TOKEN"] = api_token
            logger.info("API token successfully retrieved and stored.")
        else:
            raise RuntimeError("HashiCorp returned an invalid API token.")
    else:
        raise RuntimeError(f"Failed to retrieve API token. Code: {response.status_code}, Response: {response.text}")


def retrieve_secrets():
    """Fetches secrets from HashiCorp Vault and loads them into environment variables."""
    logger.info("Fetching secrets from HashiCorp Vault...")

    headers = {
        "Authorization": f"Bearer {os.environ.get('HASHICORP_API_TOKEN')}"
    }
    response = requests.get(os.environ.get("HCP_SECRETS_URL"), headers=headers)

    if response.status_code == 200:
        secrets_payload = response.json().get('secrets', [])
        secrets = {s['name']: s['static_version']['value'] for s in secrets_payload}

        logger.info("All secrets were successfully obtained.")
        return secrets
    else:
        raise RuntimeError(f"Failed to retrieve secrets. Code: {response.status_code}, Response: {response.text}")


def save_to_file(secrets: dict):
    with open(DOT_ENV, 'w') as file:
        for k, v in secrets.items():
            file.write(f"{k}={v}\n")
    logger.info("All secrets were successfully saved to .env")


if __name__ == "__main__":
    try:
        retrieve_api_token()
        secrets = retrieve_secrets()
        save_to_file(secrets)
    except Exception as e:
        logger.error(f"Unhandled error: {e}\n{traceback.format_exc(limit=5)}")
    finally:
        logger.clear_logs()
