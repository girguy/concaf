import pandas as pd
from datetime import datetime
from scipy.stats import poisson
import itertools
import logging


def add_weights(df):
    # 'Date' column in datetime format
    # If 'Date' is not in datetime format, convert it first:
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Reference date
    reference_date = pd.to_datetime(datetime.now())

    # Calculate the difference in years from the reference date
    df['YearsFromRef'] = reference_date.year - df['Date'].dt.year

    # Apply an exponentially decaying weight based on years
    # Adjust the decay rate as needed. A smaller decay rate means that the weight decreases more slowly.
    decay_rate = 0.1  # Example decay rate
    df['Weight'] = df['YearsFromRef'].apply(lambda x: 2.71828 ** (-decay_rate * x))

    return df


# Calculating weighted average goals for each team
def weighted_avg_goals(df, team_column, goals_column):
    return (df['Weight'] * df[goals_column]).sum() / df['Weight'].sum()


# Adjusting for the opponent and applying Poisson model
def predict_goals(team, opponent, home_or_away, df):
    # Weighted averages
    team_goals_avg = weighted_avg_goals(df[df[home_or_away + 'Team'] == team], home_or_away + 'Team', home_or_away + 'TeamGoal')
    opponent_def_avg = weighted_avg_goals(df[df[home_or_away + 'Team'] == opponent], home_or_away + 'Team', 'AwayTeamGoal' if home_or_away == 'Home' else 'HomeTeamGoal')

    # Poisson probabilities for each scoreline up to 5 goals
    adjusted_avg = team_goals_avg * opponent_def_avg
    return [poisson.pmf(i, adjusted_avg) for i in range(7)]


def get_match_probabilities(home_team, away_team, team_home_probs, team_away_probs):
    goal_combinations = list(itertools.product(range(len(team_home_probs)), range(len(team_away_probs))))
    # Calculate the probability of each combination and store with the combination
    match_probabilities = []
    for home_team_goal, away_team_goal in goal_combinations:
        match_probabilities.append(
            (home_team, away_team, home_team_goal, away_team_goal, team_home_probs[home_team_goal] * team_away_probs[away_team_goal])
            )

    # Sort the combinations by probability in descending order
    match_probabilities.sort(key=lambda x: x[4], reverse=True)

    match_probabilities = pd.DataFrame(match_probabilities, columns=['HomeTeam', 'AwayTeam', 'HomeTeamGoal', 'AwayTeamGoal', 'OutcomeProb'])
    match_probabilities['TotalGoalScored'] = match_probabilities['HomeTeamGoal'] + match_probabilities['AwayTeamGoal']

    return match_probabilities


def get_final_probabilities(home_team, away_team, df):
    finalProbabilities = {}

    finalProbabilities['HomeTeam'] = home_team
    finalProbabilities['AwayTeam'] = away_team
    finalProbabilities['Win'] = sum(df.query("HomeTeamGoal > AwayTeamGoal")["OutcomeProb"])*100
    finalProbabilities['Draw'] = sum(df.query("HomeTeamGoal == AwayTeamGoal")["OutcomeProb"])*100
    finalProbabilities['Loose'] = sum(df.query("HomeTeamGoal < AwayTeamGoal")["OutcomeProb"])*100
    finalProbabilities['BothScore'] = sum(df.query("(HomeTeamGoal > 0) and (AwayTeamGoal > 0)")["OutcomeProb"])*100
    finalProbabilities['Over 1.5'] = sum(df.query("TotalGoalScored > 1")["OutcomeProb"])*100
    finalProbabilities['Over 2.5'] = sum(df.query("TotalGoalScored > 2")["OutcomeProb"])*100
    finalProbabilities['Over 3.5'] = sum(df.query("TotalGoalScored > 3")["OutcomeProb"])*100

    return finalProbabilities


def main():
    logging.info('Poisson Predictions.')
    logger = logging.getLogger('__predictions__')
    logger.setLevel(logging.INFO)

    past_games_df = pd.read_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/PastGames.csv")
    games_df = pd.read_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/Game.csv")
    fixtures_df = pd.read_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/Fixture.csv")
    logger.info("Local datasets successfully read.")

    past_games_df = past_games_df[['Date', 'HomeTeam', 'AwayTeam', 'HomeTeamGoal', 'AwayTeamGoal']]
    all_games_df = pd.concat([past_games_df, games_df])
    all_games_df = add_weights(all_games_df)

    probabilities_list = []
    for i in range(fixtures_df.shape[0]):
        home_team = fixtures_df.iloc[i]['HomeTeam']
        away_team = fixtures_df.iloc[i]['AwayTeam']
        team_a_probs = predict_goals(home_team, away_team, 'Home', all_games_df)
        team_b_probs = predict_goals(away_team, home_team, 'Away', all_games_df)

        match_probabilities = get_match_probabilities(home_team, away_team, team_a_probs, team_b_probs)
        finalProbabilities = get_final_probabilities(home_team, away_team, match_probabilities)

        probabilities_list.append(finalProbabilities)

    probabilities_df = pd.DataFrame(probabilities_list)

    probabilities_df.to_csv("C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/Outcome.csv", encoding='utf-8-sig', index=False)
    logger.info("Poisson predictions successfully saved in local computer!")
