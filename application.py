import time
import os
import threading

from constants import *
from dotenv import load_dotenv

from betr_scraper import RaceBuilder
from betfair_api import BetfairAPIController
from betfair_scraper import BetfairRaceScraper

from race import Race, RaceType

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

path = os.environ.get("PATH")
certs_path = os.environ.get("CERTS_PATH")
betfair_username = os.environ.get("USERNAME")
betfair_password = os.environ.get("BETFAIR_PASSWORD")
my_app_key = os.environ.get("MY_APP_KEY")

betfair = BetfairAPIController(certs_path, betfair_username, betfair_password, my_app_key)
betfair.login()

number_of_races = 1
race_builder = RaceBuilder(URL, number_of_races)
races = set()
betfair.keep_alive()

def start_betfair_thread(race, betfair_event):
    scraper = BetfairRaceScraper(path, race.get_betfair_url(), betfair_username, betfair_password)
    if race.get_type() == RaceType.HORSE_RACE and race.get_venue() in AMERICAN_RACES:
            price_method = scraper.get_lay_prices_american
            midpoint_method = scraper.get_prices_american
    elif race.get_type() == RaceType.HORSE_RACE and race.get_venue() not in AMERICAN_RACES:
        price_method = scraper.get_lay_prices_horses
        midpoint_method = scraper.get_prices_horses
    elif race.get_type() == RaceType.TROT_RACE:
        price_method = scraper.get_lay_prices_trots
        midpoint_method = scraper.get_prices_trots
    else:
        price_method = scraper.get_lay_prices_dogs
        midpoint_method = scraper.get_prices_dogs
    while betfair_event.is_set():
        try:
            scraper.refresh()
        except NoSuchElementException:
            print(f"Exiting {scraper.url}")
            betfair_event.clear()
            break

        try:
            prices, volume = price_method()
            race.set_betfair_prices(prices)
            race.set_volume(volume)
            prices, _ = midpoint_method()
            race.set_midpoint_prices(prices)
        except NoSuchElementException:
            print(f"No Such element, closing thread for race {race.get_race_number()} {race.get_venue()}!")
            betfair_event.clear()
            break
            #Close betr and betfair threads if for some reason the betfair scraping fails
    betfair_event.clear()
    scraper.close()
    time.sleep(1)

t_end = time.time() + 60 * 15
while time.time() < t_end:
    if len(races) < number_of_races:
        races_update = race_builder.goto_every_race()
        for race in races_update:
            if race not in races:
                print("Update races", race.get_venue(), race.get_race_number())
                race.set_market_id(betfair.get_market(race))
                if race.get_market_id() == 0:
                    print("Couldn't match market ID")
                    continue
                betfair_event = threading.Event()
                betfair_event.set()
                thread = threading.Thread(target = start_betfair_thread, args = [race, betfair_event])
                thread.start()
                races.add(race)
    time.sleep(30)

race_builder.wd.close()
time.sleep(1)