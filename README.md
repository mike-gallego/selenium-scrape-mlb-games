# baseball-game-prediction
Python language using sci-kit learn and Selenium to scrape mlb websites and collection information to get inputs and outputs to potentially predict who will win the next game.

# What is the goal of this project?
The machine learning model is designed to essentially predict which team is going to win the game

# How will the data be collected?
- A python script will navigate through https://www.espn.com/mlb/schedule/_/YYYYMMDD
- It will iterate through and collect the scores and that will be the outputs we want from the data
- Each game has information that will essentially be our inputs for the model to train on
- This is going be a work of web scraping to collect that data and store it into a type of data format (JSON, CSV, etc

# What kind of machine learning algorithm is being used?
Linear Regression Model because the inputs have a strong correlation on the output of the game

# What are the steps for the project?
Step 1: Using Selenium package to create a webdriver to open the desired web page to scrape
```
path_to_chromedriver = 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=path_to_chromedriver)
date = datetime.datetime(2019, 3, 20)
date = date.strftime('%Y%m%d')
url = 'https://www.espn.com/mlb/schedule/_/date/{}'.format(date)
browser.get(url)
```
