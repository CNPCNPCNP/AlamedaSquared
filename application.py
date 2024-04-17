import time
import os

from constants import *
from dotenv import load_dotenv

from betr_scraper import RaceBuilder
from betfair_api import BetfairAPIController
from race import Race, RaceType

path = os.environ.get("PATH")
certs_path = os.environ.get("CERTS_PATH")
my_username = os.environ.get("MY_USERNAME")
my_password = os.environ.get("MY_PASSWORD")
my_app_key = os.environ.get("MY_APP_KEY")

betfair = BetfairAPIController(certs_path, my_username, my_password, my_app_key)
betfair.login()

number_of_races = 5
race_builder = RaceBuilder(URL, number_of_races)

betfair.keep_alive()
races_update = race_builder.goto_every_race()

race_builder.wd.close()
time.sleep(1)

for race in races_update:
    print(race)