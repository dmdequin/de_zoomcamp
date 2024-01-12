## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits*

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

**SOLUTION:** `--rm`


## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ).

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0 - nothing
- 23.0.1 - nope, veresion of pip
- 58.1.0 - nope, version of setuptools

**SOLUTION:**
RUN ```docker run -it --entrypoint=bash  python:3.9```
0.42.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


**SOLUTION**
```bash
# run pgadmin and postgres with docker compose
docker compose up

URL_TRIPS="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
URL_ZONES="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

# Build the container using the Dockerfile
docker build -t data_ingest:v001 .

# Run the container
docker run -it \
  --network=homework_pg-network \
  data_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name_trips=green_taxi_trips  \
    --table_name_zones=zone_data \
    --url_trips=${URL_TRIPS} \
    --url_zones=${URL_ZONES}
```


## Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767 - no, this is just the count of pickups that day
- 15612 - yep
- 15859
- 89009 - way too high

**SOLUTION:**
15612
```sql
SELECT COUNT(*) FROM
	(
	SELECT gt.pickup, gt.dropoff
	FROM
	(
		SELECT
			CAST(lpep_pickup_datetime AS DATE) as "pickup",
			CAST(lpep_dropoff_datetime AS DATE) as "dropoff"
		FROM
			green_taxi_trips
	) as gt
	WHERE
		( gt.pickup = CAST('2019-09-18' as DATE))
	AND
		( gt.dropoff = CAST('2019-09-18' as DATE))
	ORDER BY gt.pickup ASC
) as FOO;
```


## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26 - yep
- 2019-09-21

**SOLUTION:**
2019-09-26

```sql
SELECT
	trip_distance, lpep_pickup_datetime
FROM
	green_taxi_trips
ORDER BY
	trip_distance DESC;
```


## Question 5. The number of passengers

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens"
- "Brooklyn" "Queens" "Staten Island"

**SOLUTION:** "Brooklyn" "Manhattan" "Queens"

```sql
SELECT
	ROUND(CAST(SUM(g.total_amount) AS numeric),1) AS total,
	zpu."Borough" as "pick_up_loc"
FROM
	(
		SELECT
			*
		FROM
		(
			SELECT
				CAST(lpep_pickup_datetime AS DATE) AS pickup,
				total_amount,
				"PULocationID"
			FROM
				green_taxi_trips
		) as boo
		WHERE
			boo.pickup = CAST('2019-09-18' as DATE)
	) as g
LEFT JOIN zone_data zpu
	ON g."PULocationID" = zpu."LocationID"
GROUP BY pick_up_loc
ORDER BY total DESC;
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

**SOLUTION:**
JFK Airport at 62.31

started writing the query
```sql
SELECT
	tip_amount,
	drop_off_zone
FROM
(
	SELECT
		tip_amount,
		zpu."Zone" as "pick_up_zone",
		zdo."Zone" as "drop_off_zone"
	FROM
		green_taxi_trips g
	LEFT JOIN zone_data zpu
		ON g."PULocationID" = zpu."LocationID"
	LEFT JOIN zone_data zdo
		ON g."DOLocationID" = zdo."LocationID"
	WHERE
		extract (month from lpep_pickup_datetime)=9
	AND
		extract (year from lpep_pickup_datetime)=2019
) d
WHERE
	d.pick_up_zone='Astoria'
ORDER BY d.tip_amount DESC;
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting:
* You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: