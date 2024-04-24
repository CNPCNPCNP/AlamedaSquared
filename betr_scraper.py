import string

from constants import *
from race import Race, RaceType
from dotenv import load_dotenv

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
"""
Main controller class for building our list of races
"""
class RaceBuilder():

    """
    Creates a browser controller with the associated webdriver and URL path. Use self.wd inside this class to access 
    webdriver. If you need to  access the webdriver outside this class, use the getter method get_webdriver. Uses 
    betfair controller to get the market id and betfair url for each race as well. Races specifies the number of 
    races to track. Tracking more races uses more threads
    """
    def __init__(self, url: str, races: int) -> None:
        uc_options = uc.ChromeOptions()
        uc_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
                
        self.wd = uc.Chrome(options = uc_options)
        self.wd.maximize_window() # For maximizing window
        self.wd.implicitly_wait(3) # gives an implicit wait for 2 seconds
        self.wd.get(url)

        self.url = url
        self.races = races

    """
    Creates a list of every upcoming race from the upcoming races page on BETR. Hopefully classname doesn't change a lot 
    or this will be a bad way to do it
    """
    def get_all_upcoming_races(self) -> list:
        races = self.wd.find_elements(By.CLASS_NAME, "RaceUpcoming_row__rS63w")
        return races

    """
    Goes to every race on the upcoming races page and then returns a list of Races and their details
    """
    def goto_every_race(self) -> list[Race]:
        self.wd.implicitly_wait(1)
        races_number = len(self.get_all_upcoming_races()) - 1
        races = []  
        index = 0
        # Had issues with trying to iterate over list normally with for loop, so reload the race list every time and 
        # access each race by index. Inefficient but it works fine. Only scraping 5 races at this stage, may scrape more
        # if this approach is successful.
        while len(races) < self.races and index < races_number:
            races_links = self.get_all_upcoming_races()
            race = races_links[index]
            race.click_safe()
            try:
                race = self.get_race_details()
                if race.valid_race():
                    races.append(race)
            except Exception as ex:
                print("Exception when getting race details. Skipping race")
                print(ex)
            self.wd.back()
            index += 1
        return races
    
    """
    Starting with the webdriver on a race page, collects all the key details about a race such as the venue, race type,
    race number and url
    """
    def get_race_details(self) -> Race:
        # Race name is location + race number
        try:
            venue = self.wd.find_element(By.XPATH, '//*[@id="bm-content"]/div[2]/div/div/div[1]/ul/li[2]/a').text
            venue = VENUES.get(venue) # Gives us None if no equivalent venue on betfair
        except NoSuchElementException:
            print("Unable to determine venue")

        try:
            race_number = int(self.wd.find_element(By.XPATH, '//*[@id="bm-content"]/div[2]/div/div/div[1]/ul/li[3]/a').text.split(" ")[-1])
        except NoSuchElementException:
            print("Unable to determine race number")
            race_number = 0 # Use sentinel value of 0 for races where we can't determine number, will skip matching later
        except ValueError:
            print("Found wrong value for race number?")
            race_number = 0

        # Get url so we can access the race later to bet
        url = self.wd.current_url

        # Can extract SVG (icon) to get type of race. Annoyingly no text on page stating race type so this method is 
        # overly complex
        try:
            race_icon = self.wd.find_element(By.CSS_SELECTOR, CSS_SELECTOR).get_attribute('d').split(" ", 1)[0]
            if race_icon == HORSE_ICON:
                race_type = RaceType.HORSE_RACE
            elif race_icon == TROT_ICON:
                race_type = RaceType.TROT_RACE
            else:
                race_type = RaceType.GREYHOUND_RACE
        except NoSuchElementException:
            race_icon = None
            race_type = RaceType.UNKNOWN_RACE
            print('Unknown icon')
        return Race(venue, race_number, url, race_type)