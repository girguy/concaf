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

page = st.sidebar.selectbox(' ', ['Nations', 'Tournament'])

if page == 'Nations':
    page_title()

    top_5_league, top_30_teams, avg_market, avg_age = st.columns(4)

    font_size = 10
    height_plot = 130
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    best_club_nb_players, top_league_nb_players, avg_age_players, avg_nation_market_vakue = data_extractor.get_kpis()

    with top_5_league:
        visualizer.kpi('Players in top 5 leagues', best_club_nb_players, height_plot, font_size, background_plot_color, bar_plot_color)

    with top_30_teams:
        visualizer.kpi('Players In Top 30 Clubs', top_league_nb_players, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_market:
        visualizer.kpi('Market Value Per Nation', avg_nation_market_vakue, height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_age:
        visualizer.kpi('Player Average Age', avg_age_players, height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 15
    width_plot = 300
    height_plot = 300
    background_plot_color = "#191919"
    plot_bgcolor = "#006400"
    with col_1:
        data = data_extractor.get_number_of_player_per_top_league()
        visualizer.plot_players_per_league('Number of Players per Top 5 Leagues', data, width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        data = data_extractor.get_ranking_per_nation()
        visualizer.plot_fifa_ranking('African Football Nations FIFA Rankings', data, width_plot, height_plot, font_size, background_plot_color)

    col_1, col_2 = st.columns(2)

    with col_1:
        data = data_extractor.get_market_value_per_nation()
        visualizer.market_value_per_team('Team Market Values of African Football Nations', data, width_plot, height_plot, font_size, background_plot_color)

    with col_2:
        data = data_extractor.get_market_value_per_position()
        visualizer.position_market_value('Market Value Per Position', data, width_plot, height_plot, font_size, background_plot_color)

    data = data_extractor.get_average_age_cap()
    visualizer.average_age_and_cap('Average Age and Cap of African Football Nations', data, width_plot, height_plot, font_size, background_plot_color)

elif page == 'Tournament':
    page_title()

    nb_games, nb_goals, avg_goals, nb_wins, nb_draws = st.columns(5)

    font_size = 10
    width_plot = 300
    height_plot = 150
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    data = data_extractor.get_tournament_info()

    with nb_games:
        visualizer.kpi('Number Of Games Played', data[0], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_goals:
        visualizer.kpi('Number Of Goals', data[1], height_plot, font_size, background_plot_color, bar_plot_color)

    with avg_goals:
        visualizer.kpi('Average Number Of Goals', data[2], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_wins:
        visualizer.kpi('Number Of wins', data[3], height_plot, font_size, background_plot_color, bar_plot_color)

    with nb_draws:
        visualizer.kpi('Number Of Draws', data[4], height_plot, font_size, background_plot_color, bar_plot_color)

    col_1, col_2 = st.columns(2)

    font_size = 16
    width_plot = 150
    height_plot = 300
    text_color = "#006400"
    background_plot_color = "#191919"
    bar_plot_color = "#006400"

    data = data_extractor.get_result_of_the_competiton()
    visualizer.results('Games Played', data, width_plot, height_plot, font_size, background_plot_color)

    nextFixtures, home_teams, away_teams = data_extractor.get_fixtures_info()
    fixtureChoice = st.selectbox('Fixtures', nextFixtures)
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
    print(data)
    visualizer.past_games(f'Past Games between {home_team_name} and {away_team_name}', data, width_plot, height_plot, font_size, background_plot_color)
