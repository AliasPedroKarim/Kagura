# -*- encoding:utf-8 -*-
# settings.py

import os
import sys
from pprint import pprint

from dotenv import load_dotenv, get_key, find_dotenv, dotenv_values

load_dotenv(encoding=sys.getfilesystemencoding())

token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("PREFIX")

MONOGO_HOST = os.getenv("MONOGO_HOST", "localhost")
MONOGO_PORT = os.getenv("MONOGO_PORT", "27017")
MONOGO_USERNAME = os.getenv("MONOGO_USERNAME")
MONOGO_PASS = os.getenv("MONOGO_PASS")
MONOGO_DB_NAME = os.getenv("MONOGO_DB_NAME")
MONOGO_DB_AUTH = os.getenv("MONOGO_DB_AUTH")

DISCORD_TOKEN_RANDOM = os.getenv("DISCORD_TOKEN_RANDOM")
