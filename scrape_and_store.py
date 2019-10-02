import sys
import requests
import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.common.exceptions import *

# Start browser
path_to_chromedriver = 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

# Start date
date = datetime.datetime(2019, 3, 30)

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
        score = []
        for game in games:
            try:
                score = game.find_element_by_xpath(".//a[contains(@href, 'mlb/game')]")
                if not score.get_attribute('innerHTML') == 'Postponed':
                    game_links.append(score.get_attribute('href'))
            except NoSuchElementException:
                browser.refresh()
                print('No games were found')



        # Replace part of the URL to have it navigate to the Box Score
        for index, game_link in enumerate(game_links):
            game_links[index] = game_link.replace('game?', 'boxscore?')

        for game_link in game_links:
            try:
                browser.get(game_link)

                away = True

                away_batting_average = 0.0
                away_on_base_percentage = 0.0
                away_slug_percentage = 0.0

                home_batting_average = 0.0
                home_on_base_percentage = 0.0
                home_slug_percentage = 0.0

                away_team_scrape = browser.find_elements_by_class_name('team__content')[0].find_element_by_class_name('abbrev')
                away_team = away_team_scrape.get_attribute('innerHTML')

                home_team_scrape = browser.find_elements_by_class_name('team__content')[1].find_element_by_class_name('abbrev')
                home_team = home_team_scrape.get_attribute('innerHTML')

                away_totals_scrape = browser.find_elements_by_class_name('totals')[0].find_elements_by_tag_name('td')[2:7]
                away_at_bats = away_totals_scrape[0].get_attribute('innerHTML')
                away_runs = away_totals_scrape[1].get_attribute('innerHTML')
                away_hits = away_totals_scrape[2].get_attribute('innerHTML')
                away_rbis = away_totals_scrape[3].get_attribute('innerHTML')
                away_walks = away_totals_scrape[4].get_attribute('innerHTML')

                home_totals_scrape = browser.find_elements_by_class_name('totals')[2].find_elements_by_tag_name('td')[2:7]
                home_at_bats = home_totals_scrape[0].get_attribute('innerHTML')
                home_runs = home_totals_scrape[1].get_attribute('innerHTML')
                home_hits = home_totals_scrape[2].get_attribute('innerHTML')
                home_rbis = home_totals_scrape[3].get_attribute('innerHTML')
                home_walks = home_totals_scrape[4].get_attribute('innerHTML')

                away_team_players = browser.find_element_by_css_selector('div.boxscore-2017__wrap.boxscore-2017__wrap--away').find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')
                #home_team_players = browser.find_elements_by_xpath(".//table[contains(@data-behavior, 'responsive_table')]")[4].find_elements_by_tag_name('tbody')
                home_team_players = browser.find_element_by_css_selector('div.boxscore-2017__wrap.boxscore-2017__wrap--home').find_elements_by_tag_name('table')[0].find_elements_by_tag_name('tbody')

                for away_player in away_team_players:
                    if len(away_player.find_elements_by_tag_name('td')) == 12:
                        avg_obp_slg = away_player.find_elements_by_tag_name('td')[9:12]
                    else:
                        avg_obp_slg = away_player.find_elements_by_tag_name('td')[8:11]
                    print('the length of avg_obp_slg is:', len(avg_obp_slg))
                    for index, val in enumerate(avg_obp_slg):
                        if index == 0:
                            try:
                                away_batting_average += float(avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of batting averages so far:', away_batting_average)
                            except ValueError:
                                away_batting_average += 0.0
                        elif index == 1:
                            try:
                                away_on_base_percentage += float(avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of on base percentage so far:', away_on_base_percentage)
                            except ValueError:
                                away_on_base_percentage += 0.0
                        elif index == 2:
                            try:
                                away_slug_percentage += float(avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of slugging percentage so far:', away_slug_percentage)
                            except ValueError:
                                away_slug_percentage += 0.0

                for home_player in home_team_players:
                    if len(home_player.find_elements_by_tag_name('td')) == 12:
                        home_avg_obp_slg = home_player.find_elements_by_tag_name('td')[9:12]
                    else:
                        home_avg_obp_slg = home_player.find_elements_by_tag_name('td')[8:11]
                    print('the length of avg_obp_slg is:', len(home_avg_obp_slg))
                    for index, val in enumerate(home_avg_obp_slg):
                        if index == 0:
                            try:
                                home_batting_average += float(home_avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of batting averages so far:', home_batting_average)
                            except ValueError:
                                home_batting_average += 0.0
                        elif index == 1:
                            try:
                                home_on_base_percentage += float(home_avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of on base percentage so far:', home_on_base_percentage)
                            except ValueError:
                                home_on_base_percentage += 0.0
                        elif index == 2:
                            try:
                                home_slug_percentage += float(home_avg_obp_slg[index].get_attribute('innerHTML'))
                                print('The sum of slugging percentage so far:', home_slug_percentage)
                            except ValueError:
                                home_slug_percentage += 0.0

                away_batting_average = away_batting_average / len(away_team_players)
                away_on_base_percentage = away_on_base_percentage / len(away_team_players)
                away_slug_percentage = away_slug_percentage / len(away_team_players)

                away_batting_average = round(away_batting_average, 3)
                away_on_base_percentage = round(away_on_base_percentage, 3)
                away_slug_percentage = round(away_slug_percentage, 3)

                home_batting_average = home_batting_average / len(home_team_players)
                home_on_base_percentage = home_on_base_percentage / len(home_team_players)
                home_slug_percentage = home_slug_percentage / len(home_team_players)

                home_batting_average = round(home_batting_average, 3)
                home_on_base_percentage = round(home_on_base_percentage, 3)
                home_slug_percentage = round(home_slug_percentage, 3)

                print('The away team is {}, with {} at bats, {} runs, {} hits, {} rbis, {} walks, {:0.3f} avg, {:0.3f} obp, and {:0.3f} slg'.format(away_team, away_at_bats, away_runs, away_hits, away_rbis, away_walks, away_batting_average, away_on_base_percentage, away_slug_percentage))
                print('The home team is {}, with {} at bats, {} runs, {} hits, {} rbis, {} walks, {:0.3f} avg, {:0.3f} obp, and {:0.3f} slg'.format(home_team, home_at_bats, home_runs, home_hits, home_rbis, home_walks, home_batting_average, home_on_base_percentage, home_slug_percentage))

                away_win = int(away_runs) > int(home_runs)

                with open('mlb_games_overview', 'a') as f:
                    f.write('{},{},{},{},{},{},{},{},{},{},{},{}\n{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(date, away_team, int(away), away_at_bats, away_runs, away_hits, away_rbis, away_walks, away_batting_average, away_on_base_percentage, away_slug_percentage, int(away_win), date, home_team, int(not away), home_at_bats, home_runs, home_hits, home_rbis, home_walks, home_batting_average, home_on_base_percentage, home_slug_percentage, int(not away_win)))

            except Exception as e:
                browser.refresh()
                print('browser has refreshed because of error: {}'.format(e))

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
        browser.refresh()
        print('Web page unavailable...\nIncrementing one day\n', date)
        continue
    except requests.exceptions.RequestException as e:
        sys.exit(1)
