# client-for-tvdb

[![CI](https://github.com/opacam/client-for-tvdb/workflows/CI/badge.svg?branch=master)](https://github.com/opacam/client-for-tvdb/actions)
[![codecov](https://codecov.io/gh/opacam/client-for-tvdb/branch/master/graph/badge.svg)](https://codecov.io/gh/opacam/client-for-tvdb)
[![Python versions](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/release/opacam/client-for-tvdb.svg)](https://gitHub.com/opacam/client-for-tvdb/releases/)
[![GitHub tag](https://img.shields.io/github/tag/opacam/client-for-tvdb.svg)](https://gitHub.com/opacam/client-for-tvdb/tags/)
[![GitHub license](https://img.shields.io/github/license/opacam/client-for-tvdb.svg)](https://github.com/opacam/client-for-tvdb/blob/master/LICENSE.md)


A simple client for the [Tvdb API v3](https://api.thetvdb.com/swagger).

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

#### Tvdb Account

You will need an API key from TVDb.com to access the client. To obtain a
key, follow these steps:

- 1. [Register](https://thetvdb.com/auth/register) for and verify an account.
- 2. [Log into](https://thetvdb.com/auth/login) your account.
- 3. [Fill your details](https://thetvdb.com/dashboard/account/apikey/create) to generate a new API key.

#### Python Installation (recommended to use a virtual env)

You also need python >= 3.6 up and running. If your OS does not have the
appropriate python version, you could install [pyenv](https://github.com/pyenv/pyenv) 
and create a virtual environment with the proper python version. Also you will
need an up to date pip installation (version `20.0.2` or greater is our
recommendation). So once you have `pyenv` installed
(see [pyenv install instructions](https://github.com/pyenv/pyenv#installation)), 
make an virtual environment for the project (we will use python version 3.8):

```
pyenv virtualenv 3.8.1 client-for-tvdb
```

Enter inside the python environment we recently created (`client-for-tvdb`):
```
pyenv activate client-for-tvdb
```

Upgrade `pip` package:
```
pip install --upgrade pip
```

Install `poetry` package:
```
pip install poetry
```

### Installing

Once you have the prerequisites installed, you can proceed installing the
project. The project uses an `pyproject.toml` file to manage the installation
(PEP517) and also we will make use of the python package
[poetry](https://github.com/python-poetry/poetry) as our `build-system`
(PEP518). So, to do the install you only need to `cd` to the
project folder:

```
cd client-for-tvdb
```

And run the install of the dependencies via `poetry` command:

```
poetry install
```


## Running API client

To use this tvdb API client, first you must initialize the client with
the proper credentials:

```python
from client_for_tvdb import TvdbClient

tvdb_client = TvdbClient(
    user_name="Your user name",
    user_key="Your user key",
    api_key="Your API key"
)
```

Also you could setup your credentials via environment variables, wrote
in `.env` file which should be located inside the `client_for_tvdb`
module (or you could `export` them):
```
TVDB_USER_NAME=<Your user name>
TVDB_USER_KEY=<Your user key>
TVDB_API_KEY=<Your API key>
```

You can perform the following queries, assuming that you have setup your
credentials via `.env` file:

- To get a list of possible matching tvshows:
  ```python
  from client_for_tvdb import TvdbClient

  tvdb_client = TvdbClient()
  # get a list of dictionaries with tvshows from the TVDB API
  search_result = tvdb_client.search("Game of Thrones")
  ```

- To get only the closest matching tvshow:
  ```python
  from client_for_tvdb import TvdbClient

  tvdb_client = TvdbClient()
  # will return a dictionary
  search_result = tvdb_client.search_closest_matching("Game of Thrones")
  ```

- You also could perform a query supplying a `tvdb_id`
  ```python
  from client_for_tvdb import TvdbClient

  tvdb_client = TvdbClient()
  # will return a dictionary
  search_result = tvdb_client.get_serie_by_id(121361)
  ```

## Running the tests

To run our project tests you can use `pytest` with coverage:

```
PYTHONPATH=. pytest tests/ --cov client_for_tvdb/
```

## Built With

* [Python 3](https://docs.python.org/3/) - The programming language
* [Poetry](https://python-poetry.org/docs/) - Dependency Management

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.

## Versioning

We use [CalVer](https://calver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/opacam/client-for-tvdb/tags).


## Authors

* **Pol Canelles** - *Initial work* - [opacam](https://github.com/opacam)

See also the list of [contributors](https://github.com/opacam/client-for-tvdb/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Tvdb API docs](https://api.thetvdb.com/swagger)
