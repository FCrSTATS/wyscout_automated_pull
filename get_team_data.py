
## Library Setup
import pandas as pd
import numpy as np
import os
import time, sys
from glob import glob


## Selenium Packages
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

## Functions

def wait_for_page_id(wait_for_id, browser, delay = 3):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, wait_for_id)))
        print(wait_for_id + " found and page ready")
    except TimeoutException:
        print("**** Page Load Error ****")


def wait_for_page_class(wait_for_class, browser, delay = 3):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, wait_for_class)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")



    USER_EMAIL = "YOUR_EMAIL"
    PASSWORD = "YOUR_PASSWORD"

## RUN TIME
if __name__ == "__main__":


    # Top Tier
    print(sys.argv[1])

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "PATH_OF_WHERE_YOU_WANT_DOWNLOADS"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "path/to/chromedriver.exe"
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)


    browser.get("https://platform.wyscout.com/app/?")

    ## 3. Login in to the platform
    wait_for_page_id("login_password", browser) # wait for login page to load
    browser.find_element_by_name("username").send_keys(USER_EMAIL)
    browser.find_element_by_id("login_password").send_keys(PASSWORD)
    browser.find_element_by_id("login_button").click()
    wait_for_page_id("current-app-title", browser) # wait for platform page to load

    ## TO-DO - fix Finland and add it to all_countries

    countries =  sys.argv[1].split(",")

    for z in countries:

        ## 4. Select the country to click
        countries_list = [l.text for l in browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model area')]")]

        country_select = z
        # tier_select = tier_select[z]

        country_index_to_click = countries_list.index(country_select)
        browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model area')]")[country_index_to_click].click()
        print(country_select + " clicked")
        time.sleep(1)

        ## 5. Select the competition to click
        wait_for_page_id('detail_0_competition_navy_label', browser) # check if loaded
        time.sleep(1)
        competitions_list = [l.text for l in browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model competition')]")]
        browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model competition')]")[0].click()
        # print(competitions_list[0] + " clicked")
        time.sleep(1)

        ## 6. Select the Club and Download Team Stats

        club_links_index = list(range(len(browser.find_elements_by_xpath("//*[(@id = 'detail_0_competition_navy_0')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'title', ' ' ))]"))))

        for c in club_links_index:

            browser.find_elements_by_xpath("//*[(@id = 'detail_0_competition_navy_0')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'title', ' ' ))]")[c].click()
            time.sleep(2)

            club = browser.find_elements_by_id('detail_0_team_name')[0].text
            file_name = "data_download/teams/" + club.replace("/", "").replace(" ", "_").lower() + "__teamdata.xlsx"

            if file_name not in glob("data_download/teams/*.xlsx"):

                player_page_tabs = [l.text for l in browser.find_elements_by_xpath("//a[contains(@class, 'gears-button-inner size-normal button-standard')]")]
                player_page_tabs_to_click = player_page_tabs.index("Stats")
                browser.find_elements_by_xpath("//a[contains(@class, 'gears-button-inner size-normal button-standard')]")[player_page_tabs_to_click].click()

                browser.find_element_by_class_name("OpponentsToggler__thumb___3Syh1").click()
                time.sleep(1)

                browser.find_elements_by_class_name("Select-arrow")[2].click()
                time.sleep(2)

                browser.find_elements_by_class_name("Select-menu-outer")[0].find_elements_by_tag_name('div')[5].click()

                time.sleep(4)
                browser.find_element_by_class_name("Export__export___3pgAH").click()
                time.sleep(3)

                for i in glob("data_download/teams/*.xlsx"):
                    if "Team Stats" in i:
                        os.rename(i, file_name)

                print(file_name + " downloaded")

                browser.execute_script("window.history.go(-1)")
            else:
                print(club + " already processed")
                browser.execute_script("window.history.go(-1)")



        browser.execute_script("window.history.go(-1)")
        time.sleep(2)
        browser.execute_script("window.history.go(-1)")
        time.sleep(2)

        print(country_select + " pull complete")

        countries2 =  sys.argv[2].split(",")
        time.sleep(2)

    for z in countries2:

        ## 4. Select the country to click
        countries_list = [l.text for l in browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model area')]")]

        country_select = z
        # tier_select = tier_select[z]

        country_index_to_click = countries_list.index(country_select)
        browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model area')]")[country_index_to_click].click()
        print(country_select + " clicked")
        time.sleep(1)

        ## 5. Select the competition to click
        wait_for_page_id('detail_0_competition_navy_label', browser) # check if loaded
        time.sleep(1)
        competitions_list = [l.text for l in browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model competition')]")]
        browser.find_elements_by_xpath("//div[contains(@class, 'gears-list-item aengine-model competition')]")[1].click()
        # print(competitions_list[0] + " clicked")
        time.sleep(1)

        ## 6. Select the Club and Download Team Stats

        club_links_index = list(range(len(browser.find_elements_by_xpath("//*[(@id = 'detail_0_competition_navy_0')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'title', ' ' ))]"))))

        for c in club_links_index:

            browser.find_elements_by_xpath("//*[(@id = 'detail_0_competition_navy_0')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'title', ' ' ))]")[c].click()
            time.sleep(2)

            club = browser.find_elements_by_id('detail_0_team_name')[0].text
            file_name = "data_download/teams/" + club.replace("/", "").replace(" ", "_").lower() + "__teamdata.xlsx"

            if file_name not in glob("data_download/teams/*.xlsx"):

                player_page_tabs = [l.text for l in browser.find_elements_by_xpath("//a[contains(@class, 'gears-button-inner size-normal button-standard')]")]
                player_page_tabs_to_click = player_page_tabs.index("Stats")
                browser.find_elements_by_xpath("//a[contains(@class, 'gears-button-inner size-normal button-standard')]")[player_page_tabs_to_click].click()

                browser.find_element_by_class_name("OpponentsToggler__thumb___3Syh1").click()
                time.sleep(1)

                browser.find_elements_by_class_name("Select-arrow")[2].click()
                time.sleep(2)

                browser.find_elements_by_class_name("Select-menu-outer")[0].find_elements_by_tag_name('div')[5].click()

                time.sleep(4)
                browser.find_element_by_class_name("Export__export___3pgAH").click()
                time.sleep(3)

                for i in glob("data_download/teams/*.xlsx"):
                    if "Team Stats" in i:
                        os.rename(i, file_name)

                print(file_name + " downloaded")

                browser.execute_script("window.history.go(-1)")
            else:
                print(club + " already processed")
                browser.execute_script("window.history.go(-1)")



        browser.execute_script("window.history.go(-1)")
        time.sleep(2)
        browser.execute_script("window.history.go(-1)")
        time.sleep(2)

        print(country_select + " pull complete")


    # 2nd Tier
