import psycopg2
from psycopg2 import OperationalError
import yaml

with open('Util/paramsBD.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def create_connection():
    """
    Create a connection to the PostgreSQL database.
    :return: Connection object or None
    """
    try:
        connection = psycopg2.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['database']
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None