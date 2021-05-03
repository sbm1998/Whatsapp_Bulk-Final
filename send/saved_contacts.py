from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# import pandas
import time

def send_to_saved(lst,message):
    # Load the chrome driver
    driver = webdriver.Chrome()
    count = 0
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 80)
    for number in lst:
        search_box = '//*[@id="side"]/div[1]/div/label/div/div[2]'
        person_title = wait.until(lambda driver:driver.find_element_by_xpath(search_box))

        # Clear search box if any contact number is written in it
        person_title.clear()

        # Send contact number in search box
        person_title.send_keys(number)
        count = count + 1

        # Wait for 2 seconds to search contact number
        time.sleep(2)

        try:
            # Load error message in case unavailability of contact number
            element = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/span')
        except NoSuchElementException:
            # Format the message from excel sheet
        
            person_title.send_keys(Keys.ENTER)
            actions = ActionChains(driver)
            actions.send_keys(message)
            actions.send_keys(Keys.ENTER)
            actions.perform()
    # Close chrome browser
    driver.quit()
