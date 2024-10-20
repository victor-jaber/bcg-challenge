# AI Climate Adaptation Chat Application

## Overview

This project aims to build an AI-powered chat application designed to assist users in understanding and adapting to climate change. Whether you are looking for practical solutions for environmental sustainability, weather impact insights, or advice on local adaptations, this chat application will provide reliable and tailored responses.

## Project Structure

This section describes the folder structure of the project and the purpose of each directory and file.

```
bcg-challenge/RAG/
├── .pyenv/                  # Contains the virtual environment for the project
├── config/                  # Directory containing the configuration file
│   └── config.ini           # Configuration file with static parameters
├── database/                # Directory for project database
│   ├── raw_data/            # Folder with PDF files
│   └── datalake.db          # duckdb database, containing tables for the bronze, silver and gold layers
├── functions/               # Auxiliary fuctions
│   ├── bronze_ingestion.py  # Function for data ingestion in the bronze layer
│   ├── data_cleaning.py     # Auxiliary functions for cleaning and processing data
│   ├── embedding.py         # Embedding function
│   ├── get_message.py       # Returns the model response to the user query
│   ├── gold_ingestion.py    # Function for data ingestion in the gold layer
│   ├── silver_ingestion.py  # Function for data ingestion in the silver layer
│   └── utils.py             # Common functions used in the project
├── log/                     # Stores the execution log
├── queries/                 # Main database queries
├── main.py                  # The main script that you can run to start the application
├── README.md                # Project documentation
├── requirements.txt         # A file listing all the dependencies needed to run the project.
└── tests/                   # Directory for test files
    └── test.ipynb           # Project testing and verification
```

## Prerequisites

- Python 3.x installed on your system.

## Installation

Follow the steps below to set up the environment and run the project.

### 1. Clone the Repository

First, clone the repository or download the project files.

```bash
git clone https://github.com/victor-jaber/bcg-challenge.git
cd bcg-challenge/RAG
```

### 2. Create a Virtual Environment

Create a new virtual environment with the following command:

```bash
python -m venv .pyenv
```

### 3. Activate the Virtual Environment

Activate the virtual environment using the command appropriate for your operating system:

- **Linux or macOS**:
  ```bash
  source .pyenv/bin/activate
  ```

- **Windows**:
  ```bash
  .pyenv\Scripts\activate
  ```

### 4. Install Dependencies

Install the necessary libraries using the `requirements.txt` file included in the project. 
Ignore any errors or version conflicts.

```bash
pip install -r requirements.txt
```

### 5. Run the Project

After installing the dependencies, you can run the project.

```bash
python main.py
```

## Notes

- As PDF files are static, the processed data is already stored in the bronze/silver/gold layers of the database, through the file `datalake.db`. Therefore, the script identifies that the database is populated and does not rerun the entire ingestion and ETL process.	
If you want to read and process data again from end to end, simply delete this checkpoint file (datalake.db) located in the folder `database/` and rerun the project.

- **`config.ini`** is a configuration file in which the manual values ​​and static parameters necessary to execute the project are centralized. This file helps to facilitate the maintenance, organization and readability of the solution, in addition to avoiding hard coding throughout the .py scripts.

## Contributions

While the application is still under development, we welcome suggestions, feedback, and contributions! If you have ideas or would like to participate, please stay tuned for more updates on how you can get involved.

## License

This project is currently under a [MIT] license. Please see the `LICENSE` file for more information;