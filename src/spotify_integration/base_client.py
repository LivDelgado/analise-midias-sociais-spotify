import datetime
import time
from abc import ABC, abstractmethod
from typing import Dict

import requests


class BaseClient:
    _DEFAULT_TIMEOUT = 3
    __MAX_RETRIES = 4

    def __init__(self):
        self._first_request_time = None

    def __reset_first_request_time(self):
        self._first_request_time = datetime.datetime.utcnow()

    def __should_refresh_token(self):
        return (
            not self._first_request_time or
            datetime.datetime.utcnow() - self._first_request_time > datetime.timedelta(minutes=10)
        )

    @abstractmethod
    def _reset_auth_token(self):
        pass

    def _make_get_request(self, *, url: str, headers: Dict):
        if self.__should_refresh_token():
            self._reset_auth_token()
            self.__reset_first_request_time()

        retry_attempts = 0

        while retry_attempts < self.__MAX_RETRIES:
            try:
                response = requests.get(
                    url=url, headers=headers, timeout=self._DEFAULT_TIMEOUT
                )
                response.raise_for_status()

                return response.json()
            except requests.HTTPError as error:
                retry_attempts += 1

                print(error)
                if error.response.status_code not in [401, 403]:
                    time.sleep(1)
                    break
                else:
                    time.sleep(60)
                    self._reset_auth_token()

                    if retry_attempts == self.__MAX_RETRIES:
                        raise KeyboardInterrupt

            except Exception as error:
                print(error)
                retry_attempts += 1

        return None
