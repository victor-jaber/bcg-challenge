import ast
from configparser import ConfigParser
from functions.utils import get_dir_config, database_exists, log
from functions.bronze_ingestion import bronze_data_ingestion
from functions.silver_ingestion import silver_data_ingestion
from functions.gold_ingestion import gold_data_ingestion
from functions.get_message import process_input_with_retrieval

## Read the config.ini in order to get the file name and table name for each PDF
ini_config = get_dir_config()
config = ConfigParser()
config.read(ini_config, encoding="utf8")

# Object for execution log
logger = log(config)

# Check if the database already exists. If not, the ETL is executed
if not database_exists(logger):

    ## PDF file name and table name that will be create in the database
    metadata = ast.literal_eval(config["METADATA"]["TABLE_NAME"])

    ## Data ingestion in bronze, silver and gold layers
    for pdf_name in metadata.keys():
        table_name = metadata[pdf_name]

        # Bronze ingestion
        logger.info(f'>>> Starts processing the table {table_name} ...')
        logger.info(f'>>> Starts ingesting the table {table_name} in the bronze layer')
        bronze_data_ingestion(pdf_name, table_name, logger)

        # Silver ingestion
        logger.info(f'>>> Starts ingesting the table {table_name} in the silver layer')
        silver_data = silver_data_ingestion(pdf_name, table_name, logger)

        # Gold ingestion
        logger.info(f'>>> Starts ingesting the table {table_name} in the gold layer')
        gold_data_ingestion(table_name, silver_data, logger)


# User query
user_query = 'Quais fatores devo levar em consideração na hora de desenvolver um plano de adaptação climática para uma cidade de porte médio no Brasil?'

# Model return
final_response = process_input_with_retrieval(user_query)

print(final_response)