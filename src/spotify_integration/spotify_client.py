import os
import json
import base64
import requests

from typing import Dict

from settings.settings import Settings
from spotify_integration.spotify_endpoints import SpotifyEndpoints

class SpotifyClient:
    __DEFAULT_TIMEOUT = 1
    __MAX_RETRIES = 4

    def __init__(self) -> None:
        self.client_id = Settings.SPOTIFY_CLIENT_ID
        self.client_secret = Settings.SPOTIFY_CLIENT_SECRET
        self.auth_encoded = self.generate_client_authorization_encoded()
        self.client_token = self.generate_client_token()
        self.private_client_token = self.generate_private_client_token()

        self.base_header = {
            "Authorization": f"Bearer {self.client_token}"
        }

        self.private_header = {
            **self.base_header,
            "Client-Token": self.private_client_token,
        }
    
    def generate_client_authorization_encoded(self):
        auth_string = self.client_id + ":" + self.client_secret
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

    def get_playlist_items(self, playlist_id: str):
        url = SpotifyEndpoints.SPOTIFY_BASE_URL + SpotifyEndpoints.PLAYLIST_ITEMS.replace("{playlist_id}", playlist_id)
        headers = self.base_header

        return self.__make_get_request(url=url, headers=headers)
    
    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token}
    
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
                retry_attempts += 1
        
        return None
    
    # ver se tem opção de paginação
    def find_artist(self, artist_name): 
        headers = self.get_auth_header(self.client_token)
        query = f"?q={artist_name}&type=artist&limit=50&offset=50"

        try:
            response = requests.get(
                SpotifyEndpoints.SEARCH + query,
                headers=headers,
                timeout=self.__DEFAULT_TIMEOUT
            )

            response.raise_for_status()
        except requests.HTTPError as error:
            print(error)
            return None

        response_json = response.json().get("artists").get("items")
        if len(response_json) == 0:
            return None

        return response_json