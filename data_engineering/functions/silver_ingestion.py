import ast
from configparser import ConfigParser
from functions.utils import read_pdf, database_connection, get_dir_config
from functions.data_cleaning import remove_end, remove_header, remove_unwanted_chr


def silver_data_ingestion(pdf_name, table_name):

    # Read the PDF file
    doc, file = read_pdf(pdf_name)

    # Read the config.ini file in order to get the create/insert table command and 
    # some variables for data cleaning
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config)

    # Read de variables for data cleaning
    header = ast.literal_eval(config["PROCESSING"][table_name])["header"]
    unwanted_chr = ast.literal_eval(config["PROCESSING"][table_name])["unwanted_chr"]
    end = ast.literal_eval(config["PROCESSING"][table_name])["end"]

    # Read the text of each page, applies data cleaning and stores it in a tuple
    ingestion_data = []
    i = 1
    for page in doc:
        # Data cleaning
        page_content = page.extract_text()
        page_content = remove_header(page_content, header)
        page_content = remove_unwanted_chr(page_content, unwanted_chr)
        page_content = remove_end(page_content, end)
        
        # Store the data in a tuple
        doc_tuple = (i, page_content)
        ingestion_data.append(doc_tuple)
        i += 1
    
    # Creates the silver database
    conn = database_connection("silver.db")
    cursor = conn.cursor()

    # Add the table name in the SQL command
    create_table = (config["CREATE_TABLE"]["SILVER"]).replace("#TABELA#", table_name)
    insert_table = (config["INSERT_TABLE"]["SILVER"]).replace("#TABELA#", table_name)

    # Create the silver table
    cursor.execute(create_table)
    conn.commit()

    # Insert data into the silver table
    conn.executemany(insert_table, ingestion_data)

    # Closes the file and connection
    file.close()
    cursor.close()
    conn.close()