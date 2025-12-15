#!/usr/bin/env python
# coding: utf-8

# Install docker, docker-compose, python, pandas, postgres and dependencies -- in Dockerfile

# ## GET DATA FROM API ##
# > I want the database to have under 10000 entries

import requests
import os
import argparse

import pandas as pd

from sqlalchemy import create_engine

# Constants

LIMIT = 100

ART_API_URL = f'https://api.artic.edu/api/v1/exhibitions?limit={LIMIT}'

DATABASE_USERNAME = 'myuser'
DATABASE_PASSWORD = 'mypassword'
DATABASE_HOST = 'postgres'
DATABASE_PORT = '5432'
DATABASE_NAME = 'artdb'

TABLE_NAME = 'exhibitions'

COUNTER = 100000


# Function to fetch data from Art Institute of Chicago API
def fetch_art_data():
    """
    Fetch data from Art Institute of Chicago API.
    Args:
        limit (int): Number of records to fetch.
    Returns:
        list: List of exhibition data.
    """
    response = requests.get(ART_API_URL.format(LIMIT=LIMIT))
    response.raise_for_status()

    data = response.json()

    return data['data']

# Fetch and process data
def process_data():
    """
    Fetch data and convert to DataFrame.
    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    base_art_data = fetch_art_data()
    print(f"Fetched {len(base_art_data)} records.")

    base_df = pd.DataFrame(base_art_data)

    relevant_columns = ['id','title','short_description','web_url','image_url',
                               'gallery_title','artwork_ids','artwork_titles', 'artist_ids',
                               'source_updated_at','updated_at']
    df = base_df[relevant_columns]
    
    # Clean data: drop rows with missing image_url or title
    df = df.dropna(subset=['image_url','title']).reset_index(drop=True)  # type: ignore

    return df

# df = process_data()

# print(df.sample(2)[['image_url','title']].values[0])
# df.head()


# ## Push the data into Postgresql database
def main(params):
    """
    Main function to store data into PostgreSQL database.
    Gets parameters through argparse.
    """

    db_uri = f'postgresql+psycopg2://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}'

    engine = create_engine(db_uri)

    df = process_data()

    df.to_sql(name=params.table_name, 
              con=engine, 
              if_exists='replace', 
              index=True)
    
    NUM_ENTRIES = len(df)
    print(f"{NUM_ENTRIES} Data stored in table '{params.table_name}' successfully.")

    while NUM_ENTRIES < COUNTER:
        df = process_data()
        df.to_sql(name=params.table_name, 
                  con=engine, 
                  if_exists='append', 
                  index=True)
        NUM_ENTRIES += len(df)
        print(f"{NUM_ENTRIES} Data stored in table '{params.table_name}' successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Store Art Institute of Chicago data into PostgreSQL database.")
    parser.add_argument('--user', type=str, default=f'{DATABASE_USERNAME}', help='Database username')
    parser.add_argument('--password', type=str, default=f'{DATABASE_PASSWORD}', help='Database password')
    parser.add_argument('--host', type=str, default='db-postgres', help='Database host')
    parser.add_argument('--port', type=int, default=5432, help='Database port')
    parser.add_argument('--db', type=str, default=f'{DATABASE_NAME}', help='Database name to connect to')
    parser.add_argument('--table_name', type=str, default=TABLE_NAME, help='Table name to store data')

    args = parser.parse_args()

    main(args)


""" 
To run this script, ensure you have a PostgreSQL database running and accessible with the provided credentials.
You can execute the script from the command line as follows:
python main_getter.py --user myuser --password mypassword --host db-postgres --port 5432 --db artdb --table_name exhibitions

Dockerize the PostgreSQL database for local testing:
docker run --name artdb -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=artdb -p 5432:5432 -d postgres:latest 
> This will create and run a PostgreSQL container named 'artdb' with the specified user, password, and database name.
Make sure to stop and remove the container after testing:
docker stop artdb
docker rm artdb

Dockerize the application using Docker compose:
version: '3.8'
services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: artdb
    ports:
      - "5432:5432"
      app:
      build: .
      depends_on:
        - db
      environment:
        DATABASE_USERNAME: myuser
        DATABASE_PASSWORD: mypassword
        DATABASE_NAME: artdb
        DATABASE_HOST: db
        DATABASE_PORT: 5432
      command: python main_getter.py --user myuser --password mypassword --host db --port 5432 --db artdb --table_name exhibitions
To run the application with Docker Compose:
docker-compose up --build
This will build and start both the PostgreSQL database and the application, storing the data into the database as specified.
"""