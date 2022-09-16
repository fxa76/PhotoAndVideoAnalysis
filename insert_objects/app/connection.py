import psycopg2
import os
user_name = os.environ['POSTGRES_USER']
password= os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']

def get_connection():
    conn = psycopg2.connect(dbname=db_name,
              user=user_name,
              host=host,port = port,
              password=password)
    conn.autocommit = True
    return conn
