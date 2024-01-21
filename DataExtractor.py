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
