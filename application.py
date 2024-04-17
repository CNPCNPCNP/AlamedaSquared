import time
import os

from constants import *
from dotenv import load_dotenv

from race import Race, RaceType
from betfair_api import BetfairAPIController

PATH = os.environ.get("PATH")
certs_path = os.environ.get("CERTS_PATH")
my_username = os.environ.get("MY_USERNAME")
my_password = os.environ.get("MY_PASSWORD")
my_app_key = os.environ.get("MY_APP_KEY")


