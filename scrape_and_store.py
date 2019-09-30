import sys
import requests
import datetime
from datetime import timedelta
from selenium import webdriver

# Start browser
path_to_chromedriver = 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

# Start date
date = datetime.datetime(2019, 3, 20)

while True:
    try:
        # Format Date into YYYYMMDD
        date = date.strftime('%Y%m%d')
        print('The date is ', date)

        url = 'https://www.espn.com/mlb/schedule/_/date/{}'.format(date)
        browser.get(url)
        hrefs = []
        today_schedule = browser.find_element_by_id('sched-container').find_elements_by_class_name('responsive-table-wrap')[0]
        games = today_schedule.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        for game in games:
            score = game.find_element_by_xpath(".//a[contains(@href, 'mlb/game')]")
            hrefs.append(score.get_attribute('href'))

        # Replace part of the URL to have it navigate to the Box Score
        for index, href in enumerate(hrefs):
            hrefs[index] = href.replace('game?', 'boxscore?')

        for href in hrefs:
            browser.get(href)



        # Increment Date
        date = datetime.datetime.strptime(date, '%Y%m%d')
        date = date + timedelta(days=1)

        # Condition to check schedule has reached season limit
        if date > datetime.datetime(2019, 4, 29):
            print('data limit reached')
            break
    except requests.exceptions.Timeout:
        continue
    except requests.exceptions.HTTPError as err:
        # Format Date into YYYYMMDD
        date = datetime.datetime.strptime(date, '%Y%m%d')
        date = date + timedelta(days=1)
        print('Web page unavailable...\nIncrementing one day\n', date)
        continue
    except requests.exceptions.RequestException as e:
        sys.exit(1)
