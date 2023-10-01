import base64
import requests

from typing import Dict

from settings.settings import Settings
from spotify_integration.spotify_endpoints import SpotifyEndpoints

class SpotifyClient:
    __DEFAULT_TIMEOUT = 1
    __MAX_RETRIES = 4

    def __init__(self) -> None:
        self.auth_encoded = self.generate_client_authorization_encoded()
        self.reset_auth_token()

    def reset_auth_token(self):
        self.client_token = self.generate_client_token()

        self.base_header = {
            "Authorization": f"Bearer {self.client_token}"
        }
    
    def generate_client_authorization_encoded(self):
        auth_string = Settings.SPOTIFY_CLIENT_ID + ":" + Settings.SPOTIFY_CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        return auth_base64

    def generate_client_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": Settings.SPOTIFY_CLIENT_ID,
            "client_secret": Settings.SPOTIFY_CLIENT_SECRET,
        }

        headers = {
            "Authorization": "Basic " + self.auth_encoded,
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

    def get_playlist_items(self, playlist_id: str):
        url = SpotifyEndpoints.SPOTIFY_BASE_URL + SpotifyEndpoints.PLAYLIST_ITEMS.replace("{playlist_id}", playlist_id)
        headers = self.base_header

        return self.__make_get_request(url=url, headers=headers)
    
    # TODO - ver se tem opção de paginação
    def find_artist(self, artist_name): 
        query = f"?q={artist_name}&type=artist&limit=50&offset=50"

        return self.__make_get_request(url=SpotifyEndpoints.SEARCH + query, headers=self.base_header)

    def __make_get_request(self, *, url: str, headers: Dict):
        should_retry = True
        retry_attempts = 0
        
        while should_retry and retry_attempts < self.__MAX_RETRIES:
            try:
                response = requests.get(url=url, headers=headers, timeout=self.__DEFAULT_TIMEOUT)
                response.raise_for_status()

                return response.json()
            except requests.HTTPError as error:
                print(error)
                if error.response.status_code not in [401, 403]:
                    should_retry = False
                    break
                else:
                    self.reset_auth_token()
                    retry_attempts = 0

                retry_attempts += 1
        
        return None
    

