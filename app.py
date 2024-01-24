import re
import streamlit as st
import pandas as pd
import polars as pl
from PIL import Image
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from DataExtractor import DataExtractor
from Visualizer import Visualizer

# Set page configuration with custom color theme
st.set_page_config(
    page_title="African Cup of Nations Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# This is a dashboard for the African Cup of Nations"
    }
)

CONCAF_LOGO = Image.open('pictures/logo_team.png')
WIDTH_LOGO = 3000

# size of the white space above the title
reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0.4rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

# size of the side bar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def create_blob_client_with_connection_string(connection_string):
    connection_string = re.sub(r'%2B', '+', connection_string)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client


def download_parquet(container_client, blob_name):
    blob_client = container_client.get_blob_client(blob=blob_name)
    download_stream = blob_client.download_blob()
    stream = BytesIO()
    download_stream.readinto(stream)
    df = pd.read_parquet(stream, engine='pyarrow')
    return df


def extract_dataset(connection_string, container_name):
    blob_service_client = create_blob_client_with_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    datasets = {
        'Club': None,
        'Fixture': None,
        'Game': None,
        'Nation': None,
        'Outcome': None,
        'PastGames': None,
        'Player': None
    }

    for blob in container_client.list_blobs() :
        for dataset in datasets:
            if (blob.name.startswith(dataset)):
                df = download_parquet(container_client, blob.name)
                datasets[dataset] = pl.from_pandas(df)

    return datasets['Player'], datasets['Nation'], datasets['Club'], datasets['Fixture'], datasets['Outcome'], datasets['Game'],  datasets['PastGames']

@st.cache_data
def initialize_classes(connection_string, container_name):

    players_df, nations_df, clubs_df, fixtures_df, outcomes_df, games_df, past_games_df = extract_dataset(connection_string, container_name)

    dataExtractor = DataExtractor(
        players_df, nations_df, clubs_df, fixtures_df, outcomes_df, games_df, past_games_df
        )

    visualizer = Visualizer(
        players_df, nations_df, clubs_df, fixtures_df, outcomes_df, games_df, past_games_df
        )

    return dataExtractor, visualizer

@st.cache_data
def page_title():
    # Custom CSS to inject into the Streamlit interface
    st.markdown("""
        <style>
        .title-font {
            font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; /* Example of a different font */
            color: #FFFFFF;
            font-size: 32px;
            top: 0px;
            left: 01px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Custom title with HTML and CSS
    st.markdown('<div class="title-font">African Cup of Nations Dashboard \n</div>', unsafe_allow_html=True)
    st.markdown(" ")  # This creates additional space after the title


data_extractor, visualizer = initialize_classes(
    st.secrets["CONNECTION_STRING"], st.secrets["CONTAINER_NAME"]
    )

page = st.sidebar.selectbox(' ', ['Page 1', 'Page 2'])

if page == 'Page 1':
    page_title()

    top_5_league, top_30_teams, avg_market, avg_age = st.columns(4)

    font_size = 10
    height_plot = 110
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    best_club_nb_players, top_league_nb_players, avg_age_players, avg_nation_market_vakue = data_extractor.get_kpis()

    with top_5_league:
        visualizer.kpi('Players in Top 5 Leagues', best_club_nb_players, height_plot, font_size, background_plot_color, bar_plot_color)

    with top_30_teams:
        visualizer.kpi('Players in Top 30 Clubs', top_league_nb_players, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_market:
        visualizer.kpi('Teams Average Market Value', avg_nation_market_vakue, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_age:
        visualizer.kpi("Players' Age Average", avg_age_players, height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 15
    width_plot = 300
    height_plot = 300
    background_plot_color = "#191919"
    plot_bgcolor = "#006400"
    with col_1:
        data = data_extractor.get_number_of_player_per_top_league()
        visualizer.plot_players_per_league('Number of Players in Top 5 Leagues', data, width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        data = data_extractor.get_ranking_per_nation()
        visualizer.plot_fifa_ranking('African Football Nations FIFA Rankings', data, width_plot, height_plot, font_size, background_plot_color)

    col_1, col_2 = st.columns([2, 1])

    with col_1:
        data = data_extractor.get_market_value_per_nation()
        visualizer.market_value_per_team('Team Market Values of African Football Nations', data, width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        data = data_extractor.get_market_value_per_position()
        visualizer.position_market_value('Average Market Value by Player Position', data, width_plot, height_plot, font_size, background_plot_color)

    data = data_extractor.get_average_age_cap()
    visualizer.average_age_and_cap('Average Age and Cap of African Football Nations', data, width_plot, height_plot, font_size, background_plot_color)

elif page == 'Page 2':
    page_title()

    nb_games, nb_goals, avg_goals, nb_wins, nb_draws = st.columns(5)

    font_size = 10
    width_plot = 300
    height_plot = 110
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    data = data_extractor.get_tournament_info()

    with nb_games:
        visualizer.kpi('Games Played', data[0], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_goals:
        visualizer.kpi('Goals Scored', data[1], height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_goals:
        visualizer.kpi('Average Number Of Goals', data[2], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_wins:
        visualizer.kpi('Wins', data[3], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_draws:
        visualizer.kpi('Draws', data[4], height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 16
    width_plot = 150
    height_plot = 250
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    data = data_extractor.get_result_of_the_competiton()
    visualizer.results('African Cup 2024: Games Played', data, width_plot, height_plot, font_size, background_plot_color)

    nextFixtures, home_teams, away_teams = data_extractor.get_fixtures_info()
    st.markdown(" ")
    fixtureChoice = st.selectbox('Next Fixtures', nextFixtures)
    index = nextFixtures.index(fixtureChoice)
    home_team_name = home_teams[index]
    away_team_name = away_teams[index]

    st.markdown(" ")  # This creates additional space after the title

    visualizer.display_match_info(
        f'{home_team_name}', f'team_pictures/{home_team_name}.png',
        f'{away_team_name}', f'team_pictures/{away_team_name}.png'
        )

    st.markdown(" ")  # This creates additional space after the title
    st.markdown(" ")  # This creates additional space after the title

    col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)

    data = data_extractor.get_fixtures_predictions(home_team_name, away_team_name)

    win = round(float(data[0]), 2)
    draw = round(float(data[1]), 2)
    loose = round(float(data[2]), 2)
    both = round(float(data[3]), 2)
    more15 = round(float(data[4]), 2)
    more25 = round(float(data[5]), 2)
    more35 = round(float(data[6]), 2)
    font_size = 8
    height = 130

    color_1 = "#191919"  # dark grey
    color_2 = "#006400"  # green

    with col_1:
        visualizer.odd_circle(f"{home_team_name} - Win", win, 120, height, font_size, color_1, color_2)

    with col_2:
        visualizer.odd_circle(f"{away_team_name} - Win", loose, 120, height, font_size, color_1, color_2)

    with col_3:
        visualizer.odd_circle("Draw", draw, 120, height, font_size, color_1, color_2)

    with col_4:
        visualizer.odd_circle("Both teams score", both, 120, height, font_size, color_1, color_2)

    with col_5:
        visualizer.odd_circle("More than 2.5 goals", more25, 120, height, font_size, color_1, color_2)

    with col_6:
        visualizer.odd_circle("More than 3.5 goals", more35, 120, height, font_size, color_1, color_2)

    data = data_extractor.past_games(home_team_name, away_team_name)
    visualizer.past_games(f'Past Games between {home_team_name} and {away_team_name}', data, width_plot, height_plot, font_size, background_plot_color)
