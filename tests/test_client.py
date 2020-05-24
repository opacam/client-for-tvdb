import json
import os
import pytest
import requests_mock

from pathlib import Path

from client_for_tvdb import client
from client_for_tvdb.config import Config
from client_for_tvdb.end_points import end_points
from client_for_tvdb.exceptions import TvdbClientException

# Disable sqlite cache file
os.environ["TESTING_CLIENT_FOR_TVDB"] = "1"

fake_user_name = "tvdb_user_name"
fake_user_key = "tvdb_user_key"
fake_api_key = "tvdb_api_key"

json_with_token = {"token": "a valid tvdb token"}
json_with_new_token = {"token": "a new valid tvdb token"}

test_files_path = Path(Path(__file__).parent, "files")
json_search_file = Path(test_files_path, "search_result.json")
with open(json_search_file) as output_file:
    json_search_result = json.load(output_file)

simulated_tvdb_result = {
    'aliases': [
        'Game of Thrones - Das Lied von Eis und Feuer',
        'Le Trône de fer',
        '权力的游戏',
        '冰与火之歌 第四季',
        '權力遊戲'
    ],
    'banner': '/banners/graphical/121361-g19.jpg',
    'firstAired': '2010-12-5',
    'id': 121361,
    'image': '/banners/posters/121361-4.jpg',
    'network': 'HBO',
    'overview':
        'Seven noble families fight for control of the mythical land of '
        'Westeros. Friction between the houses leads to full-scale war. '
        'All while a very ancient evil awakens in the farthest north. '
        'Amidst the war, a neglected military order of misfits, the '
        "Night's Watch, is all that stands between the realms of men and "
        'the icy horrors beyond.',
    'poster': '/banners/posters/121361-4.jpg',
    'seriesName': 'Game of Thrones',
    'slug': 'game-of-thrones',
    'status': 'Ended'
}


@pytest.fixture
def mock_config_credentials(monkeypatch):
    monkeypatch.setattr(Config, "user_name", fake_user_name)
    monkeypatch.setattr(Config, "user_key", fake_user_key)
    monkeypatch.setattr(Config, "api_key", fake_api_key)


@pytest.fixture
def mock_config_missing_api(monkeypatch):
    monkeypatch.setattr(Config, "api_key", "")


@pytest.fixture
def mock_tvdb_login(mock_config_credentials):
    with requests_mock.Mocker() as mocked:
        mocked.post(end_points.login, json=json_with_token, status_code=200)
        yield mocked


def test_tvdb_client_login_success(mock_config_credentials):
    # test a straight forward login
    with requests_mock.Mocker() as m:
        m.post(end_points.login, json=json_with_token, status_code=200)
        tvdb_client = client.TvdbClient()
    assert isinstance(tvdb_client, client.TvdbClient) is True
    assert tvdb_client.token == json_with_token["token"]


def test_tvdb_client_login_after_token_refresh(mock_config_credentials):
    # test a login which requires refresh_token
    with requests_mock.Mocker() as m:
        m.post(end_points.login, json=json_with_token, status_code=401)
        m.get(
            end_points.refresh_token,
            json=json_with_new_token,
            status_code=200,
        )
        tvdb_client = client.TvdbClient()
    assert tvdb_client.token == json_with_new_token["token"]


def test_tvdb_client_login_missing_api(mock_config_missing_api):
    with pytest.raises(TvdbClientException) as tvdb_exc:
        client.TvdbClient()
    assert client.CONFIGURE_YOUR_CREDENTIALS_ERROR_MESSAGE in str(
        tvdb_exc.value
    )
    assert client.CONFIGURE_CREDENTIALS_INSTRUCTIONS_MESSAGE in str(
        tvdb_exc.value
    )


def test_tvdb_client_refresh_token(mock_tvdb_login):
    tvdb_client = client.TvdbClient()
    with requests_mock.Mocker() as m:
        m.get(
            end_points.refresh_token,
            json=json_with_new_token,
            status_code=200,
        )
        tvdb_client.refresh_token()
    assert tvdb_client.token == json_with_new_token["token"]

    # test refresh_token error (which should return an status code)
    with requests_mock.Mocker() as m:
        m.get(end_points.refresh_token, status_code=401)
        error_code = tvdb_client.refresh_token()
    assert error_code == 401


def test_tvdb_client_search(mock_tvdb_login):
    tvdb_client = client.TvdbClient()
    with requests_mock.Mocker() as m:
        m.get(
            f"{end_points.search}?name=Game+of+Thrones",
            json=json_search_result,
            status_code=200,
        )
        listed_results = tvdb_client.search("Game of Thrones")
    assert isinstance(listed_results, list) is True
    assert len(listed_results) == 5
    for item in listed_results:
        assert isinstance(item, dict) is True


def test_tvdb_client_search_error(mock_tvdb_login):
    tvdb_client = client.TvdbClient()
    with requests_mock.Mocker() as m:
        m.get(
            f"{end_points.search}?name=Game+of+Thrones",
            status_code=404,
        )
        listed_results = tvdb_client.search("Game of Thrones")
    assert listed_results is None


def test_tvdb_client_search_closest_matching(mock_tvdb_login):
    tvdb_client = client.TvdbClient()
    with requests_mock.Mocker() as mock_search:
        mock_search.get(
            f"{end_points.search}?name=Game+of+Thrones",
            json=json_search_result,
            status_code=200,
        )
        data_dict = tvdb_client.search_closest_matching("Game of Thrones")
    for k, v in data_dict.items():
        assert v == simulated_tvdb_result[k]


def test_tvdb_client_get_serie_by_id(mock_tvdb_login):
    tvdb_client = client.TvdbClient()
    serie_id = 121361

    with requests_mock.Mocker() as mock_get_id:
        mock_get_id.get(
            f"{end_points.series}/{serie_id}",
            json={"data": simulated_tvdb_result},
            status_code=200,
        )
        serie_data = tvdb_client.get_serie_by_id(serie_id)
    for k, v in serie_data.items():
        assert v == simulated_tvdb_result[k]
