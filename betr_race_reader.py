from constants import *
from race import Race, RaceType
from dotenv import load_dotenv

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class BetrRaceScraper():
    def __init__(self):
        pass

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

            # Need to handle exceptions as sometimes the races don't have prices? Probably a neater way to do this
            try:
                price = self.wd.find_element(By.XPATH, f"//*[@id='bm-content']/div[2]/div/div[2]/div[2]/div[{number}]/button/div/span[2]")
            except NoSuchElementException:
                # If the element does not exist, skip this race
                break
            
            race_summary[horse_name] = float(price.text)
        return race_summary