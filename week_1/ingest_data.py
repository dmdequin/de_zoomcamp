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
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # download the csv
    os.system(f"wget {url} -O {csv_name}")

    # Create a python engine for SQL
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # Create iterator
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(iter)

    # Make datatype corrections
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # Add column names to database
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")

    # ## Add data to the db
    while True:
        try:
            t_start = time()

            # Get next chunk of data
            df = next(df_iter)

            # Make datatype corrections
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            # Append chunk to db
            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()
            print("inserted another chunk...took %.3f seconds" % (t_end - t_start))
        except StopIteration:
            print("end of file has been reached, all data is loaded...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', 'user name for postgres')
    parser.add_argument('--pass', 'passsword for postgres')
    parser.add_argument('--host', 'host name for postgres')
    parser.add_argument('--port', 'port for postgres')
    parser.add_argument('--db', 'database name for postgres')
    parser.add_argument('--table_name', 'table of the table where we will write results to')
    parser.add_argument('--url', 'url of the cvs file')

    args = parser.parse_args()

    main(args)
