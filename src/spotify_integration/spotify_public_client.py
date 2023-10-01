import os
import json
try:
    import requests
    import random
    import httpx
    import datetime

except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install random")
    os.system("pip install httpx")
    os.system("pip install datetime")

from datetime import datetime

from spotify_integration.spotify_endpoints import SpotifyEndpoints

class SpotifyPublicClient:
    def __init__(self) -> None:
        self.client_id, self.auth = self.get_auth()
        self.session = self.get_session()
        self.token = self.get_client_token()
        self.csrf = self.get_csrf()

    def get_current_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        return current_time


    def get_session(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
        }
        session = httpx.Client(headers=headers, timeout=3600)
        return session


    def get_client_token(self):
        payload = {
            "client_data": {
                "client_id": self.client_id,
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
                headers=headers  
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

    def get_auth(self):
        self.session = self.get_session()
        try:
            headers = {
                "Authority": "authority",
                "Accept": "application/json"
            }

            params = {
                "reason": "transport",
                "productType": "web-player"
            }

            response = self.session.get(
                url=SpotifyEndpoints.GENERATE_AUTH_URL,
                headers=headers,
                params=params
            )
            if response.status_code == 200:
                current_time = self.get_current_time()

                return response.json().get("clientId"), response.json().get("accessToken")
            else:
                pass
        except requests.exceptions.RequestException as e:
            pass

    # Não está sendo udado por enquanto, mas vai que precisa
    def get_csrf(self):
        self.session = self.get_session()
        headers = {
            "Host": "www.spotify.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        } 
        current_time = self.get_current_time()
        response = self.session.get(url=SpotifyEndpoints.CSRF_URL, headers=headers)
        if response.status_code == 200:
            return response.text.split("csrfToken")[1].split('"')[2]
        else:
            pass
