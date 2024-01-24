import create_result_fixture_tables
import poisson_implementation
import push_data_to_cloud
import logging

logging.info('Data Uploaded to the Azure Blob Storage.')
logger = logging.getLogger('__To_Azure_Blob_Storage__')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    create_result_fixture_tables.main()
    logger.info("'Fixture' and 'Game' tables saved locally")
    poisson_implementation.main()
    logger.info("'Outcomes' table saved locally")
    push_data_to_cloud.main()
    logger.info("Tables saved in Azure Storage Account")
