#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name_trips = params.table_name_trips
    table_name_zones = params.table_name_zones
    url_trips = params.url_trips
    url_zones = params.url_zones


    if url_trips.endswith('.csv.gz'):
        csv_trips = 'output.csv.gz'
    else:
        csv_trips = 'output.csv'

    csv_zones = 'zones.csv'

    # download the data
    os.system(f"wget -P data {url_trips} -O {csv_trips}")
    os.system(f"wget -P data {url_zones} -O {csv_zones}")


    # Create a python engine for SQL
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # upload trips data to SQL

    # Create iterator
    df_iter = pd.read_csv(f"data/{csv_trips}", iterator=True, chunksize=100000)

    df = next(df_iter)

    # Make datatype corrections
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Add column names to database
    df.head(n=0).to_sql(name=table_name_trips, con=engine, if_exists='replace')
    df.to_sql(name=table_name_trips, con=engine, if_exists="append")

    print("Uploading trips data to SQL...")

    # ## Add data to the db
    while True:
        try:
            t_start = time()

            # Get next chunk of data
            df = next(df_iter)

            # Make datatype corrections
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # Append chunk to db
            df.to_sql(name=table_name_trips, con=engine, if_exists="append")

            t_end = time()
            print("inserted another chunk...took %.3f seconds" % (t_end - t_start))

        except StopIteration:
            print("end of file has been reached, all trips data is loaded...")
            break

    # upload zones data to postgres
    print("Uploading zones data to database...")

    df_zones = pd.read_csv(f"data/{csv_zones}")
    df_zones.to_sql(name=table_name_zones, con=engine, if_exists="replace")

    print("--- Zone data has been added to the database ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name_trips', required=True, help='name of the table where we will write the trips to')
    parser.add_argument('--table_name_zones', required=True, help='name of the table where we will write the zones to')
    parser.add_argument('--url_trips', required=True, help='url of the trips csv file')
    parser.add_argument('--url_zones', required=True, help='url of the zones csv file')


    args = parser.parse_args()

    main(args)
