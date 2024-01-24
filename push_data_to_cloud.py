import re
import pandas as pd
import polars as pl
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import logging


PLAYER = 'Player'
NATION = 'Nation'
CLUB = 'Club'
FIXTURES = 'Fixture'
OUTCOMES = 'Outcome'
GAMES = 'Game'
PAST_GAMES = 'PastGames'

players_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{PLAYER}.csv")
nations_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{NATION}.csv")
clubs_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{CLUB}.csv")
fixtures_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{FIXTURES}.csv")
outcomes_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{OUTCOMES}.csv")
games_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{GAMES}.csv")
past_games_df = pd.read_csv(f"C:/Users/guygi/OneDrive/Bureau/concaf_analytics/datasets/clean/{PAST_GAMES}.csv")


def create_blob_client_with_connection_string(connection_string):
    connection_string = re.sub(r'%2B', '+', connection_string)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client


def from_pandas_to_parquet(df):
    parquet_file = BytesIO()
    df.to_parquet(parquet_file, engine = 'pyarrow')
    return parquet_file


def main():

    logging.info('Data Uploaded to the Azure Blob Storage.')
    logger = logging.getLogger('__To_Azure_Blob_Storage__')
    logger.setLevel(logging.INFO)

    # Create a blob client
    connection_string = "DefaultEndpointsProtocol=https;AccountName=storagefootanalysis;AccountKey=UHMmYUJDVHJI1IhTCy/2UXVqjoRJYw2gJTKNPQ8jL9juuD5cJeNMIYXwXbkpfSEIE3cByx%2BkQ29e%2BAStk2zvmQ==;EndpointSuffix=core.windows.net"
    blob_service_client = create_blob_client_with_connection_string(connection_string)
    logger.info(f"Successfully created blob client\n")

    container_name = "coupe-afrique"
    logger.info(f"Successfully got container client for {container_name} container.\n")

    file_names = ['Player', 'Club', 'Nation', 'Game', 'Fixture', 'Outcome', 'PastGames']
    dataframes = [players_df, clubs_df, nations_df, games_df, fixtures_df, outcomes_df, past_games_df]

    for df_name, df in zip(file_names, dataframes):
        parquet_buffer = from_pandas_to_parquet(df)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{df_name}.parquet")
        blob_client.upload_blob(parquet_buffer.getvalue(), blob_type="BlockBlob", overwrite=True)
        logger.info(f"Successfully uploaded {df_name} to {container_name} container !\n")
