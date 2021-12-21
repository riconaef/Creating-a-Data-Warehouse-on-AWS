import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Description:
        - Connects to the data (JSON files), which are saved on the 
        	S3 storage cloud (the Redshift role needs to have a read persmission)
        - Loads the data into the 'staging_events_table' and the 'staging_songs_table'
    
    Arguments:
        cur:  the cursor object
        conn: connection to the database
        
    Returns:
        None
    """
    
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description:
	This is the ETL pipeline, which extracts the data from the events and songs table, 
		transforms some columns and inserts it into new tables, which have the 
		architecture of a star-schema.
    
    Arguments:
        cur:  the cursor object
        conn: connection to the database
        
    Returns:
        None
    """
    
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description:
        Connects to the dwh database on AWS and creates a cursor.
        Performs two functions, one to load the data into the 3NF schema tables. 
        The second function performs the ETL pipeline, which loads the data from
        the 3NF tables to the star-schema tables.
        
    Arguments:
        None
        
    Returns:
        None
    """
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
