import json
import logging
import os
import requests
import requests_cache

from difflib import get_close_matches
from typing import Union

from client_for_tvdb.config import Config
from client_for_tvdb.end_points import end_points
from client_for_tvdb.exceptions import TvdbClientException

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("tvdb")

requests_cache_name = "tvdb_api_cache"

CONFIGURE_YOUR_CREDENTIALS_ERROR_MESSAGE = (
    "TvdbClient couldn't be started due to wrong credentials. Please, review "
    "your settings and configure it properly."
)

CONFIGURE_CREDENTIALS_INSTRUCTIONS_MESSAGE = (
    "You will need an API key from `TVDb.com` to access the client. Please, "
    "Follow the instructions from: "
    "https://github.com/opacam/client-for-tvdb#tvdb-account"
)


class TvdbClient:
    token = None

    def __init__(
            self, user_name: str = "", user_key: str = "", api_key: str = "",
    ) -> None:
        """
        Initialize the tvdb client by setting user credentials, requests
        cached session and tries to login the user account with the supplied
        credentials.
        """
        self.user_name = user_name or Config.user_name
        self.user_key = user_key or Config.user_key
        self.api_key = api_key or Config.api_key
        print(f"self.username is: {self.user_name}")

        self.session = requests_cache.CachedSession(
            # cache will expire after 6 hours
            expire_after=21600,
            backend="sqlite"
            if "TESTING_CLIENT_FOR_TVDB" not in os.environ
            else "memory",
            cache_name=requests_cache_name,
            include_get_headers=True,
        )
        self.session.remove_expired_responses()

        if self.user_name and self.user_key and self.api_key:
            self.login()
        else:
            raise TvdbClientException(
                CONFIGURE_YOUR_CREDENTIALS_ERROR_MESSAGE,
                instructions=CONFIGURE_CREDENTIALS_INSTRUCTIONS_MESSAGE,
            )

    @property
    def session_headers(self) -> dict:
        """Returns a generic headers for perform our tvdb api queries."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Todo: make language dynamic
            "Accept-Language": "en",
        }
        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})
        return headers

    @property
    def user_params(self) -> dict:
        """Returns a dict with the user credentials."""
        params = {"apikey": self.api_key}
        if self.user_key and self.user_key:
            params.update({
                "userkey": self.user_key, "username": self.user_name,
            })
        return params

    def _post(self, endpoint: str) -> requests.Response:
        """Generic `requests.post` calls."""
        response = self.session.post(
            endpoint, headers=self.session_headers, json=self.user_params,
        )
        return response

    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        """Generic `requests.get` calls."""
        response = self.session.get(
            endpoint, headers=self.session_headers, params=params,
        )
        return response

    def login(self) -> Union[str, None]:
        """
        Login into tvdb account but in case that the login fails we will try
        to refresh the token before giving up.
        """
        log.info(f"Login to tvdb api with user: {self.user_name}")
        response = self._post(end_points.login)
        if response.status_code == 200:
            self.token = json.loads(response.content)["token"]
        elif response.status_code == 401:
            log.error("Cannot login into  account, trying to refresh token...")
            response_code = self.refresh_token()
            if response_code == 200:
                log.info("Ok refreshed token.")
            elif response_code == 401:
                log.error("Seems that your JWT token is missing or expired.")
            else:
                log.error("Invalid credentials and/or API token.")
        else:
            log.error(f"Error when trying to login: {response.content}")
        return self.token

    def refresh_token(self) -> int:
        """
        Refresh the current token set in the module. Returns the the status
        code of the response.
        """
        response = self._get(end_points.refresh_token, params=self.user_params)

        if response.status_code == 200:
            self.token = json.loads(response.content)["token"]
        else:
            log.error(f"Error while refreshing token: {response.content}")
        return response.status_code

    def search(self, name: str) -> Union[list, None]:
        """Given a series name, return a list of possible series."""
        response = self._get(end_points.search, params={"name": name})
        if response.status_code == 200:
            return json.loads(response.content)["data"]
        log.error(f"Error while searching series by name: {response.content}")
        return None

    def search_closest_matching(self, name: str) -> Union[dict, None]:
        """
        Given a series name, search all possible series and return the closest
        matching serie in a dict format.
        """
        series = self.search(name)
        if series is None:
            return None

        # Tries to get the closest matching series
        names = [i["seriesName"] for i in series if i["seriesName"]]
        res = get_close_matches(name, names, n=len(series))
        for serie in series:
            if res and serie["seriesName"] == res[0]:
                log.info(
                    " closest result for tvdb search is: {}".format(
                        serie["seriesName"]
                    )
                )
                return serie

        # we didn't find the closest match, so we take the first result
        return series[0]

    def get_serie_by_id(self, serie_id: int) -> Union[dict, None]:
        """Given a series name, return a list of possible series."""
        response = self._get(f"{end_points.series}/{serie_id}")
        if response.status_code == 200:
            return json.loads(response.content)["data"]
        log.error(f"Error while searching series by name: {response.content}")
        return None
