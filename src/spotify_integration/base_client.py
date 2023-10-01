import requests 
import time

from abc import ABC, abstractmethod
from typing import Dict

class BaseClient:
    _DEFAULT_TIMEOUT = 3
    __MAX_RETRIES = 4

    @abstractmethod
    def _reset_auth_token(self):
        pass

    def _make_get_request(self, *, url: str, headers: Dict):
        retry_attempts = 0
        
        while retry_attempts < self.__MAX_RETRIES:
            try:
                response = requests.get(url=url, headers=headers, timeout=self._DEFAULT_TIMEOUT)
                response.raise_for_status()

                return response.json()
            except requests.HTTPError as error:
                print(error)
                if error.response.status_code not in [401, 403]:
                    time.sleep(1)
                    break
                else:
                    self._reset_auth_token()
                    retry_attempts = 0

                retry_attempts += 1
            except Exception as error:
                print(error)
                retry_attempts += 1
        
        return None
