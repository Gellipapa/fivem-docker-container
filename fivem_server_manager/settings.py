import gettext
import json
from pathlib import Path

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


WORKING_DIR = os.getenv('WORKING_DIR', '.')
SERVER_FOLDER = os.getenv('SERVER_FOLDER', 'FiveM Servers')
DEFAULT_ARTIFACT_VERSION = os.getenv('DEFAULT_ARTIFACT_VERSION', 'recommended')
LANGUAGE = os.getenv('LANGUAGE', 'en')
LOCALE_PATH = os.getenv('LOCALE_PATH', 'locales')


with open(Path(WORKING_DIR) / Path(LOCALE_PATH) / f"{LANGUAGE}.json") as file:
    _locale_lookup = json.load(file)


def _LOCALE(key: str) -> str:
    return _locale_lookup[key]
