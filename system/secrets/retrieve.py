# Pure SOLID. How do you like it?
import os
from typing import Callable
from system.utils.custom_web_client import Client, Response


Client.init(allow_redirects=True)


class Hashicorp:
    api_token_url: str = "https://auth.idp.hashicorp.com/oauth2/token"

    api_token_headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    api_token_payload: Callable[[str, str], dict] = lambda client_id, client_secret: {
        "client_id": client_id,
        "client_secret": os.environ.get("HCP_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "audience": "https://api.hashicorp.cloud"
    }

    secrets_headers: Callable[[str], dict] = lambda api_token: {
        "Authorization": f"Bearer {api_token}"
    }


class ApiTokenRetriever:
    def __init__(self, logger, dot_vault_fp: str):
        self.hashicorp = Hashicorp
        self.logger = logger
        self.dot_vault_fp = dot_vault_fp

    def _are_vault_credentials_set(self) -> bool:
        """ Checks if vault credentials are already loaded to environ. """
        return os.environ.get("LOADED") is not None

    def _is_api_token_set(self):
        """ Checks if the API token ready to use. No need to fetch again. """
        return os.environ.get("HASHICORP_API_TOKEN") is not None

    def _request_token_api(self) -> Response:
        """Sends a POST request to obtain an API token."""
        data = self.hashicorp.api_token_payload(client_id=os.environ.get("HCP_CLIENT_ID"),
                                                client_secret=os.environ.get("HCP_CLIENT_SECRET"))

        return Client.post(
            url=self.hashicorp.api_token_url,
            headers=self.hashicorp.api_token_headers,
            data=data
        )

    def _parse_token_response(self, response: Response) -> str | Response:
        """Parses the response, returns the API token if it's good, if not the response."""
        if response.status_code == 200:
            api_token = response.json.get("access_token")
            return api_token
        return response

    def _set_api_token(self, api_token):
        os.environ["HASHICORP_API_TOKEN"] = api_token

    def retrieve_api_token(self):
        """Fetches API token from HashiCorp if not already set."""
        if not self._are_vault_credentials_set():
            raise Exception(f"Vault variables were not loaded to environ. {os.path.abspath(self.dot_vault_fp)}")

        if self._is_api_token_set():
            self.logger.info("API token is already set.")
            return

        self.logger.info("Requesting API token from HashiCorp...")

        response: Response = self._request_token_api()

        parsed_response: Response | str = self._parse_token_response(response)

        if isinstance(parsed_response, Response):
            raise RuntimeError(f"Failed to retrieve API token. Code: {response.status_code}, Response: {response}")
        else:
            self._set_api_token(api_token=parsed_response)
            self.logger.info("API token successfully retrieved and stored in environ.")


class SecretsRetriever:
    def __init__(self, logger):
        self.logger = logger
        self.hashicorp = Hashicorp

    def _request_secrets(self) -> Response:
        """Sends a GET request to obtain remote secrets."""
        headers = self.hashicorp.secrets_headers(api_token=os.environ.get('HASHICORP_API_TOKEN'))
        return Client.get(url=os.environ.get("HCP_SECRETS_URL"), headers=headers)

    def _parse_response(self, response) -> dict | Response:
        """Parses the response, returns the secrets in dict if everything's fine, otherwise - the response."""
        if response.status_code == 200:
            secrets_payload = response.json.get('secrets', [])
            secrets = {s['name']: s['static_version']['value'] for s in secrets_payload}
            return secrets
        else:
            return response

    def retrieve_secrets(self):
        """Fetches secrets from HashiCorp Vault and loads them into environment variables."""
        self.logger.info("Fetching secrets from HashiCorp Vault...")

        secrets_response = self._request_secrets()
        parsed_response = self._parse_response(response=secrets_response)

        if isinstance(parsed_response, Response):
            raise RuntimeError(
                f"Failed to retrieve secrets. Code: {parsed_response.status_code}, Response: {parsed_response.content}")
        else:
            self.logger.info("All secrets were successfully obtained.")
            secrets: dict = parsed_response
            return secrets


class SecretsKeeper:
    def __init__(self, logger, dot_env_fp: str):
        self.dot_env_fp = dot_env_fp
        self.logger = logger

    def save_to_file(self, secrets: dict):
        with open(self.dot_env_fp, 'w') as file:
            for k, v in secrets.items():
                file.write(f"{k}={v}\n")
        self.logger.info("All secrets were successfully saved to .env")
