import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import logging


# Improved function
def convert_date(date_str, default_year="2024"):
    # Remove the day of the week
    date_str = ' '.join(date_str.split()[1:])

    # Remove ordinal suffixes (st, nd, rd, th) from the day
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    # Parse the date with the default year
    date_obj = datetime.strptime(f"{date_str} {default_year}", '%d %B %Y')

    # Format the date as 'dd/mm/yyyy'
    return date_obj.strftime('%d/%m/%Y')


def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    with requests.Session() as session:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.content


def parse_fixtures(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    fixtures_info = []
    for fixture in soup.find_all('div', class_='fixres__item'):
        date = fixture.find_previous_sibling('h4', class_='fixres__header2')
        home_team = fixture.find('span', class_='matches__participant--side1')
        away_team = fixture.find('span', class_='matches__participant--side2')
        if date and home_team and away_team:
            fixtures_info.append({
                'Date': date.text.strip(),
                'HomeTeam': home_team.text.strip(),
                'AwayTeam': away_team.text.strip()
            })
    return fixtures_info


def replace_team_name(df, replacements):
    # Apply the replacements to both columns
    df['HomeTeam'] = df['HomeTeam'].replace(replacements)
    df['AwayTeam'] = df['AwayTeam'].replace(replacements)

    return df

def main():

    logging.info('Extract Fixtures and Played Games.')
    logger = logging.getLogger('__CAN_2024_')
    logger.setLevel(logging.INFO)

    logger.info("Start scrapping fixtures")

    # URL of the page to scrape
    url = "https://www.skysports.com/africa-cup-of-nations-fixtures"

    try:
        page_content = fetch_page(url)
        fixtures_info = parse_fixtures(page_content)
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Create a DataFrame from the scraped data
    fixtures_info_df = pd.DataFrame(fixtures_info, columns=['Date', 'HomeTeam', 'AwayTeam'])

    # Apply the convert_date function to the 'Date' column
    fixtures_info_df['Date'] = fixtures_info_df['Date'].apply(convert_date)

    # Convert 'Date' column to Timestamp
    fixtures_info_df['Date'] = pd.to_datetime(fixtures_info_df['Date'], format='%d/%m/%Y')

    # Get today's date as a Timestamp
    today = pd.to_datetime(datetime.now().strftime('%d/%m/%Y'), dayfirst=True)

    # Filter out rows with dates in the past
    fixtures_info_df = fixtures_info_df[fixtures_info_df['Date'] >= today]

    # List of words to filter
    words_to_filter = ['Group', 'Place', 'Round', 'Final']

    # Join the words into a regular expression
    regex_pattern = '|'.join(words_to_filter)


    # Filter rows where 'HomeTeam' contains any of the words
    fixtures_info_df = fixtures_info_df[~fixtures_info_df['HomeTeam'].str.contains(regex_pattern, case=False, na=False)]
    fixtures_info_df = fixtures_info_df[~fixtures_info_df['AwayTeam'].str.contains(regex_pattern, case=False, na=False)]

    # process team names
    replacements = {
        'Morocco': 'Maroc',
        'Tunisia': 'Tunisie',
        'DR Congo': 'Congo',
        'Burkina': 'Burkina Faso'
    }
    fixtures_info_df = replace_team_name(fixtures_info_df, replacements)
    fixtures_info_df['Date'] = fixtures_info_df['Date'].dt.strftime('%d/%m/%Y')

    logger.info("Fixtures Table created !")

    logger.info("Start scrapping games played !")

    url = "https://www.skysports.com/africa-cup-of-nations-results"
    try:
        page_content = fetch_page(url)
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Parse the HTML
    pageSoup = BeautifulSoup(page_content, 'html.parser')

    # Initialize an empty list to store game information
    games_info = []

    # Iterate through each game in the HTML
    for game in pageSoup.find_all('div', class_='fixres__item'):
        date_tag = game.find_previous_sibling('h4', class_='fixres__header2')
        team1_tag = game.find('span', class_='matches__participant--side1')
        team2_tag = game.find('span', class_='matches__participant--side2')
        score_tags = game.find_all('span', class_='matches__teamscores-side')

        if date_tag and team1_tag and team2_tag and len(score_tags) == 2:
            date = date_tag.text.strip()
            team1 = team1_tag.text.strip()
            team2 = team2_tag.text.strip()
            goal1 = score_tags[0].text.strip()
            goal2 = score_tags[1].text.strip()

            games_info.append({
                'Date': date,
                'HomeTeam': team1,
                'AwayTeam': team2,
                'HomeTeamGoal': goal1,
                'AwayTeamGoal': goal2
            })

    # Create a DataFrame from the scraped data
    games_info_df = pd.DataFrame(games_info, columns=['Date', 'HomeTeam', 'AwayTeam', 'HomeTeamGoal', 'AwayTeamGoal'])

    # Apply the convert_date function to the 'Date' column
    games_info_df['Date'] = games_info_df['Date'].apply(convert_date)

    # Convert 'Date' column to Timestamp
    games_info_df['Date'] = pd.to_datetime(games_info_df['Date'], format='%d/%m/%Y')

    # process team names
    replacements = {
        'Morocco': 'Maroc',
        'Tunisia': 'Tunisie',
        'DR Congo': 'Congo',
        'Burkina': 'Burkina Faso'
    }
    games_info_df = replace_team_name(games_info_df, replacements)
    # Format the dates to 'YYYY/MM/DD' (this will convert them to strings)
    games_info_df['Date'] = games_info_df['Date'].dt.strftime('%d/%m/%Y')

    logger.info("Games Played table created !")

    games_info_df.to_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/Game.csv", encoding='utf-8-sig', index=False)
    fixtures_info_df.to_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/Fixture.csv", encoding='utf-8-sig', index=False)
    logger.info("Fixtures and Games Played table saved in local computer !")