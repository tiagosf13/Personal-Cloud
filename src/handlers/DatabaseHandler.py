import psycopg2, configparser
from pathlib import Path

def get_current_dir(subdirectory=None):
    # Using Pathlib to get the current directory
    current_directory = Path(__file__).parent.parent
    # Add the subdirectory to the current_directory if it is not None
    return current_directory if not subdirectory else current_directory / subdirectory

def read_sql_file(filename, encoding="utf-8"):
    try:
        with open(get_current_dir(subdirectory=filename), "r", encoding=encoding) as file:
            sql_query = file.read()
        return sql_query
    except UnicodeDecodeError:
        print(f"Error: Unable to decode the file {filename} with encoding {encoding}.")
        raise

def db_connect():
    # Read the configuration file
    config_file = Path(get_current_dir(subdirectory="../credentials/conf.ini"))
    assert config_file.exists(), "conf.ini file not found"

    config = configparser.ConfigParser()
    config.read(config_file)
    
    try:
        # Connect to the database PSQL
        conn = psycopg2.connect(
            host=config["database"]["server"],
            port=config["database"]["port"],
            dbname=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"]
        )
        return conn
    except Exception as e:
        print(e)
        return None
    
conn = db_connect()

if conn == None:
        print("Failed to connect to the database")
        exit(1)

def db_query(query, params=None):

    # Initiate the cursor
    cur = conn.cursor()

    # Check if there is any parameters
    if params:
        # Execute query with parameters
        cur.execute(query, params)
    else:
        # Execute query without parameters
        cur.execute(query)

    # Define select_in_query as False by default
    select_in_query = False

    # Check if the query has SELECT
    if ("SELECT" in query or "OUTPUT" in query) and not "CREATE" in query:
        # Fetch all the data
        data = cur.fetchall()
        select_in_query = True

    # Commit the connection
    conn.commit()

    # Close the cursor
    cur.close()

    # Check if the query has SELECT
    if select_in_query:
        # Return the requested data
        return data


def check_database_tables_exist():
    
    create_tables = read_sql_file("sql/create_tables.sql")

    # Execute the combined query
    db_query(create_tables)