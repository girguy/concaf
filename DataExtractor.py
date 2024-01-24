import polars as pl

class DataExtractor:
    def __init__(self, players_df, nations_df, clubs_df, fixtures_df,
                 outcomes_df, games_df, past_games_df):

        self._players_df = players_df
        self._nations_df = nations_df
        self._clubs_df = clubs_df
        self._fixtures_df = fixtures_df
        self._outcomes_df = outcomes_df
        self._games_df = games_df
        self._past_games_df = past_games_df

    def get_kpis(self):
        df = self._players_df.join(self._clubs_df, on='ClubID', how='left')

        best_club_nb_players = (df['BestClub']).sum() # OK
        top_league_nb_players = (df['TopLeague']).sum() # OK
        percentage_best_club = best_club_nb_players/df.shape[0]*100 # OK
        percentage_top_league_players = best_club_nb_players/df.shape[0]*100 # OK
        avg_age_players = self._players_df.select('Age').mean()['Age'][0]
        avg_nation_market_vakue = self._nations_df.select('SumMarketValue').mean()['SumMarketValue'][0]

        return best_club_nb_players, top_league_nb_players, avg_age_players, avg_nation_market_vakue

    def get_number_of_player_per_top_league(self):
        df = self._players_df.join(self._clubs_df, on='ClubID', how='left')

        # Group by 'TopLeague' and count the players
        grouped_df = df.group_by('Country').agg(pl.count('PlayerID').alias('PlayerCount'))
        grouped_df = grouped_df.filter(~pl.col('Country').is_in(['No', 'POR', 'UKR']))

        grouped_df = grouped_df.with_columns(
            pl.col('Country')
            .str.replace('FR', 'Ligue 1')
            .str.replace('ESP', 'La Liga')
            .str.replace('GER', 'Bundesliga')
            .str.replace('IT', 'Serie A')
            .str.replace('ENG', 'Premier League')
        )

        return grouped_df.sort(by='PlayerCount', descending=False)

    def get_ranking_per_nation(self):
        nations_ranking = self._nations_df.select('Nationality', 'NationRanking')
        nations_ranking = nations_ranking.rename({'Nationality': 'Nation', 'NationRanking': 'Nation Ranking'})
        return nations_ranking.sort(by='Nation Ranking', descending=False)

    def get_market_value_per_nation(self):
        df = self._nations_df.select('Nationality', 'SumMarketValue')
        df = df.rename({'Nationality': 'Nation', 'SumMarketValue': 'MarketValue'})
        return df.sort(by='MarketValue', descending=True)

    def get_market_value_per_position(self):
        df = self._players_df.groupby('Position').agg(pl.mean('MarketValue').alias('MarketValue'))
        df = df.with_columns(df['MarketValue'].round(decimals=1))
        return df.sort(by='MarketValue', descending=True)

    def get_average_age_cap(self):
        df = self._nations_df.select('Nationality', 'AgeAverage', 'AverageCap')
        df = df.with_columns(df['AgeAverage'].round(decimals=2))
        df = df.with_columns(df['AverageCap'].round(decimals=2))
        return df

    def get_result_of_the_competiton(self):
        df = self._games_df.with_columns([
            self._games_df["HomeTeamGoal"].cast(pl.Utf8),
            self._games_df["AwayTeamGoal"].cast(pl.Utf8)
        ])

        df = df.with_columns(pl.concat_str([pl.col('HomeTeamGoal'), pl.lit(" - "), pl.col('AwayTeamGoal')]).alias('Result'))
        return df.select('Date', 'HomeTeam', 'AwayTeam', 'Result')

    def get_tournament_info(self):
        nb_games = self._games_df.shape[0]
        nb_goals = self._games_df['HomeTeamGoal'].sum() + self._games_df['AwayTeamGoal'].sum()
        avg_goals = nb_goals / nb_games
        nb_draws = self._games_df.filter(pl.col('HomeTeamGoal') == pl.col('AwayTeamGoal')).shape[0]
        nb_wins = nb_games - nb_draws
        return [nb_games, nb_goals, avg_goals, nb_wins, nb_draws]

    def get_fixtures_info(self):
        df = self._fixtures_df.with_columns(pl.concat_str([pl.col('Date'), pl.lit(" : "), pl.col('HomeTeam'), pl.lit(' vs '), pl.col('AwayTeam')]).alias('NextFixtures'))
        results = df.select('NextFixtures').to_series().to_list()
        home_teams = df.select('HomeTeam').to_series().to_list()
        away_teams = df.select('AwayTeam').to_series().to_list()
        return results, home_teams, away_teams

    def get_fixtures_predictions(self, home_team_name, away_team_name):
        fixture = self._outcomes_df.filter((pl.col('HomeTeam') == home_team_name) & (pl.col('AwayTeam') == away_team_name))
        return fixture.to_numpy().tolist()[0][2:]

    def past_games(self, home_team, away_team):
        df = self._past_games_df.filter(pl.col('HomeTeam').is_in([home_team, away_team]) &  pl.col('AwayTeam').is_in([home_team, away_team]))
        df = df.with_columns(pl.concat_str([pl.col('Date'), pl.lit(" : "), pl.col('HomeTeam'), pl.lit(' vs '), pl.col('AwayTeam')]).alias('NextFixtures'))

        df = df.with_columns(
            pl.when(pl.col('SpecialWinConditions').is_not_null())
            .then(pl.col('Stage') + pl.lit(' : ') + pl.col('SpecialWinConditions'))
            .otherwise(pl.col('Stage'))
            .alias('Phase')
        )

        df = df.with_columns(pl.concat_str([pl.col('HomeTeamGoal'), pl.lit(" - "), pl.col('AwayTeamGoal')]).alias('Result'))
        return df.select('Date', 'HomeTeam', 'AwayTeam', 'Result', 'Phase')
