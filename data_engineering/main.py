import ast
from configparser import ConfigParser
from functions.utils import get_dir_config, clean_database
from functions.bronze_ingestion import bronze_data_ingestion
from functions.silver_ingestion import silver_data_ingestion


# Clean database to avoid insertion of duplicate records
clean_database()

## Read the config.ini in order to get the file/table name
ini_config = get_dir_config()
config = ConfigParser()
config.read(ini_config)

## PDF file name and table name that will be create in the database
metadata = ast.literal_eval(config["METADATA"]["TABLE_NAME"])

## Data ingestion in bronze, silver and gold layers
for pdf_name in metadata.keys():
    table_name = metadata[pdf_name]
    if table_name == "ENFRENTAMENTO_NACIONAL":

        # Bronze ingestion
        bronze_data_ingestion(pdf_name, table_name)

        # Silver ingestion
        silver_data_ingestion(pdf_name, table_name)

        # Gold ingestion