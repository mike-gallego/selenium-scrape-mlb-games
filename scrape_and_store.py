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

# The data we want


while True:
    try:
        # Format Date into YYYYMMDD
        date = date.strftime('%Y%m%d')
        print('The date is ', date)

        url = 'https://www.espn.com/mlb/schedule/_/date/{}'.format(date)
        browser.get(url)
        game_links = []
        today_schedule = browser.find_element_by_id('sched-container').find_elements_by_class_name('responsive-table-wrap')[0]
        games = today_schedule.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        for game in games:
            score = game.find_element_by_xpath(".//a[contains(@href, 'mlb/game')]")
            game_links.append(score.get_attribute('href'))

        # Replace part of the URL to have it navigate to the Box Score
        for index, game_link in enumerate(game_links):
            game_links[index] = game_link.replace('game?', 'boxscore?')

        for game_link in game_links:
            browser.get(game_link)
            away = True
            away_batting_average = 0

            home_team = ''
            home_at_bats = 0
            home_runs = 0
            home_hits = 0
            home_rbis = 0
            home_walks = 0
            home_batting_average = 0

            away_team_scrape = browser.find_element_by_class_name('team-info-wrapper').find_elements_by_tag_name('span')[2]
            away_team = away_team_scrape.get_attribute('innerHTML')

            away_totals_scrape = browser.find_elements_by_class_name('totals')[0].find_elements_by_tag_name('td')[2:7]
            away_at_bats = away_totals_scrape[0].get_attribute('innerHTML')
            away_runs = away_totals_scrape[1].get_attribute('innerHTML')
            away_hits = away_totals_scrape[2].get_attribute('innerHTML')
            away_rbis = away_totals_scrape[3].get_attribute('innerHTML')
            away_walks = away_totals_scrape[4].get_attribute('innerHTML')

            print('The away team is {}, with {} at bats, {} runs, {} hits, {} rbis and {} walks'.format(away_team, away_at_bats, away_runs, away_hits, away_rbis, away_walks))




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
