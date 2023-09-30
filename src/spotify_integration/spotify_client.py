import requests

from settings.settings import Settings
from spotify_integration.spotify_endpoints import SpotifyEndpoints

class SpotifyClient:
    __DEFAULT_TIMEOUT = 1

    def generate_client_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": Settings.SPOTIFY_CLIENT_ID,
            "client_secret": Settings.SPOTIFY_CLIENT_SECRET,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(
                SpotifyEndpoints.GENERATE_CLIENT_TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=self.__DEFAULT_TIMEOUT
            )

            response.raise_for_status()
        except requests.HTTPError as error:
            print(error)
            return None

        response_json = response.json()
        return response_json.get("access_token")


    def generate_private_client_token(self):
        payload = {
            "client_data": {
                "client_id": Settings.SPOTIFY_GENERIC_CLIENT_ID,
                "js_sdk_data": {"device_model": "unknown"}
            }
        }

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                SpotifyEndpoints.PRIVATE_CLIENT_TOKEN_URL,
                json=payload,
                headers=headers,
                timeout=self.__DEFAULT_TIMEOUT
            )

            response.raise_for_status()
        except requests.HTTPError as error:
            print(error)
            return None

        response_json = response.json()
        granted_token = response_json.get("granted_token")
        if granted_token:
            return granted_token.get("token")

        return None

