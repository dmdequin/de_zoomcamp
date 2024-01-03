-- SQL refresher

SELECT COUNT(*) FROM yellow_taxi_trips;

SELECT * FROM yellow_taxi_trips
LIMIT 1;

SELECT * FROM zones;

-- Inner join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	trip_distance,
	total_amount,
	CONCAT(zpu.borough, ' / ', zpu.zone) as "pick_up_loc",
	CONCAT(zdo.borough, ' / ', zdo.zone) as "drop_off_loc"
FROM
	yellow_taxi_trips t,
	zones zpu,
	zones zdo
WHERE
	t."PULocationID" = zpu.locationid and
	t."DOLocationID" = zdo.locationid
LIMIT 10;

-- join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	trip_distance,
	total_amount,
	CONCAT(zpu.borough, ' / ', zpu.zone) as "pick_up_loc",
	CONCAT(zdo.borough, ' / ', zdo.zone) as "drop_off_loc"
FROM
	yellow_taxi_trips t
JOIN zones zpu
	ON t."PULocationID" = zpu.locationid
JOIN zones zdo
	ON t."DOLocationID" = zdo.locationid
LIMIT 10;

-- check for nulls
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM
	yellow_taxi_trips
WHERE "DOLocationID" is NULL;

-- check for missing values between tables
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM
	yellow_taxi_trips
WHERE "DOLocationID" NOT IN (SELECT LocationID FROM zones);

-- left join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	trip_distance,
	total_amount,
	CONCAT(zpu.borough, ' / ', zpu.zone) as "pick_up_loc",
	CONCAT(zdo.borough, ' / ', zdo.zone) as "drop_off_loc"
FROM
	yellow_taxi_trips t
LEFT JOIN zones zpu
	ON t."PULocationID" = zpu.locationid
LEFT JOIN zones zdo
	ON t."DOLocationID" = zdo.locationid
LIMIT 10;

-- group by pickup date
SELECT
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(tpep_pickup_datetime AS DATE) as "day",
	COUNT(1)
FROM
	yellow_taxi_trips t
GROUP BY "day"
ORDER BY "day";

-- group by count of trips
SELECT
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(tpep_pickup_datetime AS DATE) as "day",
	COUNT(1) AS "count"
FROM
	yellow_taxi_trips t
GROUP BY "day"
ORDER BY "count" DESC;

-- group by count of trips with additional info
SELECT
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(tpep_pickup_datetime AS DATE) as "day",
	COUNT(1) AS "count",
	MAX(total_amount) AS AMOUNT,
	MAX(passenger_count) AS PASSENGERS
FROM
	yellow_taxi_trips t
GROUP BY "day"
ORDER BY "count" DESC;

-- multi group by
SELECT
	--DATE_TRUNC('DAY', tpep_pickup_datetime),
	CAST(tpep_pickup_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) AS "count",
	MAX(total_amount) AS AMOUNT,
	MAX(passenger_count) AS PASSENGERS
FROM
	yellow_taxi_trips t
GROUP BY 1, 2
ORDER BY
	"day" ASC,
	"DOLocationID" ASC;
