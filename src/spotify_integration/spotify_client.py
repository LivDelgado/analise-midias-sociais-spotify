import base64

import requests

from settings.settings import Settings
from spotify_integration.base_client import BaseClient
from spotify_integration.spotify_endpoints import SpotifyEndpoints


class SpotifyClient(BaseClient):
    def __init__(self) -> None:
        self.auth_encoded = self.generate_client_authorization_encoded()
        self._reset_auth_token()

    def _reset_auth_token(self):
        self.client_token = self.generate_client_token()

        self.base_header = {"Authorization": f"Bearer {self.client_token}"}

    @staticmethod
    def generate_client_authorization_encoded():
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
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = requests.post(
                SpotifyEndpoints.GENERATE_CLIENT_TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=self._DEFAULT_TIMEOUT,
            )

            response.raise_for_status()
        except requests.HTTPError as error:
            print(error)
            return None

        response_json = response.json()
        return response_json.get("access_token")

    def get_playlist_items(self, playlist_id: str):
        url = (
            SpotifyEndpoints.SPOTIFY_BASE_URL
            + SpotifyEndpoints.PLAYLIST_ITEMS.replace("{playlist_id}", playlist_id)
        )
        headers = self.base_header

        return self._make_get_request(url=url, headers=headers)

    def find_artist(self, artist_name, offset, limit=50):
        url = SpotifyEndpoints.SPOTIFY_BASE_URL + SpotifyEndpoints.SEARCH
        query = f"?q={artist_name}&type=artist&limit={limit}&offset={offset}&market=BR"

        return self._make_get_request(url=url + query, headers=self.base_header)

    def get_artist_albums(self, artist_id, offset, limit=50):
        url = (
            SpotifyEndpoints.SPOTIFY_BASE_URL
            + SpotifyEndpoints.ARTIST_ALBUMS.replace("{artist_id}", artist_id)
        )
        query = f"?market=BR&limit={limit}&offset={offset}"

        return self._make_get_request(url=url + query, headers=self.base_header)

    def get_albums_tracks(self, album_id, offset, limit=50):
        url = SpotifyEndpoints.SPOTIFY_BASE_URL + SpotifyEndpoints.ALBUM_TRACKS.replace(
            "{album_id}", album_id
        )
        query = f"?market=BR&limit={limit}&offset={offset}"

        return self._make_get_request(url=url + query, headers=self.base_header)
