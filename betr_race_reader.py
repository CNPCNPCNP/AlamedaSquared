import re
import string
import time

from constants import *
from race import Race, RaceType
from dotenv import load_dotenv

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class BetrRaceScraper():
    def __init__(self, race, betr_username, betr_password):
        uc_options = uc.ChromeOptions()
        uc_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
                
        self.wd = uc.Chrome(options = uc_options)
        self.wd.maximize_window() # For maximizing window
        self.wd.implicitly_wait(10) # gives an implicit wait for 10 seconds
        self.url = race.get_url()
        self.race = race
        self.login(self.url, betr_username, betr_password)

    def login(self, url, username, password):
        try:
            self.wd.get(url)
            login_button = self.wd.find_element(By.XPATH, '//*[@id="bm-root"]/div[3]/header/div/div[2]/button[1]')
            login_button.click_safe()

            self.username = self.wd.find_element(By.XPATH, '//*[@id="Username"]')
            self.password = self.wd.find_element(By.XPATH, '//*[@id="Password"]')
            button = self.wd.find_element(By.XPATH, '//*[@id="floating-ui-root"]/div/div/div/div[2]/div[2]/form/div[3]/div/button')
            self.username.send_keys(username)
            self.password.send_keys(password)
            button.click_safe()
            time.sleep(3)
            self.wd.get(url)
            time.sleep(3)
        except NoSuchElementException:
            self.login(url, username, password)

    """
    Starting with the webdriver on a race page, creates a dictionary of every horse name and its current starting price
    """
    def get_prices_from_race_page(self) -> Race:
        horses = self.wd.find_elements(By.CLASS_NAME, "RunnerDetails_competitorName__UZ66s")
        prices = self.wd.find_elements(By.CLASS_NAME, "OddsButton_info__5qV64")

        race_summary = {}

        # Shrink horse list to match number of prices to account for scratched horses
        if len(prices) <= 4:
            horses = horses[:len(prices)]
        else:
            horses = horses[:len(prices) // 2]
        
        for index, horse in enumerate(horses):
            # Split the text into the horses number and the rest of the text on the first space
            horse_number, remainder = horse.text.split(" ", 1)
            # Split once from the right to get gate separate from horse name. This avoids edge case where there are 
            # spaces in the horses name
            horse_name, gate = remainder.rsplit(" ", 1)
            horse_name = horse_name.translate(str.maketrans('', '', string.punctuation)) # Remove punctuation from horse names
            gate = int(gate[1:-1]) #Remove brackets from gate

            # Get current price of horse. The div number seems to be separated by 6 each time starting from 4
            number = index * 6 + 4
            
            price = self.wd.find_element(By.XPATH, f'//*[@id="bm-content"]/div[2]/div/div/div[2]/div[2]/div[{number}]/button').text
            price = re.sub('[^0-9,.]', '', price)
            race_summary[horse_name] = float(price)
        return race_summary

    def close(self) -> None:
        self.wd.close()