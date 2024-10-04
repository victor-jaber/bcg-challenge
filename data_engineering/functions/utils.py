# ========================================================================== #
### Common functions used in the project
# ========================================================================== #

## Importing libraries
import os
import PyPDF2
import duckdb
from pathlib import Path


def get_dir_proj():
    '''
    Returns the absolute path to the main.py
    '''
    dir_proj, _ = os.path.split(os.path.abspath(__file__))
    dir_proj = dir_proj.replace(os.sep, "/")
    dir_proj = "/".join(dir_proj.split("/")[:-1])
    return dir_proj


def get_dir_config():
    '''
    Returns the absolute path to the config.ini
    '''
    dir_proj, _ = os.path.split(os.path.abspath(__file__))
    dir_proj = dir_proj.replace(os.sep, "/")
    dir_proj = "/".join(dir_proj.split("/")[:-1])
    ini_config = str(Path(dir_proj, "config", "config.ini").resolve()).replace("\\", "/")
    return ini_config


def read_pdf(file_name):
    '''
    Read the PDF file
    '''
    dir_proj = get_dir_proj()
    file = open(f'{dir_proj}/database/raw_data/{file_name}', 'rb')
    reader = PyPDF2.PdfReader(file)
    return reader.pages, file


def database_connection(database_name):
    """
    Creates the connection with de duckdb database
    """
    dir_proj = get_dir_proj()
    conn = duckdb.connect(f'{dir_proj}/database/{database_name}')
    return conn
    

def clean_database():
    """
    Clean duckdb database to avoid insertion of duplicate records
    """
    # Folder path where .db files are located
    folder = f'{get_dir_proj()}/database'

    # List all files in the folder
    for file in os.listdir(folder):
        if file.endswith('.db'):
            # Create the full file path
            full_path = (os.path.join(folder, file)).replace('\\', '/')
            # Delete the file
            os.remove(full_path)
            print(f'Deleted: {full_path}')
