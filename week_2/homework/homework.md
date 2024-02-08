## Week 2 Homework

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format, please include these directly in the README file of your repository.

> In case you don't get one option exactly, select the closest one

For the homework, we'll be working with the _green_ taxi dataset located here:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

You may need to reference the link below to download via Python in Mage:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Assignment

The goal will be to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a database (and Google Cloud!).

- [x] Create a new pipeline, call it `green_taxi_etl`
- [x] Add a data loader block and use Pandas to read data for the final quarter of 2020 (months `10`, `11`, `12`).
  - [x] You can use the same datatypes and date parsing methods shown in the course.
  - [x] `BONUS`: load the final three months using a for loop and `pd.concat`
- [x] Add a transformer block and perform the following:
  - [x] Remove rows where the passenger count is equal to 0 _and_ the trip distance is equal to zero.
  - [x] Create a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date.
  - [x] Rename columns in Camel Case to Snake Case, e.g. `VendorID` to `vendor_id`.
  - [x] Add three assertions:
    - [x] `vendor_id` is one of the existing values in the column (currently)
    - [x] `passenger_count` is greater than 0
    - [x] `trip_distance` is greater than 0
- [x] Using a Postgres data exporter (SQL or Python), write the dataset to a table called `green_taxi` in a schema `mage`. Replace the table if it already exists.
- [x] Write your data as Parquet files to a bucket in GCP, partioned by `lpep_pickup_date`. Use the `pyarrow` library!
- [x] Schedule your pipeline to run daily at 5AM UTC.

### Questions

## Question 1. Data Loading

Once the dataset is loaded, what's the shape of the data?

```python
# Data Loader Block
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):

    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{month}.csv.gz"

    data_types = {
        'VendorID': float,
        'store_and_fwd_flag': str,
        'RatecodeID': pd.Int64Dtype(),
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'ehail_fee': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'payment_type': pd.Int64Dtype(),
        'trip_type': pd.Int64Dtype(),
        'congestion_surcharge': float
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    final_quarter = ['10', '11', '12']
    dfs = []
    for month in final_quarter:
        url = base_url.format(month=month)
        df = pd.read_csv(url, compression='gzip', parse_dates=parse_dates, dtype=data_types)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
```

- [x] 266,855 rows x 20 columns<br>
- [ ] 544,898 rows x 18 columns<br>
- [ ] 544,898 rows x 20 columns<br>
- [ ] 133,744 rows x 20 columns<br>

## Question 2. Data Transformation

```python
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # Remove rows where the passenger count is equal to 0 and the trip distance is equal to zero.
    print(f"--- {data.shape[0]} rows at the starting ---")
    number_of_rows_to_remove = data[(data['passenger_count'] == 0) & data['trip_distance'] == 0].shape[0]
    print(f"--- {number_of_rows_to_remove} rows have a 0 passenger count or trip distance ---")
    data = data[~(data['passenger_count'] == 0) & ~(data['trip_distance'] == 0.0)]
    print(f"--- {data.shape[0]} rows after cleaning ---")

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    data.columns = (
        data.columns
        .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
        .str.lower()
    )

    return data


@test
def test_vendor_id(output, *args) -> None:
    # vendor_id is one of the existing values in the column (currently)
    assert 'vendor_id' in output.columns, 'vendor_id is not one of the column names'

@test
def test_passenger_count(output, *args) -> None:
    # passenger_count is greater than 0
    assert 0 not in output['passenger_count'].values, 'There is still data with a passenger count of 0'

@test
def test_trip_distance(output, *args) -> None:
    # trip_distance is greater than 0
    assert 0 not in output['trip_distance'].values, 'There are still rows containing a 0 trip distance'
```

Upon filtering the dataset where the passenger count is greater than 0 _and_ the trip distance is greater than zero, how many rows are left?

- [ ] 544,897 rows
- [ ] 266,855 rows
- [x] 139,370 rows
- [ ] 266,856 rows

## Question 3. Data Transformation

Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

- [ ] `data = data['lpep_pickup_datetime'].date`
- [ ] `data('lpep_pickup_date') = data['lpep_pickup_datetime'].date`
- [x] `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`
- [ ] `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt().date()`

## Question 4. Data Transformation

What are the existing values of `VendorID` in the dataset?

```python
# Added to transformer
print(data.vendor_id.unique())
```

- [ ] 1, 2, or 3
- [x] 1 or 2
- [ ] 1, 2, 3, 4
- [ ] 1

## Question 5. Data Transformation

How many columns need to be renamed to snake case?

- [ ] 3
- [ ] 6
- [ ] 2
- [x] 4

## Question 6. Data Exporting

```python
# Export to postgres
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:

    schema_name = 'mage'
    table_name = 'green_cab_data'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
```
```python
# Export to GCP
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/zippy-haiku-409309-0d4c9c5d91a2.json"

bucket_name = "mage-zoomcamp-dee-dequin"
project_id = "zippy-haiku-409309"
table_name = "green_taxi_data"
root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data_to_google_cloud_storage(data, **kwargs) -> None:

    # define table for pyarrow
    table = pa.Table.from_pandas(data)

    # define filesystem for pyarrow
    gcs = pa.fs.GcsFileSystem()

    # feed args to write to dataset
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["lpep_pickup_date"],
        filesystem=gcs
    )
```


Once exported, how many partitions (folders) are present in Google Cloud?

- [x] 96
- [ ] 56
- [ ] 67
- [ ] 108

## Submitting the solutions

* Form for submitting: [here](https://courses.datatalks.club/de-zoomcamp-2024/homework/hw2)
* Check the link above to see the due date

Link for learning in [public]().
