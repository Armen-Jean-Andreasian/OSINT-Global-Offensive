import requests
import os


class HashiCorp:
    """
    HashiCorp works:
        1. You obtain API token from server with your client id and client secret
        2. Then you retrieve your secrets using the obtained API token

    It's a stateless class designed to retrieve data without keeping it.
    """

    @staticmethod
    def _obtain_api_token(client_id: str, client_secret: str, api_token_url: str):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud"
        }

        response = requests.post(url=api_token_url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get("access_token")
        raise RuntimeError("Hashicorp secret loading was failed")

    @staticmethod
    def _retrieve_remote_secrets(api_token: str, url: str) -> list[dict]:
        response = requests.get(url, headers={"Authorization": f"Bearer {api_token}"})

        try:
            return response.json()['secrets']
        except Exception as e:
            raise RuntimeError(f"Error occurred while retrieving data from Hashcorp vault: {str(e)}")

    @staticmethod
    def _load_hashicorp_secrets_to_env(remote_secrets: list[dict]):
        for secret_pair in remote_secrets:
            k, v = secret_pair['name'], secret_pair['static_version']['value']
            os.environ[k] = v

    def load(self):
        if not os.environ.get('hcp_loaded'):
            # retrieving API token

            # trying if .env was loaded by load_secrets function (someone messed up)
            if os.environ.get('HCP_CLIENT_ID') is None:
                # loading .env manually
                from .dotenv_loader import load_env_vars
                load_env_vars()

            client_id = os.environ.get('HCP_CLIENT_ID')
            client_secret = os.environ.get('HCP_CLIENT_SECRET')
            api_token_url = os.environ.get('HCP_API_TOKEN_URL')

            api_token = self._obtain_api_token(client_id, client_secret, api_token_url)

            # retrieving secrets
            secrets_url = os.environ.get('HCP_SECRETS_URL')
            remote_secrets: list[dict] = self._retrieve_remote_secrets(api_token, secrets_url)

            # loading to env
            self._load_hashicorp_secrets_to_env(remote_secrets)
            print("Secrets are loaded to env!")

            # setting env_loaded to any value to indicate it has already been loaded
            os.environ['hcp_loaded'] = '1'
