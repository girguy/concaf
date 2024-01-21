import streamlit as st

import polars as pl
import logging
from PIL import Image
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

PLAYER = 'Player'
NATION = 'Nation'
CLUB = 'Club'
FIXTURES = 'Fixture'
OUTCOMES = 'Outcome'
GAMES = 'Game'
PAST_GAMES = 'PastGames'

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


def initialize_classes():

    players_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{PLAYER}.csv", infer_schema_length=10000)
    nations_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{NATION}.csv", infer_schema_length=10000)
    clubs_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{CLUB}.csv", infer_schema_length=10000)
    fixtures_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{FIXTURES}.csv", infer_schema_length=10000)
    outcomes_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{OUTCOMES}.csv", infer_schema_length=10000)
    games_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{GAMES}.csv", infer_schema_length=10000)
    past_games_df = pl.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{PAST_GAMES}.csv", infer_schema_length=10000)

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


data_extractor, visualizer = initialize_classes()

page = st.sidebar.selectbox(' ', ['Tournament', 'Nations'])

if page == 'Nations':
    page_title()

    top_5_league, top_30_teams, avg_market, avg_age = st.columns(4)

    font_size = 10
    height_plot = 130
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    with top_5_league:
        visualizer.kpi('Players in top 5 leagues', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with top_30_teams:
        visualizer.kpi('Players In Top 30 Clubs', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_market:
        visualizer.kpi('Market Value Per Nation', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_age:
        visualizer.kpi('Player Average Age', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 15
    width_plot = 300
    height_plot = 300
    background_plot_color = "#191919"
    plot_bgcolor = "#006400"
    with col_1:
        visualizer.plot_players_per_league('Number of Players per Top 5 Leagues', width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        title = 'African Football Nations FIFA Rankings'
        visualizer.plot_fifa_ranking(title, width_plot, height_plot, font_size, background_plot_color)

    col_1, col_2 = st.columns(2)

    with col_1:
        title = 'Team Market Values of African Football Nations'
        visualizer.market_value_per_team(title, width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        title = 'Market Value Per Position'
        visualizer.position_market_value(title, width_plot, height_plot, font_size, background_plot_color)

    title = 'Average Age and Cap of African Football Nations'
    visualizer.average_age_and_cap(title, width_plot, height_plot, font_size, background_plot_color)

elif page == 'Tournament':
    page_title()

    nb_games, nb_goals, avg_goals, nb_wins, nb_draws = st.columns(5)

    font_size = 10
    width_plot = 300
    height_plot = 150
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    with nb_games:
        visualizer.kpi('Number Of Games Played', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_goals:
        visualizer.kpi('Number Of Goals', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_goals:
        visualizer.kpi('Average Number Of Goals', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_wins:
        visualizer.kpi('Number Of wins', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_draws:
        visualizer.kpi('Number Of Draws', 125, height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 16
    width_plot = 150
    height_plot = 300
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    title = 'Games Played'
    visualizer.results(title, width_plot, height_plot, font_size, background_plot_color)

    nextFixtures = ['01/02/2024 : Senegal vs Guinea', '01/02/2024 : Ivory Coast vs Mali', '01/02/2024 : Tanzania vs Algeria']
    homeTeams = ['Senegal', 'Ivory Coast', 'Tanzania']
    awayTeams = ['Guinea', 'Mali', 'Algeria']
    fixtureChoice = st.selectbox('Fixtures', nextFixtures)
    index = nextFixtures.index(fixtureChoice)
    homeTeamName = homeTeams[index]
    awayTeamName = awayTeams[index]

    st.markdown(" ")  # This creates additional space after the title

    visualizer.display_match_info(
        f'{homeTeamName}', f'team_pictures/{homeTeamName}.png',
        f'{awayTeamName}', f'team_pictures/{awayTeamName}.png'
        )

    st.markdown(" ")  # This creates additional space after the title
    st.markdown(" ")  # This creates additional space after the title

    col_1, col_2, col_3, col_4, col_5, col_6 = st.columns(6)

    win = 35
    loose = 25
    draw = 40
    both = 15
    more25 = 35
    more35 = 14
    font_size = 10
    height = 130

    color_1 = "#191919" # dark grey
    color_2 = "#006400" # green

    with col_1:
        visualizer.odd_circle(f"{homeTeamName} - Win", win, 120, height, font_size, color_1, color_2)

    with col_2:
        visualizer.odd_circle(f"{awayTeamName} - Win", loose, 120, height, font_size, color_1, color_2)

    with col_3:
        visualizer.odd_circle("Draw", draw, 120, height, font_size, color_1, color_2)

    with col_4:
        visualizer.odd_circle("Both teams score", both, 120, height, font_size, color_1, color_2)

    with col_5:
        visualizer.odd_circle("More than 2.5 goals", more25, 120, height, font_size, color_1, color_2)

    with col_6:
        visualizer.odd_circle("More than 3.5 goals", more35, 120, height, font_size, color_1, color_2)
