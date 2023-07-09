import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# the URL of the NFL game boxscore page on ESPN
url = "https://www.espn.com/nfl/boxscore/_/gameId/401437654"

# send a GET request to the URL and get the HTML content
response = requests.get(url)
content = response.content

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# find the table containing the team stats
team_tables = soup.find_all("table", {"class": "mod-data"})
time.sleep(1)
home_table = team_tables[0]
away_table = team_tables[1]

# create empty lists to hold the data
home_data = []
away_data = []

# iterate over each row in the home team table and extract the data
for tr in home_table.find_all("tr"):
    row = []
    for td in tr.find_all("td"):
        row.append(td.text.strip())
    if row:
        home_data.append(row)

# iterate over each row in the away team table and extract the data
for tr in away_table.find_all("tr"):
    row = []
    for td in tr.find_all("td"):
        row.append(td.text.strip())
    if row:
        away_data.append(row)

# create a Pandas DataFrame for the home team
home_df = pd.DataFrame(home_data[1:], columns=home_data[0])

# create a Pandas DataFrame for the away team
away_df = pd.DataFrame(away_data[1:], columns=away_data[0])

# print the DataFrames
print("Home Team Stats:")
print(home_df)

print("Away Team Stats:")
print(away_df)
