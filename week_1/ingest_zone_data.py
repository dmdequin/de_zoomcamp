import argparse

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name

    df_zones = pd.read_csv("taxi_zone_lookup.csv")
    df_zones.head(2)

    # Creaat engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # engine = create_engine("postgresql://root:root@pgdatabase:5432/ny_taxi")

    # Add data to postgres
    df_zones.to_sql(name=table_name, con=engine, if_exists="replace")
    print("--- Zone data has been added to the database ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')

    args = parser.parse_args()
    main(args)
