"""Configuration for tvdb api"""
import os

from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=False)


class Config:
    user_name = os.getenv("TVDB_USER_NAME")
    user_key = os.getenv("TVDB_USER_KEY")
    api_key = os.getenv("TVDB_API_KEY")
